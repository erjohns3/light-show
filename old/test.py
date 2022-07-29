import pigpio
import json
import sys
import time
import asyncio
import math
import threading
from os import path

num = 0
lock = threading.Lock()

lock.acquire()
lock.release()


tick_start = time.perf_counter()
for x in range(10000000):
    lock.acquire()
    num = 0
    lock.release()


tick_end = time.perf_counter()

print(tick_end - tick_start)