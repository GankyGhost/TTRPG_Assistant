from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

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

# Importing routes
from routes import audio, dice, notes, statblocks 
#name your backend files as so, referred to as endpoint, so .e.g. emelia's dice.py is the dice endpoint

app.include_router(audio.router, prefix="/api/audio")
app.include_router(dice.router, prefix="/api/dice")
app.include_router(notes.router, prefix="/api/notes")
app.include_router(statblocks.router, prefix="/api/statblocks")

@app.get("/")
def root():
    return {"message": "D&D Assistant API"}

# Run with: cd backend, followed by uvicorn main:app --reload