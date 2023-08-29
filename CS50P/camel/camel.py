variable = input("What's the variable ? ")
newvar = ""

for i in variable:
    if i.isupper():
        newvar += "_" + i.lower()
    else:
        newvar += i

print(newvar)