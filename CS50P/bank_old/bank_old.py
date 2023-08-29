txt = input("Greeting: ").strip().lower()

if txt.startswith("hello"):
    print("$0")
elif txt.startswith("h"):
    print("$20")
else:
    print("$100")