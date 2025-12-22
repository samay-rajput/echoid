from fingerprint import extract_fingerprint
from matcher import sliding_window_match
from db import load_all_songs_and_fp
# client = MongoClient("mongodb://localhost:27017")

def recognize(query_audio):
    
    _, query_fp = extract_fingerprint(query_audio)

    best_song = None
    best_score = 0.0
    second_score = 0.0   # added second score for min_distance

    """
    known_songs = dict { song_name: path }

    --> for using songs from directory

    for name, path in known_songs.items():
        _, song_fp = extract_fingerprint(path)
        score = sliding_window_match(song_fp, query_fp)
    """
    
    #returns the list of dicts containing {name,fp}
    songs = load_all_songs_and_fp()

    for song in songs: 
        name = song["song_name"]
        fingerprint = song["fingerprint"]


        score = sliding_window_match(fingerprint, query_fp)
        print(f"{name}: {score:.3f}")

        if score > best_score:
            second_score = best_score   #second best score is stored
            best_score = score
            best_song = name
        elif score > second_score:      
            second_score = score

    # --- decision logic ---

    # threshold logic: 
    if best_score < 0.92:
        return None, best_score
    # if there is less difference then system is unsure
    if (best_score - second_score) < 0.03:  # diff of best and second_best score
        return None, best_score

    return best_song, best_score

if __name__ == "__main__":

    song, score = recognize("query/narmahatLaptop.m4a")

    print("\nMATCH:", song)
    print("CONFIDENCE:", score)