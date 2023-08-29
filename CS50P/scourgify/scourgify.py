import sys
import csv

if len(sys.argv) != 3:
    sys.exit("Too few command-line arguments") if len(sys.argv) < 3 else sys.exit("Too many command-line arguments")

if sys.argv[1].rsplit(".", 1)[1] != "csv":
    sys.exit("Not a CSV file")

try:
    file = open(sys.argv[1])
    file.close()
except FileNotFoundError:
    sys.exit(f"Could not read {sys.argv[1]}")

students = []

with open(sys.argv[1]) as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append(row)

with open(sys.argv[2], "w") as file:
    writer = csv.DictWriter(file,  fieldnames=["first", "last", "house"])
    writer.writeheader()
    for row in students:
        writer.writerow({
            "first" : row["name"].split(",")[1].lstrip(),
            "last" : row["name"].split(",")[0],
            "house" : row["house"]
            })