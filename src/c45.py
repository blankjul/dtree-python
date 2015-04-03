from compiler.misc import Stack


def start(p_oDatabase, p_strTable, p_strTarget):
    
    # create a stack for the processing
    s = Stack()
    s.push({ 'iLevel':0, 'lConditions':[] })
    
    print "-------------------------------------------------------------------------"
    
    while len(s) > 0:
        entry = s.pop()
        nextAttr = next_split(p_oDatabase, p_strTable, entry['lConditions'], p_strTarget)
        
        # if there is no next attribute or the information gain is zero (perfect decision found), we have a leaf.
        if nextAttr is None or nextAttr[1] == 0:
            lFreqTable = p_oDatabase.get_freq_table(p_strTable, p_strTarget, entry['lConditions'], bAsc=True)
            iSum = sum([element[1] for element in lFreqTable])
            strTarget = lFreqTable[0][0]
            fAccuracy = round(lFreqTable[0][1] * 100 / float(iSum),1)
            strInfo = "[{acc}%]".format(acc=fAccuracy)
            pretty_print(entry, p_strTarget=strTarget, p_strInfo=strInfo)
        else:
            pretty_print(entry)
            for strUnique in p_oDatabase.get_unique_value(p_strTable, nextAttr[0]):
                lConditions = list(entry['lConditions'])
                lConditions.append((nextAttr[0], strUnique))
                s.push({ 'iLevel':entry['iLevel'] + 1, 'lConditions':lConditions })
                
                
    print "-------------------------------------------------------------------------"



def pretty_print(p_dAttr, p_strTarget=None, p_strInfo=None):
    strPrint = ""
    #print p_dAttr['iLevel']
    for _ in range(0, p_dAttr['iLevel']):
        strPrint += "    "
        
    if len(p_dAttr['lConditions']) > 0:
        strPrint += "{key}={value}".format(key=p_dAttr['lConditions'][-1][0], value=p_dAttr['lConditions'][-1][1])
    else:
        strPrint += "all"
        
    if p_strTarget: strPrint += " -> " + p_strTarget 
    if p_strInfo: strPrint +=  " " + p_strInfo
    print strPrint


def next_split(p_oDatabase, p_strTable, p_lConditions, p_strTarget):
    lColumns = []
    lAttr = [attr for attr, _ in p_lConditions]
    for strColumn in p_oDatabase.get_columns(p_strTable):
        
        if strColumn in lAttr or strColumn == p_strTarget: continue
        
        fGain = p_oDatabase.info_gain(p_strTable, strColumn, p_strTarget, p_lConditions)
        lColumns.append((strColumn, fGain))
        
    if len(lColumns) == 0: return None
     
    lColumns.sort(key=lambda x:-x[1])    
    
    return lColumns[0]


