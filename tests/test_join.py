import os
import unittest

from database import Database
from join import join_index, join
from table import create_from_csv
from test_database import DatabaseTest


class JoinTest(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        DatabaseTest.create_db()
        cls.oConnection = DatabaseTest.connect_db()
        
        cls.db = Database()
        cls.db.add_table('table', create_from_csv("examples/join_table.csv", p_strDelimiter=','))
        cls.db.add_table('addr', create_from_csv("examples/join_addr.csv", p_strDelimiter=','))
        

    @classmethod
    def tearDownClass(cls):
        cls.oConnection.close()
        os.system("rm join.db")
        
    def test_join_index(self):
        self.assertEqual(join_index([[1,2,3], [1,2],[1]]), [1])

    def test_join_index_multiple(self):
        self.assertEqual(join_index([[1,2,3], [1,2],[1,2]]), [1,2])
        
    def test_join_system(self):
        t = join(JoinTest.db.get_table('table'), JoinTest.db.get_table('addr'), [('refaddr', 'id')])
        result = JoinTest.oConnection.execute("select * from join_table t join join_addr a on t.refaddr = a.id")
        self.assertTrue(DatabaseTest.data_equal(result, t))
        
    def test_left_join_system(self):
        t = JoinTest.db.join('table', 'addr', [('refaddr', 'id')], p_strType="left")
        result = JoinTest.oConnection.execute("select * from join_table t left join join_addr a on t.refaddr = a.id")
        self.assertTrue(DatabaseTest.data_equal(result, t))


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(JoinTest)
    unittest.TextTestRunner(verbosity=2).run(suite)