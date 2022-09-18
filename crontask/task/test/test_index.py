import unittest
from unittest import mock
from json import dumps

import task
from index import handler

class Testhandler(unittest.TestCase):

    def test_handler(self):
        event = {
            "triggerTime": "2018-02-09T05:49:00Z",
            "triggerName": "my_trigger",
            "payload": ["checkin189cloud"],
        }
        task.checkin189.checkin189cloud.run = mock.MagicMock()
        handler(dumps(event), '')
        task.checkin189.checkin189cloud.run.assert_called_once()
