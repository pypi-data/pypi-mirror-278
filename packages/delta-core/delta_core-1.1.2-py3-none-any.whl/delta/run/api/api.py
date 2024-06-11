import json
import logging
import logging.config
import logging.handlers
import os
import pathlib
import uuid
from contextlib import asynccontextmanager
from typing import Annotated, List, Optional

import alembic.command
import alembic.config
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Header, HTTPException, status
from pytz import utc
from starlette.responses import StreamingResponse

from delta.run.api.model import RunContextInsertModel, RunContextModel
from delta.run.config import Settings
from delta.run.db.orm import RunStatus
from delta.run.service import DeltaRunService
from delta.run.storage_manager import S3StorageManager


def setup_logging():
    config_file = pathlib.Path("log_config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)


scheduler_logger = logging.getLogger("apscheduler")
scheduler_logger.setLevel(logging.INFO)

LIMIT_DEFAULT = 100

settings = Settings()

alembic.command.upgrade(alembic.config.Config("alembic.ini"), "head")
storage = S3StorageManager(
    entry_point=settings.s3_endpoint,
    key=settings.s3_access_key,
    secret=settings.s3_secret_access_key,
    bucket=settings.s3_bucket
)
run_svc = DeltaRunService(storage)


def eviction():
    try:
        run_svc.remove_old_runs(threshold_hours=settings.eviction_keep_period)
    except Exception as e:
        scheduler_logger.error(f"Error occurred during eviction: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    scheduler = None
    if settings.eviction_active:
        scheduler = AsyncIOScheduler(timezone=utc)
        scheduler.add_job(
            eviction,
            'cron',
            day_of_week='*',
            hour=0,
            minute=0
        )
        scheduler.start()

    run_svc.set_running_runs_to_error_at_startup()

    try:
        yield
    finally:
        # Shutdown logic
        if scheduler and scheduler.running:
            scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


def check_run_id(run_id: uuid.UUID):
    if not isinstance(run_id, uuid.UUID):
        raise HTTPException(
            status_code=422, detail="'run_id' must be a valid UUID"
        )


@app.post("/runs", status_code=status.HTTP_201_CREATED)
async def create_run(
    token: Annotated[Optional[str], Header()], run_model: RunContextInsertModel
) -> RunContextModel:
    try:
        if run_svc.get_number_of_run_by_user(run_model.owner) >= \
                settings.run_limit:
            raise HTTPException(
                status_code=429,
                detail=(
                    "You have reached the number of runs allowed for the "
                    "beta version, please try again later"
                ),
            )
        return run_svc.add_run(token, run_model)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=e)


@app.get("/runs")
def read_runs(
    deltatwin_id: str = None, owner: str = None,
        status: RunStatus = None,
        limit: int = LIMIT_DEFAULT,
        offset: int = 0
) -> List[RunContextModel]:
    return run_svc.get_runs(deltatwin_id, owner, status, limit, offset)


@app.get("/runs/{run_id}")
def read_run(run_id: uuid.UUID) -> RunContextModel:
    check_run_id(run_id)
    try:
        rc = run_svc.get_run_by_id(str(run_id))
        return rc
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")


@app.delete("/runs/{run_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_run(run_id: uuid.UUID):
    try:
        run_svc.remove_run(run_id)
    except ValueError:
        raise HTTPException(status_code=404)


@app.get("/runs/{run_id}/output/{output_name}/info")
def get_output(run_id: str, output_name: str):
    run = run_svc.get_run_by_id(run_id)
    output = next(filter(lambda p: p.name == output_name, run.outputs))
    if output is not None:
        return output
    raise HTTPException(
        status_code=404, detail=f"No input found: {output_name}"
    )


@app.get("/runs/{run_id}/output/{output_name}/download")
async def download_output(run_id: str, output_name: str):
    run = run_svc.get_run_by_id(run_id)
    output = next(filter(lambda p: p.name == output_name, run.outputs))
    if output is None:
        raise HTTPException(status_code=404, detail="Output not found")

    basename = os.path.basename(output.path)
    stream_io = await run_svc.get_run_output(run_id, output_name)
    info = stream_io.info()
    response = StreamingResponse(
        stream_io,
        status_code=status.HTTP_200_OK,
        headers={
            "Content-Disposition": f"attachment; filename={basename}",
            "Content-Length": info['content-length'],
            "Content-Type": info['content-type'],
        },
        media_type=info['content-type'] or "application/octet-stream",
    )
    return response


if __name__ == "__main__":
    setup_logging()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
