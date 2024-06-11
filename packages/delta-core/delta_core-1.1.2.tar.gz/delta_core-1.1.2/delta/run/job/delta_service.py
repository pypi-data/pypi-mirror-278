import asyncio
import collections

import ansible_runner
import kubernetes

from delta.run.config import Settings
from delta.run.job import Job, JobService, RunStatus


K8sContainerState = collections.namedtuple("K8sState", ["state", "reason"])


class DeltaJobService(JobService):
    def __init__(self):
        super().__init__()
        self._config = Settings()
        # kubernetes client
        k8s_conf = self.__prepare_kubernetes_config()
        kubernetes.config.load_kube_config_from_dict(k8s_conf)
        self._k8s_cli = kubernetes.client.CoreV1Api()
        self._env = self.__prepare_ansible_config()

    def __prepare_ansible_config(self) -> dict:
        return {
            "k8s": {
                "namespace": self._config.k8s_namespace,
                "context": self._config.k8s_context,
                "cluster": {
                    "name": self._config.k8s_cluster_name,
                    "cert_auth": self._config.k8s_cluster_cert_auth,
                    "server": self._config.k8s_cluster_server,
                },
                "user": {
                    "name": self._config.k8s_user_name,
                    "client_cert_data": self._config.k8s_user_cli_cert,
                    "client_key_data": self._config.k8s_user_cli_key,
                },
            },
            "storage": {
                "data_path": "/s3",
                "s3": {
                    "bucket": {"name": self._config.s3_bucket},
                    "endpoint": self._config.s3_endpoint,
                    "region": self._config.s3_region,
                    "accesskeyid": self._config.s3_access_key,
                    "secretaccesskey": self._config.s3_secret_access_key,
                },
            },
        }

    def __prepare_kubernetes_config(self) -> dict:
        """
        Prepares kubernetes config
        """
        return {
            "apiVersion": "v1",
            "kind": "Config",
            "clusters": [
                {
                    "name": self._config.k8s_cluster_name,
                    "cluster": {
                        "certificate-authority-data":
                            self._config.k8s_cluster_cert_auth,
                        "server": self._config.k8s_cluster_server,
                    },
                }
            ],
            "contexts": [
                {
                    "name": self._config.k8s_context,
                    "context": {
                        "user": self._config.k8s_user_name,
                        "cluster": self._config.k8s_cluster_name,
                    },
                }
            ],
            "current-context": self._config.k8s_context,
            "preferences": {},
            "users": [
                {
                    "name": self._config.k8s_user_name,
                    "user": {
                        "client-certificate-data":
                            self._config.k8s_user_cli_cert,
                        "client-key-data": self._config.k8s_user_cli_key,
                    },
                }
            ],
        }

    @staticmethod
    def __retrieve_container_state_from_pod(
        pod: kubernetes.client.models.V1Pod,
    ) -> K8sContainerState:
        k8s_state = pod.status.container_statuses[0].state
        if k8s_state.running is not None:
            return K8sContainerState("running", None)
        elif k8s_state.terminated is not None:
            return K8sContainerState("terminated", k8s_state.terminated.reason)
        elif k8s_state.waiting is not None:
            return K8sContainerState("waiting", k8s_state.waiting.reason)
        raise ValueError(f"Unknown container state from pod: {pod}")

    @staticmethod
    def __check_container_state(state: K8sContainerState) -> int | None:
        match state:
            case (
                K8sContainerState("running", None)
                | K8sContainerState("terminated", "Terminating")
                | K8sContainerState("waiting", "ContainerCreating")
                | K8sContainerState("waiting", "PodInitializing")
            ):
                return None
            case (
                K8sContainerState("waiting", "ImagePullBackOff")
                | K8sContainerState("waiting", "ErrImagePull")
                | K8sContainerState("waiting", "CrashLoopBackOff")
                | K8sContainerState("waiting", "ImageInspectError")
                | K8sContainerState("waiting", "CreateContainerConfigError")
                | K8sContainerState("waiting", "ErrImageNeverPull")
                | K8sContainerState("waiting", "InvalidImageName")
                | K8sContainerState("terminated", "Error")
                | K8sContainerState("terminated", "OOMKilled")
                | K8sContainerState("terminated", "ContainerCannotRun")
                | K8sContainerState("terminated", "DeadlineExceeded")
                | K8sContainerState("terminated", "ImageGCFailed")
                | K8sContainerState("terminated", "ContainerStatusUnknown")
            ):
                return 1
            case K8sContainerState("terminated", "Completed"):
                return 0
            case _:
                raise ValueError(f"Unknown container state: {state}")

    async def execute_job(self, job: Job, **kwargs):
        # prepare environment variables to execute ansible playbook run_job
        inputs = ";".join(map(lambda x: f"{x.src},{x.dest}", job.inputs))
        outputs = ";".join(map(lambda x: f"{x.src},{x.dest}", job.outputs))
        self._env["job"] = {
            "name": str(job.id),
            "image": f"{self._config.image_repo_hostname}/{job.image.tag}",
            "cmd": job.command,
            "working_directory": job.working_dir,
            "resources": {
                "inputs": inputs,
                "outputs": outputs,
            },
            "registry": {
                "url": self._config.image_repo_hostname,
                "login": self._config.image_repo_username,
                "password": self._config.image_repo_password,
            },
        }

        # executing run_job playbook from gael.delta
        try:
            r = await asyncio.to_thread(
                ansible_runner.run,
                private_data_dir="gael.delta",
                extravars=self._env,
                playbook="playbooks/run_job.yml",
                suppress_env_files=True,
                quiet=True,
            )
            if r.rc != 0:
                self._logger.error(
                    "Ansible failure: %d\n stdout:\n%s\n stderr:\n%s",
                    r.rc, r.stdout, r.stderr
                )
                raise RuntimeError(f"Failed to start job via ansible: {r.rc}")
            self._jobs[job.id] = job
        except Exception as e:
            self._logger.info(f"Job({job.id}) failed: {e}")
            self._logger.error(e)
            job.status = RunStatus.ERROR

    def check_jobs(self):
        updated = []
        for key, job in self._jobs.items():
            try:
                pod = self._k8s_cli.read_namespaced_pod(
                    str(key), self._config.k8s_namespace)
                state = self.__retrieve_container_state_from_pod(pod)
                status = self.__check_container_state(state)
                if status is not None:
                    updated.append(key)
                    if status == 0:
                        job.status = RunStatus.SUCCESS
                    elif status == 1:
                        job.status = RunStatus.ERROR
            except kubernetes.client.exceptions.ApiException as e:
                self._logger.error(
                    f"Failed to check job status: {key}, reason: {e.reason}"
                )
            except ValueError as e:
                self._logger.error(f"Unknown job status: {e}")
            except Exception:
                self._logger.error("Pod initializing...")
        # unwatch updated jobs
        for key in updated:
            del self._jobs[key]
            self._k8s_cli.delete_namespaced_pod(
                str(key),
                self._config.k8s_namespace
            )

    def shutdown(self):
        pass
