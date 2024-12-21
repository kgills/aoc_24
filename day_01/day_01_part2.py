import csv
import argparse

parser = argparse.ArgumentParser(
                    prog='day_01_part2',
                    description='Solve AOC Day 01, Part 2')

parser.add_argument('input', help="Input CSV file.")

args = parser.parse_args()
print(args.input)

list0 = []
list1 = []
with open(args.input) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
    	list0.append(int(row[0].strip()))
    	list1.append(int(row[3].strip()))

list0.sort()
list1.sort()

sim = 0
for item0 in list0:
	sim = sim + item0 * list1.count(item0)

print("sim = ",sim) 
