import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    if s := re.findall(r"\bum\b", s, re.IGNORECASE):
        # print(s)
        return len(s)
    else:
        return 0


if __name__ == "__main__":
    main()