import threading
import pigpio
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

SUB_BEATS = 24

args = False
pi = None
light_task = False
curr_modes = []
curr_bpm = 120
curr_rate = curr_bpm / 60


async def set_light(new_modes, new_bpm):
    global light_task
    global curr_modes
    global curr_bpm
    global curr_rate

    if light_task:
        light_task.cancel()

    print("mode: " + str(curr_modes))
    curr_modes = new_modes
    curr_bpm = new_bpm
    curr_rate = curr_bpm / 60
    
    light_task = asyncio.create_task(light())

####################################

RED_PIN = 9
GREEN_PIN = 10
BLUE_PIN = 11

COLOR_PINS = [RED_PIN, GREEN_PIN, BLUE_PIN]

LIGHT_COUNT = 3

async def light():    
    tick_start = time.perf_counter()

    while True:
        time_curr = time.perf_counter()
        time_diff = time_curr - tick_start
        curr_beat = (time_diff * curr_rate) % effects_json[mode]['length']
        
        levels = [0]*LIGHT_COUNT

        for mode in curr_modes:
            for i in range(LIGHT_COUNT):
                prev_beat = False
                next_beat = False
                for beat in effects_json[mode]['beats']:
                    if curr_beat >= beat:
                        prev_beat = beat
                    if curr_beat < beat:
                        next_beat = beat
                        break

                diff_beat = (curr_beat - prev_beat) / (next_beat - prev_beat)

                levels[i] = max(levels[i], (effects_json[mode]['beats'][prev_beat][i] * diff_beat) + (effects_json[mode]['beats'][next_beat][i] * (1-diff_beat)))

        for i in range(LIGHT_COUNT):
            pi.set_PWM_dutycycle(COLOR_PINS[i], round((100 - levels[i])*2.55))

        time_taken = time.perf_counter() - time_curr
        
        await asyncio.sleep(0.02 - time_taken)

#################################################

async def init(websocket, path):
    global curr_modes
    
    message = {
        'effects_json': effects_json,
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
                    mode = msg['modes']
                    bpm = float(msg['rate'])
                    if bpm > 0:
                        await set_light(mode, bpm)

            elif msg['type'] == 'preview':
                if msg['modes'] != '' and msg['rate'] != '':
                    mode = msg['modes']
                    bpm = float(msg['rate'])
                    if bpm > 0:
                        await set_light(mode, bpm)

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

    pi.set_mode(RED_PIN, pigpio.OUTPUT)
    pi.set_mode(GREEN_PIN, pigpio.OUTPUT)
    pi.set_mode(BLUE_PIN, pigpio.OUTPUT)

    pi.set_PWM_dutycycle(RED_PIN, 255)
    pi.set_PWM_dutycycle(GREEN_PIN, 255)
    pi.set_PWM_dutycycle(BLUE_PIN, 255)

    pi.set_PWM_frequency(RED_PIN, 1000)
    pi.set_PWM_frequency(GREEN_PIN, 1000)
    pi.set_PWM_frequency(BLUE_PIN, 1000)

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

with open(path.join(drink_io_folder, 'effects_json.json'), 'r') as f:
    effects_json = json.loads(f.read())

light_modes = {}

key_frames = {}

for mode in effects_json:
    light_modes[mode] = [False] * round(effects_json[mode]['length'] * SUB_BEATS)
    key_frames[mode] = []
    prev_index = -1
    for beat in effects_json[mode]['beats']:
        index = min(len(light_modes[mode])-1, max(prev_index + 1, round((eval(beat)-1) * SUB_BEATS)))
        prev_index = index
        key_frames[mode].append(index)
        light_modes[mode][index] = effects_json[mode]['beats'][beat]
   
##################################################

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    if pi is None:
        print('signal_handler skipped for testing', flush=True)
    else:
        pi.set_PWM_dutycycle(RED_PIN, 255)
        pi.set_PWM_dutycycle(GREEN_PIN, 255)
        pi.set_PWM_dutycycle(BLUE_PIN, 255)

        pi.stop()

    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#################################################

def run_asyncio():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_server = websockets.serve(init, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    print('Ready...')
    asyncio.get_event_loop().run_forever()


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

    run_asyncio()


if __name__ == "__main__":
    main()