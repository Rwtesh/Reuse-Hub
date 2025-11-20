import pymongo
from bson import ObjectId
from fastapi import FastAPI, Request, Form, APIRouter, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["authentication"]
collection = db["items"]
router = APIRouter()
templates = Jinja2Templates(directory="templates")

def get_current_user():
    with open("currentuser.txt", "r") as f:
        return f.readline().strip()
    

@router.get("/buy_items", response_class=HTMLResponse)
async def buy_items(request: Request):
    items = list(collection.find())
    for item in items:
        item["_id"] = str(item["_id"])
        item["is_sold"] = item.get("is_sold", False)
    return templates.TemplateResponse(
    "buy_items.html",
    {
        "request": request,
        "items": items,
        "buyer": get_current_user()
    }
)


@router.get("/item/{item_id}", response_class=HTMLResponse)
async def item_detail(request: Request, item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        return HTMLResponse("<h3>Item not found.</h3>", status_code=404)

    return templates.TemplateResponse("item_detail.html", {"request": request, "item": item})


# @router.get("/chat/{seller}", response_class=HTMLResponse)
# async def chat_page(request: Request, seller: str, buyer: str = Query(None)):
#     if buyer is None:
#         buyer = get_current_user()

#     return templates.TemplateResponse(
#         "chat.html",
#         {
#             "request": request,
#             "seller_name": seller,
#             "buyer": buyer
#         }
#     )


@router.get("/find", response_class=HTMLResponse)
def find(request: Request, query: str = ""):
    search_filter = {}
    if query:
        search_filter = {"$or": [
            {"item_name": {"$regex": query, "$options": "i"}},
            {"name": {"$regex": query, "$options": "i"}},
            {"name": {"$regex": query, "$options": "i"}}
        ]}

    items = list(collection.find(search_filter))
    for item in items:
        item["_id"] = str(item["_id"])
        item["is_sold"] = item.get("is_sold", False)

    return templates.TemplateResponse(
        "buy_items.html",
        {"request": request, "items": items, "search": query, "buyer": get_current_user()}
    )


@router.post("/items/{item_id}/mark_sold")
async def mark_item_sold(request: Request, item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        return HTMLResponse("<h3>Item not found.</h3>", status_code=404)

    if item.get("seller_id") != get_current_user():
        return HTMLResponse("<h3>Not authorized.</h3>", status_code=403)

    collection.update_one({"_id": ObjectId(item_id)}, {"$set": {"is_sold": True}})
    return RedirectResponse(url="/buy_items", status_code=303)


@router.post("/items/{item_id}/delete")
async def delete_item(request: Request, item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        return HTMLResponse("<h3>Item not found.</h3>", status_code=404)

    if item.get("seller_id") != get_current_user():
        return HTMLResponse("<h3>Not authorized.</h3>", status_code=403)

    if not item.get("is_sold"):
        return HTMLResponse("<h3>Item must be sold before deleting.</h3>", status_code=400)

    collection.delete_one({"_id": ObjectId(item_id)})
    return RedirectResponse(url="/buy_items", status_code=303)