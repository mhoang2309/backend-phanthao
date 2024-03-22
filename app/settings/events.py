import redis
import pymongo
from typing import Callable

from loguru import logger
from fastapi import FastAPI

from app.settings.config import redis_config 
from app.settings.config import mongodb_config

def conect_mongodb(app: FastAPI):
    logger.info("Connecting to MongoDB")
    app.state.mongodb = pymongo.MongoClient(mongodb_config.MONGODB_URL)
    app.state.mongodb.server_info()

def conect_redis(app: FastAPI):
    logger.info("Connecting to Redis")
    app.state.redis = redis.Redis(host=redis_config.HOST_REDIS, port=redis_config.PORT_REDIS, password=redis_config.PASSWORD_REDIS)
    app.state.redis.ping()

def close_mongodb(app: FastAPI):
    logger.info("Closing connection to redis")
    app.state.redis.close()
    logger.info("Connection closed")
    
def close_redis(app: FastAPI):
    logger.info("Closing connection to mongodb")
    app.state.mongodb.close()
    logger.info("Connection closed")

def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app():
        conect_redis(app)
        conect_mongodb(app)
    return start_app

def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        """
        TODO: Add documentation here
        :rtype: object
        """
        close_redis(app)
        close_mongodb(app)
    return stop_app