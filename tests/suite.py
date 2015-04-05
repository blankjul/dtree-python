import unittest

from test_c45 import C45Test
from test_database import DatabaseTest
from test_join import JoinTest
from test_metric import MetricTest
from test_table import TestTable
from test_diff import DiffTest


c45 = unittest.TestLoader().loadTestsFromTestCase(C45Test)
db = unittest.TestLoader().loadTestsFromTestCase(DatabaseTest)
table = unittest.TestLoader().loadTestsFromTestCase(TestTable)
metric = unittest.TestLoader().loadTestsFromTestCase(MetricTest)
join = unittest.TestLoader().loadTestsFromTestCase(JoinTest)
diff = unittest.TestLoader().loadTestsFromTestCase(DiffTest)

alltests = unittest.TestSuite([c45, db, table, metric, join, diff])
unittest.TextTestRunner(verbosity=2).run(alltests)
