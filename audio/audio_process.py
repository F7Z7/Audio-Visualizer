import numpy as np



def compute_fft(audioFile):
    fft_vals = np.fft.fft(audioFile)
    fft_freq = np.fft.fftfreq(len(audioFile))
    return np.abs(fft_vals[:len(fft_vals) // 2]), fft_freq[:len(fft_freq) // 2]