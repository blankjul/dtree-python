
import unittest

from c45 import next_split, entropy, info, info_gain, start
from table import create_from_csv


class C45Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.quinlan = create_from_csv("examples/quinlan.csv", p_strDelimiter=',')

    def test_entropy(self):
        result = entropy(C45Test.quinlan, "Class")
        self.assertEqual(round(result,2), 0.940)

    def test_entropy_target_once(self):
        quinlan = create_from_csv("examples/quinlan_mod.csv", p_strDelimiter=',')
        result = entropy(quinlan, "ClassPlay")
        self.assertEqual(round(result,2), 0)
        
    def test_entropy_cond(self):
        result = entropy(C45Test.quinlan, "Class", [("Outlook", "overcast")])
        self.assertEqual(result, 0)
        
    def test_info_outlook(self):
        result = info(C45Test.quinlan, "Outlook", "Class")
        self.assertEqual(round(result,3), 0.694)
        
    def test_info_windy(self):
        result = info(C45Test.quinlan, "Windy", "Class")
        self.assertEqual(round(result,3), 0.892)
   
    def test_info_cond(self):
        result = info(C45Test.quinlan, "Windy" , "Class", [("Outlook", "overcast")])
        self.assertEqual(round(result,3), 0)
   
    def test_info_gain_outlook(self):
        result = info_gain(C45Test.quinlan, "Outlook", "Class")
        self.assertEqual(round(result,3), 0.247)
        
    def test_info_gain_windy(self):
        result = info_gain(C45Test.quinlan, "Windy", "Class")
        self.assertEqual(round(result,3), 0.048)

    def test_next_split(self):
        result = next_split(C45Test.quinlan, [], "Class")
        self.assertEqual(result[0], "Outlook")
    
    def test_info_gain_cond(self):
        result = info_gain(C45Test.quinlan, "Windy" , "Class", [("Outlook", "overcast")])
        self.assertEqual(round(result,3), 0)
        
    def test_start(self):
        pass
        #result = start(C45Test.quinlan, "Class")
        #self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
    

   

    
