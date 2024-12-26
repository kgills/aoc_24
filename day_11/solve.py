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
parser.add_argument('-b','--blink', help="Number of blinks", default="25")

args = parser.parse_args()
print(args)

args.blink = int(args.blink)

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
stones = list()
for line in textFile:
    line = line.strip()
    stones = line.split(" ")
    stones = list(map(int, stones))

# Create the list of stones
kprint(stones)

def getScore(blink, stone):

    # Reached the max depth
    if(blink == args.blink):
        return 1

    # Turn a 0 into a 1
    if(stone == 0):
        return getScore(blink+1, 1)

    # If number of digits is even
    digits = int(math.log10(stone))+1

    kprint(digits)
    if digits % 2 == 0:
        divisor = pow(10,int(digits/2))
        leftHalf = int(stone / divisor)
        rightHalf = stone - (leftHalf*divisor)

        kprint("stone    : ", stone)
        kprint("leftHalf : ", leftHalf)
        kprint("rightHalf: ", rightHalf)

        score = getScore(blink+1, leftHalf) + getScore(blink+1, rightHalf)
        return score
    
    # Number of digits is odd
    return getScore(blink+1, stone*2024)

score = 0
for stone in stones:
    score = score + getScore(0, stone)

print(score)



