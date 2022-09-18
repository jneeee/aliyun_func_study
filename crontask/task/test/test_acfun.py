import unittest
from unittest import mock

from task.acfun import acfun

class TestAcfun(unittest.TestCase):

    def setUp(self) -> None:
        self.client = acfun.AcFunCheckIn()
        return super().setUp()

    def test_get_video(self):
        self.client.set_session()
        # self.client.get_video()
        # self.client.liketask()
        # self.client.throwbanana()
        self.client.share_task()
