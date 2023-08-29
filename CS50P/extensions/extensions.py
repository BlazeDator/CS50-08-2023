file = input("Filename: ").strip().lower()

if "." in file:
    match file.split(".")[-1]:
        case "gif" | "png":
            print("image/" + file.split(".")[-1])
        case "jpg" | "jpeg" :
            print("image/jpeg")
        case "txt":
            print("text/plain")
        case "pdf":
            print("application/pdf")
        case "zip":
            print("application/zip")
        case _:
            print("application/octet-stream")
else:
    print("application/octet-stream")