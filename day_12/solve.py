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
gardenMap = list()
for line in textFile:
    line = line.strip()
    nodes = list(line)
    gardenMap.append(nodes)

# Create the garden map
gardenMap = np.array(gardenMap)
kprint(gardenMap)

# Get a list of unique elements
plants = np.unique(gardenMap)
kprint(plants)

def getNeighbors(location):
    neighbors = []

    plant = gardenMap[location]

    row = location[0]
    col = location[1]

    if(row > 0 and gardenMap[row-1,col] == plant): neighbors.append((row-1,col))
    if(row < (gardenMap.shape[0]-1) and gardenMap[row+1,col] == plant): neighbors.append((row+1,col))
    if(col > 0 and gardenMap[row,col-1] == plant): neighbors.append((row,col-1))
    if(col < (gardenMap.shape[1]-1) and gardenMap[row,col+1] == plant): neighbors.append((row,col+1))

    return neighbors

def plantSearch(plantLocation):

    visited = []   # List for visited nodes.
    queue = []     # Initialize a queue

    # Add the first location
    visited.append(plantLocation)
    queue.append(plantLocation)

    while queue: # Creating loop to visit each node
        location = queue.pop(0) 
        
        # Get a list of neighbors
        neighbors = getNeighbors(location)

        for neighbour in neighbors:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)

    return visited

def getPerimeter(plantGroup):
    perimiterTotal = 0

    for plant in plantGroup:
        neighborCount = len(getNeighbors(plant))

        perimiter = 4 - neighborCount

        perimiterTotal = perimiterTotal + perimiter

    return perimiterTotal


def addPlants(visited, plantGroup):
    for plant in plantGroup:
        visited[plant] = 1
    return visited

def getGroups(matchList):

    if matchList == []:
        return 0

    groups = 1

    for index in range(1,len(matchList)):
        if matchList[index] != matchList[index-1]+1:
            groups = groups + 1

    return groups


def getSides(plantGroup):

    sides = 0

    plant = gardenMap[plantGroup[0][0],plantGroup[0][1]]

    # Get the min/max row/col
    minRow = 9999999
    maxRow = 0
    minCol = 9999999
    maxCol = 0

    for tempPlant in plantGroup:
        if tempPlant[0] < minRow: minRow = tempPlant[0]
        if tempPlant[1] < minCol: minCol = tempPlant[1]
        if tempPlant[0] > maxRow: maxRow = tempPlant[0]
        if tempPlant[1] > maxCol: maxCol = tempPlant[1]

    # Start at the min row, sweep across to the max row
    # Find elements that are first time match, min to max row
    # Each group of first matches is a side

    for col in range(minCol, maxCol+1):
        matchList = []
        kprint(gardenMap[:,col])
        for row in range(minRow, maxRow+1):

            # Get a list of row
            if col == minCol:
                # Don't have to check previous col in first col
                if gardenMap[row,col] == plant and (row,col) in plantGroup:
                    matchList.append(row)
            else:
                # Make this this is a first time plant match
                if gardenMap[row,col] == plant and (row,col) in plantGroup and gardenMap[row,col-1] != plant:
                    matchList.append(row)

        # Figure out how many groups we have in the match list
        side = getGroups(matchList)
        kprint("side: ",side)
        sides = sides + side

    for col in range(maxCol, minCol-1,-1):
        matchList = []
        kprint(gardenMap[:,col])

        for row in range(minRow, maxRow+1):
            # Get a list of cols
            if col == maxCol:
                # Don't have to check previous row in first row
                if gardenMap[row,col] == plant and (row,col) in plantGroup:
                    matchList.append(row)
            else:
                # Make this this is a first time plant match
                if gardenMap[row,col] == plant and (row,col) in plantGroup and gardenMap[row,col+1] != plant:
                    matchList.append(row)

        # Figure out how many groups we have in the match list
        side = getGroups(matchList)
        kprint("side: ",side)
        sides = sides + side

    for row in range(minRow, maxRow+1):
        matchList = []
        kprint(gardenMap[row,:])
        for col in range(minCol, maxCol+1):

            # Get a list of col
            if row == minRow:
                # Don't have to check previous col in first col
                if gardenMap[row,col] == plant and (row,col) in plantGroup:
                    matchList.append(col)
            else:
                # Make this this is a first time plant match
                if gardenMap[row,col] == plant and (row,col) in plantGroup and gardenMap[row-1,col] != plant:
                    matchList.append(col)

        # Figure out how many groups we have in the match list
        side = getGroups(matchList)
        kprint("side: ",side)
        sides = sides + side

    for row in range(maxRow, minRow-1,-1):
        matchList = []
        kprint(gardenMap[row,:])
        for col in range(minCol, maxCol+1):

            # Get a list of col
            if row == maxRow:
                # Don't have to check previous col in first col
                if gardenMap[row,col] == plant and (row,col) in plantGroup:
                    matchList.append(col)
            else:
                # Make this this is a first time plant match
                if gardenMap[row,col] == plant and (row,col) in plantGroup and gardenMap[row+1,col] != plant:
                    matchList.append(col)

        # Figure out how many groups we have in the match list
        side = getGroups(matchList)
        kprint("side: ",side)
        sides = sides + side

    return sides

costTotal = 0
for plant in plants:

    kprint(plant)
    # Create a dictionary of visited nodes for this plant
    visited = {}

    # Get the locations of these plants
    plantLocations = np.where(gardenMap == plant)

    locationTuples = list()
    # Convert locations to list of tuples
    for index in range(0, len(plantLocations[0])):
        location = (int(plantLocations[0][index]), int(plantLocations[1][index]))
        locationTuples.append(location)

    plantLocations = locationTuples
    kprint(plantLocations)

    # Iterate through all locations
    for plantLocation in plantLocations:

        # If this location has already been visited
        if plantLocation in visited:
            continue

        # Perform search for this item
        plantGroup = plantSearch(plantLocation)
        kprint("plantGroup: ",plantGroup)

        # Add to the visited list
        visited = addPlants(visited, plantGroup)

        # Get the area and perimeter
        area = len(plantGroup)
        cost = 0
        if args.part2:
            sides = getSides(plantGroup)
            kprint("sides: ", sides)
            kprint("area : ", area)
            cost = area * sides
        else:
            perimiter = getPerimeter(plantGroup)
            cost = area * perimiter


        costTotal = costTotal + cost

print(costTotal)

# 852334, too high
# 841934
