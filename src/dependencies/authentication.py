from fastapi import Header, HTTPException
from settings import settings


def verify_api_key(x_api_key: str = Header()) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="X-Api-Key invalid")
