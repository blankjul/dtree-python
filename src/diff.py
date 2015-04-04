

def compare(p_oTable, p_strColumnLeft, p_strColumnRight):
    result = []
    left = p_oTable.dData[p_strColumnLeft]
    right = p_oTable.dData[p_strColumnRight]
    for l,r in zip(left,right):
        if l == r: result.append(True)
        else: result.append(False)
    return result