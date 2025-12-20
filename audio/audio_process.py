import numpy as np


def compute_fft(audio_chunk, sample_rate):
    n = len(audio_chunk)
    window = np.hanning(n)
    windowed = audio_chunk * window

    fft_vals = np.fft.rfft(windowed)
    magnitude = np.abs(fft_vals) / (n / 2)
    freqs = np.fft.rfftfreq(n, 1 / sample_rate)

    return magnitude, freqs

