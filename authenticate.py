from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sign_in import router as sign_in_router
from sign_up import router as sign_up_router

app = FastAPI()

app.include_router(sign_in_router)
app.include_router(sign_up_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
