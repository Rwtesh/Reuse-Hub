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

@router.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, buyer: str, seller: str):
    convo = list(messages.find({
        "$or": [
            {"buyer": buyer, "seller": seller},
            {"buyer": seller, "seller": buyer}
        ]
    }).sort("timestamp", 1))
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "buyer": buyer,
        "seller": seller,
        "messages": convo
    })

@router.post("/send")
def send_message(buyer: str = Form(...), seller: str = Form(...),
                 sender: str = Form(...), message: str = Form(...)):
    messages.insert_one({
        "buyer": buyer,
        "seller": seller,
        "sender": sender,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })
    return RedirectResponse(
        f"/chat?buyer={buyer}&seller={seller}", status_code=303
    )
