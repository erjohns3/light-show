import pigpio
import time

pi = pigpio.pi()

gpio_map = [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 2, 3, 4, 17, 27, 22]

if not pi.connected:
    exit()

for pin in gpio_map:
    pi.set_PWM_frequency(pin, 500)
    pi.set_PWM_range(pin, 400)
    pi.set_PWM_dutycycle(pin, 0)

pi.set_PWM_dutycycle(gpio_map[0], 0)

start = time.time()

for i in range(1):
    for pin in gpio_map:
        pi.set_PWM_dutycycle(pin, 0)

end = time.time()

print(end-start)