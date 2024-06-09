import os
import sqlite3

from contextlib import asynccontextmanager
from sqlite3 import Connection, Cursor

from decouple import AutoConfig

config = AutoConfig(search_path=os.getcwd())


class SQLiteInfra:

    @classmethod
    async def __get_connection(cls) -> Connection:
        str_connection = config("CLANDESTINO_SQLITE_DB_PATH")
        _connection = sqlite3.connect(str_connection)
        return _connection

    @classmethod
    @asynccontextmanager
    async def get_cursor(cls) -> Cursor:
        connection = None
        cursor = None
        try:
            connection = await cls.__get_connection()
            cursor = connection.cursor()
            yield cursor
        except Exception as e:
            print(f"{cls.__class__}::get_cursor")
            raise e
        finally:
            if connection:
                connection.commit()
                if cursor:
                    cursor.close()
                connection.close()
