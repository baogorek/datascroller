import unittest

class TestBasic(unittest.TestCase):
    def setUp(self):
        self.x = 3

    def test_x(self):
        self.assertEqual(self.x, 4)
