import sys
import random
from pyfiglet import Figlet

figlet = Figlet()

fonts = figlet.getFonts()

if len(sys.argv) == 1:
    figlet.setFont(font=fonts[random.randint(0, len(fonts)-1)])
elif len(sys.argv) != 3:
    sys.exit("Invalid usage")
elif sys.argv[1] != "-f" and sys.argv[1] != "--font":
    sys.exit("Invalid usage")
elif sys.argv[2] not in fonts:
    sys.exit("Invalid usage")
else:
    figlet.setFont(font=sys.argv[2])

text = input()

print(figlet.renderText(text))