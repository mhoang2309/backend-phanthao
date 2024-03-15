from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse

templates = Jinja2Templates(directory="./app/static/templates")


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        content = {
            "error_code": exc.detail["error_code"],
            "description": exc.detail["description"],
        }
    else:
        content = {"error_code": None, "description": exc.detail}

    return JSONResponse(content=content, status_code=exc.status_code)


def http_error_handler_templates(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error_page.html",
        {
            "request": request,
            "error_code": exc.status_code,
            "message": exc.detail,
            "error_message": "Look like you're lost the page you are looking for not avaible!",
        },
        status_code=exc.status_code,
    )
