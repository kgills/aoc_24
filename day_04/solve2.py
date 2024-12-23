import csv
import argparse
import re
import numpy as np
import sys

parser = argparse.ArgumentParser(
                    prog='solve',
                    description='Solve AOC')

parser.add_argument('input', help="Input CSV file.")
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

def getWord(inputArray, row, col, rowFactor, colFactor, wordLen):
    retWord = ""
    for index in range(0, wordLen):
        retWord = retWord + inputArray[row+index*rowFactor, col+index*colFactor]

    kprint(retWord)
    return retWord

def getCount(inputArray, row, col, inputStr):
    count = 0
    for rowFactor in range(-1,2):

        # Only search the diagonals, where rowFactor and colFactor are non zero
        if(rowFactor == 0):
            continue
        for colFactor in range(-1,2):
            if(colFactor == 0):
                continue

            # Start at the factor location, serach in the opposite direction
            tempRow = row + rowFactor
            tempCol = col + colFactor

            rowFactor = rowFactor * -1
            colFactor = colFactor * -1
            if(getWord(inputArray, tempRow, tempCol, rowFactor, colFactor, len(inputStr)) == inputStr):
                count = count + 1
    return count


# Open the input file
textFile = open(args.input, "r")

# Create the input array
inputArray = list()
for line in textFile:
    line = list(line.strip())
    inputArray.append(line)

# Convert to np
npArray = np.array(inputArray)

kprint(npArray)
kprint()

# Pad the array to get the wrap
WORD_SEARCH="MAS"
PAD_LEN=len(WORD_SEARCH)-1
npArray = np.pad(npArray,PAD_LEN,mode='constant')
kprint(npArray)
kprint()

sumXmas = 0

for row in range(PAD_LEN, npArray.shape[0]-PAD_LEN):
        for col in range(PAD_LEN, npArray.shape[1]-PAD_LEN):
            if(npArray[row,col] == WORD_SEARCH[1]):
                kprint("row: ",row," col: ",col)
                if getCount(npArray,row,col,WORD_SEARCH) == 2:
                    sumXmas = sumXmas + 1

print(sumXmas)



