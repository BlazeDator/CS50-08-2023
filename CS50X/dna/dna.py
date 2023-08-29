import csv
import sys
import re


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py file.csv dna.txt")

    # Read database file into a list/dictionary
    dnadb = []

    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            dnadb.append(row)  # This will save a dictionary in each list

    # Read DNA sequence file into a variable
    dna = ""
    with open(sys.argv[2]) as file:
        reader = csv.reader(file)
        for row in reader:
            dna = row

    # Find longest match of each STR in DNA sequence
    strs = {}

    for i in re.findall("[A-Z]*[A-Z]", str(dnadb[0].keys())):
        strs[i] = 0  # Store in a list all the short tandem repeats to use later

    for key in strs:
        strs[key] = longest_match(str(dna), key)  # Save in each str the longest matches found

    # Check database for matching profiles
    keys = len(strs)  # Save how many keys we need to have to be the right person
    counter = 0  # count how many keys the person has, if equal to keys variable, it's that person
    for i in range(len(dnadb)):  # Go trough every dict inside the list dnadb
        for key in strs:  # Go trough every key value in strs for each person in dnadb
            if int(dnadb[i][key]) == int(strs[key]):  # if any value matches count it
                counter += 1
        if counter == keys:  # if every value matched it's this person
            print(dnadb[i]["name"])
            return
        else:  # if not start counting again for next person
            counter = 0

    print("No match")  # if no one matched, it's no one

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
