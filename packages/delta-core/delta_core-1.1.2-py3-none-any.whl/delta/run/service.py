import asyncio
import logging
import os
import re
import tempfile
import uuid
import requests as req
from datetime import datetime, timedelta
from typing import IO, List

from sqlalchemy.exc import NoResultFound

import delta.run.db.daos as dao
from delta.run.api.model import (
    RunContextInsertModel,
    RunContextModel,
    RunContextUpdateModel,
    model_param_to_orm_param,
)
from delta.run.config import Settings
from delta.run.db.database import Session
from delta.run.db.orm import (
    DataParameter,
    ParameterKind,
    RunContext,
    RunStatus,
)
from delta.run.job.delta_service import DeltaJobService
from delta.run.orchestrator import DeltaOrchestrator
from delta.run.storage_manager import DeltaStorageManager
from delta.run.utils import DependencyResolver

logger = logging.getLogger("RunService")
logger.setLevel(logging.INFO)


class DeltaRunService:
    def __init__(self, storage: DeltaStorageManager):
        self._storage = storage
        self._dependency_resolver = DependencyResolver()
        self._run = set()

    @staticmethod
    def __download_deltatwin_file(
            token: str,
            deltatwin_id: str,
            deltatwin_version: str,
            file: str,
            destination_dir: str) -> None:
        url = (
            f"{Settings().api_url}deltatwins/"
            f"{deltatwin_id}/files/{file}?version={deltatwin_version}"
        )
        response = req.get(
            url.format('manifest'),
            # token format: 'Bearer <OAuth2_token>'
            headers={'Authorization': token},
            stream=True
        )
        if response.status_code != 200:
            logger.error(
                "Failed to retrieve file `%s` from deltatwin: "
                "%s v%s (%s, %s, %d)",
                file, deltatwin_id, deltatwin_version, response.url,
                response.request.method, response.status_code
            )
            raise RuntimeError(
                f"Enable to retrieve {file}  file from deltatwin: "
                f"{deltatwin_id}({deltatwin_version})"
            )

        filename = re.findall(
            'filename="?([^"]+)', response.headers["Content-Disposition"]
        )[0]
        destination = os.path.join(destination_dir, filename)
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=4096):
                f.write(chunk)

    def __download_twin(self, token, twin_id, twin_version):
        # Downloading manifest and workflow in a temporary directory
        with tempfile.TemporaryDirectory() as tmp_dir:
            self.__download_deltatwin_file(
                token, twin_id, twin_version, 'manifest', tmp_dir
            )
            self.__download_deltatwin_file(
                token, twin_id, twin_version, 'workflow', tmp_dir
            )
            self._storage.push_deltatwin(tmp_dir, twin_id, twin_version)

    def __download_twin_with_dependencies(
            self, token, twin_id, twin_version, visited=None
    ):
        if visited is None:
            visited = set()

        if twin_id in visited:
            return

        visited.add((twin_id, twin_version))
        if not self._storage.has_deltatwin(twin_id, twin_version):
            self.__download_twin(token, twin_id, twin_version)

        manifest = self._storage.get_deltatwin_manifest(twin_id, twin_version)
        if manifest.dependencies is not None:
            for dependency in manifest.dependencies.values():
                self._dependency_resolver.add_dependency(
                    twin_id, (dependency.id, dependency.version))
                if self._dependency_resolver.check_dependency_cycles(twin_id):
                    raise RuntimeError("Dependency cycle detected")
                self.__download_twin_with_dependencies(
                    token, dependency.id, dependency.version, visited)

    @staticmethod
    def __on_update_run_context(run_id: str, context: RunContextUpdateModel):
        with Session().begin() as tx:
            dao.update_run(tx.session, run_id, context)

    @staticmethod
    def __on_create_sub_run_context(run_id: str, context: RunContext):
        logger.info('Prepare sub run %s from %s', run_id, context.id)
        with Session().begin() as tx:
            dao.add_run(tx.session, context)

    async def orchestrate(self, run_ctx: RunContextModel):
        async with DeltaJobService() as executor:
            try:
                manifest = self._storage.get_deltatwin_manifest(
                    run_ctx.deltatwin_id, run_ctx.deltatwin_version
                )
                workflow = self._storage.get_deltatwin_workflow(
                    run_ctx.deltatwin_id, run_ctx.deltatwin_version
                )
                orch = DeltaOrchestrator(
                    manifest=manifest,
                    workflow=workflow,
                    run_ctx=run_ctx,
                    storage_manager=self._storage,
                    job_service=executor,
                    on_update_context=self.__on_update_run_context,
                    on_create_sub_context=self.__on_create_sub_run_context
                )
                await orch.run()
            except (ValueError, KeyError) as ex:
                run_ctx.status = RunStatus.ERROR
                if isinstance(ex, ValueError):
                    run_ctx.return_code = 311
                    run_ctx.message = "Invalid manifest content"
                if isinstance(ex, KeyError):
                    run_ctx.return_code = 310
                    run_ctx.message = (
                        f"Node {ex.args[0]} not found in manifest"
                    )
                with Session().begin() as tx:
                    rcup = RunContextUpdateModel(
                        status=run_ctx.status,
                        return_code=run_ctx.return_code,
                        message=run_ctx.message,
                    )
                    dao.update_run(tx.session, run_ctx.id, rcup)
                return
            finally:
                executor.shutdown()

    def add_run(self, token, ctx: RunContextInsertModel) -> RunContextModel:
        run_ctx = RunContext(
            id=str(uuid.uuid4()),
            deltatwin_id=ctx.deltatwin_id,
            deltatwin_version=ctx.deltatwin_version,
            owner=ctx.owner,
            status=RunStatus.CREATED,
            inputs=[
                model_param_to_orm_param(p, ParameterKind.INPUT)
                for p in ctx.inputs
            ],
            date_created=ctx.date_created,
        )
        # download and push on the storage the deltatwin if necessary
        self.__download_twin_with_dependencies(
            token, run_ctx.deltatwin_id, run_ctx.deltatwin_version
        )

        with Session().begin() as tx:
            run = RunContextModel.from_run_context(
                dao.add_run(tx.session, run_ctx)
            )
            # keep background task and remove it when finish
            task = asyncio.create_task(self.orchestrate(run))
            self._run.add(task)
            task.add_done_callback(self._run.discard)

            return run

    @staticmethod
    def get_runs(
        deltatwin_id: str = None,
        owner: str = None,
        status: RunStatus = None,
        limit: int = 0,
        offset: int = 0,
    ) -> List[RunContextModel]:
        with Session() as session:
            runs = dao.get_runs(
                session, deltatwin_id, owner, status, limit, offset
            )
            return [RunContextModel.from_run_context(r) for r in runs]

    @staticmethod
    def get_run_by_id(run_id: str) -> RunContextModel:
        with Session() as session:
            try:
                run_ctx = dao.get_run_by_id(session, run_id)
                return RunContextModel.from_run_context(run_ctx)
            except NoResultFound:
                raise ValueError(f"RunContext not found: {run_id}")

    async def get_run_output(self, run_id: str, output_name: str) -> IO:
        with Session() as session:
            run_ctx = dao.get_run_by_id(session, run_id)
            output = next(
                filter(lambda n: n.name == output_name, run_ctx.outputs), None
            )

            if output is None:
                raise RuntimeError(f"Output not found: {output_name}")

            if not isinstance(output, DataParameter):
                raise RuntimeError("Only output type Data can be requested")

            split = output.path.split("/", maxsplit=3)
            data = asyncio.to_thread(
                self._storage.get_data,
                run_id=run_ctx.id,
                job_id=split[2],
                basename=split[3],
            )
            return await data

    def remove_run(self, run_id: uuid.UUID):
        with Session() as session:
            try:
                dao.delete_run(session, str(run_id))
                self._storage.remove_run(run_id)
            except NoResultFound:
                raise ValueError(f"RunContext not found: {run_id}")

    def remove_old_runs(self, threshold_hours: int):
        now = datetime.utcnow()
        threshold_date = now - timedelta(hours=threshold_hours)
        with Session() as session:
            try:
                runs_to_remove = dao.get_runs_by_date(session, threshold_date)
                for run in runs_to_remove:
                    dao.delete_run(session, run.id)
                    self._storage.remove_run(uuid.UUID(run.id))

                logger.info(f"Successfully removed {len(runs_to_remove)} "
                            f"runs older than {threshold_date}.")
            except Exception as e:
                logger.error(f"Error occurred while removing runs: {str(e)}")

    def get_number_of_run_by_user(self, user):
        with Session() as session:
            try:
                count = dao.get_number_of_run_by_user(session, user)
                return count
            except Exception as e:
                logger.error(e)

    def set_running_runs_to_error_at_startup(self):
        with Session() as session:
            dao.set_running_runs_to_error_at_startup(session)
