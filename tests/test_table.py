import unittest

from table import Table, create_from_csv


class TestTable(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.quinlan = create_from_csv("examples/quinlan.csv", p_strDelimiter=',')

    def test_add_column_init_empty(self):
        t = Table([],[])
        self.assertEqual(t.get_columns(), [])

    def test_add_column_init_elements(self):
        t = Table(['1', '2'], [])
        self.assertEqual(t.get_columns(), ['1', '2'])   

    def test_create_from_csv_column(self):
        self.assertEqual(TestTable.quinlan.get_columns(), ['Outlook','Windy','Class'])   

    def test_create_from_csv_data(self):
        self.assertEqual(TestTable.quinlan.count(), 14)   
        
    def test_add_column(self):
        quinlan = create_from_csv("examples/quinlan.csv", p_strDelimiter=',')
        quinlan.add_column("test", [True] * quinlan.count())
        self.assertEqual(quinlan.get_columns(), ['Outlook','Windy','Class','test'])
    
    def test_add_column_fail(self):
        quinlan = create_from_csv("examples/quinlan.csv", p_strDelimiter=',')
        quinlan.add_column("test", [True] * (quinlan.count()-1))
        self.assertEqual(quinlan.get_columns(), ['Outlook','Windy','Class'])
           
    def test_get_row(self):
        row = TestTable.quinlan.get_row(0)
        self.assertEqual(row, ['sunny', 'true', 'Play'])
    
    def test_get_row_column(self):
        row = TestTable.quinlan.get_row(0, lColumns=['Class'])
        self.assertEqual(row, ['Play'])
        
    def test_get_row_index(self):
        row = TestTable.quinlan[0]
        self.assertEqual(row, ['sunny', 'true', 'Play'])

    def test_get_column_index(self):
        self.assertEqual(TestTable.quinlan.get_column_index("Class"),2)
        
    def test_create_index(self):
        h = TestTable.quinlan.create_index("Outlook")
        self.assertEqual(h, {"['overcast']": set([5, 6, 7, 8]),"['rain']": set([9, 10, 11, 12, 13]),"['sunny']": set([0, 1, 2, 3, 4])}) 
        
    def test_get_index_none(self):
        quinlan = create_from_csv("examples/quinlan.csv", p_strDelimiter=',')
        h = quinlan.get_index("Outlook")
        self.assertEqual(h, None)    
     
    def test_get_index_create(self):
        quinlan = create_from_csv("examples/quinlan.csv", p_strDelimiter=',')
        h = quinlan.get_index("Outlook", p_bCreateIfDoesNotExist=True)
        self.assertEqual(h, {"['overcast']": set([5, 6, 7, 8]),"['rain']": set([9, 10, 11, 12, 13]),"['sunny']": set([0, 1, 2, 3, 4])})   
    
    def test_get_unique(self):
        self.assertEqual(TestTable.quinlan.get_unique("Outlook", []), set(['overcast', 'sunny', 'rain']))
        
    def test_select(self):
        self.assertEqual(TestTable.quinlan.select(p_lConditions=[('Outlook', 'sunny'), ('Windy', 'true'), ('Class', "Don\'t Play")]), [1])
    
    def test_get_freq_table(self):
        self.assertEqual(TestTable.quinlan.get_freq_table('Outlook'),{"['overcast']": 4,"['rain']": 5,"['sunny']": 5})  
        
    def test_get_freq_table_conditions(self):
        self.assertEqual(TestTable.quinlan.get_freq_table(('Outlook'), p_lConditions=[('Outlook', 'sunny')]),{"['sunny']": 5})      
        
    def test_get_freq_table_conditions_multiple(self):
        self.assertEqual(TestTable.quinlan.get_freq_table(('Class'), p_lConditions=[('Outlook', 'sunny'), ('Windy', 'true')]),{'["Don\'t Play"]': 1, "['Play']": 1})      
    
    def test_get_cross_table(self):
        d = TestTable.quinlan.get_cross_table("Outlook", "Class")
        self.assertEqual(d,{'overcast': {'Play': 4}, 'sunny': {'Play': 2, "Don't Play": 3}, 'rain': {'Play': 3, "Don't Play": 2}})
        
    def test_get_cross_table_cond(self):
        d = TestTable.quinlan.get_cross_table("Windy", "Class", p_lConditions=[('Outlook', 'sunny')])
        self.assertEqual(d,{'false': {'Play': 1, "Don't Play": 2}, 'true': {'Play': 1, "Don't Play": 1}})
    
if __name__ == "__main__":
    unittest.main()