from app.storage.base import StorageConnector
from app.settings import config
import sqlite3

from typing import cast


class SqliteConnector(StorageConnector[config.SqLiteStorage]):
    __client: sqlite3.Cursor = cast(sqlite3.Cursor, None)

    INSERT_COMMAND = "insert into {table_name} ({columns}) values ({values})'"

    def create_table(self) -> None:
        table_columns = ", ".join(
            [f"{k} {v}" for k, v in self._storage.columns_typing.items()]
        )
        self.__client.execute(
            f"CREATE TABLE {self._storage.table_name} (itemid integer primary key, {table_columns})"
        )

    def init_client(self) -> None:
        self.__con = sqlite3.connect(self._storage.file_path, check_same_thread=False)
        cur = self.__con.cursor()
        self.__client = cur
        self.__client.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.__client.fetchall()
        if not tables:
            self.create_table()

    def select_all(self, name="default", *, limit=7):
        self.__client.execute(
            f"""SELECT * 
                FROM chat
                ORDER BY date DESC 
                LIMIT {limit}"""
        )

        return self.__client.fetchall()

    def insert_many(self, data) -> None:
        for data_sample in data:
            sqlite_repr = data_sample.to_sqlite_database_row()
            cols, values = sqlite_repr.keys(), list(sqlite_repr.values())
            insert_command = self.INSERT_COMMAND.format(
                table_name=self._storage.table_name,
                columns=", ".join(cols),
                values=", ".join(["?"] * len(cols)),
            )
            self.__client.execute(insert_command, values)

    def insert(self, values) -> None:
        self.__client.execute(
            """INSERT INTO chat(chat_id, date, is_ai, content) 
                                VALUES (1, datetime("now", "localtime"), ?, ?)""",
            values,
        )
        self.__con.commit()