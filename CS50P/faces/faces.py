def main():
    text = input()
    print(convert(text))

def convert(txt):
    txt = txt.replace(":)", "🙂").replace(":(", "🙁")
    return txt

main()