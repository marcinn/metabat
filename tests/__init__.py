
import unittest

class TestEnvironment(unittest.TestCase):
    """
    environment test case
    """
    def test_initialize(self):
        try:
            import pygraph
        except ImportError:
            self.fail()


"""
include all unit tests
"""
from tests.unit import *
