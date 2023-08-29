def main():
    time = input("What time is it? ").strip()
    time = convert(time)

    if 7 <= time <= 8:
        print("breakfast time")
    elif 12 <= time <= 13:
        print("lunch time")
    elif  18 <= time <= 19:
        print("dinner time")

def convert(time):
    if time.endswith("p.m."):
        time = time.split(" ")[0]
        h,m = time.split(":")
        h = int(h) + 12
    elif time.endswith("a.m."):
        time = time.split(" ")[0]
        h,m = time.split(":")
    else:
        h,m = time.split(":")

    time = float(h) + (float(m) / 60)
    return time

if __name__ == "__main__":
    main()