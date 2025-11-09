import pymongo
from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["authentication"]
collection = db["items"]

router  = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/buy_items", response_class=HTMLResponse)
def get_items(request: Request):
    items = list(collection.find())
    return templates.TemplateResponse("buy_items.html", {"request": request, "items": items})

def formatItem(doc):
    name = doc.get("name", "")
    program = doc.get("program", "")
    semester = doc.get("semester", "")
    item_name = doc.get("item_name", "")
    item_discription = doc.get("item_discription", "")
    price = doc.get("price", "")
    link = doc.get("link", "")
    return f"Seller: {name} | Program: {program} | Semester: {semester}\nItem: {item_name} | Price: {price}\nDesc: {item_discription}\nLink: {link}"

def printItems(docs):
    if not docs:
        print("No items found.")
        return
    for doc in docs:
        print("-" * 40)
        print(formatItem(doc))
    print("-" * 40)

def showAll(query):
    docs = list(collection.find(query))
    if not docs:
        print("No items found.")
        return
    printItems(docs)

def listItems():
    showAll({})

def searchItems():
    q_name = input("Search by item name: ").strip()
    query = {}
    if q_name:
        query["item_name"] = {"$regex": q_name, "$options": "i"}
    showAll(query)

def browse():
    while True:
        print("1) List all items")
        print("2) Search items")
        print("3) Quit")
        choice = input("> ").strip()
        if choice == "1":
            listItems()
        elif choice == "2":
            searchItems()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    browse()
 