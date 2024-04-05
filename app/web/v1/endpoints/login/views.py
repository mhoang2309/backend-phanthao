
from fastapi import APIRouter
from starlette.requests import Request
# from starlette.responses import RedirectResponse
from app.web.base.http import templates
from starlette.status import HTTP_200_OK
from app.web.v1.functions.cookie import Cookie


login = APIRouter()

@login.get("/login", include_in_schema = False)
@Cookie()
def redirect_to_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
            status_code=HTTP_200_OK
    )