from table import Table


class Database:

    def __init__(self):
        self.dTables = {}
    
    
    def add_table(self, p_strName, p_oTable):
        self.dTables[p_strName] = p_oTable


    def get_table(self, p_strName):
        return self.dTables[p_strName]


    def _join_columns(self, p_lColumnsLeft, p_lColumnsRight):
        # generate the header of the new table
        lJoinedColumns = list(p_lColumnsLeft)
        for strColumn in p_lColumnsRight:
            while strColumn in lJoinedColumns:
                strColumn += '_'
            lJoinedColumns.append(strColumn)
        return lJoinedColumns
        
        
    def _hash_column(self, p_strTable, p_lColumns):
        # h the first table
        oTable = self.dTables[p_strTable]
        h = {}
        for i in range(0,oTable.count()):
            entry = oTable.get_row(i, lColumns=p_lColumns)
            h[str(entry)] = i
        return h


    def join(self, p_strLeftTable, p_strRightTable, p_lJoinColumn, p_strType="inner"):
        
        left = self.dTables[p_strLeftTable]
        right = self.dTables[p_strRightTable]
        
        lJoinedColumns = self._join_columns(left.get_columns(), right.get_columns())
        result = Table(lJoinedColumns)
        
        # always hash the left column
        h = self._hash_column(p_strRightTable, [entry[1] for entry in p_lJoinColumn])
        
        # join all the rows that occur at the first table
        for i in range(0,left.count()):
            entry = left.get_row(i, lColumns=[entry[0] for entry in p_lJoinColumn])
            key = str(entry)
            if p_strType=="inner":
                if key in h: result.add_row(left[i] + right[h[key]])
            if p_strType=="left":
                if key in h: result.add_row(left[i] + right[h[key]])
                else: result.add_row(left[i] + [None] * len(right.get_columns()))
                
        return result
    
    