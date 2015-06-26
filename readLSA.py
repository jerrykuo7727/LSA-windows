import os
import numpy as np


def Read_QtUS_matrix(filename):
    qry_list = []
    with open(filename) as file:
        line = file.readline()
        while line:
            line_list = line.split()
            qry_list.append(line_list)
            line = file.readline()
        #end while
    #end with

    return qry_list
#end Read_QtUS_matrix()


class getCol:
    matrix = []
    def __init__(self, file, delim=" "):
        with open(file, 'rU') as f:
            getCol.matrix =  [filter(None, l.split(delim)) for l in f]

    def __getitem__ (self, key):
        column = []
        for row in getCol.matrix:
            try:
                column.append(row[key])
            except IndexError:
                # pass
                column.append("")
        return column
#end class

class getRow:
    matrix = []
    def __init__(self, file, delim=" "):
        with open(file, 'rU') as f:
            getRow.matrix =  [filter(None, l.split(delim)) for l in f]

    def __getitem__ (self, key):
        row = []
        for row in getRow.matrix:
            try:
                row.append(row[key])
            except IndexError:
                # pass
                row.append("")
        return row
#end class









