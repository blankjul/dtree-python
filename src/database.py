import join


class Database:

    def __init__(self):
        self.dTables = {}
    
    
    def add_table(self, p_strName, p_oTable):
        self.dTables[p_strName] = p_oTable


    def get_table(self, p_strName):
        return self.dTables[p_strName]


    def join(self, p_strLeftTable, p_strRightTable, p_lColumn, p_strType="inner"):
        return join.join(self.dTables[p_strLeftTable], self.dTables[p_strRightTable], p_lColumn, p_strType)

    
    