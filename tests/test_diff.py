
import unittest

from table import create_from_csv
from diff import compare


class DiffTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tbl = create_from_csv("examples/diff.csv", p_strDelimiter=',')

    def test_compare_equal(self):
        v = compare(DiffTest.tbl, "Outlook", "Outlook_")
        self.assertEqual(v, [True] * DiffTest.tbl.count())

    def test_compare_one_deviation(self):
        v = compare(DiffTest.tbl, "Outlook", "Outlook__")
        self.assertEqual(v, [True, True, True, True, True, False, True, True, True, True, True, True, True, True])


if __name__ == "__main__":
    unittest.main()