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
equations = list()
lineIndex = 0
equation = list()

A_X = 0
A_Y = 1
B_X = 2
B_Y = 3
P_X = 4
P_Y = 5

for line in textFile:
    line = line.strip()

    if lineIndex % 4 == 0 or lineIndex % 4 == 1:
        equation.append(int(line.split("X+")[1][0:2].strip()))
        equation.append(int(line.split("Y+")[1][0:2].strip()))

    elif lineIndex % 4 == 3:
        pass

    elif lineIndex % 4 == 2:
        equation.append(int(line.split("X=")[1].split(",")[0].strip()))
        equation.append(int(line.split("Y=")[1].strip()))
        equations.append(equation)
        equation = list()

    lineIndex = lineIndex + 1

kprint(equations)

totalCost = 0

for equation in equations:

    a_x = equation[A_X]
    b_x = equation[B_X]
    p_x = equation[P_X]
    a_y = equation[A_Y]
    b_y = equation[B_Y]
    p_y = equation[P_Y]

    if args.part2:
        p_x = p_x + 10000000000000
        p_y = p_y + 10000000000000

    # See if we can solve with just A
    x_mult = p_x/a_x
    y_mult = p_y/a_y
    if math.floor(x_mult) == math.ceil(x_mult) and math.floor(y_mult) == math.ceil(y_mult) and x_mult == y_mult :
        kprint(equation)
        kprint("Can solve with just A")

    x_mult = p_x/b_x
    y_mult = p_y/b_y
    if math.floor(x_mult) == math.ceil(x_mult) and math.floor(y_mult) == math.ceil(y_mult) and x_mult == y_mult :
        kprint(equation)
        kprint("Can solve with just B")


    # See if we can solve with system of equation

    # b = X*Ay - Ax*Y
    #     /
    # Bx*Ay - Ax*By

    b = int(int(int(p_x*a_y) - int(a_x*p_y)) / int(int(b_x*a_y) - int(a_x*b_y)))
    # kprint("b: ", b)

    # a = Y/Ay - By/Ay
    a = int(p_y/a_y) - int(b_y * b / a_y)

    # kprint("a: ",a)
    # Cost = 3a + b

    # Make sure we didn't round converting to integer
    if(a*a_x + b*b_x == p_x and a*a_y + b*b_y == p_y):
        kprint("solved!")
        kprint("a: ", a)
        kprint("b: ", b)

        cost = 3*a + b

        totalCost = totalCost + cost

        # # Find the LCM of the pairs
        # lcm_x = math.lcm(a_x, b_x)
        # lcm_y = math.lcm(a_y, b_y)

        # kprint("lcm_x: ",lcm_x)
        # kprint("lcm_y: ",lcm_y)
        # kprint("p_x  : ", p_x)
        # kprint("p_y  : ", p_y)

print(totalCost)

