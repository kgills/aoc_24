import csv
import argparse

parser = argparse.ArgumentParser(
                    prog='solve',
                    description='Solve AOC')

parser.add_argument('input', help="Input CSV file.")
parser.add_argument('-p2','--part2', help="Sove for part 2.", action='store_true')

args = parser.parse_args()
print(args)

def safe (row):

    # print(row)

    safe = True

    # Convert row to int
    row = [int(item) for item in row]

    # Determine the direction
    # 0: uninit
    # -1: down
    #  1: up
    direction = 0
    index = 0
    for level in row[:-1]:
        nextLevel = row[index+1]
        index = index+1

        if(level == nextLevel):
            direction = 0
            break
        elif(level > nextLevel):
            direction = -1
            break
        else:
            direction = 1
            break

    # print(direction)

    # Determine if the row is safe
    index = 0
    for level in row[:-1]:
        nextLevel = row[index+1]
        index = index+1

        if(level == nextLevel):
            safe = False

        if(direction == 1):
            if(nextLevel > level+3):
                safe = False
            if(nextLevel < level):
                safe = False

        else:
            if(nextLevel < level-3):
                safe = False
            if(nextLevel > level):
                safe = False

    # print(safe)

    return(safe)



with open(args.input) as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    safeCount = 0
    for row in spamreader:
        if(safe(row)):
            safeCount = safeCount+1
        elif(args.part2):
            # Remove single element from row, determine if it works
            for index in range(len(row)):

                tempRow = list(row)
                del tempRow[index]

                if(safe(tempRow)):
                    safeCount = safeCount+1
                    break

            
    print(safeCount)
        

 
