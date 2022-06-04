# -*- coding: utf-8 -*-
import sqlite3
import os
import pickle

# every obj in db should be dumped
sqlite3.register_converter("pickle", pickle.loads)
sqlite3.register_adapter(list, pickle.dumps)
sqlite3.register_adapter(dict, pickle.dumps)
sqlite3.register_adapter(set, pickle.dumps)

class DB():

    def __init__(self, db_path="/home/ubuntu/crontask.db"):
        create_table = False
        if not os.path.exists(db_path):
            create_table = True
        self.conn = sqlite3.connect(db_path, check_same_thread=False, 
                                    detect_types=sqlite3.PARSE_DECLTYPES)
        table_name = "kvdb"
        if create_table:
            self.conn.execute('''
                CREATE TABLE %s(
                    key TEXT PRIMARY KEY,
                    value pickle
                )''' % (table_name)
            )
        self.op_string = {
            'insert_string': "INSERT into %s values (?, ?)" % (table_name),
            'update_string': "UPDATE %s SET value=? WHERE key=?" % (table_name),
            'select_value': "SELECT value FROM %s WHERE key=?" % (table_name),
            'delete_key': 'DELETE from %s where key=?' % (table_name),
        }

    def select(self, key):
        cur = self.conn.cursor()
        if not key:
            cmd = "select * from kvdb"
            ret = cur.execute(cmd).fetchall()
        else:
            cmd = self.op_string['select_value']
            ret = cur.execute(cmd, (key,)).fetchone()
            if ret:
                ret = ret[0]
        cur.close()
        return ret

    def insert(self, k, v):
        if type(v) not in (list, set, dict):
            raise TypeError
        cur = self.conn.cursor()
        try:
            cur.execute(self.op_string['insert_string'], (k, v))
            oprate = 'insert'
        except sqlite3.IntegrityError:
            oprate = 'update'
            cur.execute(self.op_string['update_string'], (v, k))
        cur.close()
        self.conn.commit()
        return oprate

    def delete(self, key):
        cur = self.conn.cursor()
        cur.execute(self.op_string['delete_key'], (key,))
        cur.close()
        self.conn.commit()

    def sqlcmd(self, cmd):
        cur = self.conn.cursor()
        res = cur.execute(cmd).fetchall()
        cur.close()
        return res

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

dbclient = DB()
