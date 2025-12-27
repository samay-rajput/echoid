from pymongo import MongoClient

#created a client which connects to the mongo server.!

client = MongoClient("mongodb://localhost:27017")


db = client["music_recognition"]
songs = db["songs"] # a collection named as song: in client db

doc = {
    "song_name" : "Lafangey Parindey", 
    "duration" : 207, 
    "fingerprint" : "hdhaahhd_dummy_fp"

}

output = songs.insert_one(doc)

print("inserted id: ", output.inserted_id)
delo = songs.delete_many({"song_name": "Lafangey Parindey"})
print("\nAll documents:")
for song in songs.find():
    print(song)

print(delo.deleted_count)


