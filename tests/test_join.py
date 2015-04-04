import unittest
from join import join_index


class JoinTest(unittest.TestCase):

    def test_join_index(self):
        self.assertEqual(join_index([[1,2,3], [1,2],[1]]), [1])

    def test_join_index_multiple(self):
        self.assertEqual(join_index([[1,2,3], [1,2],[1,2]]), [1,2])

if __name__ == "__main__":
    unittest.main()