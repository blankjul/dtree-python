import unittest
from database import Database


class DatabaseCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db = Database('quinlan.db')
    
    def test_get_tables(self):
        result = DatabaseCase.db.get_tables()
        self.assertEqual(True, 'quinlan' in result and 'second' in result)

    def test_get_columns(self):
        result = DatabaseCase.db.get_columns('quinlan')
        expected = [u'Outlook',u'Windy',u'Class']
        self.assertEqual(result, expected)
        
    def test_get_unique_value(self):
        result = DatabaseCase.db.get_unique_value('quinlan', 'outlook', [])
        expected = ['sunny', 'overcast', 'rain']
        self.assertEqual(result, expected)   

    def test_get_freq_table(self):
        result = DatabaseCase.db.get_freq_table('quinlan', 'outlook', [],bAsc=True)
        self.assertEqual(result, [(u'rain', 5), (u'sunny', 5), (u'overcast', 4)])   

    def test_condition_to_str_1(self):
        result = DatabaseCase.db.condition_to_str([('Outlook', ('sunny'))])
        self.assertEqual(result, "WHERE Outlook='sunny'")
        
    def test_condition_to_str_2(self):
        result = DatabaseCase.db.condition_to_str([('Outlook', ('sunny')), ('Windy', '0')])
        self.assertEqual(result, "WHERE Outlook='sunny' AND Windy='0'")
    
    def test_metric_entropy(self):
        result = DatabaseCase.db.metric_entropy('quinlan')
        self.assertEqual(round(result,2), 0.940)

    def test_entropy_outlook(self):
        result = DatabaseCase.db.metric_entropy_column('quinlan', 'Outlook')
        self.assertEqual(round(result,3), 0.694)
        
    def test_entropy_windy(self):
        result = DatabaseCase.db.metric_entropy_column('quinlan', 'Windy')
        self.assertEqual(round(result,3), 0.892)

    def test_info_gain_outlook(self):
        result = DatabaseCase.db.info_gain('quinlan', 'Outlook')
        self.assertEqual(round(result,3), 0.247)
        
    def test_info_gain_windy(self):
        result = DatabaseCase.db.info_gain('quinlan', 'Windy')
        self.assertEqual(round(result,3), 0.048)
        
    def test_entropy_outlook_equal_overcast(self):
        result = DatabaseCase.db.metric_entropy('quinlan',  p_lConditions=[('Outlook', 'overcast')])
        self.assertEqual(round(result,3), 0)   
        
        
        
def main():
    unittest.main()

if __name__ == "__main__":
    main()
