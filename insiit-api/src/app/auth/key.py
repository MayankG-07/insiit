from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from config import api_config

api_key_header = APIKeyHeader(name="x-api-key")


def get_api_key(api_key: str = Security(api_key_header)):
    api_keys = [value for _key, value in api_config["api-keys"].items()]
    if api_key in api_keys:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"name": "API-KEY-ERROR", "message": "Invalid API key"},
        )
