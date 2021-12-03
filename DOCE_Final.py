#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random


# In[2]:


class Operator:
    def _init_(self, row, col):
        self.row = row
        self.col = col


operator = Operator()


class PreviousMove:
    def _init_(self, row, col, turn):
        self.row = row
        self.col = col
        self.turn = turn


prev_White = PreviousMove()
prev_Black = PreviousMove()


class State:
    def _init_(self, cell):
        self.cell = cell


class Move:
    def _init_(self, row, col, dice_face, blockRow, blockCol, value):
        self.row = row
        self.col = col
        self.dice_face = dice_face
        self.value = value

        self.blockRow = blockRow
        self.blockCol = blockCol


# In[3]:


cell = [[]]
cell = [["000" for i in range(5)] for i in range(5)]

current_State = State()
current_State.cell = cell


# In[4]:


BLANK = "000"
USER_WHITE = "W"
USER_BLACK = "B"
BLOCKER = "001"

BLOCKER2 = "002"

MAXEVAL = 1000


# In[5]:


def print_State(state):

    for i in range(32):
        print("-", end="")
    print()
    for i in range(5):
        for j in range(5):
            if state.cell[i][j] == BLANK:
                print("|     ", end="")
            elif state.cell[i][j] == BLOCKER:
                print("|-----", end="")
            elif state.cell[i][j] == BLOCKER2:
                print("|----2", end="")

            else:
                print("| "+state.cell[i][j]+" ", end="")

        print("|")
        for i in range(32):
            print("-", end="")
        print()


# In[6]:


def makeMove(state, operator, move):
    state.cell[operator.row][operator.col] = move


# In[7]:


def removeMarker(state, operator):
    cellValue = state.cell[operator.row][operator.col]
    state.cell[operator.row][operator.col] = cellValue[0]+cellValue[1]+" "


# In[8]:


def isvalidBlockerMove(state, operator):
    if state.cell[operator.row][operator.col] == BLANK:
        return 1
    else:
        return 0


# In[9]:


def isValidMove(state, operator, userType, previousMove):

    if operator.row > 4 or operator.row < 0 or operator.col > 5 or operator.col < 0:
        return 0

    if state.cell[operator.row][operator.col] != BLANK:
        return 0

    if previousMove.row == operator.row and previousMove.col == operator.col:
        return 0

    # add for blcoker too
    if state.cell[operator.row][operator.col] == BLOCKER:
        return 0

    if previousMove.row != -1:
        array = np.array(state.cell)

        prevRow = previousMove.row
        prevCol = previousMove.col

        decreaseRow = prevRow-1
        increaseRow = prevRow+1
        decreaseCol = prevCol-1
        increaseCol = prevCol+1

        neighbours = [[decreaseRow, decreaseCol], [decreaseRow, prevCol], [decreaseRow, increaseCol], [prevRow, decreaseCol], [prevRow, increaseCol],
                      [increaseRow, decreaseCol], [increaseRow, prevCol], [increaseRow, increaseCol]]

        if [operator.row, operator.col] not in neighbours:
            return 1
        else:
            return 0

    return 1


# In[10]:


# Function to find available space
def findBlank(state):
    blanks = []
    for i in range(len(state.cell)):
        for j in range(len(state.cell[i])):
            if state.cell[i][j] == BLANK:
                blanks.append([i, j])

    return blanks


# In[11]:


def findValidBlank(state, previousMove):
    blanks = findBlank(state)

    prevRow = previousMove.row
    prevCol = previousMove.col

    decreaseRow = prevRow-1
    increaseRow = prevRow+1
    decreaseCol = prevCol-1
    increaseCol = prevCol+1

    neighbours = [[decreaseRow, decreaseCol], [decreaseRow, prevCol], [decreaseRow, increaseCol], [prevRow, decreaseCol], [prevRow, increaseCol],
                  [increaseRow, decreaseCol], [increaseRow, prevCol], [increaseRow, increaseCol]]

    for neighbour in neighbours:
        if neighbour in blanks:
            blanks.remove(neighbour)

    return blanks


# In[12]:


def undo(state, operator):
    state.cell[operator.row][operator.col] = BLANK


# In[13]:


def undo_marker_removal(state, prev):
    element = state.cell[prev.row][prev.col]
    element = element[:2] + 'M'
    state.cell[prev.row][prev.col] = element


# In[14]:


def count_dice(state, user):
    user_face_up = []
    user_dict = dict()
    for i in range(5):
        for j in range(5):
            if state.cell[i][j][1] == user:
                user_face_up.append(state.cell[i][j][0])
    for face_up in user_face_up:
        if face_up in user_dict.keys():
            user_dict[face_up] += 1
        else:
            user_dict[face_up] = 1

#     for x in user_dict:
#         print(x, ": ", user_dict[x])
    return user_dict


# In[15]:


def isTerminal(s):
    for line in range(0, 5):
        # Check for row completion
        if ((s.cell[line][0] != BLANK and s.cell[line][0] != BLOCKER) and (s.cell[line][1] != BLANK and s.cell[line][1] != BLOCKER) and (s.cell[line][2] != BLANK and s.cell[line][2] != BLOCKER) and (s.cell[line][3] != BLANK and s.cell[line][3] != BLOCKER)) and ((s.cell[line][0][1] == s.cell[line][1][1] and s.cell[line][1][1] == s.cell[line][2][1]) or (s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1])):
            if int(s.cell[line][0][0]) + int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(s.cell[line][3][0]) == 12:
                return [s.cell[line][0], s.cell[line][1], s.cell[line][2], s.cell[line][3]]

        if ((s.cell[line][1] != BLANK and s.cell[line][1] != BLOCKER) and (s.cell[line][2] != BLANK and s.cell[line][2] != BLOCKER) and (s.cell[line][3] != BLANK and s.cell[line][3] != BLOCKER) and (s.cell[line][4] != BLANK and s.cell[line][4] != BLOCKER)) and ((s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1]) or (s.cell[line][2][1] == s.cell[line][3][1] and s.cell[line][3][1] == s.cell[line][4][1])):
            if int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(s.cell[line][3][0]) + int(s.cell[line][4][0]) == 12:
                return [s.cell[line][1], s.cell[line][2], s.cell[line][3], s.cell[line][4]]

        # Check for column completion
        if ((s.cell[0][line] != BLANK and s.cell[0][line] != BLOCKER) and (s.cell[1][line] != BLANK and s.cell[1][line] != BLOCKER) and (s.cell[2][line] != BLANK and s.cell[2][line] != BLOCKER) and (s.cell[3][line] != BLANK and s.cell[3][line] != BLOCKER)) and ((s.cell[0][line][1] == s.cell[1][line][1] and s.cell[1][line][1] == s.cell[2][line][1]) or (s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1])):
            if int(s.cell[0][line][0]) + int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(s.cell[3][line][0]) == 12:
                return [s.cell[0][line], s.cell[1][line], s.cell[2][line], s.cell[3][line]]

        if ((s.cell[1][line] != BLANK and s.cell[1][line] != BLOCKER) and (s.cell[2][line] != BLANK and s.cell[2][line] != BLOCKER) and (s.cell[3][line] != BLANK and s.cell[3][line] != BLOCKER) and (s.cell[4][line] != BLANK and s.cell[4][line] != BLOCKER)) and ((s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1]) or (s.cell[2][line][1] == s.cell[3][line][1] and s.cell[3][line][1] == s.cell[4][line][1])):
            if int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(s.cell[3][line][0]) + int(s.cell[4][line][0]) == 12:
                return [s.cell[1][line], s.cell[2][line], s.cell[3][line], s.cell[4][line]]

    # Check for diagonals - Total 8 diagonal ways
    # Main Diagonal - first 4
    if ((s.cell[0][0] != BLANK and s.cell[0][0] != BLOCKER) and (s.cell[1][1] != BLANK and s.cell[1][1] != BLOCKER) and (s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (s.cell[3][3] != BLANK and s.cell[3][3] != BLOCKER)) and ((s.cell[0][0][1] == s.cell[1][1][1] and s.cell[1][1][1] == s.cell[2][2][1]) or (s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1])):
        if int(s.cell[0][0][0]) + int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) == 12:
            return [s.cell[0][0], s.cell[1][1], s.cell[2][2], s.cell[3][3]]

    # Main Diagonal - last 4
    if ((s.cell[1][1] != BLANK and s.cell[1][1] != BLOCKER) and (s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (s.cell[3][3] != BLANK and s.cell[3][3] != BLOCKER) and (s.cell[4][4] != BLANK and s.cell[4][4] != BLOCKER)) and ((s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1]) or (s.cell[2][2][1] == s.cell[3][3][1] and s.cell[3][3][1] == s.cell[4][4][1])):
        if int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) + int(s.cell[4][4][0]) == 12:
            return [s.cell[1][1], s.cell[2][2], s.cell[3][3], s.cell[4][4]]

    # Off Diagonal - first 4
    if ((s.cell[0][4] != BLANK and s.cell[0][4] != BLOCKER) and (
            s.cell[1][3] != BLANK and s.cell[1][3] != BLOCKER) and (
                s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (
                s.cell[3][1] != BLANK and s.cell[3][1] != BLOCKER)) and ((s.cell[0][4][1] == s.cell[1][3][1] and
                                                                          s.cell[1][3][1] == s.cell[2][2][1]) or (s.cell[1][3][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][1][1])):
        if int(s.cell[0][4][0]) + int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) == 12:
            return [s.cell[0][4], s.cell[1][3], s.cell[2][2], s.cell[3][1]]

    # Off Diagonal - last 4
    if ((s.cell[1][3] != BLANK and s.cell[1][3] != BLOCKER) and (
            s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (
                s.cell[3][1] != BLANK and s.cell[3][1] != BLOCKER) and (
                s.cell[4][0] != BLANK and s.cell[4][0] != BLOCKER)) and ((s.cell[1][3][1] == s.cell[2][2][1] and
                                                                          s.cell[2][2][1] == s.cell[3][1][1]) or (s.cell[2][2][1] == s.cell[3][1][1] and s.cell[3][1][1] == s.cell[4][0][1])):
        if int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) + int(s.cell[4][0][0]) == 12:
            return [s.cell[1][3], s.cell[2][2], s.cell[3][1], s.cell[4][0]]

    # Main Diagonal's upper candrespondent
    if ((s.cell[0][1] != BLANK and s.cell[0][1] != BLOCKER) and (
            s.cell[1][2] != BLANK and s.cell[1][2] != BLOCKER) and (
                s.cell[2][3] != BLANK and s.cell[2][3] != BLOCKER) and (
                s.cell[3][4] != BLANK and s.cell[3][4] != BLOCKER)) and ((s.cell[0][1][1] == s.cell[1][2][1] and
                                                                          s.cell[1][2][1] == s.cell[2][3][1]) or (s.cell[1][2][1] == s.cell[2][3][1] and s.cell[2][3][1] == s.cell[3][4][1])):
        if int(s.cell[0][1][0]) + int(s.cell[1][2][0]) + int(s.cell[2][3][0]) + int(s.cell[3][4][0]) == 12:
            return [s.cell[0][1], s.cell[1][2], s.cell[2][3], s.cell[3][4]]

    # Main Diagonal's lower candrespondent
    if ((s.cell[1][0] != BLANK and s.cell[1][0] != BLOCKER) and (
            s.cell[2][1] != BLANK and s.cell[2][1] != BLOCKER) and (
                s.cell[3][2] != BLANK and s.cell[3][2] != BLOCKER) and (
                s.cell[4][3] != BLANK and s.cell[4][3] != BLOCKER)) and ((s.cell[1][0][1] == s.cell[2][1][1] and
                                                                          s.cell[2][1][1] == s.cell[3][2][1]) or (s.cell[2][1][1] == s.cell[3][2][1] and s.cell[3][2][1] == s.cell[4][3][1])):
        if int(s.cell[1][0][0]) + int(s.cell[2][1][0]) + int(s.cell[3][2][0]) + int(s.cell[4][3][0]) == 12:
            return [s.cell[1][0], s.cell[2][1], s.cell[3][2], s.cell[4][3]]

    # Off Diagonal's upper candrespondent
    if ((s.cell[0][3] != BLANK and s.cell[0][3] != BLOCKER) and (
            s.cell[1][2] != BLANK and s.cell[1][2] != BLOCKER) and (
                s.cell[2][1] != BLANK and s.cell[2][1] != BLOCKER) and (
                s.cell[3][0] != BLANK and s.cell[3][0] != BLOCKER)) and ((s.cell[0][3][1] == s.cell[1][2][1] and
                                                                          s.cell[1][2][1] == s.cell[2][1][1]) or (s.cell[1][2][1] == s.cell[2][1][1] and s.cell[2][1][1] == s.cell[3][0][1])):
        if int(s.cell[0][3][0]) + int(s.cell[1][2][0]) + int(s.cell[2][1][0]) + int(s.cell[3][0][0]) == 12:
            return [s.cell[0][3], s.cell[1][2], s.cell[2][1], s.cell[3][0]]

    # Off Diagonal's lower candrespondent
    if ((s.cell[1][4] != BLANK and s.cell[1][4] != BLOCKER) and (
            s.cell[2][3] != BLANK and s.cell[2][3] != BLOCKER) and (
                s.cell[3][2] != BLANK and s.cell[3][2] != BLOCKER) and (
                s.cell[4][1] != BLANK and s.cell[4][1] != BLOCKER)) and ((s.cell[1][4][1] == s.cell[2][3][1] and
                                                                          s.cell[2][3][1] == s.cell[3][2][1]) or (s.cell[2][3][1] == s.cell[3][2][1] and s.cell[3][2][1] == s.cell[4][1][1])):
        if int(s.cell[1][4][0]) + int(s.cell[2][3][0]) + int(s.cell[3][2][0]) + int(s.cell[4][1][0]) == 12:
            return [s.cell[1][4], s.cell[2][3], s.cell[3][2], s.cell[4][1]]

    # Check for any blanks- return 0 so it won't be terminal
    for i in range(0, 5):
        for j in range(0, 5):
            if s.cell[i][j] == BLANK:
                return [0]

    # For TIE
    return ['7']


# In[40]:


def eval(s):
    USER = "W"
    PROGRAM = "B"
    for line in range(0, 5):
        # Evaluation for row completion
        if ((s.cell[line][0] != BLANK and s.cell[line][0] != BLOCKER) and (s.cell[line][1] != BLANK and s.cell[line][1] != BLOCKER) and (s.cell[line][2] != BLANK and s.cell[line][2] != BLOCKER) and (s.cell[line][3] != BLANK and s.cell[line][3] != BLOCKER)) and ((s.cell[line][0][1] == s.cell[line][1][1] and s.cell[line][1][1] == s.cell[line][2][1]) or (s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1])):
            if (s.cell[line][0][1] == PROGRAM and s.cell[line][1][1] == PROGRAM and s.cell[line][2][1] == PROGRAM) or (
                    s.cell[line][1][1] == PROGRAM and s.cell[line][2][1] == PROGRAM and s.cell[line][3][1] == PROGRAM):
                if int(s.cell[line][0][0]) + int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(
                        s.cell[line][3][0]) == 12:
                    return 10
            elif (s.cell[line][0][1] == USER and s.cell[line][1][1] == USER and s.cell[line][2][
                1] == USER) or (
                    s.cell[line][1][1] == USER and s.cell[line][2][1] == USER and s.cell[line][3][1] == USER):
                if int(s.cell[line][0][0]) + int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(
                        s.cell[line][3][0]) == 12:
                    return -10

        if ((s.cell[line][1] != BLANK and s.cell[line][1] != BLOCKER) and (s.cell[line][2] != BLANK and s.cell[line][2] != BLOCKER) and (s.cell[line][3] != BLANK and s.cell[line][3] != BLOCKER) and (s.cell[line][4] != BLANK and s.cell[line][4] != BLOCKER)) and ((s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1]) or (s.cell[line][2][1] == s.cell[line][3][1] and s.cell[line][3][1] == s.cell[line][4][1])):
            if (s.cell[line][1][1] == PROGRAM and s.cell[line][2][1] == PROGRAM and s.cell[line][3][1] == PROGRAM) or (
                    s.cell[line][2][1] == PROGRAM and s.cell[line][3][1] == PROGRAM and s.cell[line][4][1] == PROGRAM):
                if int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(s.cell[line][3][0]) + int(
                        s.cell[line][4][0]) == 12:
                    return 10
            elif (s.cell[line][1][1] == USER and s.cell[line][2][1] == USER and s.cell[line][3][
                1] == USER) or (
                    s.cell[line][2][1] == USER and s.cell[line][3][1] == USER and s.cell[line][4][1] == USER):
                if int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(s.cell[line][3][0]) + int(
                        s.cell[line][4][0]) == 12:
                    return -10

        # Evaluation for column completion
        if ((s.cell[0][line] != BLANK and s.cell[0][line] != BLOCKER) and (s.cell[1][line] != BLANK and s.cell[1][line] != BLOCKER) and (s.cell[2][line] != BLANK and s.cell[2][line] != BLOCKER) and (s.cell[3][line] != BLANK and s.cell[3][line] != BLOCKER)) and ((s.cell[0][line][1] == s.cell[1][line][1] and s.cell[1][line][1] == s.cell[2][line][1]) or (s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1])):

            if (s.cell[0][line][1] == PROGRAM and s.cell[1][line][1] == PROGRAM and s.cell[2][line][1] == PROGRAM) or (
                    s.cell[1][line][1] == PROGRAM and s.cell[2][line][1] == PROGRAM and s.cell[3][line][1] == PROGRAM):
                if int(s.cell[0][line][0]) + int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(
                        s.cell[3][line][0]) == 12:
                    return 10
            elif (s.cell[0][line][1] == USER and s.cell[1][line][1] == USER and s.cell[2][line][1] == USER) or (s.cell[1][line][1] == USER and s.cell[2][line][1] == USER and s.cell[3][line][1] == USER):
                #                 print("Khai ta")
                if int(s.cell[0][line][0]) + int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(
                        s.cell[3][line][0]) == 12:

                    return -10

        if ((s.cell[1][line] != BLANK and s.cell[1][line] != BLOCKER) and (s.cell[2][line] != BLANK and s.cell[2][line] != BLOCKER) and (s.cell[3][line] != BLANK and s.cell[3][line] != BLOCKER) and (s.cell[4][line] != BLANK and s.cell[4][line] != BLOCKER)) and ((s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1]) or (s.cell[2][line][1] == s.cell[3][line][1] and s.cell[3][line][1] == s.cell[4][line][1])):
            if (s.cell[1][line][1] == PROGRAM and s.cell[2][line][1] == PROGRAM and s.cell[3][line][1] == PROGRAM) or (
                    s.cell[2][line][1] == PROGRAM and s.cell[3][line][1] == PROGRAM and s.cell[4][line][1] == PROGRAM):
                if int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(s.cell[3][line][0]) + int(
                        s.cell[4][line][0]) == 12:
                    return 10
            elif (s.cell[1][line][1] == USER and s.cell[2][line][1] == USER and s.cell[3][line][
                1] == USER) or (
                    s.cell[2][line][1] == USER and s.cell[3][line][1] == USER and s.cell[4][line][1] == USER):
                if int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(s.cell[3][line][0]) + int(
                        s.cell[4][line][0]) == 12:
                    return -10

    # Evaluation for diagonals - Total 8 diagonal ways
    # Main Diagonal - first 4
    if ((s.cell[0][0] != BLANK and s.cell[0][0] != BLOCKER) and (s.cell[1][1] != BLANK and s.cell[1][1] != BLOCKER) and (s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (s.cell[3][3] != BLANK and s.cell[3][3] != BLOCKER)) and ((s.cell[0][0][1] == s.cell[1][1][1] and s.cell[1][1][1] == s.cell[2][2][1]) or (s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1])):

        if (s.cell[0][0][1] == PROGRAM and s.cell[1][1][1] == PROGRAM and s.cell[2][2][1] == PROGRAM) or (
                s.cell[1][1][1] == PROGRAM and s.cell[2][2][1] == PROGRAM and s.cell[3][3][1] == PROGRAM):
            if int(s.cell[0][0][0]) + int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) == 12:
                return 10
        elif (s.cell[0][0][1] == USER and s.cell[1][1][1] == USER and s.cell[2][2][1] == USER) or (
                s.cell[1][1][1] == USER and s.cell[2][2][1] == USER and s.cell[3][3][1] == USER):

            if int(s.cell[0][0][0]) + int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) == 12:
                #                 print("Gayo Hajur")
                return -10

    # Main Diagonal - last 4
    if ((s.cell[1][1] != BLANK and s.cell[1][1] != BLOCKER) and (s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (s.cell[3][3] != BLANK and s.cell[3][3] != BLOCKER) and (s.cell[4][4] != BLANK and s.cell[4][4] != BLOCKER)) and ((s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1]) or (s.cell[2][2][1] == s.cell[3][3][1] and s.cell[3][3][1] == s.cell[4][4][1])):
        if (s.cell[1][1][1] == PROGRAM and s.cell[2][2][1] == PROGRAM and s.cell[3][3][1] == PROGRAM) or (
                s.cell[2][2][1] == PROGRAM and s.cell[3][3][1] == PROGRAM and s.cell[4][4][1] == PROGRAM):
            if int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) + int(s.cell[4][4][0]) == 12:
                return 10
        elif (s.cell[1][1][1] == USER and s.cell[2][2][1] == USER and s.cell[3][3][1] == USER) or (
                s.cell[2][2][1] == USER and s.cell[3][3][1] == USER and s.cell[4][4][1] == USER):
            if int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) + int(s.cell[4][4][0]) == 12:
                return -10

    # Off Diagonal - first 4
    if ((s.cell[0][4] != BLANK and s.cell[0][4] != BLOCKER) and (
            s.cell[1][3] != BLANK and s.cell[1][3] != BLOCKER) and (
                s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (
                s.cell[3][1] != BLANK and s.cell[3][1] != BLOCKER)) and ((s.cell[0][4][1] == s.cell[1][3][1] and
                                                                          s.cell[1][3][1] == s.cell[2][2][1]) or (
                    s.cell[0][4] != BLANK and s.cell[1][3][
                        1] == s.cell[2][2][1] and s.cell[2][2][
                        1] == s.cell[3][1][1])):
        if (s.cell[0][4][1] == PROGRAM and s.cell[1][3][1] == PROGRAM and s.cell[2][2][1] == PROGRAM) or (
                s.cell[1][3][1] == PROGRAM and s.cell[2][2][1] == PROGRAM and s.cell[3][1][1] == PROGRAM):
            if int(s.cell[0][4][0]) + int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) == 12:
                return 10
        elif (s.cell[0][4][1] == USER and s.cell[1][3][1] == USER and s.cell[2][2][1] == USER) or (
                s.cell[1][3][1] == USER and s.cell[2][2][1] == USER and s.cell[3][1][1] == USER):
            if int(s.cell[0][4][0]) + int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) == 12:
                return -10

    # Off Diagonal - last 4
    if ((s.cell[1][3] != BLANK and s.cell[1][3] != BLOCKER) and (
            s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER) and (
                s.cell[3][1] != BLANK and s.cell[3][1] != BLOCKER) and (
                s.cell[4][0] != BLANK and s.cell[4][0] != BLOCKER)) and ((s.cell[1][3][1] == s.cell[2][2][1] and
                                                                          s.cell[2][2][1] == s.cell[3][1][1]) or (
                    s.cell[2][2][1] == s.cell[3][1][1] and
                    s.cell[3][1][1] == s.cell[4][0][1])):
        if (s.cell[1][3][1] == PROGRAM and s.cell[2][2][1] == PROGRAM and s.cell[3][1][1] == PROGRAM) or (
                s.cell[2][2][1] == PROGRAM and s.cell[3][1][1] == PROGRAM and s.cell[4][0][1] == PROGRAM):
            if int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) + int(s.cell[4][0][0]) == 12:
                return 10
        elif (s.cell[1][3][1] == USER and s.cell[2][2][1] == USER and s.cell[3][1][1] == USER) or (
                s.cell[2][2][1] == USER and s.cell[3][1][1] == USER and s.cell[4][0][1] == USER):
            if int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) + int(s.cell[4][0][0]) == 12:
                return -10

    # Main Diagonal's upper candrespondent
    if ((s.cell[0][1] != BLANK and s.cell[0][1] != BLOCKER) and (
            s.cell[1][2] != BLANK and s.cell[1][2] != BLOCKER) and (
                s.cell[2][3] != BLANK and s.cell[2][3] != BLOCKER) and (
                s.cell[3][4] != BLANK and s.cell[3][4] != BLOCKER)) and ((s.cell[0][1][1] == s.cell[1][2][1] and
                                                                          s.cell[1][2][1] == s.cell[2][3][1]) or (
                    s.cell[1][2][1] == s.cell[2][3][1] and
                    s.cell[2][3][1] == s.cell[3][4][1])):
        if (s.cell[0][1][1] == PROGRAM and s.cell[1][2][1] == PROGRAM and s.cell[2][3][1] == PROGRAM) or (
                s.cell[1][2][1] == PROGRAM and s.cell[2][3][1] == PROGRAM and s.cell[3][4][1] == PROGRAM):
            if int(s.cell[0][1][0]) + int(s.cell[1][2][0]) + int(s.cell[2][3][0]) + int(s.cell[3][4][0]) == 12:
                return 10
        elif (s.cell[0][1][1] == USER and s.cell[1][2][1] == USER and s.cell[2][3][1] == USER) or (
                s.cell[1][2][1] == USER and s.cell[2][3][1] == USER and s.cell[3][4][1] == USER):
            if int(s.cell[0][1][0]) + int(s.cell[1][2][0]) + int(s.cell[2][3][0]) + int(s.cell[3][4][0]) == 12:
                return -10

    # Main Diagonal's lower candrespondent
    if ((s.cell[1][0] != BLANK and s.cell[1][0] != BLOCKER) and (
            s.cell[2][1] != BLANK and s.cell[2][1] != BLOCKER) and (
                s.cell[3][2] != BLANK and s.cell[3][2] != BLOCKER) and (
                s.cell[4][3] != BLANK and s.cell[4][3] != BLOCKER)) and ((s.cell[1][0][1] == s.cell[2][1][1] and
                                                                          s.cell[2][1][1] == s.cell[3][2][1]) or (
                    s.cell[2][1][1] == s.cell[3][2][1] and
                    s.cell[3][2][1] == s.cell[4][3][1])):
        if (s.cell[1][0][1] == PROGRAM and s.cell[2][1][1] == PROGRAM and s.cell[3][2][1] == PROGRAM) or (
                s.cell[2][1][1] == PROGRAM and s.cell[3][2][1] == PROGRAM and s.cell[4][3][1] == PROGRAM):
            if int(s.cell[1][0][0]) + int(s.cell[2][1][0]) + int(s.cell[3][2][0]) + int(s.cell[4][3][0]) == 12:
                return 10
        elif (s.cell[1][0][1] == USER and s.cell[2][1][1] == USER and s.cell[3][2][1] == USER) or (
                s.cell[2][1][1] == USER and s.cell[3][2][1] == USER and s.cell[4][3][1] == USER):
            if int(s.cell[1][0][0]) + int(s.cell[2][1][0]) + int(s.cell[3][2][0]) + int(s.cell[4][3][0]) == 12:
                return -10

    # Off Diagonal's upper candrespondent
    if ((s.cell[0][3] != BLANK and s.cell[0][3] != BLOCKER) and (
            s.cell[1][2] != BLANK and s.cell[1][2] != BLOCKER) and (
                s.cell[2][1] != BLANK and s.cell[2][1] != BLOCKER) and (
                s.cell[3][0] != BLANK and s.cell[3][0] != BLOCKER)) and ((s.cell[0][3][1] == s.cell[1][2][1] and
                                                                          s.cell[1][2][1] == s.cell[2][1][1]) or (
                    s.cell[1][2][1] == s.cell[2][1][1] and
                    s.cell[2][1][1] == s.cell[3][0][1])):
        if (s.cell[0][3][1] == PROGRAM and s.cell[1][2][1] == PROGRAM and s.cell[2][1][1] == PROGRAM) or (
                s.cell[1][2][1] == PROGRAM and s.cell[2][1][1] == PROGRAM and s.cell[3][0][1] == PROGRAM):
            if int(s.cell[0][3][0]) + int(s.cell[1][2][0]) + int(s.cell[2][1][0]) + int(s.cell[3][0][0]) == 12:
                return 10
        elif (s.cell[0][3][1] == USER and s.cell[1][2][1] == USER and s.cell[2][1][1] == USER) or (
                s.cell[1][2][1] == USER and s.cell[2][1][1] == USER and s.cell[3][0][1] == USER):
            if int(s.cell[0][3][0]) + int(s.cell[1][2][0]) + int(s.cell[2][1][0]) + int(s.cell[3][0][0]) == 12:
                return -10

    # Off Diagonal's lower candrespondent
    if ((s.cell[1][4] != BLANK and s.cell[1][4] != BLOCKER) and (
            s.cell[2][3] != BLANK and s.cell[2][3] != BLOCKER) and (
                s.cell[3][2] != BLANK and s.cell[3][2] != BLOCKER) and (
                s.cell[4][1] != BLANK and s.cell[4][1] != BLOCKER)) and ((s.cell[1][4][1] == s.cell[2][3][1] and
                                                                          s.cell[2][3][1] == s.cell[3][2][1]) or (
                    s.cell[2][3][1] == s.cell[3][2][1] and
                    s.cell[3][2][1] == s.cell[4][1][1])):
        if (s.cell[1][4][1] == PROGRAM and s.cell[2][3][1] == PROGRAM and s.cell[3][2][1] == PROGRAM) or (
                s.cell[2][3][1] == PROGRAM and s.cell[3][2][1] == PROGRAM and s.cell[4][1][1] == PROGRAM):
            if int(s.cell[1][4][0]) + int(s.cell[2][3][0]) + int(s.cell[3][2][0]) + int(s.cell[4][1][0]) == 12:
                return 10
        elif (s.cell[1][4][1] == USER and s.cell[2][3][1] == USER and s.cell[3][2][1] == USER) or (
                s.cell[2][3][1] == USER and s.cell[3][2][1] == USER and s.cell[4][1][1] == USER):
            if int(s.cell[1][4][0]) + int(s.cell[2][3][0]) + int(s.cell[3][2][0]) + int(s.cell[4][1][0]) == 12:
                return -10

        # Trail to WIN
    for line in range(5):
        if (s.cell[line][0][1] == s.cell[line][1][1] and s.cell[line][1][1] == s.cell[line][2][1]):
            if s.cell[line][1][1] == PROGRAM and s.cell[line][2][1] == PROGRAM:
                if int(s.cell[line][0][0]) + int(s.cell[line][1][0]) + int(s.cell[line][2][0]) < 12:
                    return 5
                else:
                    return -5
#             elif s.cell[line][0][1] == USER:
#                 print("Ayo2")
#                 return -5

        if (s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1]):
            if s.cell[line][1][1] == PROGRAM and s.cell[line][2][1] == PROGRAM:
                if int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(s.cell[line][3][0]) < 12:
                    return 5
                else:
                    return -5
#             elif s.cell[line][1][1] == USER:
#                 print("Ayo")
#                 return -5

        if (s.cell[line][2][1] == s.cell[line][3][1] and s.cell[line][3][1] == s.cell[line][4][1]):
            if s.cell[line][2][1] == PROGRAM and s.cell[line][3][1] == PROGRAM:
                if int(s.cell[line][2][0]) + int(s.cell[line][3][0]) + int(s.cell[line][4][0]) < 12:

                    return 5
                else:
                    return -5
#             elif s.cell[line][2][1] == USER:
#                 return -5

        if (s.cell[0][line][1] == s.cell[1][line][1] and s.cell[1][line][1] == s.cell[2][line][1]):
            if s.cell[1][line][1] == PROGRAM and s.cell[2][line][1] == PROGRAM:
                if int(s.cell[0][line][0]) + int(s.cell[1][line][0]) + int(s.cell[2][line][0]) < 12:
                    #                     print("Ayo")
                    return 5
                else:
                    return -5
                #             elif s.cell[0][line][1] == USER:
#                 return -5

        if (s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1]):
            if s.cell[1][line][1] == PROGRAM and s.cell[2][line][1] == PROGRAM:
                if int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(s.cell[3][line][0]) < 12:
                    return 5
                else:
                    return -5
#             elif s.cell[1][line][1] == USER:
#                 return -5

        if (s.cell[2][line][1] == s.cell[3][line][1] and s.cell[3][line][1] == s.cell[4][line][1]):
            if s.cell[2][line][1] == PROGRAM and s.cell[3][line][1] == PROGRAM:
                if int(s.cell[2][line][0]) + int(s.cell[3][line][0]) + int(s.cell[4][line][0]) < 12:
                    return 5
                else:
                    return -5
#             elif s.cell[2][line][1] == USER:
#                 return -5

    # Diagonal Trails to WIN
    # Main Diagonal
    if s.cell[0][0][1] == s.cell[1][1][1] and s.cell[1][1][1] == s.cell[2][2][1]:
        if s.cell[1][1][1] == PROGRAM and s.cell[2][2][1] == PROGRAM:
            if int(s.cell[0][0][0]) + int(s.cell[1][1][0]) + int(s.cell[2][2][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][1][1] == USER and s.cell[2][2][1] == USER:
            if int(s.cell[0][0][0]) + int(s.cell[1][1][0]) + int(s.cell[2][2][0]) < 12:
                return -5

    if s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1]:
        if s.cell[1][1][1] == PROGRAM and s.cell[2][2][1] == PROGRAM:
            if int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][1][1] == USER and s.cell[2][2][1] == USER:
            if int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) < 12:
                return -5

    if s.cell[2][2][1] == s.cell[3][3][1] and s.cell[3][3][1] == s.cell[4][4][1]:
        if s.cell[2][2][1] == PROGRAM and s.cell[3][3][1] == PROGRAM:
            if int(s.cell[2][2][0]) + int(s.cell[3][3][0]) + int(s.cell[4][4][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[2][2][1] == USER and s.cell[3][3][1] == USER:
            if int(s.cell[2][2][0]) + int(s.cell[3][3][0]) + int(s.cell[4][4][0]) < 12:
                return -5

    # Off Diagonal
    if s.cell[0][4][1] == s.cell[1][3][1] and s.cell[1][3][1] == s.cell[2][2][1]:
        if s.cell[1][3][1] == PROGRAM and s.cell[2][2][1] == PROGRAM:
            if int(s.cell[0][4][0]) + int(s.cell[1][3][0]) + int(s.cell[2][2][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][3][1] == USER and s.cell[2][2][1] == USER:
            if int(s.cell[0][4][0]) + int(s.cell[1][3][0]) + int(s.cell[2][2][0]) < 12:
                return -5

    if s.cell[1][3][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][1][1]:
        if s.cell[1][3][1] == PROGRAM and s.cell[2][2][1] == PROGRAM:
            if int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][3][1] == USER and s.cell[2][2][1] == USER:
            if int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) < 12:
                return -5

    if s.cell[2][2][1] == s.cell[3][1][1] and s.cell[3][1][1] == s.cell[4][0][1]:
        if s.cell[2][2][1] == PROGRAM and s.cell[3][1][1] == PROGRAM:
            if int(s.cell[2][2][0]) + int(s.cell[3][1][0]) + int(s.cell[4][0][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[2][2][1] == USER and s.cell[3][1][1] == USER:
            if int(s.cell[2][2][0]) + int(s.cell[3][1][0]) + int(s.cell[4][0][0]) < 12:
                return -5

    # Main Diagonal - Upper correspondents
    if s.cell[0][1][1] == s.cell[1][2][1] and s.cell[1][2][1] == s.cell[2][3][1]:
        if s.cell[1][2][1] == PROGRAM and s.cell[2][3][1] == PROGRAM:
            if int(s.cell[0][1][0]) + int(s.cell[1][2][0]) + int(s.cell[2][3][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][2][1] == USER and s.cell[2][3][1] == USER:
            if int(s.cell[0][1][0]) + int(s.cell[1][2][0]) + int(s.cell[2][3][0]) < 12:
                return -5

    if s.cell[1][2][1] == s.cell[2][3][1] and s.cell[2][3][1] == s.cell[3][4][1]:
        if s.cell[1][2][1] == PROGRAM and s.cell[2][3][1] == PROGRAM:
            if int(s.cell[1][2][0]) + int(s.cell[2][3][0]) + int(s.cell[3][4][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][2][1] == USER and s.cell[2][3][1] == USER:
            if int(s.cell[1][2][0]) + int(s.cell[2][3][0]) + int(s.cell[3][4][0]) < 12:
                return -5

    # Main Diagonal - Lower correspondents
    if s.cell[1][0][1] == s.cell[2][1][1] and s.cell[2][1][1] == s.cell[3][2][1]:
        if s.cell[2][1][1] == PROGRAM and s.cell[3][2][1] == PROGRAM:
            if int(s.cell[1][0][0]) + int(s.cell[2][1][0]) + int(s.cell[3][2][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[2][1][1] == USER and s.cell[3][2][1] == USER:
            if int(s.cell[1][0][0]) + int(s.cell[2][1][0]) + int(s.cell[3][2][0]) < 12:
                return -5

    if s.cell[2][1][1] == s.cell[3][2][1] and s.cell[3][2][1] == s.cell[4][3][1]:
        if s.cell[2][1][1] == PROGRAM and s.cell[3][2][1] == PROGRAM:
            if int(s.cell[2][1][0]) + int(s.cell[3][2][0]) + int(s.cell[4][3][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[2][1][1] == USER and s.cell[3][2][1] == USER:
            if int(s.cell[2][1][0]) + int(s.cell[3][2][0]) + int(s.cell[4][3][0]) < 12:
                return -5

    # Off Diagonal - Upper correspondent
    if s.cell[0][3][1] == s.cell[1][2][1] and s.cell[1][2][1] == s.cell[2][1][1]:
        if s.cell[1][2][1] == PROGRAM and s.cell[2][1][1] == PROGRAM:
            if int(s.cell[0][3][0]) + int(s.cell[1][2][0]) + int(s.cell[2][1][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][2][1] == USER and s.cell[2][1][1] == USER:
            if int(s.cell[0][3][0]) + int(s.cell[1][2][0]) + int(s.cell[2][1][0]) < 12:
                return -5

    if s.cell[1][2][1] == s.cell[2][1][1] and s.cell[2][1][1] == s.cell[3][0][1]:
        if s.cell[1][2][1] == PROGRAM and s.cell[2][1][1] == PROGRAM:
            if int(s.cell[1][2][0]) + int(s.cell[2][1][0]) + int(s.cell[3][0][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[1][2][1] == USER and s.cell[2][1][1] == USER:
            if int(s.cell[1][2][0]) + int(s.cell[2][1][0]) + int(s.cell[3][0][0]) < 12:
                return -5

    # Off Diagonal - Lower correspondent
    if s.cell[1][4][1] == s.cell[2][3][1] and s.cell[2][3][1] == s.cell[3][2][1]:
        if s.cell[2][3][1] == PROGRAM and s.cell[3][2][1] == PROGRAM:
            if int(s.cell[1][4][0]) + int(s.cell[2][3][0]) + int(s.cell[3][2][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[2][3][1] == USER and s.cell[3][2][1] == USER:
            if int(s.cell[1][4][0]) + int(s.cell[2][3][0]) + int(s.cell[3][2][0]) < 12:
                return -5

    if s.cell[2][3][1] == s.cell[3][2][1] and s.cell[3][2][1] == s.cell[4][1][1]:
        if s.cell[2][3][1] == PROGRAM and s.cell[3][2][1] == PROGRAM:
            if int(s.cell[2][3][0]) + int(s.cell[3][2][0]) + int(s.cell[4][1][0]) < 12:
                return 5
            else:
                return -5
        elif s.cell[2][3][1] == USER and s.cell[3][2][1] == USER:
            if int(s.cell[2][3][0]) + int(s.cell[3][2][0]) + int(s.cell[4][1][0]) < 12:
                return -5

    return 0


# In[23]:


# Minmax-  Trying tracking previous moves

def max(state, turn, prev_black, prev_white, countTurn1, countTurn2, depth, alpha, beta, maxDepth):

    turn = USER_BLACK

    m = Move()
    bestmove = Move()
    operatorAI = Operator()

    if depth == maxDepth or isTerminal(state)[0]:
        m.value = eval(state)

        return m

    bestmove.value = alpha

    first_prev_black = prev_black

    if (len(findValidBlank(state, prev_black)) != 0):

        for blanks in findValidBlank(state, prev_black):
            operatorAI.row = blanks[0]
            operatorAI.col = blanks[1]

            #dice_num = [4,2,5,1,3,6]
            dice_num = [3, 4, 2, 1, 5, 6]
            for num in dice_num:
                move = ""
                move += str(num)

                if turn == USER_BLACK:
                    move += USER_BLACK
                    move += "M"

                makeMove(state, operatorAI, move)

                prev_black.row = blanks[0]
                prev_black.col = blanks[1]
                prev_black.turn = turn

                m = min(state, turn, prev_black, prev_white, countTurn1,
                        countTurn2, depth+1, bestmove.value, beta, maxDepth)

                undo(state, operatorAI)

                if m.value > bestmove.value:
                    bestmove.value = m.value

                    bestmove.row = blanks[0]
                    bestmove.col = blanks[1]
                    bestmove.dice_face = num

                    if m.value > beta:
                        bestmove.value = beta
                        return bestmove
    return bestmove


def min(state, turn, prev_black, prev_white, countTurn1, countTurn2, depth, alpha, beta, maxDepth):

    turn = USER_WHITE

    m = Move()
    bestmove = Move()
    operatorAI = Operator()

    if depth == maxDepth or isTerminal(state)[0]:
        m.value = eval(state)
        return m
    bestmove.value = beta

    first_prev_white = prev_white

    if (len(findValidBlank(state, prev_white)) != 0):
        for blanks in findValidBlank(state, prev_white):
            operatorAI.row = blanks[0]
            operatorAI.col = blanks[1]

            dice_num = [1, 2, 3, 4, 5, 6]
            for num in dice_num:
                move = ""
                move += str(num)

                if turn == USER_WHITE:
                    move += USER_WHITE
                    move += "M"

                makeMove(state, operatorAI, move)

                prev_white.row = blanks[0]
                prev_white.col = blanks[1]
                prev_white.turn = turn

                m = max(state, turn, prev_black, prev_white, countTurn1,
                        countTurn2, depth+1, alpha, bestmove.value, maxDepth)

                undo(state, operatorAI)

                if m.value < bestmove.value:
                    bestmove.value = m.value

                    bestmove.row = blanks[0]
                    bestmove.col = blanks[1]
                    bestmove.dice_face = num

                    if m.value < alpha:
                        bestmove.value = alpha
                        return bestmove
    return bestmove


# In[43]:


def minimax(state, turn, prev_black, prev_white, countTurn1, countTurn2, depth, alpha, beta, maxDepth):
    m = Move()
    bestmove = Move()
    operatorAI = Operator()

    if depth == maxDepth or isTerminal(state)[0]:
        m.value = eval(state)

        return m

    if turn == USER_BLACK:
        bestmove.value = alpha

        first_prev_black = prev_black

        if (len(findValidBlank(state, prev_black)) != 0):

            for blanks in findValidBlank(state, prev_black):
                operatorAI.row = blanks[0]
                operatorAI.col = blanks[1]

#                 dice_num = [3, 4, 2, 1, 5, 6]
                dice_num = [3, 4, 2]
                random.shuffle(dice_num)
                dice_num.append(1)
                dice_num.append(5)
                dice_num.append(6)

                for num in dice_num:
                    move = ""
                    move += str(num)

                    if turn == USER_BLACK:
                        move += USER_BLACK
                        move += "M"

                    makeMove(state, operatorAI, move)

                    prev_black.row = blanks[0]
                    prev_black.col = blanks[1]

                    m = minimax(state, USER_WHITE, prev_black, prev_white,
                                countTurn1, countTurn2, depth + 1, alpha, beta, maxDepth)

                    undo(state, operatorAI)

                    if m.value > bestmove.value:
                        bestmove.value = m.value
                        bestmove.row = blanks[0]
                        bestmove.col = blanks[1]
                        bestmove.dice_face = num
#                     alpha = max(alpha, bestmove.value)
                    if alpha < bestmove.value:
                        alpha = bestmove.value

                    if alpha >= beta:
                        break

        return bestmove

    elif turn == USER_WHITE:
        m = Move()
        bestmove = Move()
        operatorAI = Operator()
        bestmove.value = beta
        if (len(findValidBlank(state, prev_white)) != 0):
            for blanks in findValidBlank(state, prev_white):
                operatorAI.row = blanks[0]
                operatorAI.col = blanks[1]

                dice_num = [1, 2, 3, 4, 5, 6]
                for num in dice_num:
                    move = ""
                    move += str(num)

                    if turn == USER_WHITE:
                        move += USER_WHITE
                        move += "M"

                    makeMove(state, operatorAI, move)

                    prev_white.row = operatorAI.row
                    prev_white.col = operatorAI.col

                    m = minimax(state, USER_BLACK, prev_black, prev_white,
                                countTurn1, countTurn2, depth + 1, alpha, beta, maxDepth)

                    undo(state, operatorAI)
                    #                 undo_marker_removal(state, first_prev_white)

                    if m.value < bestmove.value:
                        bestmove.value = m.value
                        bestmove.row = blanks[0]
                        bestmove.col = blanks[1]
                        bestmove.dice_face = num
#                     beta = min(beta, bestmove.value)
                    if beta > bestmove.value:
                        beta = bestmove.value
                    if alpha >= beta:
                        break
                        # bestmove.value = alpha
                        # return bestmove
        return bestmove


# In[44]:


def blocker_AI(s, prev_white):
    testOp = Operator()
    blocker_list = []
    if (len(findValidBlank(s, prev_white)) != 0):
        for blanks in findValidBlank(s, prev_white):
            testOp.row = blanks[0]
            testOp.col = blanks[1]

            dice_num = [1, 2, 3, 4, 5, 6]
            for num in dice_num:
                move = ""
                move += str(num)
                move += USER_WHITE
                move += "M"
                makeMove(s, testOp, move)

                for line in range(0, 5):
                    # Check for row completion
                    if ((s.cell[line][0] != BLANK and s.cell[line][0] != BLOCKER) and (
                            s.cell[line][1] != BLANK and s.cell[line][1] != BLOCKER and s.cell[line][1][1] != USER_BLACK) and (
                                s.cell[line][2] != BLANK and s.cell[line][2] != BLOCKER and s.cell[line][2][1] != USER_BLACK) and (s.cell[line][3] != BLANK and s.cell[line][3] != BLOCKER)) and (
                            (s.cell[line][0][1] == s.cell[line][1][1] and s.cell[line][1][1] == s.cell[line][2][1]) or (
                            s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1])):
                        if int(s.cell[line][0][0]) + int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(
                                s.cell[line][3][0]) == 12:
                            blocker_list.append([testOp.row, testOp.col])
#                             blocker_list.append([s.cell[line][0], s.cell[line][1], s.cell[line][2], s.cell[line][3]])

                    if ((s.cell[line][1] != BLANK and s.cell[line][1] != BLOCKER) and (
                            s.cell[line][2] != BLANK and s.cell[line][2] != BLOCKER and s.cell[line][2][1] != USER_BLACK) and (s.cell[line][3] != BLANK and s.cell[line][3] != BLOCKER and s.cell[line][3][1] != USER_BLACK) and (s.cell[line][4] != BLANK and s.cell[line][4] != BLOCKER)) and ((s.cell[line][1][1] == s.cell[line][2][1] and s.cell[line][2][1] == s.cell[line][3][1]) or (s.cell[line][2][1] == s.cell[line][3][1] and s.cell[line][3][1] == s.cell[line][4][1])):
                        if int(s.cell[line][1][0]) + int(s.cell[line][2][0]) + int(s.cell[line][3][0]) + int(
                                s.cell[line][4][0]) == 12:
                            blocker_list.append([testOp.row, testOp.col])

#                             blocker_list.append([s.cell[line][1], s.cell[line][2], s.cell[line][3], s.cell[line][4]])

                    # Check for column completion
                    if ((s.cell[0][line] != BLANK and s.cell[0][line] != BLOCKER) and (
                            s.cell[1][line] != BLANK and s.cell[1][line] != BLOCKER and s.cell[1][line][1] != USER_BLACK) and (
                                s.cell[2][line] != BLANK and s.cell[2][line] != BLOCKER and s.cell[2][line][1] != USER_BLACK) and (
                                s.cell[3][line] != BLANK and s.cell[3][line] != BLOCKER)) and (
                            (s.cell[0][line][1] == s.cell[1][line][1] and s.cell[1][line][1] == s.cell[2][line][1]) or (
                            s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1])):
                        if int(s.cell[0][line][0]) + int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(
                                s.cell[3][line][0]) == 12:
                            blocker_list.append([testOp.row, testOp.col])
#                             blocker_list.append([s.cell[0][line], s.cell[1][line], s.cell[2][line], s.cell[3][line]])

                    if ((s.cell[1][line] != BLANK and s.cell[1][line] != BLOCKER) and (
                            s.cell[2][line] != BLANK and s.cell[2][line] != BLOCKER and s.cell[2][line][1] != USER_BLACK) and (
                                s.cell[3][line] != BLANK and s.cell[3][line] != BLOCKER and s.cell[3][line][1] != USER_BLACK) and (
                                s.cell[4][line] != BLANK and s.cell[4][line] != BLOCKER)) and (
                            (s.cell[1][line][1] == s.cell[2][line][1] and s.cell[2][line][1] == s.cell[3][line][1]) or (
                            s.cell[2][line][1] == s.cell[3][line][1] and s.cell[3][line][1] == s.cell[4][line][1])):
                        if int(s.cell[1][line][0]) + int(s.cell[2][line][0]) + int(s.cell[3][line][0]) + int(
                                s.cell[4][line][0]) == 12:
                            blocker_list.append([testOp.row, testOp.col])
#                             blocker_list.append([s.cell[1][line], s.cell[2][line], s.cell[3][line], s.cell[4][line]])

                # Check for diagonals - Total 8 diagonal ways
                # Main Diagonal - first 4
                if ((s.cell[0][0] != BLANK and s.cell[0][0] != BLOCKER) and (
                        s.cell[1][1] != BLANK and s.cell[1][1] != BLOCKER and s.cell[1][1][1] != USER_BLACK) and (
                            s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER and s.cell[2][2][1] != USER_BLACK) and (
                            s.cell[3][3] != BLANK and s.cell[3][3] != BLOCKER)) and (
                        (s.cell[0][0][1] == s.cell[1][1][1] and s.cell[1][1][1] == s.cell[2][2][1]) or (
                        s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1])):
                    if int(s.cell[0][0][0]) + int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])

#                         blocker_list.append([s.cell[0][0], s.cell[1][1], s.cell[2][2], s.cell[3][3]])

                # Main Diagonal - last 4
                if ((s.cell[1][1] != BLANK and s.cell[1][1] != BLOCKER) and (
                        s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER and s.cell[2][2][1] != USER_BLACK) and (
                            s.cell[3][3] != BLANK and s.cell[3][3] != BLOCKER and s.cell[3][3][1] != USER_BLACK) and (
                            s.cell[4][4] != BLANK and s.cell[4][4] != BLOCKER)) and (
                        (s.cell[1][1][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][3][1]) or (
                        s.cell[2][2][1] == s.cell[3][3][1] and s.cell[3][3][1] == s.cell[4][4][1])):
                    if int(s.cell[1][1][0]) + int(s.cell[2][2][0]) + int(s.cell[3][3][0]) + int(s.cell[4][4][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[1][1], s.cell[2][2], s.cell[3][3], s.cell[4][4]])

                # Off Diagonal - first 4
                if ((s.cell[0][4] != BLANK and s.cell[0][4] != BLOCKER) and (
                        s.cell[1][3] != BLANK and s.cell[1][3] != BLOCKER and s.cell[1][3][1] != USER_BLACK) and (
                            s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER and s.cell[2][2][1] != USER_BLACK) and (
                            s.cell[3][1] != BLANK and s.cell[3][1] != BLOCKER)) and (
                        (s.cell[0][4][1] == s.cell[1][3][1] and
                         s.cell[1][3][1] == s.cell[2][2][1]) or (
                            s.cell[1][3][1] == s.cell[2][2][1] and s.cell[2][2][1] == s.cell[3][1][1])):
                    if int(s.cell[0][4][0]) + int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[0][4], s.cell[1][3], s.cell[2][2], s.cell[3][1]])

                # Off Diagonal - last 4
                if ((s.cell[1][3] != BLANK and s.cell[1][3] != BLOCKER) and (
                        s.cell[2][2] != BLANK and s.cell[2][2] != BLOCKER and s.cell[2][2][1] != USER_BLACK) and (
                            s.cell[3][1] != BLANK and s.cell[3][1] != BLOCKER and s.cell[3][1][1] != USER_BLACK) and (
                            s.cell[4][0] != BLANK and s.cell[4][0] != BLOCKER)) and (
                        (s.cell[1][3][1] == s.cell[2][2][1] and
                         s.cell[2][2][1] == s.cell[3][1][1]) or (
                            s.cell[2][2][1] == s.cell[3][1][1] and s.cell[3][1][1] == s.cell[4][0][1])):
                    if int(s.cell[1][3][0]) + int(s.cell[2][2][0]) + int(s.cell[3][1][0]) + int(s.cell[4][0][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[1][3], s.cell[2][2], s.cell[3][1], s.cell[4][0]])

                # Main Diagonal's upper candrespondent
                if ((s.cell[0][1] != BLANK and s.cell[0][1] != BLOCKER) and (
                        s.cell[1][2] != BLANK and s.cell[1][2] != BLOCKER and s.cell[1][2][1] != USER_BLACK) and (
                            s.cell[2][3] != BLANK and s.cell[2][3] != BLOCKER and s.cell[2][3][1] != USER_BLACK) and (
                            s.cell[3][4] != BLANK and s.cell[3][4] != BLOCKER)) and (
                        (s.cell[0][1][1] == s.cell[1][2][1] and
                         s.cell[1][2][1] == s.cell[2][3][1]) or (
                            s.cell[1][2][1] == s.cell[2][3][1] and s.cell[2][3][1] == s.cell[3][4][1])):
                    if int(s.cell[0][1][0]) + int(s.cell[1][2][0]) + int(s.cell[2][3][0]) + int(s.cell[3][4][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[0][1], s.cell[1][2], s.cell[2][3], s.cell[3][4]])

                # Main Diagonal's lower candrespondent
                if ((s.cell[1][0] != BLANK and s.cell[1][0] != BLOCKER) and (
                        s.cell[2][1] != BLANK and s.cell[2][1] != BLOCKER and s.cell[2][1][1] != USER_BLACK) and (
                            s.cell[3][2] != BLANK and s.cell[3][2] != BLOCKER and s.cell[3][2][1] != USER_BLACK) and (
                            s.cell[4][3] != BLANK and s.cell[4][3] != BLOCKER)) and (
                        (s.cell[1][0][1] == s.cell[2][1][1] and
                         s.cell[2][1][1] == s.cell[3][2][1]) or (
                            s.cell[2][1][1] == s.cell[3][2][1] and s.cell[3][2][1] == s.cell[4][3][1])):
                    if int(s.cell[1][0][0]) + int(s.cell[2][1][0]) + int(s.cell[3][2][0]) + int(s.cell[4][3][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[1][0], s.cell[2][1], s.cell[3][2], s.cell[4][3]])

                # Off Diagonal's upper candrespondent
                if ((s.cell[0][3] != BLANK and s.cell[0][3] != BLOCKER) and (
                        s.cell[1][2] != BLANK and s.cell[1][2] != BLOCKER and s.cell[1][2][1] != USER_BLACK) and (
                            s.cell[2][1] != BLANK and s.cell[2][1] != BLOCKER and s.cell[2][1][1] != USER_BLACK) and (
                            s.cell[3][0] != BLANK and s.cell[3][0] != BLOCKER)) and (
                        (s.cell[0][3][1] == s.cell[1][2][1] and
                         s.cell[1][2][1] == s.cell[2][1][1]) or (
                            s.cell[1][2][1] == s.cell[2][1][1] and s.cell[2][1][1] == s.cell[3][0][1])):
                    if int(s.cell[0][3][0]) + int(s.cell[1][2][0]) + int(s.cell[2][1][0]) + int(s.cell[3][0][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[0][3], s.cell[1][2], s.cell[2][1], s.cell[3][0]])

                # Off Diagonal's lower candrespondent
                if ((s.cell[1][4] != BLANK and s.cell[1][4] != BLOCKER) and (
                        s.cell[2][3] != BLANK and s.cell[2][3] != BLOCKER and s.cell[2][3][1] != USER_BLACK) and (
                            s.cell[3][2] != BLANK and s.cell[3][2] != BLOCKER and s.cell[3][2][1] != USER_BLACK) and (
                            s.cell[4][1] != BLANK and s.cell[4][1] != BLOCKER)) and (
                        (s.cell[1][4][1] == s.cell[2][3][1] and
                         s.cell[2][3][1] == s.cell[3][2][1]) or (
                            s.cell[2][3][1] == s.cell[3][2][1] and s.cell[3][2][1] == s.cell[4][1][1])):
                    if int(s.cell[1][4][0]) + int(s.cell[2][3][0]) + int(s.cell[3][2][0]) + int(s.cell[4][1][0]) == 12:
                        blocker_list.append([testOp.row, testOp.col])
#                         blocker_list.append([s.cell[1][4], s.cell[2][3], s.cell[3][2], s.cell[4][1]])
            undo(s, testOp)
    return blocker_list


# In[31]:


# HumanvsHuman


def HumanvsHuman():

    print("Let's play the game Player 1 vs Player 2")
    while True:
        choice = input("Who should go first? (0=Player 1   1=Player 2): ")
        if int(choice) == 0:
            turn = USER_WHITE
            print("Player 1 will have White dice")
            break
        elif int(choice) == 1:
            turn = USER_BLACK
            print("Player 2 will have Black dice")
            break
        else:
            print("Choose again!")

    current_State.cell = [["000" for i in range(5)] for i in range(5)]
    print_State(current_State)

    prev_White = PreviousMove()
    prev_Black = PreviousMove()

    prev_White.row = -1
    prev_Black.row = -1

    countTurn1 = 0
    countTurn2 = 0

    blockCount1 = 0
    blockCount2 = 0

    while True:

        if(turn == USER_WHITE):
            print("White's(Player 1) Turn")

            if blockCount1 == 0:

                choice = int(
                    input("Do you want to place a blocker? Enter 1 for yes, else for No!"))

                if choice == 1:
                    while True:
                        blockRow = int(input("Block Row (1-5): "))-1
                        blockCol = int(input("Block Col (1-5): "))-1

                        operator.row = blockRow
                        operator.col = blockCol

                        if isvalidBlockerMove(current_State, operator):
                            current_State.cell[operator.row][operator.col] = BLOCKER

                            blockCount1 += 1
                            print("A blocker is placed!")
                            print_State(current_State)
                            break
                        else:
                            print("Not valid place! ")
                else:
                    print("No blocker!")

            print("Please input your move!")
            row = int(input("Row (1-5): "))-1
            col = int(input("Col (1-5): "))-1

            operator.row = row
            operator.col = col

            while True:
                diceNum = int(input("What dice? (1-6): "))
                if diceNum == 1 or diceNum == 2 or diceNum == 3 or diceNum == 4 or diceNum == 5 or diceNum == 6:
                    break
                else:
                    print("Wrong dice! Please input another dice number!")

            move = ""
            move += str(diceNum)

            if(turn == USER_WHITE):
                move += USER_WHITE
                move += "M"

            if isValidMove(current_State, operator, turn, prev_White):
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn1 != 0:
                    operator.row = prev_White.row
                    operator.col = prev_White.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_White.row = row
                prev_White.col = col
                prev_White.turn = turn

                print_State(current_State)
                countTurn1 += 1
                turn = USER_BLACK

                print()
                print("-------------------------------------------")

            else:
                print("Not a valid move! Please tell another move!")

        elif(turn == USER_BLACK):

            print("Player 2 (Black's) Turn")

            if blockCount2 == 0:
                choice = int(input(
                    "Do you want to place a blocker? Enter 1 for yes, else other number for No!"))
                if choice == 1:
                    while True:
                        blockRow = int(input("Block Row (1-5): "))-1
                        blockCol = int(input("Block Col (1-5): "))-1

                        operator.row = blockRow
                        operator.col = blockCol

                        if isvalidBlockerMove(current_State, operator):
                            current_State.cell[operator.row][operator.col] = BLOCKER

                            blockCount1 += 1
                            print("A blocker is placed!")
                            print_State(current_State)
                            break
                        else:
                            print("Not valid place! ")
                else:
                    print("No blocker!")

            print("Please input your move!")
            row = int(input("Row (1-5): "))-1
            col = int(input("Col (1-5): "))-1

            operator.row = row
            operator.col = col

            while True:
                diceNum = int(input("What dice? (1-6): "))
                if diceNum == 1 or diceNum == 2 or diceNum == 3 or diceNum == 4 or diceNum == 5 or diceNum == 6:
                    break
                else:
                    print("Wrong dice! Please input another dice number!")

            move = ""
            move += str(diceNum)

            if(turn == USER_BLACK):
                move += USER_BLACK
                move += "M"

            if isValidMove(current_State, operator, turn, prev_Black):
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn2 != 0:
                    operator.row = prev_Black.row
                    operator.col = prev_Black.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_Black.row = row
                prev_Black.col = col
                prev_Black.turn = turn

                print_State(current_State)
                countTurn2 += 1
                turn = USER_WHITE

                print()
                print("-------------------------------------------")

            else:
                print("Not a valid move! Please tell another move!")

        finalResult = isTerminal(current_State)

        if finalResult[0]:

            if finalResult[0] == '7':
                print("TIE!")
                return 'T'
            elif finalResult[1][1] == 'W':
                print("White Wins!")
                return 'W'
            elif finalResult[1][1] == 'B':
                print("Black Wins!")
                return 'B'

        if isTerminal(current_State)[0]:
            break

        if countTurn1 != 0 and countTurn2 != 0:
            if len(findValidBlank(current_State, prev_White)) == 0 and turn == USER_WHITE:
                print("No valid space available for White! It's a tie")
                return 'T'
                break

            elif len(findValidBlank(current_State, prev_Black)) == 0 and turn == USER_BLACK:
                print("No Valid space available for Black! It's a tie")
                return 'T'
                break


# HumanvsHuman()


# In[32]:


# HumanVRandom

def HumanvsRandom():
    print("Let's play the game Player 1 vs Player 2")
    while True:
        choice = input("Who should go first? (0=Player 1   1=Random): ")
        if int(choice) == 0:
            turn = USER_WHITE
            print("Player 1 will have White dice")
            break
        elif int(choice) == 1:
            turn = USER_BLACK
            print("Random will have Black dice")
            break
        else:
            print("Choose again!")

    current_State.cell = [["000" for i in range(5)] for i in range(5)]
    print_State(current_State)

    prev_White = PreviousMove()
    prev_Black = PreviousMove()

    prev_White.row = -1
    prev_Black.row = -1

    countTurn1 = 0
    countTurn2 = 0

    blockCount1 = 0
    blockCount2 = 0

    while True:

        if(turn == USER_WHITE):
            print("White's(Player 1) Turn")

            if blockCount1 == 0:

                choice = int(
                    input("Do you want to place a blocker? Enter 1 for yes, else for No!"))

                if choice == 1:
                    while True:
                        blockRow = int(input("Block Row (1-5): "))-1
                        blockCol = int(input("Block Col (1-5): "))-1

                        operator.row = blockRow
                        operator.col = blockCol

                        if isvalidBlockerMove(current_State, operator):
                            current_State.cell[operator.row][operator.col] = BLOCKER

                            blockCount1 += 1
                            print("A blocker is placed!")
                            print_State(current_State)
                            break
                        else:
                            print("Not valid place! ")
                else:
                    print("No blocker!")

            print("Please input your move!")
            row = int(input("Row (1-5): "))-1
            col = int(input("Col (1-5): "))-1

            operator.row = row
            operator.col = col

            while True:
                diceNum = int(input("What dice? (1-6): "))
                if diceNum == 1 or diceNum == 2 or diceNum == 3 or diceNum == 4 or diceNum == 5 or diceNum == 6:
                    break
                else:
                    print("Wrong dice! Please input another dice number!")

            move = ""
            move += str(diceNum)

            if(turn == USER_WHITE):
                move += USER_WHITE
                move += "M"

            if isValidMove(current_State, operator, turn, prev_White):
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn1 != 0:
                    operator.row = prev_White.row
                    operator.col = prev_White.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_White.row = row
                prev_White.col = col
                prev_White.turn = turn

                print_State(current_State)
                countTurn1 += 1
                turn = USER_BLACK

                print()
                print("-------------------------------------------")

            else:
                print("Not a valid move! Please tell another move!")

        elif(turn == USER_BLACK):

            print("Black's (Random Player) Turn")
    #         print("Please input your move!")

            if blockCount2 == 0:
                choice = random.randint(0, 1)
                if choice == 0:
                    print("No blocker!")
                else:
                    blanks = findBlank(current_State)
                    blank = random.choice(blanks)

                    blockRow = blank[0]
                    blockCol = blank[1]
    #                 blockRow=random.randint(0,4)
    #                 blockCol=random.randint(0,4)

                    operator.row = blockRow
                    operator.col = blockCol

                    if isvalidBlockerMove(current_State, operator):
                        current_State.cell[operator.row][operator.col] = BLOCKER

                    blockCount1 += 1
                    print("A blocker is placed!")
                    print_State(current_State)

            # For move
            blanks = findBlank(current_State)
            blank = random.choice(blanks)

            row = blank[0]
            col = blank[1]

            operator.row = row
            operator.col = col

            diceNum = random.randint(1, 6)
            move = ""
            move += str(diceNum)

            if(turn == USER_BLACK):
                move += USER_BLACK
                move += "M"

            if isValidMove(current_State, operator, turn, prev_Black):
                print("Random moves...")
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn2 != 0:
                    operator.row = prev_Black.row
                    operator.col = prev_Black.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_Black.row = row
                prev_Black.col = col
                prev_Black.turn = turn

                print_State(current_State)
                countTurn2 += 1

                turn = USER_WHITE

                print()
                print("-------------------------------------------")

        finalResult = isTerminal(current_State)

        if finalResult[0]:

            if finalResult[0] == '7':
                print("TIE!")
                return 'T'
            elif finalResult[1][1] == 'W':
                print("White Wins!")
                print(finalResult)
                return 'W'
            elif finalResult[1][1] == 'B':
                print("Black Wins!")
                print(finalResult)
                return 'B'

        if isTerminal(current_State)[0]:
            print(finalResult)
            break

        if countTurn1 != 0 and countTurn2 != 0:
            if len(findValidBlank(current_State, prev_White)) == 0 and turn == USER_WHITE:
                print("No valid space available for White! It's a tie")
                return 'T'
                break

            elif len(findValidBlank(current_State, prev_Black)) == 0 and turn == USER_BLACK:
                print("No Valid space available for Black! It's a tie")
                return 'T'
                break

# HumanvsRandom()


# In[33]:


# RandomvsRandom- to test the game

def RandomvsRandom():

    current_State.cell = [["000" for i in range(5)] for i in range(5)]

    prev_White = PreviousMove()
    prev_Black = PreviousMove()

    prev_White.row = -1
    prev_Black.row = -1

    turn = USER_WHITE
    countTurn1 = 0
    countTurn2 = 0

    blockCount1 = 0
    blockCount2 = 0

    while True:

        if(turn == USER_WHITE):
            print("White's (Player 1) Turn")

            if blockCount1 == 0:
                choice = random.randint(0, 1)
                if choice == 0:
                    print("No blocker!")
                else:

                    blanks = findBlank(current_State)
                    blank = random.choice(blanks)

                    blockRow = blank[0]
                    blockCol = blank[1]
    #                 blockRow=random.randint(0,4)
    #                 blockCol=random.randint(0,4)

                    operator.row = blockRow
                    operator.col = blockCol

                    if isvalidBlockerMove(current_State, operator):
                        current_State.cell[operator.row][operator.col] = BLOCKER

                    blockCount1 += 1
                    print("A blocker is placed!")
                    print_State(current_State)

            # finding blank space
            blanks = findBlank(current_State)
            blank = random.choice(blanks)

            row = blank[0]
            col = blank[1]

            operator.row = row
            operator.col = col

            diceNum = random.randint(1, 6)
            move = ""
            move += str(diceNum)

            if(turn == USER_WHITE):
                move += USER_WHITE
                move += "M"

            if isValidMove(current_State, operator, turn, prev_White):
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn1 != 0:
                    operator.row = prev_White.row
                    operator.col = prev_White.col
                    print(operator.row, operator.col)
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_White.row = row
                prev_White.col = col
                prev_White.turn = turn

                print_State(current_State)
                countTurn1 += 1

                turn = USER_BLACK

                print()
                print("-------------------------------------------")

        elif(turn == USER_BLACK):

            print("Black's (Random Player) Turn")
    #         print("Please input your move!")

            if blockCount2 == 0:
                choice = random.randint(0, 1)
                if choice == 0:
                    print("No blocker!")
                else:
                    blanks = findBlank(current_State)
                    blank = random.choice(blanks)

                    blockRow = blank[0]
                    blockCol = blank[1]

    #                 blockRow=random.randint(0,4)
    #                 blockCol=random.randint(0,4)

                    operator.row = blockRow
                    operator.col = blockCol

                    if isvalidBlockerMove(current_State, operator):
                        current_State.cell[operator.row][operator.col] = BLOCKER

                    blockCount2 += 1
                    print("A blocker is placed!")
                    print_State(current_State)

            blanks = findBlank(current_State)
            blank = random.choice(blanks)

            row = blank[0]
            col = blank[1]

    #         row=random.randint(0,4)
    #         col=random.randint(0,4)

            operator.row = row
            operator.col = col

            diceNum = random.randint(1, 6)
            move = ""
            move += str(diceNum)

            if(turn == USER_BLACK):
                move += USER_BLACK
                move += "M"

            if isValidMove(current_State, operator, turn, prev_Black):
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn2 != 0:
                    operator.row = prev_Black.row
                    operator.col = prev_Black.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_Black.row = row
                prev_Black.col = col
                prev_Black.turn = turn

                print_State(current_State)
                countTurn2 += 1

                turn = USER_WHITE

                print()
                print("-------------------------------------------")

        finalResult = isTerminal(current_State)

        if finalResult[0]:

            if finalResult[0] == '7':
                print("TIE!")
            elif finalResult[1][1] == 'W':
                print("White Wins!")
    #             print()
            elif finalResult[1][1] == 'B':
                print("Black Wins!")

        if isTerminal(current_State)[0]:
            break

        if countTurn1 != 0 and countTurn2 != 0:
            if len(findValidBlank(current_State, prev_White)) == 0 and turn == USER_WHITE:
                print("No valid space available for White! It's a tie")
                break
            elif len(findValidBlank(current_State, prev_Black)) == 0 and turn == USER_BLACK:
                print("No Valid space available for Black! It's a tie")
                break


# RandomvsRandom()


# In[70]:


# New RandomvsAI

# RandomvsRandom- to test the game
def RandomvsAI(choice):

    print("Let's play the game Random vs Ace")
    while True:
        #choice=input("Who should go first? (0=Random  1=Ace): ")
        if int(choice) == 0:
            turn = USER_WHITE
            print("Random will have White dice")
            break
        elif int(choice) == 1:
            turn = USER_BLACK
            print("Ace will have Black dice")
            break
        else:
            print("Choose again!")

    current_State.cell = [["000" for i in range(5)] for i in range(5)]
    print_State(current_State)

    prev_White = PreviousMove()
    prev_Black = PreviousMove()

    prev_White.row = -1
    prev_Black.row = -1

#     turn=USER_WHITE
    countTurn1 = 0
    countTurn2 = 0

    blockCount1 = 0
    blockCount2 = 0

    while True:

        if(turn == USER_WHITE):
            print("White's (Player 1) Turn")

            if blockCount1 == 0:
                choice = random.randint(0, 1)
                if choice == 0:
                    print("No blocker!")
                else:

                    blanks = findBlank(current_State)
                    blank = random.choice(blanks)

                    blockRow = blank[0]
                    blockCol = blank[1]
    #                 blockRow=random.randint(0,4)
    #                 blockCol=random.randint(0,4)

                    operator.row = blockRow
                    operator.col = blockCol

                    if isvalidBlockerMove(current_State, operator):
                        current_State.cell[operator.row][operator.col] = BLOCKER

                    blockCount1 += 1
                    print("A blocker is placed!")
                    print_State(current_State)

            # finding blank space
            blanks = findBlank(current_State)
            blank = random.choice(blanks)

            row = blank[0]
            col = blank[1]

            operator.row = row
            operator.col = col

            diceNum = random.randint(1, 6)
            move = ""
            move += str(diceNum)

            if(turn == USER_WHITE):
                move += USER_WHITE
                move += "M"

            if isValidMove(current_State, operator, turn, prev_White):
                print("White moves")
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn1 != 0:
                    operator.row = prev_White.row
                    operator.col = prev_White.col
#                     print(operator.row, operator.col)
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_White.row = row
                prev_White.col = col
                prev_White.turn = turn

                print_State(current_State)
                countTurn1 += 1

                turn = USER_BLACK

                print()
                print("-------------------------------------------")

        elif(turn == USER_BLACK):

            print("Black's (AI) Turn")
    #         print("Please input your move!")

            if blockCount2 == 0 and countTurn2 > 1:
                pv_Black = PreviousMove()
                pv_White = PreviousMove()

                pv_Black.row = prev_Black.row
                pv_Black.col = prev_Black.col

                pv_White.row = prev_White.row
                pv_White.col = prev_White.col

                checkWin = minimax(current_State, turn, pv_Black, pv_White,
                                   countTurn1, countTurn2, 0, -MAXEVAL, MAXEVAL, 2)
                print(checkWin.value)

                if checkWin.value != 10:

                    dummy_state = State()
                    cell = [[]]
                    cell = [["000" for i in range(5)] for i in range(5)]

                    dummy_state.cell = cell

                    for i in range(5):
                        for j in range(5):
                            dummy_state.cell[i][j] = current_State.cell[i][j]

                    if len(blocker_AI(dummy_state, prev_White)) == 1:
                        for blocker in blocker_AI(dummy_state, prev_White):
                            if blocker in findValidBlank(current_State, prev_Black):
                                print("No blocker")
                            else:
                                print("Placed Blocker.")
                                current_State.cell[blocker[0]
                                                   ][blocker[1]] = BLOCKER
                                blockCount2 += 1
                                print_State(current_State)
                    if len(blocker_AI(dummy_state, prev_White)) > 1:
                        block_list = []
                        for win_tile in blocker_AI(dummy_state, prev_White):
                            while blockCount2 == 0 and win_tile not in findValidBlank(current_State, prev_Black):
                                current_State.cell[win_tile[0]
                                                   ][win_tile[1]] = BLOCKER
                                print("Placed Blocker.")
                                blockCount2 += 1
                                print_State(current_State)
                                break
                            if win_tile in findValidBlank(current_State, prev_Black):
                                block_list.append(win_tile)
                        while blockCount2 == 0:
                            if len(block_list) > 1:
                                current_State.cell[block_list[0]
                                                   [0]][block_list[0][1]] = BLOCKER
                                print("Placed Blocker.")
                                blockCount2 += 1
                                print_State(current_State)

            if countTurn2 == 0:
                move = ""
                move += str(3)
                move += USER_BLACK
                move += 'M'

                if current_State.cell[2][2] == BLANK and current_State.cell[2][2] != BLOCKER:
                    operator.row = 2
                    operator.col = 2
                    makeMove(current_State, operator, move)
                else:
                    operator.row = 0
                    operator.col = 0
                    makeMove(current_State, operator, move)

                prev_Black.row = operator.row
                prev_Black.col = operator.col
                prev_Black.turn = turn

                print_State(current_State)
                countTurn2 += 1

                turn = USER_WHITE

                print()
                print("-------------------------------------------")

#             dummy_State=current_State
            else:
                p_Black = PreviousMove()
                p_White = PreviousMove()

                p_Black.row = prev_Black.row
                p_Black.col = prev_Black.col

                p_White.row = prev_White.row
                p_White.col = prev_White.col

                p2_Black = PreviousMove()
                p2_White = PreviousMove()

                p2_Black.row = prev_Black.row
                p2_Black.col = prev_Black.col

                p2_White.row = prev_White.row
                p2_White.col = prev_White.col

                check = minimax(current_State, turn, p2_Black, p2_White,
                                countTurn1, countTurn2, 0, -MAXEVAL, MAXEVAL, 2)

                m = minimax(current_State, turn, p_Black, p_White,
                            countTurn1, countTurn2, 0, -MAXEVAL, MAXEVAL, 3)

                if check.value == 10 and m.value == 10:
                    operator.row = check.row
                    operator.col = check.col
                    face = check.dice_face
                    print(check.value)
                else:

                    operator.row = m.row
                    operator.col = m.col
                    face = m.dice_face

                    print(m.value)

                print(operator.row+1, operator.col+1)
                print(face)

                move = ""
                move += str(face)

                if(turn == USER_BLACK):
                    move += USER_BLACK
                    move += "M"

                if isValidMove(current_State, operator, turn, prev_Black):
                    print("Black Moves")
                    makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn2 != 0:
                    operator.row = prev_Black.row
                    operator.col = prev_Black.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                    prev_Black.row = m.row
                    prev_Black.col = m.col
                    prev_Black.turn = turn

                    print_State(current_State)
                    countTurn2 += 1

                    turn = USER_WHITE

                    print()
                    print("-------------------------------------------")

        finalResult = isTerminal(current_State)

        if finalResult[0]:

            if finalResult[0] == '7':
                print("TIE!")
                return 'T'
            elif finalResult[1][1] == 'W':
                print("White Wins!")
                print(finalResult)
                return 'W'
            elif finalResult[1][1] == 'B':
                print("Black Wins!")
                print(finalResult)
                return 'B'

        if isTerminal(current_State)[0]:
            print(finalResult)
            break

        if countTurn1 != 0 and countTurn2 != 0:
            if len(findValidBlank(current_State, prev_White)) == 0 and turn == USER_WHITE:
                print("No valid space available for White! It's a tie")
                return 'T'
                break

            elif len(findValidBlank(current_State, prev_Black)) == 0 and turn == USER_BLACK:
                print("No Valid space available for Black! It's a tie")
                return 'T'
                break


# RandomvsAI(1)

# i=0
# w=0
# b=0
# t=0


# for i in range(10):


#     result=RandomvsAI(i%2)
#     if result=="W":
#         w=w+1
#     elif result=="B":
#         b=b+1
#     elif result=="T":
#         t=t+1
# #     print_State(current_State)

# print("White: ",w)
# print("AI: ", b)
# print("TIE: ", t)


# In[36]:


# HumanvsAI-final minmax new
def HumanvsAI():

    print("Let's play the game Human vs Ace")
    while True:
        choice = input("Who should go first? (0=Human 1=Ace): ")
        if int(choice) == 0:
            turn = USER_WHITE
            print("Random will have White dice")
            break
        elif int(choice) == 1:
            turn = USER_BLACK
            print("Ace will have Black dice")
            break
        else:
            print("Choose again!")

    current_State.cell = [["000" for i in range(5)] for i in range(5)]
    print_State(current_State)

    prev_White = PreviousMove()
    prev_Black = PreviousMove()

    prev_White.row = -1
    prev_Black.row = -1

    countTurn1 = 0
    countTurn2 = 0

    blockCount1 = 0
    blockCount2 = 0

    while True:

        if(turn == USER_WHITE):
            print("White's(Player 1) Turn")

            if blockCount1 == 0:

                choice = int(
                    input("Do you want to place a blocker? Enter 1 for yes, else for No!"))

                if choice == 1:
                    while True:
                        blockRow = int(input("Block Row (1-5): "))-1
                        blockCol = int(input("Block Col (1-5): "))-1

                        operator.row = blockRow
                        operator.col = blockCol

                        if isvalidBlockerMove(current_State, operator):
                            current_State.cell[operator.row][operator.col] = BLOCKER

                            blockCount1 += 1
                            print("A blocker is placed!")
                            print_State(current_State)
                            break
                        else:
                            print("Not valid place! ")
                else:
                    print("No blocker!")

            print("Please input your move!")
            row = int(input("Row (1-5): "))-1
            col = int(input("Col (1-5): "))-1

            operator.row = row
            operator.col = col

            while True:
                diceNum = int(input("What dice? (1-6): "))
                if diceNum == 1 or diceNum == 2 or diceNum == 3 or diceNum == 4 or diceNum == 5 or diceNum == 6:
                    break
                else:
                    print("Wrong dice! Please input another dice number!")

            move = ""
            move += str(diceNum)

            if(turn == USER_WHITE):
                move += USER_WHITE
                move += "M"

            if isValidMove(current_State, operator, turn, prev_White):
                makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn1 != 0:
                    operator.row = prev_White.row
                    operator.col = prev_White.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                prev_White.row = row
                prev_White.col = col
                prev_White.turn = turn

                print_State(current_State)
                countTurn1 += 1
                turn = USER_BLACK

                print()
                print("-------------------------------------------")

            else:
                print("Not a valid move! Please tell another move!")

        elif(turn == USER_BLACK):

            print("Black's (AI) Turn")
            if blockCount2 == 0 and countTurn2 > 1:
                pv_Black = PreviousMove()
                pv_White = PreviousMove()

                pv_Black.row = prev_Black.row
                pv_Black.col = prev_Black.col

                pv_White.row = prev_White.row
                pv_White.col = prev_White.col

                checkWin = minimax(current_State, turn, pv_Black, pv_White,
                                   countTurn1, countTurn2, 0, -MAXEVAL, MAXEVAL, 2)
                print(checkWin.value)
                if checkWin.value != 10:

                    dummy_state = State()
                    cell = [[]]
                    cell = [["000" for i in range(5)] for i in range(5)]

                    dummy_state.cell = cell

                    for i in range(5):
                        for j in range(5):
                            dummy_state.cell[i][j] = current_State.cell[i][j]

                    if len(blocker_AI(dummy_state, prev_White)) == 1:
                        for blocker in blocker_AI(dummy_state, prev_White):
                            if blocker in findValidBlank(current_State, prev_Black):
                                print("No blocker")
                            else:
                                print("Placed Blocker.")
                                current_State.cell[blocker[0]
                                                   ][blocker[1]] = BLOCKER
                                blockCount2 += 1
                                print_State(current_State)
                    if len(blocker_AI(dummy_state, prev_White)) > 1:
                        block_list = []
                        for win_tile in blocker_AI(dummy_state, prev_White):
                            while blockCount2 == 0 and win_tile not in findValidBlank(current_State, prev_Black):
                                current_State.cell[win_tile[0]
                                                   ][win_tile[1]] = BLOCKER
                                print("Placed Blocker.")
                                blockCount2 += 1
                                print_State(current_State)
                                break
                            if win_tile in findValidBlank(current_State, prev_Black):
                                block_list.append(win_tile)
                        while blockCount2 == 0:
                            if len(block_list) > 1:
                                current_State.cell[block_list[0]
                                                   [0]][block_list[0][1]] = BLOCKER
                                print("Placed Blocker.")
                                blockCount2 += 1
                                print_State(current_State)

            if countTurn2 == 0:
                move = ""
                move += str(3)
                move += USER_BLACK
                move += 'M'

                if current_State.cell[2][2] == BLANK and current_State.cell[2][2] != BLOCKER:
                    operator.row = 2
                    operator.col = 2
                    makeMove(current_State, operator, move)
                elif current_State.cell[0][0] == BLANK and current_State.cell[0][0] != BLOCKER:
                    operator.row = 0
                    operator.col = 0
                    makeMove(current_State, operator, move)
                else:
                    operator.row = 0
                    operator.col = 4
                    makeMove(current_State, operator, move)

                prev_Black.row = operator.row
                prev_Black.col = operator.col
                prev_Black.turn = turn

                print_State(current_State)
                countTurn2 += 1

                turn = USER_WHITE

                print()
                print("-------------------------------------------")

#             dummy_State=current_State
            else:
                p_Black = PreviousMove()
                p_White = PreviousMove()

                p_Black.row = prev_Black.row
                p_Black.col = prev_Black.col

                p_White.row = prev_White.row
                p_White.col = prev_White.col

                p2_Black = PreviousMove()
                p2_White = PreviousMove()

                p2_Black.row = prev_Black.row
                p2_Black.col = prev_Black.col

                p2_White.row = prev_White.row
                p2_White.col = prev_White.col

                check = minimax(current_State, turn, p2_Black, p2_White,
                                countTurn1, countTurn2, 0, -MAXEVAL, MAXEVAL, 2)

                m = minimax(current_State, turn, p_Black, p_White,
                            countTurn1, countTurn2, 0, -MAXEVAL, MAXEVAL, 3)

                if check.value == 10 and m.value == 10:
                    operator.row = check.row
                    operator.col = check.col
                    face = check.dice_face
                    print(check.value)
                else:

                    operator.row = m.row
                    operator.col = m.col
                    face = m.dice_face

                    print(m.value)

                print(operator.row+1, operator.col+1)
                print(face)

                move = ""
                move += str(face)

                if(turn == USER_BLACK):
                    move += USER_BLACK
                    move += "M"

                if isValidMove(current_State, operator, turn, prev_Black):
                    makeMove(current_State, operator, move)

            # Removing marker from previous move
                if countTurn2 != 0:
                    operator.row = prev_Black.row
                    operator.col = prev_Black.col
                    removeMarker(current_State, operator)

                # Tracking previous move
                    prev_Black.row = m.row
                    prev_Black.col = m.col
                    prev_Black.turn = turn

                    print_State(current_State)
                    countTurn2 += 1

                    turn = USER_WHITE

                    print()
                    print("-------------------------------------------")

    #         else:
    #             print("Not a valid move! Please tell your move again!")

        finalResult = isTerminal(current_State)

        if finalResult[0]:

            if finalResult[0] == '7':
                print("TIE!")
#                 return 'T'
            elif finalResult[1][1] == 'W':
                print("White Wins!")
#                 return 'W'
            elif finalResult[1][1] == 'B':
                print("Black Wins!")
#                 return 'B'

        if isTerminal(current_State)[0]:
            print(finalResult)
            break

        if countTurn1 != 0 and countTurn2 != 0:
            if len(findValidBlank(current_State, prev_White)) == 0 and turn == USER_WHITE:
                print("No valid space available for White! It's a tie")
                return 'T'
                break

            elif len(findValidBlank(current_State, prev_Black)) == 0 and turn == USER_BLACK:
                print("No Valid space available for Black! It's a tie")
                return 'T'
                break


# HumanvsAI()


# In[47]:
print("Welcome to the DOCE Game. The game consists of 5x5 board with 11 dice of BLACK colors and 11 dice of White colors. To begin, please choose who you want to play the game with:")
print("1. Another human")
print("2. Random Player")
print("3. AI")
player_option = int(input("Please enter your option(1, 2, 3): "))
if player_option == 1:
    HumanvsHuman()
    pass
elif player_option == 2:
    HumanvsRandom()
    pass
elif player_option == 3:
    HumanvsAI()
    pass
