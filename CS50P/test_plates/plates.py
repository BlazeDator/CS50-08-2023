def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    first_num = False

    if 2 <= len(s) <= 6 and s.isalnum() and s[0].isalpha() and s[1].isalpha():
        for i in s:
            if not first_num and i.isdigit() and i != "0":
                first_num = True
            elif not first_num and i.isdigit() and i == "0":
                return False
            elif first_num and i.isalpha():
                return False
        return True
    else:
        return False

if __name__ == "__main__":
    main()