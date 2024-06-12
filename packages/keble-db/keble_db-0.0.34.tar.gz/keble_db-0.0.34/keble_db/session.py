from qdrant_client import QdrantClient
from redis import Redis as R, ConnectionPool

from .schemas import DbSettingsABC
from pymongo import MongoClient
from qdrant_client.http import models as qdrant_models
from sqlmodel import create_engine, Session
from sqlalchemy import Engine
from typing import Optional, Mapping, Union
from qdrant_client.http.exceptions import UnexpectedResponse


class Db:

    def __init__(self, settings: DbSettingsABC):
        self.__settings = settings
        self.__redis_pool = ConnectionPool.from_url(settings.redis_uri, decode_responses=True) if settings.redis_uri is not None else None
        self.__sql_read_engine = create_engine(
            str(settings.sql_read_uri if settings.sql_read_uri is not None else settings.sql_uri),
            pool_pre_ping=True,
            pool_size=1000,
            max_overflow=10,
            pool_recycle=3600,
            pool_use_lifo=True,
            echo=False,
        ) if settings.sql_read_uri is not None or settings.sql_uri is not None else None
        self.__sql_write_engine = create_engine(
            str(settings.sql_write_uri if settings.sql_write_uri is not None else settings.sql_uri),
            pool_pre_ping=True,
            pool_size=1000,
            max_overflow=10,

            pool_recycle=3600,
            pool_use_lifo=True,
            echo=False
        ) if settings.sql_write_uri is not None or settings.sql_uri is not None else None

    @property
    def sql_write_engine(self) -> Optional[Engine]:
        return self.__sql_write_engine

    @property
    def sql_read_engine(self) -> Optional[Engine]:
        return self.__sql_read_engine

    def get_redis(self) -> Optional[R]:
        """Return conn to redis
        You do not need to explicitly close the redis conn"""
        if self.__redis_pool is None: return None
        return R(connection_pool=self.__redis_pool)

    def get_mongo(self) -> Optional[MongoClient]:
        """Return a mongo conn
        You do not need to close PyMongo connections. Leave them open so that PyMongo connection pooling gives you the most efficient performance"""
        if self.__settings.mongo_db_uri is None: return None
        return MongoClient(self.__settings.mongo_db_uri, uuidRepresentation="standard")

    def get_qdrant_client(self) -> Optional[QdrantClient]:
        if self.__settings.qdrant_host is None or self.__settings.qdrant_port is None: return None
        return QdrantClient(host=self.__settings.qdrant_host, port=self.__settings.qdrant_port, timeout=120)

    def get_sql_write_client(self) -> Optional[Session]:
        if self.sql_write_engine is None: return None
        return Session(self.sql_write_engine)

    def get_sql_read_client(self) -> Optional[Session]:
        if self.sql_read_engine is None: return None
        return Session(self.sql_read_engine)

    @staticmethod
    def ready_mongo(client: MongoClient):
        # check by list
        client.list_databases()

    @staticmethod
    def ready_redis(redis: R):
        # check by get key
        redis.get("k")

    @staticmethod
    def ready_qdrant(client: QdrantClient, collection: str,
                     vectors_config: Union[qdrant_models.VectorParams, Mapping[str, qdrant_models.VectorParams]]):
        # need to check database exist or not
        try:
            client.get_collection(collection_name=collection)
        except (AssertionError, UnexpectedResponse) as e:
            # collection not found, or connection error. Try to create
            client.create_collection(
                collection_name=collection,
                vectors_config=vectors_config,
            )

    @staticmethod
    def try_close(*sessions: Optional[MongoClient | R | Session | QdrantClient]):
        for session in sessions:
            if session is not None:
                try:
                    session.close()
                except Exception as e:
                    print(f"Failed to close a db session due to {e}")
