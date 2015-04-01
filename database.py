
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.schema import MetaData
from util import log2


class Database:
    
    def __init__(self, p_strDatabase):
        strConnect = 'sqlite:///{path}'.format(path=p_strDatabase)
        engine = create_engine(strConnect, echo=False)
        self.meta = MetaData()
        self.meta.reflect(bind=engine)
        self.oConnection = engine.connect()
        self.session = sessionmaker(bind=engine)
    
    def __del__(self):
        self.oConnection.close()
    
    def get_tables(self):
        return [table.name for table in reversed(self.meta.sorted_tables)]
    
    def get_columns(self, p_strTable):
        oTable = self.meta.tables[p_strTable]
        return [c.name for c in oTable.c]
    
    def get_unique_value(self, p_strTable, p_strColumn, p_lConditions=[]):
        strConditions = self.condition_to_str(p_lConditions)
        strQuery = "select distinct {column} from {table} {conditions}".format(column=p_strColumn, table=p_strTable, conditions=strConditions)
        result = self.oConnection.execute(strQuery)
        return [row[0] for row in result]
    
    
    def calc_gain(self, lNums):
        fSum = float(sum(lNums))
        fResult = 0
        for num in lNums:
            value = (num / fSum)
            fResult += - value * log2(value)
        return fResult
    
    def condition_to_str(self,p_lConditions=[]):
        strConditions = ""
        if len(p_lConditions) > 0:
            strConditions = "WHERE"
            for entry in p_lConditions:
                strConditions += """ {key}='{value}' AND""".format(key=entry[0],value=entry[1])
        return strConditions[:-4]


    def info_gain(self, p_strTable, p_strColumn, p_lConditions=[]):
        return self.metric_entropy(p_strTable, p_lConditions) - self.metric_entropy_column(p_strTable, p_strColumn, p_lConditions)
        
        
    def get_freq_table(self, p_strTable, p_strColumn, p_lConditions=[], bAsc=None):
        strConditions = self.condition_to_str(p_lConditions)
        
        if bAsc:
            strOrder ="ORDER BY count(*) DESC"
        else:
            strOrder=""
            
        strQuery = "select {column}, count(*) from {table} {conditions} group by {column} {order}".format(table=p_strTable, conditions=strConditions, column=p_strColumn, order=strOrder)
        result = self.oConnection.execute(strQuery)
        return [(row[0],row[1]) for row in result]



    def metric_entropy(self, p_strTable, p_lConditions=[], bCrossTable=False):
        strConditions = self.condition_to_str(p_lConditions)
        strQuery = "select class, count(*) from {table} {conditions} group by Class".format(table=p_strTable, conditions=strConditions)
        result = self.oConnection.execute(strQuery)
        
        lNums = [row[1] for row in result]
        
        fEntropy = self.calc_gain(lNums)
        if bCrossTable:
            lCross = [(row[0],row[1]) for row in result]
            return fEntropy, lCross
        return fEntropy
        
        
    
    def metric_entropy_column(self, p_strTable, p_strColumn, p_lConditions=[]):
        strConditions = self.condition_to_str(p_lConditions)
        strQuery = "select {column}, count(*) from {table} {conditions} group by {column},Class".format(table=p_strTable, conditions=strConditions, column=p_strColumn)
        result = self.oConnection.execute(strQuery)
        
        counter = 0
        strLastColumn = None
        
        lNums = []
        lInfo = []
        lCount = []
       
        while True:
            # fetch the row
            row = result.fetchone()
            
            # if there is no next row -> we're done
            if row is None:
                lInfo.append(self.calc_gain(lNums))
                lCount.append(counter)
                break
            
            # if there is a column switch
            if strLastColumn is not None and row[0] != strLastColumn:
                lInfo.append(self.calc_gain(lNums))
                lCount.append(counter)
                counter = 0
                lNums = []
                
            counter += row[1]
            lNums.append(row[1])
                
            # set the new column
            strLastColumn = row[0]
        
        # calculate the weighted average    
        fGain = 0
        fSum = float(sum(lCount))
        for count, info in zip(lCount, lInfo):
            fGain += (count / fSum) * info
        
        return fGain
   



        
    
    
