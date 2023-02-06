import psycopg2.pool

from typing import Generator
from psycopg2.extensions import connection
from contextlib import contextmanager

from .config import Config


class Pool:
    pools = dict()

    @classmethod
    def init_pool(cls, name, minconn=1, maxconn=10):
        cls.pools[name] = psycopg2.pool.ThreadedConnectionPool(
            minconn,
            maxconn,
            Config.main["connect_string"],
        )

    @classmethod
    @contextmanager
    def get_db(cls, name="default") -> Generator[connection, None, None]:
        if name not in cls.pools:
            cls.init_pool(name)

        connect = cls.pools[name].getconn()
        try:
            yield connect
        except Exception:
            raise Exception("Failed to get connection!")
        finally:
            cls.pools[name].putconn(connect)
