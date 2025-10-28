import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["authentication"]   
collection = db["items"]

def add():
    name= input("Enter your name : ")
    program = input("Enter the program: ")
    semester = int(input("Enter your semester: "))
    item_name = input("Enter the name of item: ")
    item_discription =  input("enter the descripton: ")
    price = float(int("Enter the price: "))
    link = input("enter the image drive link: ")
    if not drive_link.startswith("http://drive"):
        print("Invalid link! Please paste a valid Google Drive link.")
        return
    else:
        note_doc = {
            "name": name,
            "semester": sem,
            "program": program,
            "item_name": item_name,
            "item_discription": item_discription,
            "price": price,
            "link": link
        }
    print("Item added successfully!")

    