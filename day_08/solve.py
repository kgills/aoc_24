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
antennaMap = list()
for line in textFile:
    line = line.strip()
    nodes = list(line)
    antennaMap.append(nodes)

# Create the antenna map
antennaMap = np.array(antennaMap)
kprint("antennaMap")
kprint(antennaMap)

# Create the antinode map
antinodeMap = np.full(antennaMap.shape, ".")
kprint("antinodeMap")
kprint(antinodeMap)

def validAnt(row, col):
    # Make sure the row and col are valid
    if row < 0 or row >= antennaMap.shape[0]:
        return False
    if col < 0 or col >= antennaMap.shape[1]:
        return False

    return True

# Iterate over the antenna map
for row in range(0,antennaMap.shape[0]):
    for col in range(0,antennaMap.shape[1]):

        # Find the antennas
        if(antennaMap[row,col] != "."):
            antenna = antennaMap[row,col]
            kprint(row, " ", col, " ", antenna)

            # Find the other antennas that match
            otherAntennas = np.where(antennaMap == antenna)
            kprint(otherAntennas)

            # Set the antinodes
            for otherAntIndex in range(0,len(otherAntennas[0])):
                otherAntRow = otherAntennas[0][otherAntIndex]
                otherAntCol = otherAntennas[1][otherAntIndex]

                # Antinode appears on antennas that have a peer
                if args.part2:
                    antinodeMap[row,col] = "#"

                # Skip the current antenna
                if otherAntRow == row and otherAntCol == col:
                    continue
                kprint(otherAntRow, " ", otherAntCol)

                # Find the antinode location
                antiRow = row + -1 * (otherAntRow-row)
                antiCol = col + -1 * (otherAntCol-col)

                if not validAnt(antiRow, antiCol):
                    continue

                # Set the antinode
                antinodeMap[antiRow,antiCol] = "#"

                if(args.part2):

                    # Set the harmonic antennas
                    harmonicRow = antiRow + -1 * (otherAntRow-row)
                    harmonicCol = antiCol + -1 * (otherAntCol-col)

                    while validAnt(harmonicRow, harmonicCol):
                        antinodeMap[harmonicRow,harmonicCol] = "#"
                        harmonicRow = harmonicRow + -1 * (otherAntRow-row)
                        harmonicCol = harmonicCol + -1 * (otherAntCol-col)


kprint(antinodeMap)
print(np.count_nonzero(antinodeMap == "#"))
