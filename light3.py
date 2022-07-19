from helpers import *

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

try:
    SUB_BEATS = 24
    LIGHT_COUNT = 7

    args = False
    pi = None
    curr_modes = []
    curr_bpm = 120
    tick_start = time.perf_counter()

    light_lock = threading.Lock()
    light_task = False


    import pigpio
    import board
    import busio
    import adafruit_pca9685

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)
    
    pca.frequency = 200

except Exception as e:
    print(f'{bcolors.FAIL}Could not import / setup hardware due to exception "{e}"{bcolors.ENDC}')



################################################

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        http.server.SimpleHTTPRequestHandler.end_headers(self)
        
PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def run_http_server():
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print("serving at port " + str(PORT), flush=True)
    httpd.serve_forever()

################################################

async def init(websocket, path):
    global light_task

    if not light_task:
        light_task = asyncio.create_task(light(light_array))

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

            if msg['type'] == 'apply':
                if msg['modes'] != '' and msg['rate'] != '':
                    modes = msg['modes']
                    bpm = float(msg['rate'])
                    if bpm > 0:
                        await set_light(modes, bpm)

            elif msg['type'] == 'preview':
                if msg['modes'] != '' and msg['rate'] != '':
                    modes = msg['modes']
                    bpm = float(msg['rate'])
                    if bpm > 0:
                        await set_light(modes, bpm)

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

#################################################



def setup_pigpio():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    for i in range(len(pca.channels)):
        pca.channels[i].duty_cycle = 0

#################################################

async def set_light(new_modes, new_bpm, debug=True):
    global curr_modes
    global curr_bpm
    global tick_start

    light_lock.acquire()
    curr_modes = new_modes
    curr_bpm = new_bpm
    # tick_start = time.perf_counter()
    light_lock.release()
    if debug:
        print("mode: " + str(curr_modes))

####################################

async def light(light_array, optional_callback=None):
    while True:
        light_lock.acquire()
        modes = curr_modes
        rate = curr_bpm / 60 * SUB_BEATS
        time_start = tick_start
        light_lock.release()
        
        time_curr = time.perf_counter()
        time_diff = time_curr - time_start
        num = int(time_diff * rate)
        time_delay = ((num + 1) / rate) - time_diff
        
        all_levels = []
        for i in range(LIGHT_COUNT):
            level = 0
            for mode in modes:
                index = num % len(light_array[mode])
                level += light_array[mode][index][i]
            if optional_callback:
                all_levels.append(level)
            else:
                pca.channels[i].duty_cycle = max(0, min(0xFFFF, int(level * 0xFFFF / 100)))
        if optional_callback:
            await optional_callback(all_levels)

        await asyncio.sleep(time_delay)



######################################

def read_config(config_filepath):    
    with open(config_filepath, 'r') as f:
        config = json.loads(f.read())

    light_dict = {}
    light_array = {}

    for mode in config:
        light_dict[mode] = {}
        config[mode]['beats'][str(config[mode]['length']+1)] = False
        beats = list(config[mode]['beats'].keys())
        config[mode]['beats'][str(config[mode]['length']+1)] = config[mode]['beats'][beats[0]]
        for i in range(len(beats)):
            curr_beat = round((eval(beats[i])-1)*SUB_BEATS) / SUB_BEATS
            light_dict[mode][curr_beat] = config[mode]['beats'][beats[i]]
            if 'interpolation' in config[mode] and config[mode]['interpolation'] == 'hold' and i+1 < len(beats):
                next_beat = eval(beats[i+1]) - 1 - (1/SUB_BEATS)
                if abs(next_beat - curr_beat) > 0.5/SUB_BEATS:
                    light_dict[mode][next_beat] = light_dict[mode][curr_beat]

    for mode in config:
        print(f'{mode}')
        for beat in light_dict[mode]:
            print(f'    {beat}: {round(light_dict[mode][beat][0])}, {round(light_dict[mode][beat][1])}, {round(light_dict[mode][beat][2])}')


    for mode in config:
        light_array[mode] = [False] * round(config[mode]['length'] * SUB_BEATS)
        beats = list(light_dict[mode].keys())
        for i in range(len(beats)-1):
            start_index = round(beats[i] * SUB_BEATS)
            end_index = round(beats[i+1] * SUB_BEATS)
            start_light = light_dict[mode][beats[i]]
            end_light = light_dict[mode][beats[i+1]]

            for j in range(start_index, end_index):
                light_array[mode][j] = [0] * LIGHT_COUNT
                shift = (j - start_index) / (end_index - start_index)
                for k in range(LIGHT_COUNT):
                    light_array[mode][j][k] = (end_light[k] * shift) + (start_light[k] * (1 - shift))

    for mode in config:
        print(f'{mode}')
        for i in range(len(light_array[mode])):
            print(f'    {i}: {round(light_array[mode][i][0])}, {round(light_array[mode][i][1])}, {round(light_array[mode][i][2])}')
    return light_array

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



#################################################



if __name__ == "__main__":
    setup_pigpio()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    light_array = read_config(python_file_directory.joinpath('config.json'))

    http_thread = threading.Thread(target=run_http_server, args=[], daemon=True)
    http_thread.start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(init, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()