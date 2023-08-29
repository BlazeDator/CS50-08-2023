import random

def main():
    score = 0
    level = get_level()


    for _ in range(10):
        x = generate_integer(level)
        y = generate_integer(level)
        tries = 0

        while True:
            if tries == 3:
                print(x, "+", y, "= ", x+y)
                break
            
            print(x, "+", y, "=", end=" ")

            try:
                answer = int(input())
            except ValueError:
                print("EEE")
                tries +=1
            else:
                if answer == x + y:
                    score += 1
                    break
                else:
                    tries += 1
                    print("EEE")


    print(score)

def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            pass
        else:
            return level

def generate_integer(level):
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(100, 999)

if __name__ == "__main__":
    main()