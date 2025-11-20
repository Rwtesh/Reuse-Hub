
import pymongo
from fastapi import FastAPI, Request, Form
from fastapi import APIRouter
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

import re

router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.get("/sign_up", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["authentication"]   
collection = db["users"]

@router.post("/sign_up", response_class=HTMLResponse)
def signup_submit(request: Request, user_name: str = Form(...), user_password: str = Form(...),  comform_password: str = Form(...)):

    if " " in user_name:
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "User name cant have space"})
    pattern = r'^\d+@geu\.ac\.in$'
    if not re.match(pattern, user_name):
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "invalid user name"})
    else:
        exist = collection.find_one({"user_name": user_name})
        if exist:
            return templates.TemplateResponse("sign_up.html", {"request": request, "message": "user name already exist"})


    if " " in user_password:
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "password cannot be empty or space"})

    if not any(c.islower() for c in user_password):
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "password must have lowercase letter"})

    if not any(c.isupper() for c in user_password):
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "password must have uppercase letter"})

    if not any(c.isdigit() for c in user_password):
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "atleast one number"})

    if user_password != comform_password:
        return templates.TemplateResponse("sign_up.html", {"request": request, "message": "Password didn't Match"})
    
    collection.insert_one({
            "user_name": user_name,
            "password": user_password
        })

    with open("currentuser.txt","w") as curr:
        curr.write(user_name)
    
    return RedirectResponse(url="/sell_items", status_code=303)