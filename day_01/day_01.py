import csv
import argparse

parser = argparse.ArgumentParser(
                    prog='day_01',
                    description='Solve AOC Day 01')

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

index1 = 0
distance = 0
for item0 in list0:
	distance = distance + abs(item0 - list1[index1])
	index1 = index1 + 1

print("distance = ",distance) 
