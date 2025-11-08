# imports fastapi and pymongo
from fastapi import APIRouter
import pymongo

router = APIRouter()
client = pymongo.MongoClient("mongodb+srv://mrnagrat_db_user:blueFUHSHUHd00d@dndatabase.hduyis6.mongodb.net/""?retryWrites=true&w=majority&tls=true")
db = client["dndatabase"]
collection = db["statblocks"]

@router.post("/statblock")
def create_statblock(statblock: dict):
    result = collection.insert_one(statblock)
    return {"inserted_id": str(result.inserted_id)}

def ability_modifier(score) -> int:
   
    if not isinstance(score, int):
        raise TypeError("Score must be an integer.")
    if score < 1 or score > 30:
        raise ValueError("Score must be between 1 and 30.")
    
    return ((score - 10) // 2)
    
    
"""""if __name__ == "__main__":

    data = {
        "name": "Test Dragon",
        "size": "Huge",
        "creature_type": "Dragon",
        "ac": 19,
        "hp": 230,
        "speed": "40 ft., fly 80 ft.",
        "abilities": {"STR": 23, "DEX": 10, "CON": 21, "INT": 14, "WIS": 11, "CHA": 19},
        "skills": ["Stealth +6"],
        "senses": ["Eyesight"],
        "languages": ["Draconic"],
        "challenge_rating": 17,
        "proficiency_bonus": 6,
        "traits": ["Sixth Sense"],
        "actions": ['Fire Breath 10d10']
    }

    print(data)
    result = collection.insert_one(data)
    print(f"✅ Uploaded with id {result.inserted_id}")"""""
