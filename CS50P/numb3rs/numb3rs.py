import re
import sys


def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    ip = ip.strip()
    if ip := re.search(r"^((?:[1-2])?\d?\d)\.((?:[1-2])?\d?\d)\.((?:[1-2])?\d?\d)\.((?:[1-2])?\d?\d)$", ip):
        iptest = [int(ip.group(1)), int(ip.group(2)), int(ip.group(3)), int(ip.group(4))]
        for ip in iptest:
            if ip < 0 or ip > 255:
                return False
        return True
    return False


if __name__ == "__main__":
    main()