from pathlib import Path
from recognize import recognize
from dejavu_implementation import dejavu_recognize

EVAL_DIR = Path("evaluation")

total = 0
correct = 0
false_positive = 0
false_negative = 0

print("--Tests for different types of song Queries--")

for folder in EVAL_DIR.iterdir():
    expected = folder.name
    print(f"\nEntering folder: {expected}")

    for audio in folder.glob("*"):
        if audio.suffix.lower() in {".m4a", ".mp3", ".wav"}:

            predicted, score = recognize(str(audio))
            total += 1

            if expected == "unknown":
                if predicted is None:
                    correct += 1
                else:
                    false_positive += 1
            else:
                if predicted == expected:
                    correct += 1
                else:
                    false_negative += 1

            print(f"{audio.name:25} | expected={expected:18} | "
                f"predicted={predicted} | score={score:.3f}")

print("\n--- SUMMARY ---")
print(f"Total tests       : {total}")
print(f"Correct           : {correct}")
print(f"Accuracy          : {correct/total:.2f}")
print(f"False positives   : {false_positive}")
print(f"False negatives   : {false_negative}")
