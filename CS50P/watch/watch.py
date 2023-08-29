import re
import sys


def main():
    print(parse(input("HTML: ")))


def parse(s):
    if s := re.search(r"src=\".*youtube\.com/embed/+(\w+)", s):
        return "https://youtu.be/" + s.group(1)
    return None


if __name__ == "__main__":
    main()