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
labMap = list()
for line in textFile:
    line = line.strip()

    line = list(line)
    labMap.append(line)

# Convert to np
labMap = np.array(labMap)
kprint(labMap)

# Find the starting position
startPosition = np.where(labMap == "^")
startPosition = (int(startPosition[0][0]),int(startPosition[1][0]))
startDirection = [-1,0]

# Replace start position with "X"
labMap[startPosition] = "^"
kprint(startPosition)
kprint(startDirection)
kprint(labMap)

def advanceGuard(labMap, position, direction):

    kprint(position)
    kprint(direction)
    kprint(labMap)

    # Advance the position
    nextPosition = position
    nextPosition = (position[0] + direction[0], position[1] + direction[1])
    kprint(nextPosition)

    # See if it's off the map
    if(nextPosition[0] < 0 or nextPosition[1] < 0 or
        nextPosition[0] >= labMap.shape[0] or nextPosition[1] >= labMap.shape[1]):

        kprint("Off the map")
        return (False,position,direction,labMap)

    # See if there is an obstacle in the next position
    kprint(labMap[nextPosition])
    if(labMap[nextPosition] == "#"):
        kprint("Rotating")
        nextPosition = position
        if   direction == [0,1]:  direction = [1,0]
        elif direction == [1,0]:  direction = [0,-1]
        elif direction == [0,-1]: direction = [-1,0]
        elif direction == [-1,0]: direction = [0,1]

    position = nextPosition

    return (True,position,direction,labMap)


def in_sorted_list(elem, sorted_list):
    i = bisect.bisect_left(sorted_list, elem)
    return i != len(sorted_list) and sorted_list[i] == elem

if args.part2:

    loopCount = 0

    # Save the original path
    # Advance the while he's still in the map
    validGuard = True
    position = startPosition
    direction = startDirection

    while validGuard:
        # Save the guard's path
        labMap[position] = "X"

        # Advance the guard
        validGuard,position,direction,labMap = advanceGuard(labMap,position,direction)


    # Add one obstacle
    for row in range(0,labMap.shape[0]):
        for col in range(0,labMap.shape[1]):

            # Only add obstacles to the guard's original path
            if(labMap[(row,col)]) == "X":
                print(row," ",col)
                # Add a temp obstacle
                labMap[(row,col)] = "#"

                # Advance the while he's still in the map
                validGuard = True
                position = startPosition
                direction = startDirection

                # Save a list of positions and directions
                positionDirectionLog = []
                positionDirectionLog.append([position[0],position[1],direction[0],direction[1]])
                kprint(positionDirectionLog)

                while validGuard:

                    # Advance the guard
                    validGuard,position,direction,labMap = advanceGuard(labMap,position,direction)

                    posDir = [position[0],position[1],direction[0],direction[1]]

                    # If we stay on the map and are in a position with the same direction, we're in a loop
                    if validGuard and in_sorted_list(posDir,positionDirectionLog):
                        loopCount = loopCount + 1
                        kprint(labMap)
                        kprint(positionDirectionLog)
                        break

                    # Log this position and direction
                    # positionDirectionLog.append(posDir)
                    bisect.insort(positionDirectionLog, posDir)

                # Remove the temp obstacle
                labMap[(row,col)] = "X"

    print(loopCount)

else:

    # Advance the while he's still in the map
    validGuard = True
    position = startPosition
    direction = startDirection

    labMap[startPosition] = "X"


    while validGuard:
        # Save the guard's path
        labMap[position] = "X"

        # Advance the guard
        validGuard,position,direction,labMap = advanceGuard(labMap,position,direction)

    # Count the number of "X" in the map
    print(np.count_nonzero(labMap == "X"))
    

