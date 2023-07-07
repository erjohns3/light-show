import time
import random
import pigpio

pi = pigpio.pi()

pin = 12

pi.set_mode(pin, pigpio.OUTPUT)

while True:
    pi.write(pin,0)
    print('low')
    time.sleep(1)
    pi.write(pin,1)
    print('high')
    time.sleep(1)