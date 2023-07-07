from re import L
import matplotlib.pyplot as plt            
from scipy.io import wavfile as wav
from scipy.fft import fft, fftfreq
import numpy as np
import time
import math

SUB_BEATS = 24

rate, data = wav.read('songs/shelter.wav')
samples = [item[0] for item in data]

T1 = 1.0 / rate
N1 = len(samples)

T2 = 1.0 / 100
N2 = math.ceil(N1 * T1 / T2)

blocks = [0] * N2

for i in range(N1):
    blocks[int(i * T1 / T2)] += abs(samples[i])

start_index = int(0.5 * N2 * T2)
end_index = int(3.0 * N2 * T2)

yf = fft(blocks)
xf = fftfreq(N2, T2)

# start_index = int(0.5 * N1 * T1)
# end_index = int(3.0 * N1 * T1)

# yf = fft(samples)
# xf = fftfreq(N1, T1)

af = np.abs(yf)

max_i = start_index
for i in range(start_index, end_index):
    if af[i] > af[max_i]:
        max_i = i

frequency = xf[max_i]
period = 1.0 / frequency
bpm = frequency * 60.0
phase = np.angle(yf[max_i])
offset = phase / np.pi * period
if offset < 0:
    offset += 2 * np.pi
print(f'scanning: {round(1/T2)}, i: {max_i}')
print(f'phase: {phase}, offset: {offset}')
print(f'frequency: {frequency}, bpm: {bpm}')

# plt.plot(xf[start_index:end_index], af[start_index:end_index])
# plt.grid()
# plt.show()

delay = int((period * rate) / SUB_BEATS)
x = int(offset * rate)
end = len(samples)

N = delay
T = 1.0 / 2000

start_index = int(10 * N * T)
end_index = int(100 * N * T)

bass = [0] * ((end - x) // delay)

print(f'samples ber scan: {delay}')
i = 0
while x + delay < end:
    arr = samples[x:x+delay]
    x += delay

    yf = fft(arr)
    xf = fftfreq(N, T)[:N//2]

    for j in range(start_index, end_index):
        bass[i] += 2.0/N * np.abs(yf[j])

    i += 1

plt.plot(bass[0:4*SUB_BEATS])
plt.grid()
plt.show()