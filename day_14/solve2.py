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

def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

# Open the input file
textFile = open(args.input, "r")

# Create 2D list
positions = list()
velocities = list()

for line in textFile:
    line = line.strip()

    position = line.split(" v=")[0].split("p=")[1].split(",")
    position = list(map(int, position))
    # kprint("p  =",position)

    velocity = line.split(" v=")[1].split(",")
    velocity = list(map(int, velocity))
    # kprint("v  =",velocity)

    positions.append(position)
    velocities.append(velocity)

minStdDev = 9999999
minStdDevSeconds = 0

for seconds in range(1,args.wide*args.tall+1):

    # Fill the temp positions list
    tempPositionsX = list()
    tempPositionsY = list()
    for index in range(0, len(positions)):
        kprint(index)
        position_x = (positions[index][0] + velocities[index][0]*seconds)%args.wide
        position_y = (positions[index][1] + velocities[index][1]*seconds)%args.tall
        tempPositionsX.append(position_x)
        tempPositionsY.append(position_y)

    # Find the standard deviation
    tempStdDev = stddev(tempPositionsX) + stddev(tempPositionsY)

    if(tempStdDev < minStdDev):
        minStdDev = tempStdDev
        minStdDevSeconds = seconds

print("minStdDev : ",minStdDev)
print("minStdDevS: ", minStdDevSeconds)

# minStdDevSeconds = 28

# Fill the temp positions list
picture = np.full(shape=(args.tall,args.wide), dtype=str, fill_value=".")
for index in range(0, len(positions)):
    kprint(index)
    position_x = (positions[index][0] + velocities[index][0]*minStdDevSeconds)%args.wide
    position_y = (positions[index][1] + velocities[index][1]*minStdDevSeconds)%args.tall
    
    picture[position_y,position_x] = "#"

np.savetxt("foo.csv", picture, delimiter="", fmt='%1s')

