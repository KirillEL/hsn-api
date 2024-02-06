from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from typing import Dict, Optional
import os
from pathlib import Path

class Config(BaseSettings):
    model_config = ConfigDict(extra='ignore')

    ENV: Optional[str] = "development"
    DEBUG: Optional[bool] = True
    APP_HOST: Optional[str] = "0.0.0.0"
    APP_PORT: Optional[int] = 9999

    DB_SERVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_NAME: str
    DB_URI: str

    JWT_SECRET: Optional[str] = "frtrtt"
    JWT_ALGORITHM: Optional[str] = "HS256"



class LocalConfig(Config):
    pass


class ProductionConfig(Config):
    DEBUG: Optional[bool] = False



def get_config(env_file):
    env = os.getenv("ENV", "local")
    config_type = {
        "local": LocalConfig(_env_file=env_file),
        "prod": ProductionConfig(_env_file=env_file)
    }
    return config_type[env]


config: Config = get_config(env_file=os.path.join(Path(__file__).parents[1], ".env"))
