import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fft import fft, fftfreq
import numpy as np

rate, data = wav.read('songs/shelter.wav')
left = [item[0] for item in data]

N = len(left)

yf = fft(left)
xf = fftfreq(N, 1 / rate)

plt.plot(xf, np.abs(yf))
plt.show()

# fft_out = fft(left)
# plt.plot(left, np.abs(fft_out))
# plt.show()