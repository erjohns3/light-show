import time
import serial

ser = serial.Serial(
    port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate = 2000000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

num = 0

# print(leds)
leds = [0] * 640 * 3

while 1:
    start_time = time.time()
    for i in range(2, len(leds), 3):
        leds[i] = 255
    # leds[num] = 255
    ser.write(bytes(leds))
    end_time = time.time()
    print(f'time: {(end_time - start_time)*1000}')
    time.sleep(0.1)
    num = (num + 3) % len(leds)
