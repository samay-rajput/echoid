import math

def cosine_similarity(a, b):
    """
    Computes cosine similarity between two equal-length lists
    """

    dot = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(y * y for y in b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot / (magnitude_a * magnitude_b)
