import pymongo
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import re

# app = FastAPI()
router = APIRouter()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@router.get("/sign_in", response_class=HTMLResponse)
def signin_page(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["authentication"]   
collection = db["users"]

@router.post("/sign_in", response_class=HTMLResponse)
def signin_submit(request: Request, user_name: str = Form(...), user_password: str = Form(...)):

    pattern = r'^\d+@geu\.ac\.in$'
    if not re.match(pattern, user_name):
        return templates.TemplateResponse("sign_in.html", {"request": request, "message": "invalid user name"})
    else:
        exist = collection.find_one({"user_name": user_name})
        if not exist:
            return templates.TemplateResponse("sign_in.html", {"request": request, "message": "User Name not Found"})


    if not collection.find_one({"user_name":  user_name, "password": user_password }):
        return templates.TemplateResponse("sign_in.html", {"request": request, "message": "Wrong Password"})
    
    with open("currentuser.txt","w") as curr:
        curr.write(user_name)
    return RedirectResponse(url="/sell_items", status_code=303)
