import subprocess


FPCALC_PATH = r"C:\softwares\chromaprint\fpcalc.exe"
def extract_fingerprint(audio_path):
    """
    Runs fpcalc -raw on an audio file
    Returns (duration, fingerprint_list)
    """

    result = subprocess.run(
        [FPCALC_PATH, "-raw", audio_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    duration = None
    fingerprint = None

    for line in result.stdout.splitlines():
        if line.startswith("DURATION="):
            duration = int(line.split("=")[1])
        elif line.startswith("FINGERPRINT="):
            fingerprint = list(map(int, line.split("=")[1].split(",")))

    return duration, fingerprint


if __name__ == "__main__":
    duration, fp = extract_fingerprint("known_songs/Lafangey_Parindey.mp3")
    print("Duration:", duration)
    print("Fingerprint length:", len(fp))
    print("First 10 values:", fp[:10])
