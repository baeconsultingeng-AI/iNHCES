from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_key: str
    supabase_jwt_secret: str

    # Cloudflare R2
    cloudflare_r2_endpoint: str = ""
    cloudflare_r2_access_key: str = ""
    cloudflare_r2_secret_key: str = ""
    cloudflare_r2_bucket: str = "inhces-storage"

    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment: str = "nhces_cost_estimation"

    # Airflow
    airflow_api_url: str = "http://localhost:8080/api/v1"
    airflow_username: str = "admin"
    airflow_password: str = "admin"

    # App
    secret_key: str = "dev-secret-key-change-in-production"
    environment: str = "development"
    allowed_origins: str = "http://localhost:3000"

    # Optional data source keys
    eia_api_key: str = ""
    fred_api_key: str = ""

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def r2_configured(self) -> bool:
        return bool(self.cloudflare_r2_endpoint and self.cloudflare_r2_access_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()

