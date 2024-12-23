import csv
import argparse
import re
import numpy as np
import sys
from collections import defaultdict
import math

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

# Create the rules lists
beforeRules = list()
afterRules = list()
updates = list()
for line in textFile:
    line = line.strip()
    
    if("|" in line):
        beforeRules.append(line.split("|")[0])
        afterRules.append(line.split("|")[1])
    elif ("," in line):
        updates.append(line.split(","))
        
kprint("beforeRuless:")
kprint(beforeRules)

kprint("afterRuless:")
kprint(afterRules)

kprint("updates:")
kprint(updates)

ruleDict = defaultdict(list)

for beforeIndex in range(0,len(beforeRules)):
    if(beforeRules[beforeIndex] in ruleDict):
        ruleDict[beforeRules[beforeIndex]].append(afterRules[beforeIndex])
    else:
        ruleDict[beforeRules[beforeIndex]] = [afterRules[beforeIndex]]

kprint(ruleDict)

def testOrder(update):
    correctOrder = True
    # Search the updates in reverse order
    for index in range(len(update)-1,-1,-1):
        # Make sure this update doesn't need to be printed before the previous pages
        for prev in range(index-1,-1,-1):
            if (update[prev] in ruleDict[update[index]]):
                correctOrder = False
                break

        if(not correctOrder):
            break

    return correctOrder

def insertPage(update, page):
    if(update == []):
        update.append(page)
        return update


    for index in range(0,len(update)+1):
        newUpdate = list(update)
        newUpdate.insert(index, page)
        if(testOrder(newUpdate)):
            return newUpdate

    print("Failed to add page", update, page)
    sys.exit(1)


updateSum = 0
for update in updates:
    correctOrder = testOrder(update)
    if args.part2:
        if not correctOrder:
            # put in the right order
            newUpdate = []

            for index in range(0,len(update)):
                newUpdate = insertPage(newUpdate,update[index])

            updateSum = updateSum + int(newUpdate[math.floor(len(newUpdate)/2)])
    else:
        if correctOrder:
            kprint(update)
            updateSum = updateSum + int(update[math.floor(len(update)/2)])

print(updateSum)


