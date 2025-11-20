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
def send_message(seller: str = Form(...),
                 sender: str = Form(...), message: str = Form(...)):
    buyer = get_current_user()

    messages.insert_one({
        "buyer": buyer,
        "seller": seller,
        "sender": sender,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    return RedirectResponse(f"/chat/{seller}", status_code=303)
