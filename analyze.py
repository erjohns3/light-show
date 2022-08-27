import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fft import fft, fftfreq
import numpy as np
import time

rate, data = wav.read('songs/shelter.wav')
samples = [item[0] for item in data]

bpm = 100
first_beat = 0.21 # seconds to first beat

delay = int((60 / 120 * rate) / 4)
x = int(first_beat * rate)
end = len(samples)

x += 

print(f'samples ber scan: {delay}')

while x + delay < end:
    arr = samples[x:x+delay]
    x += len(arr)
    N = len(arr)
    T = 1.0 / 1600.0

    yf = fft(arr)
    xf = fftfreq(N, T)[:N//2]

    plt.clf()
    plt.axis([-10, 200, 0, 20000])
    plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
    plt.draw()
    print(f'beat: {(x / rate) - first_beat}')
    plt.pause(0.01)
