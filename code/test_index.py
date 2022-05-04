import unittest
from unittest import mock

from index import process189ret
from index import initializer
import utils.db

class test_indexhandle(unittest.TestCase):

    def setUp(self) -> None:
        initializer('asd')
        return super().setUp()

    @mock.patch.object(utils.db, 'DB')
    def test_process189(self, dbclient_mock):
        dbclient_mock.select.return_value = [["""
            {'checkin189': '{
                "time": "2023-05-04 04:55:12", 
                "checkin_space": 95, 
                "lottery_space": 100, 
                "total": 585}'}"""]]
        ret = {'time': '2022-05-04 04:55:12', 'checkin_space': 50, 'lottery_space': 50}
        dbclient_mock.insert.return_value = None
        process189ret(ret)
        dbclient_mock.insert.assert_called_with('checkin189', {'time': '2023-05-04 04:55:12', 'checkin_space': 95, 'lottery_space': 100, 'total': 780})
        
if __name__ == '__main__':
    unittest.main()
