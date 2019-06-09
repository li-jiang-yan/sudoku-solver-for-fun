# -*- coding: utf-8 -*-
from math import sqrt
sudokuSize = 9
sudokuRoot = sqrt(sudokuSize) 
totalCells = sudokuSize ** 2

class Group():
    def __init__(self):
        self.cellList = []
        self.valueList = []
    
    def setCellList(self, newCellList):
        self.cellList = newCellList
        
    def addCells(self, newCell):
        self.setCellList(self.getCellList() + [newCell])
    
    def getCellList(self):
        return self.cellList
    
    def setValueList(self, newValueList):
        self.valueList = newValueList
    
    def getValueList(self):
        return self.valueList
    
    def genNewValueList(self):
        newValueList = []
        for cell in self.getCellList():
            if cell.getValuePresent():
                newValueList += [cell.getValue()]
        return newValueList
    
    def setNewValueList(self):
        self.setValueList(self.genNewValueList())

rowList = []
colList = []
boxList = []

for groupIndex in range(sudokuSize):
    rowList += [Group()]
    colList += [Group()]
    boxList += [Group()]

class Cell():
    def __init__(self, cellIndex):
        self.cellIndex = cellIndex
        self.valuePresent = False
    
    def getCellIndex(self):
        return self.cellIndex
    
    def getRowIndex(self):
        self.rowIndex = self.getCellIndex() // sudokuSize
        return self.rowIndex
    
    def getColIndex(self):
        self.colIndex = self.getCellIndex() % sudokuSize
        return self.colIndex
    
    def getBoxIndex(self):
        self.boxIndex = (self.getColIndex() // sudokuRoot) + sudokuRoot * (self.getRowIndex() // sudokuRoot)
        return self.boxIndex
    
    def getRow(self):
        return rowList[self.getRowIndex()]
    
    def getCol(self):
        return colList[self.getColIndex()]
    
    def getBox(self):
        return boxList[int(self.getBoxIndex())]
    
    def getValuePresent(self):
        return self.valuePresent
    
    def setValue(self, value):
        self.value = value
        self.valuePresent = True
    
    def getValue(self):
        return self.value
    
    def getPossibilities(self):
        self.rowNumList = (self.getRow()).getValueList()
        self.colNumList = (self.getCol()).getValueList()
        self.boxNumList = (self.getBox()).getValueList()
        self.valuePossibilities = []
        for numberIndex in range(sudokuSize):
            if not((numberIndex in self.rowNumList) or (numberIndex in self.colNumList) or (numberIndex in self.boxNumList)):
                self.valuePossibilities += [numberIndex]
        return self.valuePossibilities
    
    def checkCell(self):
        if len(self.getPossibilities()) == 1:
            self.setValue((self.getPossibilities())[0])

cellList = []

for cellIndex in range(totalCells):
    cellList += [Cell(cellIndex)]
    N = cellIndex
    rowList[N // sudokuSize].addCells(cellList[N])
    colList[N % sudokuSize].addCells(cellList[N])
    boxList[int((N % sudokuSize) // sudokuRoot + sudokuRoot * (N // (sudokuRoot * sudokuSize)))].addCells(cellList[N])

# cellList[cellIndex].setValue(value)
for eachTuple in [(1, 4, 2), (1, 5, 6), (1, 7, 7), (1, 9, 1), (2, 1, 6), 
                  (2, 2, 8), (2, 5, 7), (2, 8, 9), (3, 1, 1), (3, 2, 9), 
                  (3, 6, 4), (3, 7, 5), (4, 1, 8), (4, 2, 2), (4, 4, 1), 
                  (4, 8, 4), (5, 3, 4), (5, 4, 6), (5, 6, 2), (5, 7, 9), 
                  (6, 2, 5), (6, 6, 3), (6, 8, 2), (6, 9, 8), (7, 3, 9), 
                  (7, 4, 3), (7, 8, 7), (7, 9, 4), (8, 2, 4), (8, 5, 5), 
                  (8, 8, 3), (8, 9, 6), (9, 1, 7), (9, 3, 3), (9, 5, 1), 
                  (9, 6, 8)]:
    rowNum = eachTuple[0] - 1
    colNum = eachTuple[1] - 1
    valNum = eachTuple[2] - 1
    celNum = rowNum * sudokuSize + colNum
    cellList[celNum].setValue(valNum)

def solveComplete():
    for cell in cellList:
        if not cell.getValuePresent():
            return False
    return True

while not solveComplete():
    for cell in cellList:
        for row in rowList:
            row.setNewValueList()
        for col in colList:
            col.setNewValueList()
        for box in boxList:
            box.setNewValueList()
        if not cell.getValuePresent():
            cell.checkCell()

import numpy as np

sudokuSol = np.zeros([sudokuSize, sudokuSize])

for cell in cellList:
    sudokuSol[cell.getRowIndex()][cell.getColIndex()] = cell.getValue()

print(sudokuSol + 1)