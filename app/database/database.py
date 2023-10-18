import sqlite3

class SQLDatabase:
    def __init__(self, name):
        self.conn = sqlite3.connect(name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self, name="default_"):
        self.cur.execute(
            f"""CREATE TABLE IF NOT EXISTS {name} (
                message_id INTEGER PRIMARY KEY,
                chat_id INTEGER,
                date DATETIME,
                AI BOOLEAN,
                content TEXT
            );"""
        )
    
    def add_record(self, name="default_", *, values):
        self._execute(f"""INSERT INTO {name} (chat_id, date, AI, content) 
                         VALUES (1, datetime("now", "localtime"), ?, ?)""", values)
        self._commit()

    def select_all(self, name="default_", *, limit=7):
        self._execute(f"""SELECT * 
                        FROM {name}
                        ORDER BY date DESC 
                        LIMIT {limit}""")
    
        return self._fetchall()
    
    def _execute(self, command, value=None):
        if value:
            self.cur.execute(command, value)
        else:
            self.cur.execute(command)
    
    def _commit(self):
        self.conn.commit()
    
    def _fetchall(self):
        return self.cur.fetchall()