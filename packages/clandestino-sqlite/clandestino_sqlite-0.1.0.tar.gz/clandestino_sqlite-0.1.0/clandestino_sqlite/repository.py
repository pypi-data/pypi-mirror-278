from .infra import SQLiteInfra

from clandestino_interfaces import IMigrateRepository


class SQLiteMigrateRepository(IMigrateRepository, SQLiteInfra):

    @classmethod
    def get_control_table(cls):
        return "clandestino"

    @classmethod
    async def create_control_table(cls) -> None:
        control_table = cls.get_control_table()
        sql = f"""
            CREATE TABLE IF NOT EXISTS {control_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT UNIQUE NOT NULL,
                created_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """
        async with cls.get_cursor() as cursor:
            await cursor.execute(sql)

    @classmethod
    async def control_table_exists(cls) -> bool:
        control_table = cls.get_control_table()
        sql = f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name=?
        """
        async with cls.get_cursor() as cursor:
            await cursor.execute(sql, [control_table])
            result = await cursor.fetchone()
        return bool(result)

    @classmethod
    async def register_migration_execution(cls, migration_name: str) -> None:
        control_table = cls.get_control_table()
        sql = f"""
            INSERT INTO {control_table} (migration_name)
            VALUES (?)
        """
        async with cls.get_cursor() as cursor:
            await cursor.execute(sql, [migration_name])

    @classmethod
    async def remove_migration_execution(cls, migration_name: str) -> None:
        control_table = cls.get_control_table()
        sql = f"""
            DELETE FROM {control_table} WHERE migration_name = ?
        """
        async with cls.get_cursor() as cursor:
            await cursor.execute(sql, [migration_name])

    @classmethod
    async def migration_already_executed(cls, migration_name: str) -> bool:
        control_table = cls.get_control_table()
        sql = f"""
            SELECT EXISTS (
                SELECT 1 FROM {control_table}
                WHERE migration_name = ?
            )
        """
        async with cls.get_cursor() as cursor:
            await cursor.execute(sql, [migration_name])
            result = await cursor.fetchone()
        return bool(result[0])
