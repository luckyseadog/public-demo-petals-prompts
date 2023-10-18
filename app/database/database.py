import sqlite3

class SQLDatabase:
    def __init__(self, name):
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            user VARCHAR(32),
            date DATETIME,
            content TEXT
        );"""
        )
    
    def execute(self, command, value=None):
        if value:
            self.cur.execute(command, value)
        else:
            self.cur.execute(command)

    def commit(self):
        self.conn.commit()

    def fetchall(self):
        return self.cur.fetchall()