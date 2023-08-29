def main():
    text = input("input: ")
    print(shorten(text))


def shorten(word):
    vowels = ["a", "e", "i", "o", "u"]
    newtext = ""

    for i in word:
        if i.lower() in vowels:
            continue
        newtext += i

    return newtext


if __name__ == "__main__":
    main()