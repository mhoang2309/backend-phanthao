<<<<<<< HEAD
import redis
import pymongo
from typing import Callable

from loguru import logger
from fastapi import FastAPI

from app.settings.config import redis_config 
from app.settings.config import mongodb_config
=======
from typing import Callable

import pymongo
import redis
from fastapi import FastAPI
from loguru import logger

from app.settings.config import mongodb_config
from app.settings.config import redis_config

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037

def conect_mongodb(app: FastAPI):
    logger.info("Connecting to MongoDB")
    app.state.mongodb = pymongo.MongoClient(mongodb_config.MONGODB_URL)
    app.state.mongodb.server_info()

<<<<<<< HEAD
def conect_redis(app: FastAPI):
    logger.info("Connecting to Redis")
    app.state.redis = redis.Redis(host=redis_config.HOST_REDIS, port=redis_config.PORT_REDIS, password=redis_config.PASSWORD_REDIS)
    app.state.redis.ping()

=======

def conect_redis(app: FastAPI):
    logger.info("Connecting to Redis")
    app.state.redis = redis.Redis(
        host=redis_config.HOST_REDIS,
        port=redis_config.PORT_REDIS,
        password=redis_config.PASSWORD_REDIS,
    )
    app.state.redis.ping()


>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
def close_mongodb(app: FastAPI):
    logger.info("Closing connection to redis")
    app.state.redis.close()
    logger.info("Connection closed")
<<<<<<< HEAD
    
=======


>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
def close_redis(app: FastAPI):
    logger.info("Closing connection to mongodb")
    app.state.mongodb.close()
    logger.info("Connection closed")

<<<<<<< HEAD
=======

>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app():
        conect_redis(app)
        conect_mongodb(app)
<<<<<<< HEAD
    return start_app

=======

    return start_app


>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        """
        TODO: Add documentation here
        :rtype: object
        """
        close_redis(app)
        close_mongodb(app)
<<<<<<< HEAD
    return stop_app
=======

    return stop_app
>>>>>>> b445676237800b9fcee4fb02e59bd54a2e21b037
