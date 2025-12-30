from similarity import cosine_similarity

def sliding_window_match(song_fp, query_fp, step=1):
    """
    Slides query fingerprint over song fingerprint
    Returns the best cosine similarity score
    """
    q_len = len(query_fp)
    s_len = len(song_fp)

    if q_len > s_len:
        return 0.0

    best_score = 0.0

    for i in range(0, s_len - q_len + 1, step):
        window = song_fp[i:i + q_len]
        score = cosine_similarity(window, query_fp)

        if score > best_score:
            best_score = score

    return best_score

