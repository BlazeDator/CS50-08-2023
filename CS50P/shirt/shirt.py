import sys
from PIL import Image,ImageOps

if len(sys.argv) != 3:
    sys.exit("Too few command-line arguments") if len(sys.argv) < 3 else sys.exit("Too many command-line arguments")

img_types = ["png", "jpeg", "jpg"]

if sys.argv[1].rsplit(".", 1)[1] not in img_types:
    sys.exit("Invalid input")
if sys.argv[2].rsplit(".", 1)[1] not in img_types:
    sys.exit("Invalid output")

if sys.argv[1].rsplit(".", 1)[1] != sys.argv[2].rsplit(".", 1)[1]:
    sys.exit("Input and output have different extensions")

try:
    file = open(sys.argv[1])
    file.close()
except FileNotFoundError:
    sys.exit("Input does not exist")


muppet = Image.open(sys.argv[1])
shirt = Image.open("shirt.png")

size = shirt.size
muppet = ImageOps.fit(muppet,size, bleed=0.0, centering=(0.5, 0.5))

muppet.paste(shirt, shirt)

muppet.save(sys.argv[2])