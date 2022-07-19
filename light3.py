import threading
import time
import sys
import json
import signal
import pathlib
import asyncio
import websockets
import http.server
import argparse
import os
from os import path
import math
import pigpio
import board
import busio
import adafruit_pca9685

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c)

pca.frequency = 200

SUB_BEATS = 24
LIGHT_COUNT = 7

args = False
pi = None
curr_modes = []
curr_bpm = 120
time_start = time.perf_counter()
beat_index = 0

light_lock = threading.Lock()
light_task = False

########################################

async def set_time(new_bpm):
    global time_start
    global curr_bpm

    light_lock.acquire()
    time_start = time.perf_counter()
    curr_bpm = new_bpm
    light_lock.release()
    print("set time")


async def set_light(new_modes):
    global curr_modes
    global curr_offsets

    light_lock.acquire()
    curr_modes = new_modes
    curr_offsets = [0] * len(curr_modes)
    for i in range(len(curr_modes)):
        curr_offsets[i] = (beat_index % light_array[curr_modes[i]]["snap"]) - beat_index
    light_lock.release()
    print("mode: " + str(curr_modes))

####################################

async def light(): 
    global beat_index

    while True:
        light_lock.acquire()

        rate = curr_bpm / 60 * SUB_BEATS
        time_diff = time.perf_counter() - time_start
        beat_index = int(time_diff * rate)
        
        for i in range(LIGHT_COUNT):
            level = 0
            for j in range(len(curr_modes)):
                index = (beat_index + curr_offsets[j]) % len(light_array[curr_modes[j]]["beats"])
                level += light_array[curr_modes[j]]["beats"][index][i]
            pca.channels[i].duty_cycle = max(0, min(0xFFFF, round(level * 0xFFFF / 100)))

        time_diff = time.perf_counter() - time_start
        time_delay = ((beat_index + 1) / rate) - time_diff

        light_lock.release()
        # print(beat_index)
        await asyncio.sleep(time_delay)

#################################################

async def init(websocket, path):
    global light_task

    if not light_task:
        light_task = asyncio.create_task(light())

    message = {
        'config': config,
        'status': {
            'rate': curr_bpm,
            'modes': curr_modes
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print("socket send failed", flush=True)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            print("socket recv FAILED - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
            break
        print("socket recv - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
        msg = json.loads(msg_string)
        print(msg, flush=True)

        if 'type' in msg:

            if msg['type'] == 'modes':
                if msg['modes'] != '':
                    modes = msg['modes']
                    await set_light(modes)

            elif msg['type'] == 'time':
                if msg['rate'] != '':
                    bpm = float(msg['rate'])
                if bpm > 0:
                    await set_time(bpm)

            message = {
                'status': {
                    'modes': curr_modes,
                    'rate': curr_bpm
                }
            }
            dump = json.dumps(message)
            try:
                await websocket.send(dump)
            except:
                print("socket send failed", flush=True)

######################################

def setup_pigpio():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    for i in range(len(pca.channels)):
        pca.channels[i].duty_cycle = 0

#################################################

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        http.server.SimpleHTTPRequestHandler.end_headers(self)
        
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def http_server(testing=False):
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print("serving at port " + str(PORT), flush=True)
    httpd.serve_forever()

################################################

loc = pathlib.Path(__file__).parent.absolute()
drink_io_folder = str(loc)

with open(path.join(drink_io_folder, 'config.json'), 'r') as f:
    config = json.loads(f.read())

light_dict = {}
light_array = {}

for mode in config:
    if 'snap' not in config[mode]:
        config[mode]['snap'] = 1 / SUB_BEATS
    if 'interpolation' not in config[mode]:
        config[mode]['interpolation'] = 'smooth'

    light_dict[mode] = {
        'length': config[mode]['length'],
        'snap': round(config[mode]['snap'] * SUB_BEATS),
        'beats': {}
    }
    config[mode]['beats'][str(config[mode]['length']+1)] = False
    beats = list(config[mode]['beats'].keys())
    config[mode]['beats'][str(config[mode]['length']+1)] = config[mode]['beats'][beats[0]]
    for i in range(len(beats)):
        curr_beat = round((eval(beats[i])-1)*SUB_BEATS) / SUB_BEATS
        light_dict[mode]['beats'][curr_beat] = config[mode]['beats'][beats[i]]
        if config[mode]['interpolation'] == 'hold' and i+1 < len(beats):
            next_beat = eval(beats[i+1]) - 1 - (1/SUB_BEATS)
            if abs(next_beat - curr_beat) > 0.5/SUB_BEATS:
                light_dict[mode]['beats'][next_beat] = light_dict[mode]['beats'][curr_beat]

for mode in config:
    print(f'{mode}')
    for beat in light_dict[mode]["beats"]:
        print(f'    {beat}: {round(light_dict[mode]["beats"][beat][0])}, {round(light_dict[mode]["beats"][beat][1])}, {round(light_dict[mode]["beats"][beat][2])}')


for mode in config:
    light_array[mode] = {
        'length': config[mode]['length'],
        'snap': round(config[mode]['snap'] * SUB_BEATS),
        'beats': [False] * round(config[mode]['length'] * SUB_BEATS)
    }
    beats = list(light_dict[mode]["beats"].keys())
    for i in range(len(beats)-1):
        start_index = round(beats[i] * SUB_BEATS)
        end_index = round(beats[i+1] * SUB_BEATS)
        start_light = light_dict[mode]["beats"][beats[i]]
        end_light = light_dict[mode]["beats"][beats[i+1]]

        for j in range(start_index, end_index):
            light_array[mode]["beats"][j] = [0] * LIGHT_COUNT
            shift = (j - start_index) / (end_index - start_index)
            for k in range(LIGHT_COUNT):
                light_array[mode]["beats"][j][k] = (end_light[k] * shift) + (start_light[k] * (1 - shift))

for mode in config:
    print(f'{mode}')
    for i in range(len(light_array[mode]["beats"])):
        print(f'    {i}: {round(light_array[mode]["beats"][i][0])}, {round(light_array[mode]["beats"][i][1])}, {round(light_array[mode]["beats"][i][2])}')

##################################################

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    if pi is None:
        print('signal_handler skipped for testing', flush=True)
    else:
        for i in range(len(pca.channels)):
            pca.channels[i].duty_cycle = 0

        pi.stop()

    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#################################################


def main():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action='store_true', default=False,
                   help='To run webserver without drinkmaker attached')
    parser.add_argument('--local', action='store_true', default=False,
                   help='To run webserver without drinkmaker attached')
    args = parser.parse_args()

    if not args.testing:
        setup_pigpio()

    http_thread = threading.Thread(target=http_server, args=[args.testing], daemon=True)
    http_thread.start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(init, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
