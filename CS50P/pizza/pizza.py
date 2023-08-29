import sys
import csv
from tabulate import tabulate

if len(sys.argv) != 2:
    sys.exit("Too few command-line arguments") if len(sys.argv) < 2 else sys.exit("Too many command-line arguments")

if sys.argv[1].rsplit(".", 1)[1] != "csv":
    sys.exit("Not a CSV file")

try:
    file = open(sys.argv[1])
    file.close()
except FileNotFoundError:
    sys.exit("File does not exist")

menu = []

with open(sys.argv[1]) as file:
    reader = csv.reader(file)
    for row in reader:
        menu.append(row)


print(tabulate(menu,headers="firstrow", tablefmt="grid"))