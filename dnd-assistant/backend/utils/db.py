import pymongo

dnd_client = pymongo.MongoClient("mongodb+srv://mrnagrat_db_user:blueFUHSHUHd00d@dndatabase.hduyis6.mongodb.net/?appName=dndatabase")


for d in dnd_client.list_databases():
    print(d)

dnd_database = dnd_client["dndatabase"]

for d in dnd_database.list_collections():
    print(d)

audio = dnd_database["audio"]

for f in audio.find():
    print(f)

# sample_sound = {"name": "Glass Shatters", "preview": "this link amirite"}

# audio.insert_one(sample_sound)