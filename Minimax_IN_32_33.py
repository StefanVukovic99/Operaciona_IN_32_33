import numpy as np
from copy import deepcopy

def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0

def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

def checkWin(board):
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)

T = [['', '', ''],
     ['', '', ''],
     ['', '', '']]

def printBoard(board):
    T = board;
    print(f'\n[{T[0][0]}] [{T[0][1]}] [{T[0][2]}] \n[{T[1][0]}] [{T[1][1]}] [{T[1][2]}] \n[{T[2][0]}] [{T[2][1]}] [{T[2][2]}]')

def getField(board, move):
    return board[(move-1)//3][(move-1)%3];

def setField(board, move, mark):
    if(move < 1 or move > 9):
        print('Out of range');
    elif(getField(board, move)):
        print('Occupied');
    else:
        board[(move-1)//3][(move-1)%3] = mark;
        return move;
    return 0;82

def movesLeft(board):
    return sum(row.count('') for row in board);
    
def minMax(parentBoard, mark):
    x = 0 if mark == 'X' else 1
    values = [[x, x, x],
             [x, x, x],
             [x, x, x]]
    for i in range(1, 10):
        if(not getField(parentBoard, i)): 
            childBoard =  deepcopy(parentBoard)
            setField(childBoard, i, mark);
            winner = checkWin(childBoard)
            if(winner == 'O'): val = 0;
            elif(winner == 'X'): val = 1;
            elif(not movesLeft(childBoard)): val = 0.5;
            else:
                val = minMax(childBoard, 'X' if mark == 'O' else 'O')['value'];
            values[(i-1)//3][(i-1)%3] = val;
            
    if(mark == 'X'): return {'value': max([max(row) for row in values]), 'move': np.array(values).argmax()+1};
    if(mark == 'O'): return {'value': min([min(row) for row in values]), 'move': np.array(values).argmin()+1};
                

def cpuMove():
    aiMove = minMax(T, 'O')
    print(aiMove)
    setField(T, aiMove['move'], 'O')
    
while(True):
    
    okMove = 0
    while(not okMove):
        printBoard(T);
        move = int(input("Select a field, 1 through 9 \n"));
        okMove = setField(T, move, 'X');
    
    if(checkWin(T) or not movesLeft(T)): break;
    
    cpuMove();
    
    if(checkWin(T) or not movesLeft(T)): break;

printBoard(T);

if(checkWin(T)):
    print(f'{checkWin(T)} wins.')
else:
    print("Draw.")