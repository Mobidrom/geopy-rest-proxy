from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    api_token: SecretStr = Field(..., env="API_TOKEN")

    class Config:
        env_prefix = ""
        case_sensitive = False
