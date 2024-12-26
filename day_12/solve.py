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
        kprint(plantGroup)

        # Add to the visited list
        visited = addPlants(visited, plantGroup)

        # Get the area and perimeter
        area = len(plantGroup)
        perimiter = getPerimeter(plantGroup)

        cost = area * perimiter
        costTotal = costTotal + cost

print(costTotal)
