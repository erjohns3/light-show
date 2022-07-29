import threading
import time
import sys
import json
import signal
import pathlib
import asyncio
from tracemalloc import start
import websockets
import http.server
import argparse
import os
import math
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from helpers import *

# stop warning in python10 about DeprecationWarning: There is no current event loop asyncio.get_event_loop().run_forever()
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


try:
    import board
    import busio
    import adafruit_pca9685

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)

    pca.frequency = 200
except Exception as e:
    print(f'Cant start with hardware support because of {e}')

pygame.init()
pygame.mixer.init()

SUB_BEATS = 24
LIGHT_COUNT = 7

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
            'pads': curr_modes,
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
    rbg_colors = list(map(lambda x: min(max(int(x * 2.55), 0), 255), all_levels[:6]))
    character = '▆ '

    console.print('  ' + character, style=f'rgb({rbg_colors[0]},{rbg_colors[1]},{rbg_colors[2]})', end='')
    console.print(character, style=f'rgb({rbg_colors[3]},{rbg_colors[4]},{rbg_colors[5]})', end='')

    purple = [153, 50, 204]
    purple = list(map(lambda x: int(x * (all_levels[6] / 100.0)), purple))
    console.print(character, style=f'rgb({purple[0]},{purple[1]},{purple[2]})', end='')

    mode_useful_info = list(map(lambda x: x[3], curr_modes))
    console.print(f'Mode: {mode_useful_info}, BPM: {curr_bpm}{" " * 10}', end='\r')


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
                remove_curr_mode(i)
                update = True
            else:
                i+=1
        for i in range(LIGHT_COUNT):
            level = 0
            for j in range(len(curr_modes)):
                index = beat_index + curr_modes[j][1]
                if index >= 0:
                    index = index % light_array[curr_modes[j][0]]["length"]
                    level += light_array[curr_modes[j][0]]["beats"][index][i]

            # if print_to_terminal:
            #     await terminal(level, i)
            # else:
            #     pca.channels[i].duty_cycle = max(0, min(0xFFFF, round(level * 0xFFFF / 100)))

        if update:
            await send_update()

        time_diff = time.perf_counter() - time_start
        time_delay = ((beat_index + 1) / rate) - time_diff


        light_lock.release()
        # print(beat_index)
        await asyncio.sleep(time_delay)

#################################################

def curr_mode_index(profile, pad):
    for i in range(len(curr_modes)):
        if curr_modes[i][2] == profile and curr_modes[i][3] == pad:
            return i
    return False

def remove_curr_mode(index):
    profile = curr_modes[index][2]
    pad = curr_modes[index][3]
    curr_modes.pop(index)
    if "song" in pads[profile][pad]:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

async def init(websocket, path):
    global light_task
    global curr_modes
    global curr_bpm
    global time_start
    global beat_index

    if not light_task:
        light_task = asyncio.create_task(light())

    message = {
        'config': pads,
        'status': {
            'rate': curr_bpm,
            'pads': curr_modes
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print("socket send failed", flush=True)

    sockets.append(websocket)
    print(sockets)

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

            if msg['type'] == 'add_pad':
                profile = msg['profile']
                pad = msg['pad']
                if pads[profile][pad]["button"] != "toggle" or curr_mode_index(profile, pad) is False:
                    mode = pads[profile][pad]["mode"]
                    if "bpm" in pads[profile][pad]:
                        time_start = time.perf_counter() + pads[profile][pad]["delay"]
                        curr_bpm = pads[profile][pad]["bpm"]
                        curr_modes = []
                        beat_index = int((-pads[profile][pad]["delay"]) * (curr_bpm / 60 * SUB_BEATS))
                        offset = 0
                    else:
                        offset = (beat_index % round(pads[profile][pad]["snap"] * SUB_BEATS)) - beat_index
                    if "song" in pads[profile][pad]:
                        pygame.mixer.music.load('data/'+pads[profile][pad]["song"])
                        pygame.mixer.music.play()
                    curr_modes.append([mode, offset, profile, pad])

            elif msg['type'] == 'remove_pad':
                profile = msg['profile']
                pad = msg['pad']
                index = curr_mode_index(profile, pad)
                if index is not False:
                    remove_curr_mode(index)

            elif msg['type'] == 'clear_pads':
                curr_modes = []

            elif msg['type'] == 'update_config':
                curr_modes = []
                update_config()

            elif msg['type'] == 'set_bpm':
                time_start = time.perf_counter()
                curr_bpm = float(msg['bpm'])
                curr_modes = []

            light_lock.release()

            await send_update() # we might not to lock this
        print(msg, flush=True)
        if not print_to_terminal:
            print(msg, flush=True)

######################################

def setup_io():
    for i in range(len(pca.channels)):
        pca.channels[i].duty_cycle = 0

    pca.channels[0].duty_cycle = 0xFFFF
    pca.channels[1].duty_cycle = 0xFFFF
    pca.channels[2].duty_cycle = 0xFFFF
    pca.channels[3].duty_cycle = 0xFFFF
    pca.channels[4].duty_cycle = 0xFFFF
    pca.channels[5].duty_cycle = 0xFFFF

#################################################

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

def http_server():
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print("serving at port " + str(PORT), flush=True)
    httpd.serve_forever()

################################################

filepath = os.path.realpath(__file__)
dirpath = os.path.dirname(filepath)

config = {}
pads = {}
light_array = {}

graph = {}
found = {}
simple_modes = []
complex_modes = []

def config_sort(path):
    curr = path[-1]
    if curr in found:
        return
    found[curr] = True
    for next in graph[curr]:
        if next in path:
            print(f'Cycle Found: {curr} -> {next}')
            exit()
        config_sort(path + [next])
    if len(graph[curr]) == 0:
        simple_modes.append(curr)
    else:
        complex_modes.append(curr)

def update_config():
    global config
    global pads
    global light_array
    global graph
    global found
    global simple_modes
    global complex_modes

    config = {}
    pads = {}
    light_array = {}

    graph = {}
    found = {}
    simple_modes = []
    complex_modes = []

    for file in os.listdir(os.path.join(dirpath, 'configs')):
        with open(os.path.join(dirpath, 'configs', file), 'r') as f:
            config.update(json.loads(f.read()))

    for file in os.listdir(os.path.join(dirpath, 'pads')):
        with open(os.path.join(dirpath, 'pads', file), 'r') as f:
            pads.update(json.loads(f.read()))

    for mode in config:
        if 'loop' not in config[mode]:
            config[mode]['loop'] = True

        graph[mode] = {}
        for beat in config[mode]["beats"]:
            if type(config[mode]["beats"][beat]) is str:
                config[mode]["beats"][beat] = [[config[mode]["beats"][beat]]]
            elif type(config[mode]["beats"][beat][0]) is str:
                config[mode]["beats"][beat] = [config[mode]["beats"][beat]]
            elif type(config[mode]["beats"][beat][0]) in [int, float]:
                config[mode]["beats"][beat] = [[config[mode]["beats"][beat]]]
            elif type(config[mode]["beats"][beat][0][0]) in [int, float]:
                config[mode]["beats"][beat] = [config[mode]["beats"][beat]]

            if type(config[mode]["beats"][beat][0][0]) is str:
                for entry in config[mode]["beats"][beat]:
                    graph[mode][entry[0]] = True
        graph[mode] = list(graph[mode].keys())


    for profile in pads:
        for pad in pads[profile]:
            if 'snap' not in pads[profile][pad]:
                pads[profile][pad]['snap'] = 1 / SUB_BEATS
            if 'button' not in pads[profile][pad]:
                pads[profile][pad]['button'] = "toggle"
            if 'bpm' in pads[profile][pad]:
                if 'delay' not in pads[profile][pad]:
                    pads[profile][pad]['delay'] = 0
            pads[profile][pad]['length'] = config[pads[profile][pad]['mode']]['length']
            pads[profile][pad]['loop'] = config[pads[profile][pad]['mode']]['loop']

    for mode in graph:
        config_sort([mode])

    for mode in simple_modes:    
        light_array[mode] = {
            'length': round(config[mode]['length'] * SUB_BEATS),
            'loop': config[mode]['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(config[mode]['length'] * SUB_BEATS)],
        }
        for beat in config[mode]["beats"]:
            for effect in config[mode]["beats"][beat]: # effect -> ['name', 1, 0, 8, 0]
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                
                if len(effect) == 1:
                    effect.append(config[mode]['length'])
                if len(effect) == 2:
                    effect.append(1)
                if len(effect) == 3:
                    effect.append(1)

                channels = effect[0]
                length = round(min(effect[1] * SUB_BEATS, light_array[mode]["length"] - start_beat))
                start_mult = effect[2]
                end_mult = effect[3]

                for i in range(length):
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        light_array[mode]["beats"][start_beat + i][x] += channels[x] * mult


    for mode in complex_modes:
        light_array[mode] = {
            'length': round(config[mode]['length'] * SUB_BEATS),
            'loop': config[mode]['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(config[mode]['length'] * SUB_BEATS)],
        }
        for beat in config[mode]["beats"]:
            for effect in config[mode]["beats"][beat]:
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                name = effect[0]

                if len(effect) == 1:
                    if config[name]["loop"]:
                        effect.append(config[mode]['length'])
                    else:
                        effect.append(config[name]['length'])
                if len(effect) == 2:
                    effect.append(1)
                if len(effect) == 3:
                    effect.append(1)
                if len(effect) == 4:
                    effect.append(0)

                length = round(min(effect[1] * SUB_BEATS, light_array[mode]["length"] - start_beat))
                start_mult = effect[2]
                end_mult = effect[3]
                offset = round(effect[4] * SUB_BEATS)

                for i in range(length):
                    channels = light_array[name]["beats"][(i + offset) % light_array[name]["length"]]
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        light_array[mode]["beats"][start_beat + i][x] += channels[x] * mult
                    
        # for i in range(light_array[mode]["length"]):
        #     for x in range(LIGHT_COUNT):
        #         light_array[mode]["beats"][i][x] = min(100, max(0, light_array[mode]["beats"][i][x]))
    print("config updated")

update_config()

##################################################

def kill_in_n_seconds(seconds):
    time.sleep(seconds)
    if is_windows():
        kill_string = f'taskkill /PID {os.getpid()} /F'
    else:
        kill_string = f'kill -9 {os.getpid()}'
    print(f'{kill_string}')
    os.system(kill_string)

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    if not args.print_to_terminal:
        x = threading.Thread(target=kill_in_n_seconds, args=(0.5,))
        x.start()
        for i in range(len(pca.channels)):
            pca.channels[i].duty_cycle = 0
    exit()

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
    setup_io()

http_thread = threading.Thread(target=http_server, args=[], daemon=True)
http_thread.start()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

start_server = websockets.serve(init, "0.0.0.0", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
