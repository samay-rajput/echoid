from fingerprint import extract_fingerprint
from matcher import sliding_window_match

def recognize(query_audio, known_songs):
    """
    known_songs = dict { song_name: path }
    """

    _, query_fp = extract_fingerprint(query_audio)

    best_song = None
    best_score = 0.0

    for name, path in known_songs.items():
        _, song_fp = extract_fingerprint(path)
        score = sliding_window_match(song_fp, query_fp)

        print(f"{name}: {score:.3f}")

        if score > best_score:
            best_score = score
            best_song = name

    return best_song, best_score


if __name__ == "__main__":
    known = {
        "Lafangey Parindey": "known_songs/Lafangey_Parindey.mp3",
        "Killa Klassic" : "known_songs/killa_klassic.mp3",
        "Narmahat Freestyle" : "known_songs/narmahat_freestyle.mp3"
    }

    song, score = recognize("query/concertKillaKlassic.mp3", known)

    print("\nMATCH:", song)
    print("CONFIDENCE:", score)

