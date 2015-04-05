from compiler.misc import Stack

from metric import calc_gain


def start(p_oTable, p_strTarget):
    
    # create a stack for the processing
    s = Stack()
    s.push({ 'iLevel':0, 'lConditions':[] })
    
    print "-------------------------------------------------------------------------"
    
    while len(s) > 0:
        entry = s.pop()
        nextAttr = next_split(p_oTable, entry['lConditions'], p_strTarget)
        # if there is no next attribute or the information gain is zero (perfect decision found), we have a leaf.
        if nextAttr is None or nextAttr[1] == 0:
            
            # get the frequencies and sort them
            dFreq = p_oTable.get_freq_table(p_strTarget, entry['lConditions'])
            lFreqTable = [(k, dFreq[k]) for k in dFreq]
            lFreqTable.sort(key=lambda x: -x[1])
            
            iSum = sum([dFreq[k] for k in dFreq])
            strTarget = lFreqTable[0][0][0]
            fAccuracy = round(lFreqTable[0][1] * 100 / float(iSum), 1)
            
            strInfo = "[{acc}%]".format(acc=fAccuracy)
            pretty_print(entry, p_strTarget=strTarget, p_strInfo=strInfo)
            
        else:
            pretty_print(entry)
            for strUnique in p_oTable.get_unique(nextAttr, entry['lConditions']):
                lConditions = list(entry['lConditions'])
                lConditions.append((nextAttr[0], strUnique))
                s.push({ 'iLevel':entry['iLevel'] + 1, 'lConditions':lConditions })
                
                
    print "-------------------------------------------------------------------------"



def pretty_print(p_dAttr, p_strTarget=None, p_strInfo=None):
    strPrint = ""
    # print p_dAttr['iLevel']
    for _ in range(0, p_dAttr['iLevel']):
        strPrint += "    "
        
    if len(p_dAttr['lConditions']) > 0:
        strPrint += "{key}={value}".format(key=p_dAttr['lConditions'][-1][0], value=p_dAttr['lConditions'][-1][1])
    else:
        strPrint += "all"
        
    if p_strTarget: strPrint += " -> " + p_strTarget
    if p_strInfo: strPrint += " " + p_strInfo
    print strPrint



def entropy(p_oTable, p_strColumn, p_lConditions=[]):
    dIndex = p_oTable.get_index(p_strColumn, p_bCreateIfDoesNotExist=True)
    if len(p_lConditions) == 0: lNums = [len(dIndex[strKey]) for strKey in dIndex]
    else: 
        lNums = []
        dRows = set()
        for entry in p_oTable.select(p_lConditions): dRows.add(entry)
        for strKey in dIndex:
            iLength = len([key for key in dIndex[strKey] if key in dRows])
            if iLength > 0: lNums.append(iLength)
    fEntropy =  calc_gain(lNums)
    return fEntropy

def info(p_oTable, p_strColumn, p_strTarget, p_lConditions=[]):
    dCross, lRows = p_oTable.get_cross_table(p_strColumn, p_strTarget, p_lConditions, p_bReturnRowIndex=True)
    iCount = len(lRows)
    fInfo = 0
    for strUnique in dCross:
        dIndex = dCross[strUnique]
        # calculate the info gain if split
        lNums = [dIndex[strKey] for strKey in dIndex]
        iSum = sum(lNums)
        fGain = calc_gain(lNums, iSum)
        # add the weighted value
        fInfo += (iSum / float(iCount)) * fGain
    return fInfo


def info_gain(p_oTable, p_strColumn, p_strTarget, p_lConditions=[], par_fEntropy=None):
    if par_fEntropy is None: par_fEntropy = entropy(p_oTable, p_strTarget, p_lConditions)
    return par_fEntropy - info(p_oTable, p_strColumn, p_strTarget, p_lConditions)


def next_split(p_oTable, p_lConditions, p_strTarget):
    lColumns = []
    lAttr = [attr for attr, _ in p_lConditions]
    fEntropy = entropy(p_oTable, p_strTarget, p_lConditions)
    if fEntropy == 0: return None
    
    for strColumn in p_oTable.get_columns():
        if strColumn in lAttr or strColumn == p_strTarget: continue
        fGain = info_gain(p_oTable, strColumn, p_strTarget, p_lConditions, par_fEntropy=fEntropy)
        lColumns.append((strColumn, fGain))
        
    if len(lColumns) == 0: return None
    lColumns.sort(key=lambda x:-x[1])    
    
    return lColumns[0]


