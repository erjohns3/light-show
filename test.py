import pigpio
import json
import sys
import time
import asyncio
import math
from os import path

PIN = 23


rate = 120 / 60 # beats per second
sub_rate = rate * 32

pi = pigpio.pi()
pi.set_mode(PIN, pigpio.INPUT)


def light():
    tick_start = time.perf_counter()
    while True:
        index =  round((time.perf_counter() - tick_start) * sub_rate)
        print(index)
        time.sleep(0.005)


#print(ticks)