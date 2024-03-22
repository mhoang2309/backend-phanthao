from typing import Any
from typing import Coroutine

import jwt
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Request
from fastapi.security import APIKeyHeader
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import ValidationError
from redis import Redis
from starlette.status import HTTP_401_UNAUTHORIZED
from typing_extensions import Annotated

from app.settings.config import jwt_config


class HTTPBearer_test:
    def __init__(self, scheme_name):
        self.scheme_name = scheme_name

    def __call__(self, request: Request) -> Any:
        return request


reusable_oauth2 = HTTPBearer(scheme_name="Token")
session = APIKeyHeader(name="session", auto_error=False, scheme_name="Sessiony")
hash_user = APIKeyHeader(name="hash-user", auto_error=False, scheme_name="Hash User")


async def validate_token(http_authorization_credentials=Depends(reusable_oauth2)):
    """
    Decode JWT token to get username => return username
    """
    try:
        payload = jwt.decode(
            http_authorization_credentials.credentials,
            jwt_config.SECRET_KEY,
            algorithms=[jwt_config.ALGORITHMS],
        )
        if payload.get("refresh_token") == "True":
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail="Token expired"
            )
        else:
            return (
                payload.get("username"),
                payload.get("refresh_token"),
                payload.get("role"),
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


async def verify_session(
    request: Request,
    session=Depends(session),
    hash_user=Depends(hash_user),
    http_authorization_credentials=Depends(reusable_oauth2),
):
    redis: Redis = request.app.state.redis
    session_info = redis.hgetall(session)
    list_session_user = redis.lrange(hash_user, 0, -1)
    if (
        session_info
        and http_authorization_credentials.credentials
        == session_info.get(b"access_token", b"").decode()
    ):
        return session, hash_user
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate session",
    )


def get_token_rights(dependencies):
    if dependencies[2] == "admin":
        return [True, True]
    elif dependencies[2] == "staff":
        return [True, False]
    elif dependencies[2] == "shipper":
        return [False, True]
    else:
        return [False, False]
