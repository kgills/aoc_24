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
equations = list()
for line in textFile:
    line = line.strip()

    result = int(line.split(":")[0].strip())
    operands = list(map(int,line.split(":")[1].strip().split(" ")))
    equations.append([result,operands])

kprint(equations)

def strAppend(left, right):
    # Convert int to string
    left = str(left)
    right = str(right)

    return int(left+right)

def getPossbileValues(values):
    
    if(len(values) == 1):
        return list(values)

    # Get the possible values for the rest of the list, save the last element
    possibleValues = getPossbileValues(values[:-1])

    newValues = []

    for possibleValue in possibleValues:
        newValues.append(values[-1] + possibleValue)
        newValues.append(values[-1] * possibleValue)
        newValues.append(strAppend(possibleValue, values[-1]))

    return newValues

testValues = 0
for equation in equations:

    kprint(equation)

    # Get a list of the possible values from the rest of the list, except the last value
    possibleValues = getPossbileValues(equation[1][:-1])

    kprint(possibleValues)

    # See if we can make a valid equation with the possible values
    for possibleValue in possibleValues:
        if(equation[1][-1] * possibleValue == equation[0] or equation[1][-1] + possibleValue == equation[0] or 
            strAppend(possibleValue, equation[1][-1]) == equation[0]):
            kprint("Valid equation")
            testValues = testValues + equation[0]
            break

print(testValues)
    

