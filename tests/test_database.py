
from csvkit.utilities.csvsql import CSVSQL
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.schema import MetaData
import sys
import unittest



class DatabaseTest(unittest.TestCase):
    
    @classmethod
    def create_db(cls):
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
    def connect_db(cls):
        strConnect = 'sqlite:///join.db'
        engine = create_engine(strConnect, echo=False)
        cls.meta = MetaData()
        cls.meta.reflect(bind=engine)
        return engine.connect()
        
        
        
        
    @classmethod         
    def data_equal(cls, p_genFirst, p_genSecond):
        lFirst = [row for row in p_genFirst]
        lSecond = [row for row in p_genSecond]
        if len(lFirst) != len(lSecond): return False
        for rowOfFirst, rowOfSecond in zip(lFirst, lSecond):
            for entryOfFirst, entryOfSecond in zip (rowOfFirst, rowOfSecond):
                if str(entryOfFirst) != str(entryOfSecond): return False
        return True   
    



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(DatabaseTest)
    unittest.TextTestRunner(verbosity=2).run(suite)