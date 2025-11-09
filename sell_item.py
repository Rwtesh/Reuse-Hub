import pymongo
from fastapi import FastAPI, Request, Form, APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["authentication"]   
collection = db["items"]

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/sell_items", response_class=HTMLResponse)
def signin_page(request: Request):
    return templates.TemplateResponse("sell_items.html", {"request": request})

@router.post("/add_item")

def add( 
    request: Request,
    name: str = Form(...),
    program: str = Form(...),
    semester: int = Form(...),
    item_name: str = Form(...),
    item_discription: str = Form(...),
    price: float = Form(...),
    link: str = Form(...),
         ):
    if semester <=0 and semester >= 9:
        message = "invalid semester"
        return templates.TemplateResponse(
        "sell_items.html",
        {"request": request, "message": message}
        )    
    if not link.startswith("https://drive"):
        message = "Invalid link! Please paste a valid Google Drive link."
        return templates.TemplateResponse(
        "sell_items.html",
        {"request": request, "message": message}
        )
    else:
        Items = {
            "name": name,
            "semester": semester,
            "program": program,
            "item_name": item_name,
            "item_discription": item_discription,
            "price": price,
            "link": link
        }
    collection.insert_one(Items)
    message = "Item added successfully to the market!"

    return templates.TemplateResponse(
        "sell_items.html",
        {"request": request, "message": message}
    )
