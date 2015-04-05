
def _join_columns( p_lColumnsLeft, p_lColumnsRight):
    # generate the header of the new table
    lJoinedColumns = list(p_lColumnsLeft)
    for strColumn in p_lColumnsRight:
        while strColumn in lJoinedColumns:
            strColumn += '_'
        lJoinedColumns.append(strColumn)
    return lJoinedColumns
    
    
def __gen_inner( p_oLeftTable, p_oRightTable, p_lJoinColumn, p_dHash):
    for i in range(0,p_oLeftTable.count()):
        entry = p_oLeftTable.get_row(i, lColumns=[entry[0] for entry in p_lJoinColumn])
        if entry in p_dHash: 
            for row in p_dHash[entry]: yield p_oLeftTable[i] + p_oRightTable[row]
    
    
def __gen_left(p_oLeftTable, p_oRightTable, p_lJoinColumn, p_dHash):
    for i in range(0,p_oLeftTable.count()):
        entry = p_oLeftTable.get_row(i, lColumns=[entry[0] for entry in p_lJoinColumn])
        if entry in p_dHash: 
            for row in p_dHash[entry]: yield p_oLeftTable[i] + p_oRightTable[row]   
        else: yield p_oLeftTable[i] + tuple([None] * len(p_oRightTable.get_columns()))
        

def join_index(p_lDictRows):
    lResult = []
    # search for the smallest list
    lNums = [len(dRow) for dRow in p_lDictRows]
    index_min = lNums.index(min(lNums))
    # iterate through the list
    for iEntry in p_lDictRows[index_min]:
        bAdd = True
        for i, dRow in enumerate(p_lDictRows):
            if i == index_min: continue
            elif iEntry not in dRow:
                bAdd = False
                break
        if bAdd: lResult.append(iEntry)
    return lResult


def join(p_oLeftTable, p_oRightTable, p_lColumn, p_strType="inner"):
    
    # create the joined columns
    lColumns = _join_columns(p_oLeftTable.get_columns(), p_oRightTable.get_columns())
    lJoinColumns = [entry[1] for entry in p_lColumn]
    
    # always hash the p_oLeftTable column
    dHash = p_oRightTable.get_index(lJoinColumns, p_bCreateIfDoesNotExist=True)
    
    # join all the rows that occur at the first table
    from table import Table
    if p_strType=="inner": return Table(lColumns, __gen_inner(p_oLeftTable, p_oRightTable, p_lColumn, dHash))
    elif p_strType=="left": return Table(lColumns, __gen_left(p_oLeftTable, p_oRightTable, p_lColumn, dHash))
    else: return None