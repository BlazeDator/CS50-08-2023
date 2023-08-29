import inflect

p = inflect.engine()

names = []

while True:
    try:
        txt = input()
        names.append(txt)
    except EOFError:
        break

text = "Adieu, adieu, to "

names = p.join(names)

print(text + names)