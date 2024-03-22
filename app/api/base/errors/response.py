from pydantic import BaseModel
from pydantic import Extra


class BaseResponse(BaseModel):
    class Config:
        extra = Extra.forbid


# class Response(BaseResponse):
#     message: str = Field(default="",
#                         example="",
#                         description="")

# class SuccessfulResponse(Response):
#     data: Union[dict, list] = Field(default={},
#                         example="",
#                         description="")
#     status_code: int = Field(default=HTTP_200_OK,
#                     example="",
#                     description="")

# class ErrorResponse(Response):
#     status_code: int = Field(default=HTTP_400_BAD_REQUEST,
#                         example="",
#                         description="")
