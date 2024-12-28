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
lineIndex = 0
equation = list()

for line in textFile:
    line = line.strip()

    if lineIndex % 4 == 0 or lineIndex % 4 == 1:
        equation.append(int(line.split("X+")[1][0:2].strip()))
        equation.append(int(line.split("Y+")[1][0:2].strip()))

    elif lineIndex % 4 == 3:
        pass

    elif lineIndex % 4 == 2:
        equation.append(int(line.split("X=")[1].split(",")[0].strip()))
        equation.append(int(line.split("Y=")[1].strip()))
        equations.append(equation)
        equation = list()

    lineIndex = lineIndex + 1

kprint(equations)

