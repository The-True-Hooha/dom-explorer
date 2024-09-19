from pydantic_settings import BaseSettings, SettingsConfigDict
from slowapi import Limiter
from slowapi.util import get_remote_address

class AppSetting(BaseSettings):
    APP_NAME: str
    DATABASE_URL: str
    JWT_TOKEN: str
    ALGORITHM:str

    model_config = SettingsConfigDict(
        env_file=".env")


app_setting = AppSetting()


limiter = Limiter(key_func=get_remote_address)