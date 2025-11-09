from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pymongo import MongoClient
import os

from .routes import dice, statblock
# Importing routes
 #notes, audio


app = FastAPI()

# CORS (cross origin resource sharing), so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['dnd_assistant']

# app.include_router(audio.router, prefix="/api/audio")
app.include_router(dice.router, prefix="/api/dice")
# app.include_router(notes.router, prefix="/api/notes")
app.include_router(statblock.router, prefix="/api/statblock")

app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.mount("/img", StaticFiles(directory="frontend/img"), name="img")


# Override the default root route to serve index.html
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("frontend/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

# Run with: cd backend, followed by uvicorn main:app --reload