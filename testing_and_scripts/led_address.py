import board
import neopixel
import time
import sys
import signal

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

count = 100

pixels = neopixel.NeoPixel(board.D12, count, auto_write=False, pixel_order=neopixel.RGB)

num = 0

while True:
    for i in range(count):
        pixels[i] = (0, 0, 0)
    pixels[num % count] = (0, 0, 255)

    pixels.show()
    print(f'Show: {num % count}')
    num += 1
    input()
