glist = {}

while True:
    try:
        item = input().strip().upper()
    except EOFError:
        print()
        break
    else:
        if item in glist:
            glist[item] += 1
        else:
            glist[item] = 1

gl = list(glist)
gl.sort()

for i in gl:
    print(glist[i], i)