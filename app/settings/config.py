import logging
<<<<<<< HEAD
import sys
import configparser
import yaml
from loguru import logger
from pydantic import BaseModel
from enum import Enum
from typing import List
from typing import Dict
from typing import Union
from pydantic import validator
from pydantic import AnyHttpUrl
from pydantic import PostgresDsn
from app.settings.logging import InterceptHandler

with open('config/env.yml') as stream:
    config = yaml.safe_load(stream)

=======
from enum import Enum
from typing import Dict
from typing import List
from typing import Union

import yaml
from loguru import logger
from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import PostgresDsn

from app.settings.logging import InterceptHandler

with open("config/env.yml") as stream:
    config = yaml.safe_load(stream)


>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    WARN = WARNING
<<<<<<< HEAD
    FATAL = CRITICAL    
=======
    FATAL = CRITICAL

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037

class ServerConfig(BaseModel):
    PROJECT_NAME: str = "Fast api"
    ALLOWED_HOSTS: str = "127.0.0.1"
    VERSION: str = "v1.0.0"
    PORT: int = 8000
<<<<<<< HEAD
    DEBUG: bool = False
    WORKERS: int = 1
    PREFIX: str = None
    DOCS_ROUTE: str = "/docs"
    RE_DOC_ROUTE: str = "/redoc"
    
class LoggingConfig(BaseModel):    
=======
    DEBUG: bool = True
    WORKERS: int = 1
    PREFIX: str = ""
    DOCS_ROUTE: str = "/docs"
    RE_DOC_ROUTE: str = "/redoc"


class LoggingConfig(BaseModel):
>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
    RECORD_LOG: bool = True
    LOG_LEVEL: LogLevel = LogLevel.DEBUG
    MAX_BYTES: int = 5000000
    BACKUP_COUNT: int = 7
    PATH_LOG: str = "logs"
<<<<<<< HEAD
    
class CorsMiddlewareConfig(BaseModel):   
    CORS_MIDDLEWARE: Dict[str, Union[List[Union[AnyHttpUrl, str]], bool]] = None
=======


class CorsMiddlewareConfig(BaseModel):
    CORS_MIDDLEWARE: Union[Dict[str, Union[List[Union[AnyHttpUrl, str]], bool]]] = None  # noqa

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037

class RedisConfig(BaseModel):
    HOST_REDIS: str = "127.0.0.1"
    PORT_REDIS: int = 6379
    PASSWORD_REDIS: str = None
<<<<<<< HEAD
    
=======


>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
class MongodbConfig(BaseModel):
    def set_db_url():
        class __Config(BaseModel):
            MONGODB_HOST: str = "127.0.0.1"
            MONGODB_PORT: str = "27017"
            MONGODB_UESR: str = None
            MONGODB_PASSWORD: str = None
            MONGODB_PATH: str = None
<<<<<<< HEAD
=======

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
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
<<<<<<< HEAD
        return PostgresDsn.build(scheme="mongodb", user=cfg.MONGODB_UESR, password=cfg.MONGODB_PASSWORD, host=host, port=port, path=cfg.MONGODB_PATH)
    MONGODB_URL: str = set_db_url()

    
=======
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
>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037


# config = configparser.ConfigParser()
# config.read("./config/config.cfg")

# print(config.get('CONFIG_SERVER','PROJECT_NAME'))
# print(config['CONFIG_SERVER'])
<<<<<<< HEAD
    
=======

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
redis_config = RedisConfig(**config)
server_config = ServerConfig(**config)
logging_config = LoggingConfig(**config)
cors_middleware_config = CorsMiddlewareConfig(**config)
mongodb_config = MongodbConfig(**config)
<<<<<<< HEAD
=======
jwt_config = JWTConfig(**config)
>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037

LOGGING_LEVEL = logging.DEBUG if server_config.DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")

<<<<<<< HEAD
logger.add(logging_config.PATH_LOG + "/{time:YYYY-MM-DD}.log", rotation="1 day", retention="30 days", level=LOGGING_LEVEL)
=======
logger.add(
    logging_config.PATH_LOG + "/{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level=LOGGING_LEVEL,
)

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]
<<<<<<< HEAD
    


=======
>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
