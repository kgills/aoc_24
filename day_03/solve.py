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

# Open the input file
textFile = open(args.input, "r")
inputString = textFile.read()

kprint("inputString: ",inputString)

sumPairs = 0

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

print(sumPairs)


