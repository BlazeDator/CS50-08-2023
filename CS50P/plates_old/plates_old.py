def main():
    plate = input("Plate: ").strip()
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    first_num = False

    if check_length(s) and s.isalnum() and check_first_two(s):
        for i in s:
            if not first_num and i.isdigit() and i != "0":
                first_num = True
            elif not first_num and i.isdigit() and i == "0":
                return False
            elif first_num and i.isalpha():
                return False
        return True

    return False

def check_length(s):
    return 2 <= len(s) <= 6

def check_first_two(s):
    return s[0].isalpha() and s[1].isalpha()

main()