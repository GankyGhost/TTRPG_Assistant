import pymongo
import base64
from fastapi import APIRouter

router = APIRouter()

dnd_client = pymongo.MongoClient("mongodb+srv://mrnagrat_db_user:blueFUHSHUHd00d@dndatabase.hduyis6.mongodb.net/?appName=dndatabase")


dnd_database = dnd_client["dndatabase"]

audio_buttons = dnd_database["audio"]

audio_previews = dnd_database["audio_previews"]

def upload_preview(fill_dict):
    audio_previews.insert_one(fill_dict)

def upload_button(fill_dict):
    audio_buttons.insert_one(fill_dict)

def retrieve_mp3(q_name):
    free = audio_previews.find_one({"name": q_name})
    with open("dnd-assistant/sounds/"+q_name+".mp3", "wb") as f:
        f.write(free["file"])

@router.get("/audio")
def get_buttons():
    return audio_buttons.find()


# free = audio_previews.find_one({"name": "Ipa_MeowVoice_25_C5.wav"})
# with open(free["name"]+".mp3", "wb") as f:
#     f.write(free["file"])
# print(free["file"])
# print(free["file"].decode('utf-8'))
# print(free["file"])
# for e in free:
#     print(e)
# nice_dict = {}
# play_preview(nice_dict)