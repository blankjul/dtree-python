
import unittest
import metric


class Test(unittest.TestCase):


    def test_info_gain(self):
        self.assertEqual(round(metric.calc_gain([9,5]),2), 0.940)
        


if __name__ == "__main__":
    unittest.main()