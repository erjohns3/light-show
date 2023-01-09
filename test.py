import board
import busio
import adafruit_pca9685
import time

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 200

start = time.time()

for x in range(0, 16):
    pca.channels[x%16].duty_cycle = 0

end = time.time()

print(end - start)