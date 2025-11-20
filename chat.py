from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

client = MongoClient("mongodb://localhost:27017/")
db = client["reuse_hub"]
messages = db["messages"]

def get_current_user():
    with open("currentuser.txt", "r") as f:
        return f.readline().strip()


@router.get("/chats", response_class=HTMLResponse)
def chat_list(request: Request):
    user = get_current_user()

    convo_cursor = messages.find({
        "$or": [
            {"buyer": user},
            {"seller": user}
        ]
    })

    partners = set()
    for msg in convo_cursor:
        if msg.get("buyer") == user and "seller" in msg:
            partners.add(msg["seller"])
        elif msg.get("seller") == user and "buyer" in msg:
            partners.add(msg["buyer"])

    partner_list = sorted(list(partners))

    return templates.TemplateResponse(
        "chat_list.html",
        {
            "request": request,
            "current_user": user,
            "partners": partner_list,
        },
    )

@router.get("/chat/{seller}", response_class=HTMLResponse)
def chat_page(request: Request, seller: str):
    buyer = get_current_user()

    convo = list(messages.find({
        "$or": [
            {"buyer": buyer, "seller": seller},
            {"buyer": seller, "seller": buyer}
        ]
    }).sort("timestamp", 1))

    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "buyer": buyer,
            "seller": seller,
            "messages": convo
        }
    )

@router.post("/send")
def send_message(seller: str = Form(...), message: str = Form(...)):
    current_user = get_current_user()

    existing = messages.find_one({
        "$or": [
            {"buyer": current_user, "seller": seller},
            {"buyer": seller, "seller": current_user},
        ]
    })

    if existing:
        buyer = existing["buyer"]
        seller_id = existing["seller"]
    else:
        buyer = current_user
        seller_id = seller

    messages.insert_one({
        "buyer": buyer,
        "seller": seller_id,
        "sender": current_user,
        "message": message,
        "timestamp": datetime.now().isoformat(),
    })

    return RedirectResponse(f"/chat/{seller}", status_code=303)
