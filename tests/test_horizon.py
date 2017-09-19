"""Test horizon functions."""

import unittest
from WallpDesk import horizon

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_horizon_time(self):
        """> Check horizon for london city"""
        result = horizon.get_horizon_time("London")
        self.assertEqual(list(result.keys()), ["sunset", "sunrise", "today_time", "timezone"])

    def test_get_wrong_horizon_time(self):
        """> Check horizon for mars city"""
        result = horizon.get_horizon_time("Mars City")
        self.assertEqual(result, {})

if __name__ == "__main__":
    unittest.main()
