# imports fastapi and pymongo
from fastapi import APIRouter
import pymongo
import base64

router = APIRouter()
client = pymongo.MongoClient("mongodb+srv://mrnagrat_db_user:blueFUHSHUHd00d@dndatabase.hduyis6.mongodb.net/""?retryWrites=true&w=majority&tls=true")
db = client["dndatabase"]
collection = db["statblocks"]

# helper function that stores the statblock dictionary into MongoDB
def store_statblock(statblock: dict):
    result = collection.insert_one(statblock)
    return {"inserted_id": str(result.inserted_id)}


# helper function that returns the modifier for any given score between 1-30
def ability_modifier(score) -> int:
   
    if not isinstance(score, int):
        raise TypeError("Score must be an integer")
    if score < 1 or score > 30:
        raise ValueError("Score must be between 1 and 30")
    
    return ((score - 10) // 2)


# helper function to determine proficient skill bonuses
def determine_bonus(skill:str, abilities:dict):
    # a dictionary with keys named after each ability with a list containing the respective skills
    skills_by_ability = {
    "STR": ["Athletics"],
    "DEX": ["Acrobatics", "Sleight of Hand", "Stealth"],
    "INT": ["Arcana", "History", "Investigation", "Nature", "Religion"],
    "WIS": ["Animal Handling", "Insight", "Medicine", "Perception", "Survival"],
    "CHA": ["Deception", "Intimidation", "Performance", "Persuasion"] }

    # determines which ability is tied to the skill
    used_ability = ''
    for ability, skill_list in skills_by_ability.items():
        if skill in skill_list:
           used_ability = ability
    
    return ability_modifier(abilities[used_ability])

# helper function to encode imnage into base64
def image_to_base64(path):
    with open(path, "rb") as image_file:      # read image in binary mode
        encoded_string = base64.b64encode(image_file.read())  # encode to base64
        return encoded_string.decode("utf-8") 


# helper function to decode image from base64
def base64_to_image(b64_string, output_path):   # read binary
    img_data = base64.b64decode(b64_string)  # decode from base64
    with open(output_path, "wb") as f:
        f.write(img_data)
    
    
# create statblock based on info from user input
@router.post("/statblock")
def create_statblock(stats: dict) -> None:
    # determines the proficency bonus based on creatures CR
    pb_table = [2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4,
    5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9] # this list is size 31 for each CR level that is possible i.e CR0-4 makes PB = 2

    stats['pb'] = pb_table[stats['cr']]

    # properly formats the strings containing the skills
    new_skills = [] # empty list that will hold the formatted skills that will replace the orignal skills element
    for skill in stats['skills']:
        bns = determine_bonus(skill, stats['abilities'])
        new_skills.append(f"{skill} +{bns + stats['pb']}")
    
    stats['skills'] = new_skills # replacing the orignal skills with new_skills

    # inputs base64 image
    stats['image'] = image_to_base64(stats['image_path'])

    store_statblock(stats)

    print("Statblock creation complete")


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
