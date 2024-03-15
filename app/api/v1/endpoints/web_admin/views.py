import datetime
import hashlib
import uuid

import jwt
import unidecode
from bson import ObjectId
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Request
from redis import Redis
from starlette.responses import JSONResponse
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.api.base.errors.functions import open_api_standard_responses
from app.api.v1.endpoints.web_admin.constants import *
from app.api.v1.endpoints.web_admin.models import *
from app.library.constant.constants import DB_MANAGE
from app.library.constant.constants import Role
from app.services.decentralization import access
from app.services.security import validate_token
from app.services.security import verify_session
from app.settings.config import jwt_config

api_user = APIRouter()


@api_user.post(
    path="/register",
    name="Register",
    dependencies="",
    responses=open_api_standard_responses(
        success_response_model=SchemaRegister.SuccessfulRegister,
        fail_response_model=SchemaRegister.ErrorRegister,
    ),
    response_model=SchemaRegister.SuccessfulRegister,
)
@access()
async def register(
    request: Request,
    payload: SchemaRegister.Register = Body(...),
    dependencies: str = Depends(validate_token),
    session_info: tuple = Depends(verify_session),
):
    db = getattr(request.app.state.mongodb, DB_MANAGE)
    tb_user = getattr(db, TB_USER)

    username = unidecode.unidecode(payload.username)
    info_user = tb_user.find_one({"username": username})
    if info_user:
        error_response = SchemaRegister.ErrorRegister()
        return JSONResponse(error_response.dict(), error_response.status_code)
    role = payload.role or Role.UNDEFINED
    if role == "admin" and role not in Role.__dict__.values():
        error_response = SchemaRegister.ErrorRegister(
            message="You can not react new account which role is admin"
        )
        return JSONResponse(error_response.dict(), error_response.status_code)
    payload.password = generate_password_hash(
        payload.password,
        method=METHOD_PASSWORD_HASH,
        salt_length=SALT_LENGTH_PASSWORD_HASH,
    )
    payload.role = role
    payload: dict = payload.dict()
    payload.update({"_id": str(ObjectId()), "active": False})
    tb_user.insert_one(payload)
    payload.pop("password")
    return SchemaRegister.SuccessfulRegister(data=payload)


@api_user.post(
    path="/login",
    name="Login",
    dependencies="",
    responses=open_api_standard_responses(
        success_response_model=SchemaLogin.SuccessfulLogin,
        fail_response_model=SchemaLogin.ErrorLogin,
    ),
    response_model=SchemaLogin.SuccessfulLogin,
)
async def login(request: Request, payload: Login = Body(...)):
    db = getattr(request.app.state.mongodb, DB_MANAGE)
    tb_user = getattr(db, TB_USER)
    redis: Redis = request.app.state.redis

    username = unidecode.unidecode(payload.username)
    info_user: dict = tb_user.find_one({"username": username})
    if info_user.get("active") and check_password_hash(
        info_user.pop("password"), payload.password
    ):
        token = jwt.encode(
            {
                "username": info_user.get("username"),
                "role": info_user.get("role"),
                "refresh_token": "False",
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    seconds=int(jwt_config.JWT_ACCESS_EXPIRATION_SECONDS)
                ),
            },
            jwt_config.SECRET_KEY,
        )
        refresh_token = jwt.encode(
            {
                "username": info_user.get("username"),
                "role": info_user.get("role"),
                "refresh_token": "True",
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(
                    seconds=int(jwt_config.JWT_REFRESH_EXPIRATION_SECONDS)
                ),
            },
            jwt_config.SECRET_KEY,
        )
        session = uuid.uuid4().hex
        hash_username = hashlib.sha256(username.encode()).hexdigest()
        device_info_headers = {
            "host": request.headers.get("host", ""),
            "user_agent": request.headers.get("user-agent", ""),
            "platform": request.headers.get("sec-ch-ua-platform", ""),
        }
        device_id = request.headers.get("device-id")
        if not device_id:
            device_id = uuid.uuid4().hex
            redis.hset(device_id, mapping=device_info_headers)
            redis.expire(name=device_id, time=jwt_config.JWT_REFRESH_EXPIRATION_SECONDS)
        else:
            device_info = redis.hgetall(device_id)
            device_info = {
                key.decode("utf-8"): value.decode("utf-8")
                if isinstance(value, bytes)
                else value
                for key, value in data.items()
            }
            if device_info != device_info_headers:
                error_response = SchemaLogin.ErrorLogin()
                return JSONResponse(error_response.dict(), error_response.status_code)

        tokens = {"access_token": token, "refresh_token": refresh_token}

        if redis.lpush(hash_username, device_id) >= TOTAL_DEVICE:
            # _session = redis.lpop(hash_username, -1)
            # redis.delete(_session)
            #     # list_session = [hash_username]
            #     # list_session += redis.lrange(hash_username, 0, -1)
            #     # for item in list_session:
            #     #     redis.delete(item)
            #     # redis.lpush(hash_username, session)
            error_response = SchemaLogin.ErrorLogin()
            return JSONResponse(error_response.dict(), error_response.status_code)
        redis.hset(session, mapping=tokens)
        redis.expire(name=session, time=jwt_config.JWT_ACCESS_EXPIRATION_SECONDS)
        redis.expire(name=hash_username, time=jwt_config.JWT_REFRESH_EXPIRATION_SECONDS)
        info_user.pop("_id")
        info_user.pop("active")
        data = {
            "session": session,
            "hash_username": hash_username,
            "tokens": tokens,
            "user": info_user,
        }
        return SchemaLogin.SuccessfulLogin(data=data)
    error_response = SchemaLogin.ErrorLogin()
    return JSONResponse(error_response.dict(), error_response.status_code)


@api_user.post(
    path="/logout",
    name="Logout",
    dependencies="",
    responses=open_api_standard_responses(
        success_response_model=SchemaLogin.SuccessfulLogin,
        fail_response_model=SchemaLogin.ErrorLogin,
    ),
    response_model=SchemaLogin.SuccessfulLogin,
)
async def logout(
    request: Request,
    dependencies: tuple = Depends(validate_token),
    session_info: tuple = Depends(verify_session),
):
    redis: Redis = request.app.state.redis
    session, hash_username = session_info
    redis.lrem(hash_username, 1, session)
    redis.delete(session)
    return Successful()
