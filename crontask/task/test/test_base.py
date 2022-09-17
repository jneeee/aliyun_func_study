import unittest

from task import base

class TestTask(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_run(self):
        with self.assertRaises(NotImplementedError):
            base.Task().run()
