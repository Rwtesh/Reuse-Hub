from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["notes_database"]
collection = db["notes_info"]

router  = APIRouter()
templates = Jinja2Templates(directory="templates")
@router.get("/notes", response_class=HTMLResponse)
def get_notes(request: Request):
    notes = list(collection.find())
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})

@router.post("/add_note")
def add_note(
    name: str = Form(...),
    semester: str = Form(...),
    branch: str = Form(...),
    subject: str = Form(...),
    chapter: str = Form(...),
    drive_link: str = Form(...)
):
    if not drive_link.startswith("https://drive"):
        print("Invalid Drive link!")
        return RedirectResponse(url="/notes", status_code=303)

    note_doc = {
        "name": name,
        "semester": semester,
        "branch": branch,
        "subject": subject,
        "chapter": chapter,
        "drive_link": drive_link
    }

    collection.insert_one(note_doc)
    return RedirectResponse(url="/notes", status_code=303)

@router.get("/find_note", response_class=HTMLResponse)
def find_note(request: Request, query: str = ""):
    search_filter = {
        "$or": [
            {"branch": {"$regex": query, "$options": "i"}},
            {"subject": {"$regex": query, "$options": "i"}},
            {"chapter": {"$regex": query, "$options": "i"}}
        ]
    }
    notes = list(collection.find(search_filter))
    return templates.TemplateResponse("notes.html", {"request": request, "notes": notes})
