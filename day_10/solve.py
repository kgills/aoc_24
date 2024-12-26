import csv
import argparse
import re
import numpy as np
import sys
from collections import defaultdict
import math
import bisect

parser = argparse.ArgumentParser(
                    prog='solve',
                    description='Solve AOC')

parser.add_argument('input', help="Input CSV file.")
parser.add_argument('-p2','--part2', help="Sove for part 2.", action='store_true')
parser.add_argument('-v','--verbose', help="Verbose output", action='store_true')

args = parser.parse_args()
print(args)

if args.verbose:
    def kprint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
           print(arg,end="")
        print()
else:   
    kprint = lambda *a: None      # do-nothing function

# Open the input file
textFile = open(args.input, "r")

# Create 2D list
trailMap = list()
for line in textFile:
    line = line.strip()
    nodes = list(line)
    nodes = list(map(int, nodes))

    trailMap.append(nodes)

# Create the trail map
trailMap = np.array(trailMap)
kprint(trailMap)

maxRows = trailMap.shape[0]
maxCols = trailMap.shape[1]

kprint(maxRows)
kprint(maxCols)

def getLocations(row,col,number):

    # Find number surrounding row,col, not diagonal
    rows = []
    cols = []

    if(row < (maxRows-1)):
        if trailMap[row+1,col] == number:
            rows.append(row+1)
            cols.append(col)
    if(col < (maxCols-1)):
        if trailMap[row,col+1] == number:
            rows.append(row)
            cols.append(col+1)
    if(row > 0):
        if trailMap[row-1,col] == number:
            rows.append(row-1)
            cols.append(col)
    if(col > 0):
        if trailMap[row,col-1] == number:
            rows.append(row)
            cols.append(col-1)

    return rows,cols


def getScore(row, col):

    if(trailMap[row,col] == 9):
        location = [(int(row),int(col))]
        return location

    # Get the number at this location, look for the surrounding nodes that have this number + 1
    thisNumber = trailMap[row,col]

    rows,cols = getLocations(row,col,thisNumber+1)

    score = list()
    for index in range(0,len(rows)):
        score = score + getScore(rows[index],cols[index])

    return score


# Find the starting points
startingPoints = np.where(trailMap == 0)
kprint(startingPoints)

scores = 0
for startingPoint in range(0, len(startingPoints[0])):
    row = startingPoints[0][startingPoint]
    col = startingPoints[1][startingPoint]
    kprint(row, " ", col)
    
    # Get the score for the path
    score = getScore(row,col)
    kprint("score")
    kprint(score)

    # Remove duplicates
    score = list(dict.fromkeys(score))
    # Count the number of entries
    score = len(score)

    kprint(score)
    scores = scores + score

print(scores)

