from app.storage.base import StorageConnector
from app.settings import config
import sqlite3

from typing import cast


class SqliteConnector(StorageConnector[config.SqLiteStorage]):
    _client: sqlite3.Cursor = cast(sqlite3.Cursor, None)

    INSERT_COMMAND = "insert into {table_name} ({columns}) values ({values})'"

    def __init__(self, storage_) -> None:
        super().__init__(storage_)
        self._con = sqlite3.connect(self._storage.file_path, check_same_thread=False)
        self._client = self._con.cursor()
        self.create_table()

    def create_table(self) -> None:
        table_columns = ", ".join(
            [f"{k} {v}" for k, v in self._storage.columns_typing.items()]
        )
        self._client.execute(
            f"""CREATE TABLE IF NOT EXISTS {self._storage.table_name} 
            (message_id integer primary key, {table_columns})"""
        )
        self._con.commit()

    def select_all(self, *, limit=7):
        self._client.execute(
            f"""SELECT * 
                FROM {self._storage.table_name}
                ORDER BY date DESC 
                LIMIT {limit}"""
        )

        return self._client.fetchall()

    def select_by_chat(self, *, chat_id, limit=7):
        self._client.execute(
            f"""SELECT *
                FROM {self._storage.table_name}
                WHERE chat_id = {chat_id}
                ORDER BY date DESC 
                LIMIT {limit}"""
        )

        return self._client.fetchall()


    # def insert_many(self, data) -> None:
    #     for data_sample in data:
    #         sqlite_repr = data_sample.to_sqlite_database_row()
    #         cols, values = sqlite_repr.keys(), list(sqlite_repr.values())
    #         insert_command = self.INSERT_COMMAND.format(
    #             table_name=self._storage.table_name,
    #             columns=", ".join(cols),
    #             values=", ".join(["?"] * len(cols)),
    #         )
    #         self._client.execute(insert_command, values)

    def insert(self, chat_id, is_ai, content) -> None:
        self._client.execute(
            """INSERT INTO messages(chat_id, date, is_ai, content) 
                                VALUES (?, datetime("now", "localtime"), ?, ?)""",
            (chat_id, is_ai, content)
        )
        self._con.commit()