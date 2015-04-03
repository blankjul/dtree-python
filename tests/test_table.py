import unittest

from table import Table, create_from_csv


class TestTable(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_add_column_init_empty(self):
        t = Table([])
        self.assertEqual(t.get_columns(), [], "No Columns when initialized")

    def test_add_column_init_elements(self):
        t = Table(['1', '2'])
        self.assertEqual(t.get_columns(), ['1', '2'], "Two columns matches.")   

    def test_create_from_csv_column(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        self.assertEqual(t.get_columns(), ['Outlook','Windy','Class'])   

    def test_create_from_csv_data(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        self.assertEqual(t.count(), 14)   
        
    def test_remove_row(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        t.remove_row(0)
        lCount = []
        for strColumn in t.lColumns:
            lCount.append(len(t.dData[strColumn])) 
        self.assertEqual(lCount, [13,13,13])   
        
    def test_get_row(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        row = t.get_row(0)
        self.assertEqual(row, ['sunny', 'true', 'Play'])
    
    def test_get_row_column(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        row = t.get_row(0, lColumns=['Class'])
        self.assertEqual(row, ['Play'])
        
    def test_get_row_index(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        row = t[0]
        self.assertEqual(row, ['sunny', 'true', 'Play'])

    def test_get_column_index(self):
        t = create_from_csv("../examples/quinlan.csv", p_strDelimiter=',')
        self.assertEqual(t.get_column_index("Class"),2)

    
if __name__ == "__main__":
    unittest.main()