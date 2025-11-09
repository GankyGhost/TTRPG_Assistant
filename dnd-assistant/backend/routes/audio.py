# Freesound is the library of sounds we will pull from
import freesound
import bson
import base64
from bson.binary import Binary
import vlc
import time
from fastapi import APIRouter
import requests
import os
import db

client = freesound.FreesoundClient()
client.set_token("eKPAn2CykoHlEAJH7XZgE66fUinbP70Ns4Nn5yE3","token")

def search(word):
    candidates = client.text_search(query=word, page_size="10", fields="id,name,previews,url")
    return candidates

def prev_up(snd):
    nombres = []
    for n in db.audio_previews.find():
        nombres.append(n["name"])
    if snd.name not in nombres:
        snd.retrieve_preview(".", snd.name+".mp3")
        with open(snd.name+".mp3", "rb") as f:
            encoded = Binary(f.read())
        data = {"name": snd.name, "file": encoded}
        db.upload_preview(data)
        os.remove(snd.name+".mp3")

def button_up(snd):
    snd.retrieve_preview(".", snd.name+".mp3")
    with open(snd.name+".mp3", "rb") as f:
        encoded = Binary(f.read())
    data = {"name": snd.name, "file": encoded}
    db.upload_button(data)
    os.remove(snd.name+".mp3")

def play_preview(snd_name):
    db.retrieve_mp3(snd_name)
    speaker = vlc.Instance()
    noise = speaker.media_player_new("dnd-assistant/sounds/"+snd_name+".mp3")
    # noise = vlc.MediaPlayer(snd_name+".mp3")
    noise.play()
    noise.audio_set_volume(100)
    time.sleep(0.2)
    while noise.is_playing():
        time.sleep(0.5)

def delete_preview(snd):
    db.audio_previews.delete_one({"name": snd.name})
    os.remove("dnd-assistant/sounds/"+snd.name+".mp3")

def delete_button(snd):
    db.audio_buttons.delete_one({"name": snd.name})



router = APIRouter()

FREESOUND_API_KEY = "eKPAn2CykoHlEAJH7XZgE66fUinbP70Ns4Nn5yE3"  # Get from freesound.org

# # @router.get("/search")
# def search_audio(query: str):
#     url = f"https://freesound.org/apiv2/search/text/"
#     params = {
#         "query": query,
#         "token": FREESOUND_API_KEY,
#         "fields": "id,name,previews,url"
#     }
#     response = requests.get(url, params=params)
#     return response.json()

# # @router.post("/save-button")
# def save_audio_button(label: str, audio_url: str):
#     button = {
#         "label": label,
#         "audio_url": audio_url,
#         "loop": False,
#         "volume": 1.0
#     }
#     result = db.upload_button(button)
#     return {"message": "success"}

# # @router.get("/buttons")
# def get_audio_buttons():
#     buttons = list(db.audio_buttons.find())
#     for button in buttons:
#         button['_id'] = str(button['_id'])
#     return {"buttons": buttons}

# # @router.delete("/buttons/{button_id}")
# def delete_button(button_id: str):
#     from bson import ObjectId
#     db.audio_buttons.delete_one({"_id": ObjectId(button_id)})
#     return {"message": "success"}

def main():

    # results = search_audio("siren")
    my_results = search("fire breath")

    for sound in my_results:
        
        print(sound.name)
        print(sound.previews)
        button_up(sound)
        
        # prev_up(sound)
        # play_preview(sound.name)

        # delete_preview(sound)
        
        # save_audio_button(sound.name, sound.url)

if __name__ == "__main__":

    main()
    print("ok")