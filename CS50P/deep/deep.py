txt = input("The answer to the Great Question of Life, the Universe and Everything ? ")

match txt.strip().lower():
    case "42" | "forty-two" | "forty two":
        print("Yes")
    case _:
        print("No")