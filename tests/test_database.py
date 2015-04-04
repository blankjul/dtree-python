
from csvkit.utilities.csvsql import CSVSQL
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.schema import MetaData
import sys, os
import unittest

from database import Database
from table import create_from_csv


class DatabaseTest(unittest.TestCase):
    
    @classmethod
    def __create_db(cls):
        sys.stdin.close()
        utility = CSVSQL()
        utility.args.connection_string = "sqlite:///join.db"
        utility.args.insert = True
        utility.args.query = None
        utility.args.input_paths = ["examples/join_table.csv"]
        utility.main()
        utility.args.input_paths = ["examples/join_addr.csv"]
        utility.main()

    @classmethod
    def __connect_db(cls):
        strConnect = 'sqlite:///join.db'
        engine = create_engine(strConnect, echo=False)
        cls.meta = MetaData()
        cls.meta.reflect(bind=engine)
        return engine.connect()
        
        
    @classmethod
    def setUpClass(cls):
        DatabaseTest.__create_db()
        cls.oConnection = DatabaseTest.__connect_db()
        cls.db = Database()
        cls.db.add_table('table', create_from_csv("examples/join_table.csv", p_strDelimiter=','))
        cls.db.add_table('addr', create_from_csv("examples/join_addr.csv", p_strDelimiter=','))
        

    @classmethod
    def tearDownClass(cls):
        cls.oConnection.close()
        os.system("rm join.db")
        
             
    def __data_equal(self, p_genFirst, p_genSecond):
        lFirst = [row for row in p_genFirst]
        lSecond = [row for row in p_genSecond]
        if len(lFirst) != len(lSecond): return False
        for rowOfFirst, rowOfSecond in zip(lFirst, lSecond):
            for entryOfFirst, entryOfSecond in zip (rowOfFirst, rowOfSecond):
                if str(entryOfFirst) != str(entryOfSecond): return False
        return True   
    
    def test_join_system(self):
        t = DatabaseTest.db.join('table', 'addr', [('refaddr', 'id')])
        result = DatabaseTest.oConnection.execute("select * from join_table t join join_addr a on t.refaddr = a.id")
        self.assertEqual(True, self.__data_equal(result, t))
        
    def test_left_join_system(self):
        t = DatabaseTest.db.join('table', 'addr', [('refaddr', 'id')], p_strType="left")
        result = DatabaseTest.oConnection.execute("select * from join_table t left join join_addr a on t.refaddr = a.id")
        self.assertEqual(True, self.__data_equal(result, t))


if __name__ == "__main__":
    unittest.main()