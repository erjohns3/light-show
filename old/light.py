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
curr_rate = curr_bpm / 60 * SUB_BEATS


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
    curr_rate = curr_bpm / 60 * SUB_BEATS
    
    light_task = asyncio.create_task(light())

####################################

RED_PIN = 9
GREEN_PIN = 10
BLUE_PIN = 11

COLOR_PINS = [RED_PIN, GREEN_PIN, BLUE_PIN]

async def light():    
    tick_start = time.perf_counter()

    while True:
        time_curr = time.perf_counter()
        time_diff = time_curr - tick_start
        num = int(time_diff * curr_rate)
        time_delay = ((num + 1) / curr_rate) - time_diff
        
        for i in range(3):
            level = 0
            for mode in curr_modes:
                index = num % len(light_modes[mode])
                level = max(level, light_modes[mode][index][i])
            pi.set_PWM_dutycycle(COLOR_PINS[i], round((100 - level)*2.55))
        
        await asyncio.sleep(time_delay)

#################################################

async def init(websocket, path):
    global curr_modes
    
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

    pi.set_PWM_frequency(RED_PIN, 200)
    pi.set_PWM_frequency(GREEN_PIN, 200)
    pi.set_PWM_frequency(BLUE_PIN, 200)

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

light_modes = {}

key_frames = {}

for mode in config:
    light_modes[mode] = [False] * round(config[mode]['length'] * SUB_BEATS)
    key_frames[mode] = []
    prev_index = -1
    for beat in config[mode]['beats']:
        index = min(len(light_modes[mode])-1, max(prev_index + 1, round((eval(beat)-1) * SUB_BEATS)))
        prev_index = index
        key_frames[mode].append(index)
        light_modes[mode][index] = config[mode]['beats'][beat]

for mode in light_modes:
    for x in range(len(key_frames[mode])):
        start_index = key_frames[mode][x]
        if x < len(key_frames[mode]) - 1:
            end_index = key_frames[mode][x+1]
        else:
            end_index = key_frames[mode][(x+1)%len(key_frames[mode])] + len(light_modes[mode])
        start_color = light_modes[mode][start_index]
        end_color = light_modes[mode][end_index % len(light_modes[mode])]

        for y in range(start_index + 1, end_index):
            light_modes[mode][y % len(light_modes[mode])] = [0] * 3

            if len(start_color) == 4 and start_color[3] == "hold":
                for i in range(3):
                    light_modes[mode][y % len(light_modes[mode])][i] = start_color[i]
            else:
                shift = (y - start_index) / (end_index - start_index)
                for i in range(3):
                    light_modes[mode][y % len(light_modes[mode])][i] = (end_color[i] * shift) + (start_color[i] * (1 - shift))
                    
for mode in config:
    print(f'{mode}')
    for i in range(len(light_modes[mode])):
        print(f'    {i}: {round(light_modes[mode][i][0])}, {round(light_modes[mode][i][1])}, {round(light_modes[mode][i][2])}')

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
