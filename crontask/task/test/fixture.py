from unittest import mock

class fakedb:
    def __init__(self) -> None:
        # name: db name/path
        self.db = {}
    
    def select(self, key):
        if key == '*':
            return self.db
        return self.db.get(key)

    def insert(self, key, value):
        self.db[key] = value

