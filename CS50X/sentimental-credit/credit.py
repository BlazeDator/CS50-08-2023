import re


def main():
    ccnum = input("CC Number: ")  # Getting Card Number

    if len(ccnum) >= 13 and len(ccnum) <= 16:  # Check Card Number, if not within range, is invalid
        if check_cc(ccnum) == True:  # Check hash of number, if its True
            print(type_cc(ccnum))  # Determine if it's from a known Card provider and print it
        else:
            print("INVALID")
    else:
        print("INVALID")


def check_cc(num):
    checker = re.findall(".", num)  # This function saves all the characters inside num, into an "array" called checker
    length = len(num)  # Determine number's given length
    hash = 0  # Create a variable hash where we'll calculate the hash and determine if it's a valid card

    for i in range(length - 2, -1, -2):  # This range makes it loop between every other number starting on the second-to-last
        x = int(checker[i]) * 2  # start multiplying this numbers by 2
        if x > 9:  # if bigger then 10 separate them, since we need to add them
            tinycheck = re.findall(".", str(x))  # reusing findall to store those 2 numbers in an array
            hash += int(tinycheck[0]) + int(tinycheck[1])  # now add them to the hash separately
        else:
            hash += x  # otherwise, just add them to hash

    for i in range(length - 1, -1, -2):  # This range makes it loop between every other number starting on the last one
        hash += int(checker[i])  # Then add them

    tinycheck = re.findall(".", str(hash))  # reusing findall to separate the hash final value
    # print(hash), line used to testing, make sure hash was calculating correctly
    if int(tinycheck[1]) == 0:  # if final value's second number is 0, it's a valid card number
        return True
    else:
        return False


def type_cc(num):  # reusing findall, I check the first two numbers, and provide the appropriate brand,
    checker = re.findall(".", num)
    if int(checker[0]) == 4:
        return "VISA"
    elif int(checker[0]) == 5 and int(checker[1]) in {1, 2, 3, 4, 5}:
        return "MASTERCARD"
    elif int(checker[0]) == 3 and int(checker[1]) in {4, 7}:
        return "AMEX"
    else:  # if it didn't fall into any brand, it's invalid
        return "INVALID"


main()