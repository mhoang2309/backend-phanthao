import uvicorn
from fastapi import FastAPI, Request, applications
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger
from starlette.responses import RedirectResponse
from starlette.status import (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                              HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                              HTTP_429_TOO_MANY_REQUESTS,
                              HTTP_500_INTERNAL_SERVER_ERROR,
                              HTTP_503_SERVICE_UNAVAILABLE)

from app.api.base.errors.http_error import http_error_handler  # noqa
from app.api.base.errors.http_error import http_error_handler_templates
from app.api.v1.routers import api
from app.web.v1.routers import web
from app.settings.config import (cors_middleware_config, logging_config,
                                 server_config)
from app.settings.events import (create_start_app_handler,
                                 create_stop_app_handler)

# import fastapi.openapi.utils as fu


# fu.validation_error_response_definition = ErrorResponse.schema()


def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args, **kwargs, swagger_favicon_url="static/img/free-logo.svg"
    )


def swagger_redoc(*args, **kwargs):
    return get_redoc_html(*args, **kwargs, redoc_favicon_url="static/img/free-logo.svg")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=server_config.PROJECT_NAME + " documentation",
        version=server_config.VERSION,
        description="",
        routes=app.routes,
    )

    openapi_schema["info"]["x-logo"] = {"url": "/static/img/free-logo.svg"}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def get_application() -> FastAPI:
    applications.get_swagger_ui_html = swagger_monkey_patch
    applications.get_redoc_html = swagger_redoc
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
            allow_origins=cors_middleware_config.CORS_MIDDLEWARE.get(
                "allow_origins", ["*"]
            ),
            allow_credentials=cors_middleware_config.CORS_MIDDLEWARE.get(
                "allow_credentials", False
            ),
            allow_methods=cors_middleware_config.CORS_MIDDLEWARE.get(
                "allow_methods", ["*"]
            ),
            allow_headers=cors_middleware_config.CORS_MIDDLEWARE.get(
                "allow_headers", ["*"]
            ),
        )
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)

    # application.include_router(master_router)
    application.include_router(api, prefix=server_config.PREFIX_API)
    application.include_router(web, prefix=server_config.PREFIX_WEB)

    return application


app = get_application()


@app.exception_handler(HTTP_400_BAD_REQUEST)
# @app.exception_handler(HTTP_404_NOT_FOUND)
@app.exception_handler(HTTP_503_SERVICE_UNAVAILABLE)
@app.exception_handler(HTTP_429_TOO_MANY_REQUESTS)
@app.exception_handler(HTTP_413_REQUEST_ENTITY_TOO_LARGE)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return http_error_handler_templates(request, exc)

@app.exception_handler(HTTP_404_NOT_FOUND)
async def redirect_response(request: Request, exc: HTTPException):
    return RedirectResponse(url = '/')

@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as ex:
        trace = None
        tb = ex.__traceback__
        message = f" {str(type(ex).__name__)} {str(ex)}"
        while tb is not None:
            trace = tb
            tb = tb.tb_next
        logger.error("".join(str(trace.tb_frame).split(",")[1:3]) + message)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"message": message}
        )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        port=server_config.PORT,
        host=server_config.ALLOWED_HOSTS,
        workers=server_config.WORKERS,
        log_level=logging_config.LOG_LEVEL,
    )
