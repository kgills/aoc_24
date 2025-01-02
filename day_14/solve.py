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
parser.add_argument('wide', help="How many tiles wide the map is.", type=int)
parser.add_argument('tall', help="How many tiles tall the map is.", type=int)
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
positions = list()
velocities = list()

seconds = 100

q0 = 0
q1 = 0
q2 = 0
q3 = 0

# 9 : 0 1 2 3    4    5 6 7 8
# 10: 0 1 2 3 4       5 6 7 8 9
widthMid = math.floor(args.wide/2)
widthLow = 0
widthHigh = 0
if args.wide % 2 != 0: 
    widthLow = widthMid-1
    widthHigh = widthMid+1
else:
    widthLow = widthMid-1
    widthHigh = widthMid


heightMid = math.floor(args.tall/2)
heightLow = 0
heightHigh = 0
if args.tall % 2 != 0: 
    heightLow = heightMid-1
    heightHigh = heightMid+1
else:
    heightLow = heightMid-1
    heightHigh = heightMid

kprint("widthLow  : ",widthLow)
kprint("widthHigh : ",widthHigh)
kprint("heightLow : ",heightLow)
kprint("heightHigh: ",heightHigh)

for line in textFile:
    line = line.strip()

    position = line.split(" v=")[0].split("p=")[1].split(",")
    position = list(map(int, position))
    kprint("p  =",position)

    velocity = line.split(" v=")[1].split(",")
    velocity = list(map(int, velocity))
    # kprint("v  =",velocity)

    position[0] = (position[0] + velocity[0]*seconds)%args.wide
    position[1] = (position[1] + velocity[1]*seconds)%args.tall

    positions.append(position)
    velocities.append(velocity)
    # kprint("fp =",position)
    # kprint()

    if   position[0] <= widthLow  and position[1] <= heightLow: q0 = q0 + 1
    elif position[0] >= widthHigh and position[1] <= heightLow: q1 = q1 + 1
    elif position[0] <= widthLow  and position[1] >= heightHigh: q2 = q2 + 1
    elif position[0] >= widthHigh and position[1] >= heightHigh: q3 = q3 + 1
    else: 
        kprint("In the middle")
        kprint("v  =",velocity)
        kprint("fp  =",position)


kprint("q0: ",q0)
kprint("q1: ",q1)
kprint("q2: ",q2)
kprint("q3: ",q3)

print(q0*q1*q2*q3)

# 227918385 too high
# 224438715



