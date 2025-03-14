from pydantic_settings import SettingsConfigDict, BaseSettings


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="S3_",
    )

    DOCUMENTS_BUCKET: str
