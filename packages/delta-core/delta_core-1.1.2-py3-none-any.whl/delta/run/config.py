from typing import Annotated

from pydantic import Field, HttpUrl, PostgresDsn, UrlConstraints
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


SQLiteUrl = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=False,
        allowed_schemes=['sqlite', 'sqlite3'],
    )
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix='DELTA_',
    )

    # Deltatwin Run
    api_url: HttpUrl
    run_limit: int = Field(default=10)
    eviction_active: bool = Field(default=False)
    eviction_keep_period: int = Field(default=48)
    database_url: SQLiteUrl | PostgresDsn = Field(
        default="sqlite:///.delta-run.db?check_same_thread=false"
    )
    database_show_sql: bool = Field(default=False)
    page_limit: int = Field(default=100)

    # DeltaTwin container image registry
    image_repo_hostname: str
    image_repo_username: str
    image_repo_password: str

    # DeltaTwin Run output storage
    s3_endpoint: str
    s3_region: str
    s3_access_key: str
    s3_secret_access_key: str
    s3_bucket: str

    # kubernetes executor
    k8s_context: str
    k8s_namespace: str
    k8s_cluster_name: str
    k8s_cluster_cert_auth: str
    k8s_cluster_server: str
    k8s_user_name: str
    k8s_user_cli_cert: str
    k8s_user_cli_key: str
