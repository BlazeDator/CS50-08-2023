def main():
    while True:  # Getting height logic
        try:
            x = int(input("Height: "))
        except:
            x = 0
        if x > 0 and x < 9:
            break
    draw_pyramid(x)  # Call draw function


def draw_pyramid(height):
    blanks = height
    for i in range(height):

        for j in range(blanks - 1):  # Draw empty spaces equivalent to the rows left
            print(" ", end="")

        blanks -= 1  # Make sure next row as 1 less empty space

        for i in range(i + 1):  # Draw left side of pyramid
            print("#", end="")

        print("  ", end="")  # 2 Empty spaces between pyramid

        for i in range(i + 1):  # Draw right side of pyramid
            print("#", end="")

        print()  # New Line


main()