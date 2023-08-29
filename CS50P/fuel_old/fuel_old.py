while True:

    try:
        x = round(int(fraction.split("/")[0]) / int(fraction.split("/")[1]), 2)
    except ValueError:
        print("Not Integers")
    except ZeroDivisionError:
        print("Number 0 used")
    else:
        if 0.99 <= x <= 1:
            print("F")
        elif 0 <= x <= 0.01:
            print("E")
        elif x > 1 or x < 0:
            continue
        else:
            print(str(x).split(".")[1] + "%")
        break