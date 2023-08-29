from validator_collection import validators

try:
    email = validators.email(input("What's your email address  ?"))
except ValueError:
    print("Invalid")
else:
    print("Valid")