import unittest
from unittest import mock

from task import checkin189
from task.test.fixture import fakedb


class TestCheckin189(unittest.TestCase):
    def setUp(self) -> None:
        self.task = checkin189.checkin189cloud()
        self.db = fakedb()
        return super().setUp()
    
    def test_run_task(self):
        print(f'task name: {self.task.name}')
        with mock.patch('task.utils.db.kvdb', self.db):
            self.task._process189ret = mock.MagicMock()
            self.task.run()
            # 还没账号环境变量
            # self.task._process189ret.assert_called_once()
