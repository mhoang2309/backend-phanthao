from fastapi import APIRouter
from starlette.responses import RedirectResponse

from app.web.v1.endpoints import login

web = APIRouter()

@web.get("/", include_in_schema = False)
async def redirect_to_re_doc():
    return RedirectResponse(url = '/login')

web.include_router(login, include_in_schema = False)
