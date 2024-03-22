import logging
from enum import Enum
from typing import Dict, List, Union

import yaml
from loguru import logger
from pydantic import AnyHttpUrl, BaseModel, PostgresDsn

from app.settings.logging import InterceptHandler

with open("config/env.yml") as stream:
    config = yaml.safe_load(stream)


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    WARN = WARNING
    FATAL = CRITICAL


class ServerConfig(BaseModel):
    PROJECT_NAME: str = "Fast api"
    ALLOWED_HOSTS: str = "127.0.0.1"
    VERSION: str = "v1.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    WORKERS: int = 1
    PREFIX: str = ""
    DOCS_ROUTE: str = "/docs"
    RE_DOC_ROUTE: str = "/redoc"


class LoggingConfig(BaseModel):
    RECORD_LOG: bool = True
    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    MAX_BYTES: int = 5000000
    BACKUP_COUNT: int = 7
    PATH_LOG: str = "logs"


class CorsMiddlewareConfig(BaseModel):
    CORS_MIDDLEWARE: Union[Dict[str, Union[List[Union[AnyHttpUrl, str]], bool]]] = None  # noqa


class RedisConfig(BaseModel):
    HOST_REDIS: str = "127.0.0.1"
    PORT_REDIS: int = 6379
    PASSWORD_REDIS: str = None


class MongodbConfig(BaseModel):
    def set_db_url():
        class __Config(BaseModel):
            MONGODB_HOST: str = "127.0.0.1"
            MONGODB_PORT: str = "27017"
            MONGODB_UESR: str = None
            MONGODB_PASSWORD: str = None
            MONGODB_PATH: str = None
        cfg = __Config(**config)
        port = cfg.MONGODB_PORT
        host = cfg.MONGODB_HOST
        if len(str(cfg.MONGODB_HOST).split(":")) > 1:
            if len(str(cfg.MONGODB_HOST).split(",")) > 1:
                port = None
        elif len(str(cfg.MONGODB_HOST).split(",")) > 1:
            host = ""
            for i in str(cfg.MONGODB_HOST).split(","):
                host += i + ":" + str(port) + ","
            if host.endswith(","):
                host = host[:-1]
        return PostgresDsn.build(
            scheme="mongodb",
            user=cfg.MONGODB_UESR,
            password=cfg.MONGODB_PASSWORD,
            host=host,
            port=port,
            path=cfg.MONGODB_PATH,
        )

    MONGODB_URL: str = set_db_url()


class JWTConfig(BaseModel):
    SECRET_KEY: str = ""
    ALGORITHMS: str = "HS256"
    JWT_VERIFY_EMAIL_EXPIRATION_SECONDS: str = ""
    JWT_ACCESS_EXPIRATION_SECONDS: str = ""
    JWT_REFRESH_EXPIRATION_SECONDS: str = ""


# config = configparser.ConfigParser()
# config.read("./config/config.cfg")

# print(config.get('CONFIG_SERVER','PROJECT_NAME'))
# print(config['CONFIG_SERVER'])
redis_config = RedisConfig(**config)
server_config = ServerConfig(**config)
logging_config = LoggingConfig(**config)
cors_middleware_config = CorsMiddlewareConfig(**config)
mongodb_config = MongodbConfig(**config)
jwt_config = JWTConfig(**config)

LOGGING_LEVEL = logging.DEBUG if server_config.DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

logger.add(
    logging_config.PATH_LOG + "/{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level=LOGGING_LEVEL,
)

logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
