price = 50
allowed = [25, 10, 5]

while price > 0:
    money = int(input("Amount due: " + str(price) + "\n"))
    if money in allowed:
        if money >= price:
            print("Change owed: ", money - price)
        price -= money

