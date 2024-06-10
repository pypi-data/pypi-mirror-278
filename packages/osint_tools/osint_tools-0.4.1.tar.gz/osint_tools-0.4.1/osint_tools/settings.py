from functools import lru_cache
from pydantic import BaseSettings
from os import environ

class _BaseSettings(BaseSettings):
    LOGGER_NAME: str = environ.get('LOGGER_NAME', 'osint_tools')
    MONGO_URI: str = environ.get('MONGO_URI')
    MONGO_DB_NAME: str = environ.get('MONGO_DB_NAME')

@lru_cache()
def get_settings() -> BaseSettings:
    return _BaseSettings()
