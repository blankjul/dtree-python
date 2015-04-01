import unittest
from c45 import next_split, start
from database import Database


class C45Case(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db = Database('quinlan.db')
    
    def test_next_split(self):
        result = next_split(C45Case.db, 'quinlan', [], 'Class')
        self.assertEqual(result, ('Outlook', 0.2467498197744391))
        
    def test_next_split_no_attributes(self):
        result = next_split(C45Case.db, 'quinlan', [('Outlook', ('sunny')), ('Windy', '0')], 'Class')
        self.assertEqual(result, None)
    
    def test_start(self):
        result = start(C45Case.db, 'quinlan', 'Class')
        self.assertEqual(result, None)
