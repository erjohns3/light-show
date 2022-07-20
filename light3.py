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
    import pigpio
    import board
    import busio
    import adafruit_pca9685

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)

    pca.frequency = 200
except Exception as e:
    print(f'Cant start with hardware support because of {e}')


SUB_BEATS = 24
LIGHT_COUNT = 7

pi = None
curr_modes = []
curr_bpm = 120
time_start = time.perf_counter()
beat_index = 0

light_lock = threading.Lock()
light_task = False

sockets = []

########################################

async def send_update():
    message = {
        'status': {
            'modes': curr_modes,
            'rate': curr_bpm
        }
    }
    dump = json.dumps(message)
    for socket in sockets:
        try:
            await socket.send(dump)
        except:
            print("socket send failed", flush=True)


####################################



async def render_to_terminal(all_levels):
    rbg_colors = list(map(lambda x: int(x * 2.55), all_levels[:6]))
    character = '▆ '

    console.print('  ' + character, style=f'rgb({rbg_colors[0]},{rbg_colors[1]},{rbg_colors[2]})', end='')
    console.print(character, style=f'rgb({rbg_colors[3]},{rbg_colors[4]},{rbg_colors[5]})', end='')

    purple = [153, 50, 204]
    purple = list(map(lambda x: int(x * (all_levels[6] / 100.0)), purple))
    console.print(character, style=f'rgb({purple[0]},{purple[1]},{purple[2]})', end='')

    console.print(f'Mode: {curr_modes}, BPM: {curr_bpm}{" " * 10}', end='\r')


all_levels = [0] * LIGHT_COUNT
async def terminal(level, i):
    all_levels[i] = level
    if i == LIGHT_COUNT - 1:
        await render_to_terminal(all_levels)


####################################

async def light():
    global beat_index
    print_to_terminal = args.print_to_terminal
    while True:
        light_lock.acquire()

        rate = curr_bpm / 60 * SUB_BEATS
        time_diff = time.perf_counter() - time_start
        beat_index = int(time_diff * rate)
        update = False

        i = 0
        while i < len(curr_modes):
            if not light_array[curr_modes[i][0]]["loop"] and beat_index + curr_modes[i][1] >= light_array[curr_modes[i][0]]["length"]:
                curr_modes.pop(i)
                update = True
            else:
                i+=1
        for i in range(LIGHT_COUNT):
            level = 0
            for j in range(len(curr_modes)):
                index = (beat_index + curr_modes[j][1]) % light_array[curr_modes[j][0]]["length"]
                level += light_array[curr_modes[j][0]]["beats"][index][i]

            if print_to_terminal:
                await terminal(level, i)
            else:
                pca.channels[i].duty_cycle = max(0, min(0xFFFF, round(level * 0xFFFF / 100)))


        if update:
            await send_update()

        time_diff = time.perf_counter() - time_start
        time_delay = ((beat_index + 1) / rate) - time_diff


        light_lock.release()
        # print(beat_index)
        await asyncio.sleep(time_delay)

#################################################

async def init(websocket, path):
    global light_task
    global curr_modes
    global curr_bpm
    global time_start

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

    sockets.append(websocket)
    print(sockets)

    brake_modes = False

    print_to_terminal = args.print_to_terminal
    while True:
        try:
            msg_string = await websocket.recv()
        except:
            for i in range(len(sockets)):
                if sockets[i] == websocket:
                    sockets.pop(i)
                    break
            print("socket recv FAILED - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'type' in msg:

            light_lock.acquire()

            if msg['type'] == 'set_show':
                curr_show = msg['show']
                time_start = time.perf_counter()
                curr_bpm = float(msg['bpm'])

            if msg['type'] == 'add_mode':
                mode = msg['mode']
                print(mode)
                curr_modes.append((mode, (beat_index % light_array[mode]["snap"]) - beat_index))

            elif msg['type'] == 'remove_mode':
                mode = msg['mode']
                for i in range(len(curr_modes)):
                    if curr_modes[i][0] == mode:
                        curr_modes.pop(i)
                        break

            elif msg['type'] == 'toggle_mode':
                mode = msg['mode']
                found = False
                for i in range(len(curr_modes)):
                    if curr_modes[i][0] == mode:
                        curr_modes.pop(i)
                        found = True
                        break
                if not found:
                    curr_modes.append((mode, (beat_index % light_array[mode]["snap"]) - beat_index))

            elif msg['type'] == 'clear_modes':
                curr_modes = []

            elif msg['type'] == 'brake_press':
                brake_modes = curr_modes
                curr_modes = []

            elif msg['type'] == 'brake_release':
                curr_modes = brake_modes

            elif msg['type'] == 'set_bpm':
                time_start = time.perf_counter()
                curr_bpm = float(msg['bpm'])

            light_lock.release()

            await send_update()

        if not print_to_terminal:
            print(msg, flush=True)

######################################

def setup_pigpio():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        exit()

    for i in range(len(pca.channels)):
        pca.channels[i].duty_cycle = 0

    pca.channels[0].duty_cycle = 0xFFFF
    pca.channels[1].duty_cycle = 0xFFFF
    pca.channels[2].duty_cycle = 0xFFFF
    pca.channels[3].duty_cycle = 0xFFFF
    pca.channels[4].duty_cycle = 0xFFFF
    pca.channels[5].duty_cycle = 0xFFFF

#################################################

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        http.server.SimpleHTTPRequestHandler.end_headers(self)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def http_server():
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
    if 'loop' not in config[mode]:
        config[mode]['loop'] = True
    if 'interpolation' not in config[mode]:
        config[mode]['interpolation'] = 'smooth'

    light_dict[mode] = {
        'length': config[mode]['length'],
        'snap': round(config[mode]['snap'] * SUB_BEATS),
        'beats': {},
        'loop': config[mode]['loop']
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

# for mode in config:
#     print(f'{mode}')
#     for beat in light_dict[mode]["beats"]:
#         print(f'    {beat}: {round(light_dict[mode]["beats"][beat][0])}, {round(light_dict[mode]["beats"][beat][1])}, {round(light_dict[mode]["beats"][beat][2])}')


for mode in config:
    light_array[mode] = {
        'length': config[mode]['length'] * SUB_BEATS,
        'snap': round(config[mode]['snap'] * SUB_BEATS),
        'beats': [False] * round(config[mode]['length'] * SUB_BEATS),
        'loop': config[mode]['loop']
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

# for mode in config:
#     print(f'{mode}')
#     for i in range(len(light_array[mode]["beats"])):
#         print(f'    {i}: {round(light_array[mode]["beats"][i][0])}, {round(light_array[mode]["beats"][i][1])}, {round(light_array[mode]["beats"][i][2])}')

##################################################

def kill_in_n_seconds(seconds):
    time.sleep(seconds)
    kill_string = f'kill -9 {os.getpid()}'
    print(f'trying to kill with "{kill_string}"')
    os.system(kill_string)

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    print('Attemping to reset lights to off, but exiting in 1 second regardless')
    x = threading.Thread(target=kill_in_n_seconds, args=(1,))
    x.start()
    if pi is None:
        print('Not turning off lights, in testing mode', flush=True)
    else:
        sys.exit(0)
        for i in range(len(pca.channels)):
            pca.channels[i].duty_cycle = 0

        pi.stop()
    time.sleep(2000)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#################################################


parser = argparse.ArgumentParser(description = '')
parser.add_argument('--terminal', dest='print_to_terminal', default=False, action='store_true')
args = parser.parse_args()

if args.print_to_terminal:
    from rich.console import Console
    console = Console()
else:
    setup_pigpio()

http_thread = threading.Thread(target=http_server, args=[], daemon=True)
http_thread.start()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

start_server = websockets.serve(init, "0.0.0.0", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
