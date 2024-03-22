from functools import wraps

from app.library.constant.constants import *


def access():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            session_info = kwargs.get("session_info")
            result = await func(*args, **kwargs)
            return result

        return wrapper

    return decorator
