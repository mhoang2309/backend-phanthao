from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import JSONResponse

templates = Jinja2Templates(directory="./app/static/templates")