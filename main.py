from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sign_in import router as sign_in_router
from sign_up import router as sign_up_router
from notes import router as notes_r
from sell_item import router as sell_item_r
from chat import router as chat_r
from buy_items import router as buy_r
app = FastAPI()
from fastapi.responses import RedirectResponse

@app.get("/")
def root():
    return RedirectResponse(url="/sign_in")

app.include_router(sign_in_router)
app.include_router(sign_up_router)
app.include_router(sell_item_r)
app.include_router(notes_r)
app.include_router(chat_r)
app.include_router(buy_r)
app.mount("/static", StaticFiles(directory="static"), name="static")
