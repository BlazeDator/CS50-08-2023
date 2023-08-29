from datetime import date
import re
import sys
import inflect

def main():
    bdate = get_date(input("Date of birth: "))
    minutes = get_minutes(bdate)
    p = inflect.engine()
    minutes = (p.number_to_words(minutes, andword="") + " minutes").capitalize()
    print(minutes)

def get_date(bdate):
    try:
        if re.search(r"^\d\d\d\d-\d\d-\d\d$", bdate):
            year, month, day = bdate.split("-")
            bdate = date(int(year),int(month),int(day))
    except:
        sys.exit("Invalid Date")
    else:
        return bdate


def get_minutes(bdate):
    today = date.today()
    try:
        delta = today - bdate
    except:
        sys.exit("Invalid Date")
    else:
        return delta.days * 24 * 60

if __name__ == "__main__":
    main()