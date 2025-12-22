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

def main():
    djv = Dejavu(config)

    # Fingerprint your local songs
    djv.fingerprint_directory("known_songs/", [".mp3", ".wav", ".m4a"])

    # Example recognition
    result = djv.recognize(FileRecognizer, "query/narmahatLaptop.m4a")
    print(result)

if __name__ == "__main__":

    main()
