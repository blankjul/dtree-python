# -*- coding: utf-8 -*-

import csv
from tabulate import tabulate

from join import join_index


def gen(oReader):
    for row in oReader:
        yield row

def create_from_csv(p_strPath, p_strDelimiter=';', p_strQuotechar="|"):
    with open(p_strPath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=p_strDelimiter, quotechar=p_strQuotechar)
        oTable = Table(reader.next(), gen(reader))
    return oTable



"""
This is an Implementation of a column based Database 
for processing Data with Python.
"""
class Table:
    
    def __init__(self, p_lColumns, p_genData):
        self.lColumns = p_lColumns
        self.dData = {}
        self.iCounter = 0
        for strColumn in p_lColumns:
            self.dData[strColumn] = []
        for lRow in p_genData:
            if len(lRow) != len(self.lColumns): continue
            self.iCounter += 1
            for i, entry in enumerate(lRow):
                self.dData[self.lColumns[i]].append(entry)
        self.dIndex = {}


    def __getitem__(self, iIndex):
        return self.get_row(iIndex)
    
    def __iter__(self):
        for i in range(0, self.count()):
            yield self.get_row(i)

    def get_columns(self):
        return self.lColumns

    def get_row(self, iIndex, lColumns=None):
        row = []
        for strColumn in self.lColumns:
            if lColumns is not None and strColumn not in lColumns: continue
            row.append(self.dData[strColumn][iIndex])
        return row
    
    def count(self):
        return self.iCounter
    
    def add_column(self, p_strName, p_lData):
        if self.iCounter == len(p_lData):
            self.dData[p_strName] = p_lData
            self.lColumns.append(p_strName)
            return True
        else:
            return False
    
    def get_column_index(self, p_strColumnName):
        return self.lColumns.index(p_strColumnName)
    
    def pretty_print(self):
        print tabulate(self.dData, headers="keys", tablefmt="simple")
        
    def get_index(self, p_lColumns, p_bCreateIfDoesNotExist=False):
        if p_bCreateIfDoesNotExist and str(p_lColumns) not in self.dIndex:
            self.create_index(p_lColumns)
        if str(p_lColumns) in self.dIndex: return self.dIndex[str(p_lColumns)]
        else: return None
       
    def create_index(self, p_lColumns):
        h = {}
        for i in range(0, self.count()):
            entry = self.get_row(i, lColumns=p_lColumns)
            if str(entry) not in h: h[str(entry)] = set()
            h[str(entry)].add(i)
        self.dIndex[str(p_lColumns)] = h
        return h


    def select(self, p_lConditions=[]):
        # create a list of rows that are interesting
        if p_lConditions is None or len(p_lConditions) == 0:
            lDictRows = range(0, self.count())
        elif len(p_lConditions) == 1:
            key, value = p_lConditions[0]
            dIndex = self.get_index([key], p_bCreateIfDoesNotExist=True)
            lDictRows = dIndex[str([value])]
        else:
            lDictRows = []
            for key, value in p_lConditions:
                dIndex = self.get_index([key], p_bCreateIfDoesNotExist=True)
                lDictRows.append(dIndex[str([value])])
            lDictRows = join_index(lDictRows)
        return lDictRows
    
    
    def get_freq_table(self, p_strColumn, p_lConditions=[]):
        result = {}
        # get all rows that are fitting to all the conditions
        dIndex = self.get_index([p_strColumn], p_bCreateIfDoesNotExist=True)
        
        # if there are no conditions we are faster
        if p_lConditions is None or len(p_lConditions) == 0:
            for entry in dIndex: result[entry] = len(dIndex[entry])
        # create a selection and look for the conditions while counting
        else: 
            lHashes = self.select(p_lConditions)
            for entry in dIndex:
                joined_hashes = join_index([dIndex[entry], lHashes])
                if len(joined_hashes) > 0: result[entry] = len(joined_hashes)
        return result
    
    def get_cross_table(self, p_strFirstColumn, p_strSecondColumn, p_lConditions=[]):
        if len(p_lConditions) == 0: lRows = range(0, self.count())
        else: lRows = self.select(p_lConditions)
        dResult = {}
        for iRow in lRows:
            lEntry = self.get_row(iRow, [p_strFirstColumn,p_strSecondColumn])
            if lEntry[0] not in dResult: dResult[lEntry[0]] = {}
            if lEntry[1] not in dResult[lEntry[0]]:
                dResult[lEntry[0]][lEntry[1]] = 1
            else:
                dResult[lEntry[0]][lEntry[1]] += 1
        return dResult
        
        
        
      
            
