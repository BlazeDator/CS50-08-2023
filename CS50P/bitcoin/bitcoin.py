import requests
import sys
import json

if len(sys.argv) != 2:
    sys.exit("Missing command-line argument")
else:
    try:
        bitcoins = float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line argument is not a number")

try:
    r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
except requests.RequestException:
    sys.exit("Request Exception")

# print(json.dumps(r.json(), indent=2))

f = r.json()["bpi"]["USD"]["rate"]

price = float(f.replace(",", ""))

amount = bitcoins * price

print(f"${amount:,.4f}")