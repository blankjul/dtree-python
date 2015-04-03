# -*- coding: utf-8 -*-

from tabulate import tabulate
import csv


def create_from_csv(p_strPath, p_strDelimiter=';', p_strQuotechar="|"):
    with open(p_strPath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=p_strDelimiter, quotechar=p_strQuotechar)
        oTable = Table(reader.next())
        for row in reader:
            oTable.add_row(row)
    return oTable



"""
This is an Implementation of a column based Database 
for processing Data with Python.
"""
class Table:
    
    def __init__(self, p_lColumns):
        self.lColumns = p_lColumns
        self.dData = {}
        for strColumn in p_lColumns:
            self.dData[strColumn] = []

    def __getitem__(self, iIndex):
        return self.get_row(iIndex)
    
    def __iter__(self):
        for i in range(0,self.count()):
            yield self.get_row(i)

    def get_columns(self):
        return self.lColumns


    def add_row(self, p_lRow):
        if len(p_lRow) != len(self.lColumns): return False
        for i, entry in enumerate(p_lRow):
            self.dData[self.lColumns[i]].append(entry)
        return True   
    
    
    def remove_row(self, iIndex):
        for strColumn in self.lColumns:
            del self.dData[strColumn][iIndex]
    
    def get_row(self, iIndex, lColumns=None):
        row = []
        for strColumn in self.lColumns:
            if lColumns is not None and strColumn not in lColumns: continue
            row.append(self.dData[strColumn][iIndex])
        return row
    
    def count(self):
        return len(self.dData[self.lColumns[0]])
    
    def get_column_index(self, p_strColumnName):
        return self.lColumns.index(p_strColumnName)
    
    def pretty_print(self):
        print tabulate(self.dData, headers="keys", tablefmt="simple")
            
    
      
            