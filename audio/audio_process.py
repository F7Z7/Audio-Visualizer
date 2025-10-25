import numpy as np


def compute_fft(audio_chunk, sample_rate=44100):
    n = len(audio_chunk)
    fft_vals = np.fft.fft(audio_chunk)
    fft_freq = np.fft.fftfreq(n, 1 / sample_rate)


    positive_freqs = fft_freq[:n // 2]
    magnitude = np.abs(fft_vals[:n // 2])

    return magnitude, positive_freqs
