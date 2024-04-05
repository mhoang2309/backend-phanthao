import functools
from starlette.requests import Request
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from app.services.security import verify_session
from dataclasses import dataclass
import asyncio

@dataclass
class Credentials:
    credentials: str = ""

class Cookie:
    def __init__(self):
        pass
    def __call__(self, func) :
        return self.check_session(func=func)
    
    def check_session(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                request: Request = kwargs.get("request")
                token = request.cookies.get("_authorization", "")
                session = request.cookies.get("_session", "")
                hash_user = request.cookies.get("_hash_user", "")
                http_authorization_credentials = Credentials(token)
                asyncio.run(verify_session(request=request, session=session, hash_user=hash_user, http_authorization_credentials=http_authorization_credentials))
                if func.__name__=="redirect_to_login":
                    raise HTTPException(
                        status_code=HTTP_404_NOT_FOUND, detail="Token expired"
                    )
                result = func(*args, **kwargs)
                return result
            except HTTPException as exc:
                if func.__name__=="redirect_to_login":
                    result = func(*args, **kwargs)
                    return result
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND, detail="Token expired"
                )

        return wrapper