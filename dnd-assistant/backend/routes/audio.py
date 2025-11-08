# Freesound is the library of sounds we will pull from
import freesound

client = freesound.FreesoundClient()
client.set_token("eKPAn2CykoHlEAJH7XZgE66fUinbP70Ns4Nn5yE3","token")

results = client.text_search(query="Rattlesnake",page_size="30",fields="id,name,previews,url")

print(results.count)
# length = 0

for sound in results:
    # sound.retrieve_preview(".",sound.name+".mp3")
    print(sound.name)
    print(sound.url)
    # length += 1

# print(length)

for sound in results[0].get_similar(fields="id,name,previews,url"):
    print(sound.name)
    print(sound.url)