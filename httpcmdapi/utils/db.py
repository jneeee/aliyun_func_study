import sqlite3
import os
import json

class DB():

    def __init__(self, db_path="/home/ubuntu/crontask.db"):
        create_table = False
        if not os.path.exists(db_path):
            create_table = True
        self.conn = sqlite3.connect(db_path)
        if create_table:
            self.conn.execute('''
                CREATE TABLE kvdb(
                    key text UNIQUE,
                    value text
                )'''
            )
        self.cur = self.conn.cursor()
    
    def select(self, key):
        ret = self.cur.execute(f"select * from kvdb where key = '{key}';")
        data = {}
        for k, v in ret.fetchall():
            data[k] = json.loads(v)
        return data

    def insert(self, k, v):
        try:
            self.cur.execute(f"insert into kvdb values ('{k}','{json.dumps(v)}');")
        except sqlite3.IntegrityError:
            self.cur.execute(f"update kvdb set value = '{json.dumps(v)}' where key = '{k}';")
        self.conn.commit()

    def delete(self, key):
        self.cur.execute("delete from kvdb where key = '{key}';")
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()
