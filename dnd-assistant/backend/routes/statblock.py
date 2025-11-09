from fastapi import APIRouter
from pydantic import BaseModel, Field
import pymongo
from bson.objectid import ObjectId
import base64
from typing import List, Optional

router = APIRouter()

client = pymongo.MongoClient("mongodb+srv://mrnagrat_db_user:blueFUHSHUHd00d@dndatabase.hduyis6.mongodb.net/""?retryWrites=true&w=majority&tls=true")
db = client["dndatabase"]
collection = db["statblocks"]

class StatblockData(BaseModel):
    name: str
    size: str
    creature_type: str = Field(default="Beast")
    ac: int
    hp: int
    speed: str
    abilities: dict # e.g., {"STR": 10, "DEX": 10, ...}
    skills: List[str] # e.g., ["Athletics", "Stealth"]
    senses: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    cr: int = Field(alias="challenge_rating") # Maps the frontend 'challenge_rating' field to 'cr' in Python
    traits: List[str] = Field(default_factory=list)
    actions: List[str]
    image_path: Optional[str] = None # Expecting a path or URL for image


# helper function that stores the statblock dictionary into MongoDB
def store_statblock(statblock: dict):
    result = collection.insert_one(statblock)
    return {"inserted_id": str(result.inserted_id)}


# helper function that returns the modifier for any given score between 1-30
def ability_modifier(score) -> int:
    if not isinstance(score, int):
        return 0
    if score < 1 or score > 30:
        return 0
    return ((score - 10) // 2)


# helper function to determine proficient skill bonuses

def determine_bonus(skill:str, abilities:dict):
    # Dictionary mapping skills to their respective abilities
    skills_by_ability = {
        "Athletics": "STR", 
        "Acrobatics": "DEX", "Sleight of Hand": "DEX", "Stealth": "DEX",
        "Arcana": "INT", "History": "INT", "Investigation": "INT", "Nature": "INT", "Religion": "INT",
        "Animal Handling": "WIS", "Insight": "WIS", "Medicine": "WIS", "Perception": "WIS", "Survival": "WIS",
        "Deception": "CHA", "Intimidation": "CHA", "Performance": "CHA", "Persuasion": "CHA"

    }

    # determines which ability is tied to the skill
    used_ability = skills_by_ability.get(skill.split()[0]) # Gets ability from skill name
    
    if used_ability in abilities:
        return ability_modifier(abilities[used_ability])
    return 0


# helper function to encode imnage into base64
# helper function to encode image into base64
def image_to_base64(path):
    # NOTE: This relies on the path being available locally on the server.
    if not path or not os.path.exists(path):
        return None 
    try:
        with open(path, "rb") as image_file:           # read image in binary mode
            encoded_string = base64.b64encode(image_file.read())   # encode to base64
            return encoded_string.decode("utf-8") 
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None
    


# # helper function to decode image from base64
# def base64_to_image(b64_string, output_path):   # read binary
#     img_data = base64.b64decode(b64_string)  # decode from base64
#     with open(output_path, "wb") as f:
#         f.write(img_data)
    
@router.post("/statblock", response_model=dict)
def create_statblock_api(stats: StatblockData):
    # Convert Pydantic model to dict for processing
    stats_dict = stats.model_dump(by_alias=True)
    
    # determines the proficency bonus based on creatures CR
    # CR is 0-30, list index needs to be 0-based
    pb_table = [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9] 
    
    # Ensure CR is within bounds [0, 30]
    cr_index = min(max(stats_dict['cr'], 0), 30)
    stats_dict['pb'] = pb_table[cr_index]

    # Process skills and add proficiency bonus (assuming input skills are just names, like 'Stealth')
    new_skills = [] 
    for skill in stats_dict['skills']:
        bns = determine_bonus(skill, stats_dict['abilities'])
        # Assumes input is just the skill name; result is formatted string
        new_skills.append(f"{skill} +{bns + stats_dict['pb']}")
    
    stats_dict['skills'] = new_skills 

    # inputs base64 image (Only works if stats_dict['image_path'] points to a local file on the server)
    # Since the frontend only sends text, we'll skip base64 for now unless you provide a simple way to upload files.
    # stats_dict['image'] = image_to_base64(stats_dict.get('image_path'))
    stats_dict['image_b64'] = "" # Placeholder

    return store_statblock(stats_dict)

# create statblock based on info from user input
@router.get("/statblock", response_model=List[dict])
def list_statblocks():
    """Returns a list of all statblocks, showing only essential information for the list view."""
    
    # Only fetch fields needed for the display list
    projection = {"name": 1, "ac": 1, "hp": 1, "size": 1, "creature_type": 1}
    blocks = list(collection.find({}, projection))
    
    # Convert MongoDB ObjectId to string for JSON serialization
    for block in blocks:
        block['_id'] = str(block['_id'])
        
    return blocks

@router.get("/statblock/{statblock_id}")
def get_statblock(statblock_id: str):
    """Retrieves a single, full statblock by its MongoDB ID."""
    
    # Attempt to find the document by its ObjectId
    block = collection.find_one({"_id": ObjectId(statblock_id)})
    
    if block:
        block['_id'] = str(block['_id'])
        return block
        
    # Standard 404 response
    return {"error": "Statblock not found"}


# test case   
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
