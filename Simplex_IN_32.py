import numpy as np
import math

def simplexStep(optCrit, constraintsL, constraintsR, base, table):
    
    w = table[0,1:-2]
    
    baseCandidates = [math.inf]*nVariables
    
    nonBase = np.setdiff1d(list(range(nVariables)), base)
    
    for index in nonBase:
        mul = w * constraintsL[0:,index:index+1] - optCrit[index]
        baseCandidates[index] = float(mul)
        
    newBase = min(baseCandidates)
        
    newBaseIndex = baseCandidates.index(newBase)
    
    table[0,-1] = newBase

    table[1:,nConstraints+2:] = table[1:,1:nConstraints+1] * constraintsL[0:,newBaseIndex:newBaseIndex+1]

    if newBase >= 0:
        print("PROGRAM END \n")
        print("Value:", table[0,nConstraints+1])
        for i in range(1, nConstraints+1):
            if table[i,0] < nVariables - nConstraints:
                print("Variable X", table[i,0].astype(int), " = ", table[i, nConstraints+1], sep='')
        print("Other vars are 0.")
        return
    
    pvtColCandidate = [0]*nConstraints

    for i in range(1,nConstraints+1):
        pvtColCandidate[i-1] = table[i, nConstraints+1]/table[i,nConstraints+2]
    
    minPvtIndex = pvtColCandidate.index(min(pvtColCandidate))+1
    pvtEl = table[minPvtIndex,nConstraints+2]
    
    table[minPvtIndex, 0] = newBaseIndex
    base = table[1:,0:1]
    
    tempTable = table.copy()
    for row in range(nConstraints+1):
        for col in range(1,nVariables):
            if row == minPvtIndex:
                table[row, col] /= pvtEl
            else:
                table[row, col] -= tempTable[minPvtIndex, col] * tempTable[row, nConstraints+2] / pvtEl
                
    simplexStep(optCrit, constraintsL, constraintsR, base, table)

optCrit = [1, 2, 3, 0, 0, 0]
constraintsL = np.matrix([[1, 2, 3, 1, 0, 0], [2, 3, 1, 0, 1, 0], [4, 5, 6, 0, 0, 1]])
constraintsR = np.array([[100], [200], [250]])
base = np.array([[3], [4], [5]])

nVariables = len(optCrit)
nConstraints = len(base)

table = np.zeros((nConstraints + 1, nConstraints + 3))

table[1:,1:nConstraints+1] = np.eye(nConstraints)
table[1:,nConstraints+1:nConstraints+2] = constraintsR
table[1:,0:1] = base

simplexStep(optCrit, constraintsL, constraintsR, base, table)