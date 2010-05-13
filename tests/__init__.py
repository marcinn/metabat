
import unittest

class TestEnvironment(unittest.TestCase):
    def test_initialize(self):
        try:
            import pygraph
        except ImportError:
            self.fail()
