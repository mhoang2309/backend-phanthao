import uvicorn
import json
from fastapi import FastAPI
from fastapi import Request

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.exceptions import HTTPException

from app.settings.config import server_config
from app.settings.config import cors_middleware_config
from app.settings.config import logging_config
from app.api.base.errors.http_error import http_error_handler
from app.api.base.errors.http_error import http_error_handler_templates
from app.settings.events import create_start_app_handler
from app.settings.events import create_stop_app_handler

from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_413_REQUEST_ENTITY_TOO_LARGE
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=server_config.PROJECT_NAME + " documentation",
        version=server_config.VERSION,
        description="",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {"url": "/static/img/logo.gif"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def get_application() -> FastAPI:
    application = FastAPI(
        title=server_config.PROJECT_NAME,
        debug=server_config.DEBUG,
        version=server_config.VERSION,
        docs_url=server_config.DOCS_ROUTE,
        redoc_url=server_config.RE_DOC_ROUTE,
    )

    application.mount("/static", StaticFiles(directory="app/static"), name="static")
    application.openapi = custom_openapi
    if cors_middleware_config.CORS_MIDDLEWARE:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=cors_middleware_config.CORS_MIDDLEWARE.get("allow_origins", ["*"]),
            allow_credentials=cors_middleware_config.CORS_MIDDLEWARE.get("allow_credentials", False),
            allow_methods=cors_middleware_config.CORS_MIDDLEWARE.get("allow_methods", ["*"]),
            allow_headers=cors_middleware_config.CORS_MIDDLEWARE.get("allow_headers", ["*"]),
        )
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    
    application.add_exception_handler(HTTPException, http_error_handler)
    
    # application.include_router(master_router)
    # application.include_router(api_router, prefix=server_config.PREFIX)

    return application

app = get_application()

@app.exception_handler(HTTP_400_BAD_REQUEST)
@app.exception_handler(HTTP_404_NOT_FOUND)
@app.exception_handler(HTTP_503_SERVICE_UNAVAILABLE)
@app.exception_handler(HTTP_429_TOO_MANY_REQUESTS)
@app.exception_handler(HTTP_413_REQUEST_ENTITY_TOO_LARGE)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return http_error_handler_templates(request, exc)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        port=server_config.PORT,
        host=server_config.ALLOWED_HOSTS,
        workers=server_config.WORKERS,
        log_level=logging_config.LOG_LEVEL,
    )