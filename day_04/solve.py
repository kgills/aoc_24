import csv
import argparse
import re
import numpy as np

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

def get_2d_list_slice(matrix, start_row, end_row, start_col, end_col):
    return [row[start_col:end_col] for row in matrix[start_row:end_row]]

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
npArray = np.pad(npArray,3,mode='wrap')
kprint(npArray)
kprint()

