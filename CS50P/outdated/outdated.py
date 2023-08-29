months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

# 9/8/1636 or September 8, 1636
def main():
    day, month, year = getdate()
    if month.isnumeric():
        print(f"{year}-{int(month):02}-{int(day):02}")
    else:
        print(f"{year}-{months.index(month)+1:02}-{int(day):02}")



def getdate():
    d = list()
    while True:
        date = input("Date: ").strip()
        if date.count("/") == 2:
            if not date.split("/")[0].isnumeric():
                pass
            else:
                d.append(date.split("/")[1])
                d.append(date.split("/")[0])
                d.append(date.split("/")[2])
        elif date.count(" ") == 2:
            if date.find(",")  < 1:
                pass
            else:
                d.append(date.split(" ")[1].split(",")[0])
                d.append(date.split(" ")[0].lower().title())
                d.append(date.split(" ")[2])
        if len(d) == 3 and checkdate(d):
            break
        else:
            d.clear()
    return d

def checkdate(d):
    day, month, year = d

    if not month.isnumeric():
        if month not in months:
            return False
    else: # Check Numeric Month
        try:
            month = int(month)
        except ValueError:
            return False
        else:
            if month <= 0 or month > 12:
                return False
    try:
        day = int(day)
        year = int(year)
    except ValueError:
        return False

    if day <= 0 or day > 31:
        return False
    if 0 > year:
        return False

    return True

main()