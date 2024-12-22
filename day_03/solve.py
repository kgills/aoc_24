import csv
import argparse
import re

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


def getSum(inputString):
    sumPairs = 0

    kprint(inputString)

    # Split on "mul(", skip the first element
    for item in inputString.split("mul(")[1:]:
        # kprint(item)

        # \d{1,3},\d{1,3}\)
        match = re.match(r'\d{1,3},\d{1,3}\)', item)
        if(match):

            # Remove the ")"
            pair = match.group(0)[:-1]
            kprint(pair)

            leftOp = int(pair.split(",")[0])
            rightOp = int(pair.split(",")[1])

            sumPairs = sumPairs + leftOp*rightOp
    return(sumPairs)

# Open the input file
textFile = open(args.input, "r")
inputString = textFile.read()

kprint("inputString: ",inputString)
kprint()

sumPairs = 0

if(args.part2):
    
    # Find the first "don't", mul is enabled to begin with
    endIndex = inputString.index("don't()")

    # Get the sum for the first section
    sumPairs = sumPairs + getSum(inputString[:endIndex])

    # Seek to the end index
    inputString = inputString[endIndex:]


    while(inputString != None):

        try:
            # Seek to the start index
            startIndex = inputString.index("do()")
        except ValueError:
            # "do" not found
            break

        inputString = inputString[startIndex:]

        try:
            endIndex = inputString.index("don't()")
        except ValueError:
            # "don't" isn't found
            endIndex = len(inputString)


        # Add the sumPairs
        sumPairs = sumPairs + getSum(inputString[:endIndex])

        # Seek to the end index
        inputString = inputString[endIndex:]

else:
    sumPairs = getSum(inputString)

print(sumPairs)
