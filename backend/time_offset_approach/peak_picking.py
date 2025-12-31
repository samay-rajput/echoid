import numpy as np
import librosa
from spectogram import plot_spectogram


def find_peaks(
    audio_path,
    n_fft=2048,
    hop_length=512,
    neighborhood_size=15,
    threshold_db=-40,
):
    """
    Detect spectral peaks from a spectrogram.

    Args:
        audio_path (str): Path to the audio file.
        n_fft (int): FFT window size.
        hop_length (int): Hop length for STFT.
        neighborhood_size (int): Size of the neighborhood for local maxima detection.
        threshold_db (float): Minimum dB threshold for peaks.

    Returns:
        peaks (list of tuples): [(time_sec, freq_hz), ...]
    """
    # Compute spectrogram in dB scale
    S_db, sr = plot_spectogram(audio_path)

    # Neighborhood padding
    pad = neighborhood_size // 2
    padded = np.pad(S_db, pad_width=pad, mode="constant", constant_values=-np.inf)

    # Initialize local maxima mask
    local_max = np.ones_like(S_db, dtype=bool)

    # A point is a peak if it is greater than all its neighbors
    for i in range(-pad, pad + 1):
        for j in range(-pad, pad + 1):
            if i == 0 and j == 0:
                continue
            local_max &= S_db > padded[
                pad + i : pad + i + S_db.shape[0],
                pad + j : pad + j + S_db.shape[1],
            ]

    # Apply loudness threshold
    peaks_mask = local_max & (S_db > threshold_db)

    # Convert indices to time & frequency
    freq_idxs, time_idxs = np.where(peaks_mask)
    times = librosa.frames_to_time(time_idxs, sr=sr, hop_length=hop_length)
    freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)[freq_idxs]

    # Combine into (time, freq) pairs
    peaks = list(zip(times, freqs))

    return peaks


if __name__ == "__main__":
    plot_spectogram("../chromaprint approach/evaluation/Killa Klassic/concertKillaKlassic.mp3")
