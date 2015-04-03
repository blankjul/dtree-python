
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
        utility.args.input_paths = ["../examples/join_table.csv"]
        utility.main()
        utility.args.input_paths = ["../examples/join_addr.csv"]
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
        

    @classmethod
    def tearDownClass(cls):
        cls.oConnection.close()
        os.system("rm join.db")
        
             
    def __data_equal(self, p_lFirst, p_lSecond):
        if len(p_lFirst) != len(p_lSecond): return False
        for rowOfFirst, rowOfSecond in zip(p_lFirst, p_lSecond):
            for entryOfFirst, entryOfSecond in zip (rowOfFirst, rowOfSecond):
                if str(entryOfFirst) != str(entryOfSecond): return False
        return True   
        
    """
    def test_hash_column(self):
        db = Database()
        db.add_table('system', create_from_csv("../examples/qfin_system.csv"))
        h = db._hash_column('system', "Trade Nr")
        self.assertEqual(len(h), 66429)
    """   
    
    def test_join_system(self):
        db = Database()
        db.add_table('table', create_from_csv("../examples/join_table.csv", p_strDelimiter=','))
        db.add_table('addr', create_from_csv("../examples/join_addr.csv", p_strDelimiter=','))
        t = db.join('table', 'addr', [('refaddr', 'id')])
        strQuery = "select * from join_table t join join_addr a on t.refaddr = a.id"
        result = DatabaseTest.oConnection.execute(strQuery)
        lDataSQL = [row for row in result]
        lDataDB = [row for row in t]
        self.assertEqual(True, self.__data_equal(lDataSQL, lDataDB))
        
    def test_left_join_system(self):
        db = Database()
        db.add_table('table', create_from_csv("../examples/join_table.csv", p_strDelimiter=','))
        db.add_table('addr', create_from_csv("../examples/join_addr.csv", p_strDelimiter=','))
        t = db.join('table', 'addr', [('refaddr', 'id')], p_strType="left")
        strQuery = "select * from join_table t left join join_addr a on t.refaddr = a.id"
        result = DatabaseTest.oConnection.execute(strQuery)
        lDataSQL = [row for row in result]
        lDataDB = [row for row in t]
        self.assertEqual(True, self.__data_equal(lDataSQL, lDataDB))    


if __name__ == "__main__":
    unittest.main()