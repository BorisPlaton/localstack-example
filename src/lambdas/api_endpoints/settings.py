from pydantic_settings import SettingsConfigDict, BaseSettings


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
    )

    USER: str
    PASSWORD: str
    DATABASE: str
    PORT: str
    HOST: str


class S3Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="S3_",
    )

    DOCUMENTS_BUCKET: str
