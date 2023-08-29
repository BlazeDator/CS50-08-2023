vowels = ["a", "e", "i", "o", "u"]

text = input("input: ")
newtext = ""

for i in text:
    if i.lower() in vowels:
        continue
    newtext += i

print(newtext)