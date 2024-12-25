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

disk = textFile.read()
disk = list(map(int, disk))
kprint(disk)

# Get the file sizes, the even indices
fileSizes= disk[::2]
fileSizes = list(fileSizes)
kprint("fileSizes")
kprint(fileSizes)

# Get the free spaces
freeSpaces = disk[1::2]
freeSpaces = list(freeSpaces)
kprint("free")
kprint(freeSpaces)

# Create a list of ids
ids =  list()
for i in range(0,len(fileSizes)):
    ids.append(i)

kprint("ids")
kprint(ids)

# Build the data structure
# id, size, freeSpace to right
fileSystem = list()

# Position of each field in the file system list
FILE_ID = 0
FILE_SIZE = 1
FILE_FREE = 2

for sizeIndex in range(0, len(fileSizes)):
    size = fileSizes[sizeIndex]
    fileId = sizeIndex
    freeSpace = 0

    if(sizeIndex != len(fileSizes)-1):
        freeSpace = freeSpaces[sizeIndex]

    fileSystem.append([fileId, size, freeSpace])

kprint("fileSystem")
kprint(fileSystem)

print("files: ",len(fileSystem))

# Start from the end of the file system
fileId = len(fileSystem)-1
while fileId > 0:

    inputIndex = 0

    # Find the index of the fileId, start from the rear
    fileIndex = len(fileSystem) - 1
    while(fileSystem[fileIndex][FILE_ID] != fileId):
        fileIndex = fileIndex - 1

    fileId = fileId - 1

    # Search for a space that can hold this file
    while(inputIndex < fileIndex):
        if(fileSystem[inputIndex][FILE_FREE] >= fileSystem[fileIndex][FILE_SIZE]):
            # Insert a new file to the right
            newId = fileSystem[fileIndex][FILE_ID]
            newSize = fileSystem[fileIndex][FILE_SIZE]
            newFree = fileSystem[inputIndex][FILE_FREE]-newSize
            fileSystem.insert(inputIndex+1, [newId, newSize, newFree])

            # Clear out the free space from the input file index
            fileSystem[inputIndex][FILE_FREE] = 0

            # Advance the file indices
            fileIndex = fileIndex + 1

            if(fileIndex-1 != inputIndex):
                # Add free space to the previous
                fileSystem[fileIndex-1][FILE_FREE] = fileSystem[fileIndex-1][FILE_FREE] + fileSystem[fileIndex][FILE_SIZE] + fileSystem[fileIndex][FILE_FREE]

            # Remove the moved file
            del fileSystem[fileIndex]
            fileIndex = fileIndex - 1

            # Subtract one more if we 

            kprint(fileSystem)
            break

        # Advance the input index
        inputIndex = inputIndex + 1

    # Advance the fileIndex
    fileIndex = fileIndex - 1

# kprint(fileSystem)

# Calculate the checksum
fileIndex = 0
blockIndex = 0
checksum = 0
fileLen = 0

print("files: ",len(fileSystem))

while fileIndex < len(fileSystem):
    checksum = checksum + blockIndex * fileSystem[fileIndex][FILE_ID]

    blockIndex = blockIndex + 1
    fileLen = fileLen + 1

    if(fileLen == fileSystem[fileIndex][FILE_SIZE]):
        fileLen = 0
        blockIndex = blockIndex + fileSystem[fileIndex][FILE_FREE]
        fileIndex = fileIndex + 1

print(checksum)

# Namespace(input='input.txt', part2=False, verbose=False)
# 9859946348838 too high
# 9859946524209 too high
# 9859946348838
# 6448168620520

