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

fileIndex = 0
lastFileIndex = len(fileSystem)-1
while fileIndex < len(fileSystem) and fileSystem[fileIndex][FILE_SIZE]:

    # See if we have any free space and need to insert a new file
    while fileSystem[fileIndex][FILE_FREE]:

        # Move block from the end file to here
        if fileSystem[fileIndex][FILE_ID] != fileSystem[lastFileIndex][FILE_ID]:

            # Insert a new file to the right, move the free space there, -1
            newId = fileSystem[lastFileIndex][FILE_ID]
            newSize = 1
            newFree = fileSystem[fileIndex][FILE_FREE]-1
            fileSystem.insert(fileIndex+1, [newId, newSize, newFree])

            # Clear out the free space on the current file
            fileSystem[fileIndex][FILE_FREE] = 0

            # Advance the file indices
            lastFileIndex = lastFileIndex + 1
            fileIndex = fileIndex + 1

            # Subtract one from the last file size
            fileSystem[lastFileIndex][FILE_SIZE] = fileSystem[lastFileIndex][FILE_SIZE] - 1

        else:
            # Move one from the last file, move it to the current file, subtract a free space
            fileSystem[fileIndex][FILE_SIZE] = fileSystem[fileIndex][FILE_SIZE] + 1
            fileSystem[fileIndex][FILE_FREE] = fileSystem[fileIndex][FILE_FREE] - 1
            fileSystem[lastFileIndex][FILE_SIZE] = fileSystem[lastFileIndex][FILE_SIZE] - 1

        if fileSystem[lastFileIndex][FILE_SIZE] == 0:
            # Remove last empty file
            del fileSystem[lastFileIndex]
            lastFileIndex = lastFileIndex - 1

    fileIndex = fileIndex+1

kprint(fileSystem)

fileIndex = 0
blockIndex = 0
checksum = 0
fileLen = 0
while fileIndex < len(fileSystem):
    checksum = checksum + blockIndex * fileSystem[fileIndex][FILE_ID]

    blockIndex = blockIndex + 1
    fileLen = fileLen + 1

    if(fileLen == fileSystem[fileIndex][FILE_SIZE]):
        fileLen = 0
        fileIndex = fileIndex + 1

print(checksum)

