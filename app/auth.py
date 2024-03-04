# from db import check_api_key, get_user_from_api_key

from config import AppSettings
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from prometheus_client import Counter
from pydantic import ValidationError

c = Counter("requests_by_token", "Usage", ["user"])

try:
    settings = AppSettings()
except ValidationError as e:
    raise Exception("Environment variable 'API_TOKEN' could not be accessed correctly. Is it set?", e)

api_key_header = APIKeyHeader(name="X-API-Token")


def check_api_key(api_key: str):
    return api_key == settings.api_token.get_secret_value()


def get_user_from_api_key(api_key: str):
    c.labels(user="Mobidrom").inc()
    return "Mobidrom"


def get_user(api_key_header: str = Security(api_key_header)):
    if check_api_key(api_key_header):
        user = get_user_from_api_key(api_key_header)
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid API key")
