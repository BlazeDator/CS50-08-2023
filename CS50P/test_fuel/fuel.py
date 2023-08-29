def main():
    fraction = input("What's the fuel fraction ?")
    fraction = convert(fraction)
    fraction = gauge(fraction)
    print(fraction)

def convert(fraction):
    try:
        x = int(fraction.split("/")[0])
        y = int(fraction.split("/")[1])
        fraction = round(x / y, 2)
        if fraction > 1:
            raise ValueError
        elif fraction == 1:
            fraction = 100
        else:
            fraction = int(f"{fraction:.2f}".split(".")[1])
    except ValueError:
        raise ValueError
    except ZeroDivisionError:
        raise ZeroDivisionError
    else:
        return fraction

def gauge(percentage):
    if 99 <= percentage <= 100:
        return "F"
    elif 0 <= percentage <= 1:
        return "E"
    else:
        return str(percentage) + "%"

if __name__ == "__main__":
    main()