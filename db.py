from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")

db = client["music_recognition"] #db name ->music_recognition
songs_col = db["songs"] #collection name -> songs

def load_all_songs_and_fp(): 
    return list(songs_col.find({}, {
        "_id" : 0, 
        "song_name" : 1, 
        "fingerprint": 1
    })) # returns the list of dicts of song_names & fps

if __name__ == "__main__":

    songs = load_all_songs_and_fp()

    for song in songs: 
        print(song["song_name"], end="\n")
        print(song["fingerprint"][:10])