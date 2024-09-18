from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSetting(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    JWT_TOKEN: str
    ALGORITHM:str

    model_config = SettingsConfigDict(
        env_file=".env")


app_setting = AppSetting()
