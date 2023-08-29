import sys

if len(sys.argv) != 2:
    sys.exit("Too few command-line arguments") if len(sys.argv) < 2 else sys.exit("Too many command-line arguments")

if sys.argv[1].rsplit(".", 1)[1] != "py":
    sys.exit("Not a Python file")


try:
    file = open(sys.argv[1])
    file.close()
except FileNotFoundError:
    sys.exit("File does not exist")
    

counter = 0

with open(sys.argv[1]) as file:
    for line in file:
        if line.strip() == "" or line.lstrip()[0] == "#":
            pass
        else:
            counter +=1

print(f"Lines of code: {counter}")
