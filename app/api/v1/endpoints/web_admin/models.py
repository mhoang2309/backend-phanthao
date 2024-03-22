from typing import Union

from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_400_BAD_REQUEST

from app.api.base.errors.response import BaseResponse


class Login(BaseModel):
    username: str = Field(..., example="mhoang1998", description="")
    password: str = Field(..., example="123456789X@x", description="")

    class Config:
        extra = Extra.forbid


class Successful(BaseResponse):
    message: str = Field(default="Successful", example="", description="")
    data: Union[dict, list] = Field(default={}, example="", description="")
    status_code: int = Field(default=HTTP_200_OK, example="", description="")


class Error(BaseResponse):
    message: str = Field(default="Bad Request", example="", description="")
    status_code: int = Field(default=HTTP_400_BAD_REQUEST, example="", description="")


class SchemaLogin:
    class SuccessfulLogin(Successful):
        data: dict = Field(
            example={
                "tokens": {"access_token": "token", "refresh_token": "refresh_token"},
                "user": {
                    "id": "id",
                    "username": "username",
                    "name": "name",
                    "phone": "phone",
                    "email": "email",
                    "role": "role",
                },
            },
            description="",
        )

    class ErrorLogin(Error):
        message: str = Field(default="Login false", example="", description="")


class SchemaRegister:
    class Register(Login):
        name: str = Field(
            ...,
            example="Hoang Nguyen",
            description="",
        )
        email: str = Field(..., example="mhoang1998@gmail.com", description="")
        phone: str = Field(..., example="0355438866", description="")
        role: str = Field(default=None, example="shiper", description="")

    class SuccessfulRegister(Successful):
        pass

    class ErrorRegister(Error):
        message: str = Field(
            default="Account already exists", example="", description=""
        )
