from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse

templates = Jinja2Templates(directory="./app/static/templates")

<<<<<<< HEAD
async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        content = {
            'error_code': exc.detail['error_code'],
            'description': exc.detail['description']
        }
    else:
        content = {
            'error_code': None,
            'description': exc.detail
        }
        
    return JSONResponse(
        content=content,
        status_code=exc.status_code
    )
    
=======

async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc.detail, dict):
        content = {
            "error_code": exc.detail["error_code"],
            "description": exc.detail["description"],
        }
    else:
        content = {"error_code": None, "description": exc.detail}

    return JSONResponse(content=content, status_code=exc.status_code)


>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
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
<<<<<<< HEAD
    )
=======
    )
>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
