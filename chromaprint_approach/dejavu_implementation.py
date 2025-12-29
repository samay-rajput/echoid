from dejavu import Dejavu
from dejavu.recognize import FileRecognizer

config = {
    "database": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "SamayMySql@1202",
        "database": "dejavu",
    },
    "database_type": "mysql",
}

def dejavu_recognize(audio_path):
    djv = Dejavu(config)

    # Fingerprint your local songs
    djv.fingerprint_directory("known_songs/", [".mp3", ".wav", ".m4a"])

    # Example recognition
    return djv.recognize(FileRecognizer, audio_path)

if __name__ == "__main__":

    result = dejavu_recognize("evaluation/Killa Klassic/lowVolumeKillaKlassic_.m4a")

    print(result)
