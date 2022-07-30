import socket
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


pca = None

pygame.init()
pygame.mixer.init()

SUB_BEATS = 24
LIGHT_COUNT = 7

curr_effects = []
curr_bpm = 120
time_start = time.perf_counter()

beat_index = 0

light_lock = threading.Lock()

sockets = []


########################################


PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
local_ip = socket.gethostbyname(socket.gethostname())

def http_server():
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print(f'serving at: http://{local_ip}:{PORT}', flush=True)
    httpd.serve_forever()


########################################

async def init_client(websocket, path):
    global curr_effects, curr_bpm, time_start, beat_index

    message = {
        'effects_json': profiles_json,
        'status': {
            'rate': curr_bpm,
            'curr_effects': curr_effects
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print("socket send failed", flush=True)

    sockets.append(websocket)
    # print(sockets)

    local = args.local
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

            if msg['type'] == 'add_button':
                add_effect(msg['profile'], msg['button'])

            elif msg['type'] == 'remove_button':
                profile = msg['profile']
                button = msg['button']
                index = curr_effect_index(profile, button)
                if index is not False:
                    remove_effect(index)

            elif msg['type'] == 'clear_effects':
                clear_effects()

            elif msg['type'] == 'update_effects_json':
                clear_effects()
                update_effects_json()

            elif msg['type'] == 'set_bpm':
                time_start = time.perf_counter()
                curr_bpm = float(msg['bpm'])
                clear_effects()

            light_lock.release()

            await send_update() # we might not to lock this
        print(msg, flush=True)
        if not local:
            print(msg, flush=True)

async def send_update():
    message = {
        'status': {
            'curr_effects': curr_effects,
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
    character = '▆▆▆▆▆ '

    console.print('  ' + character, style=f'rgb({rbg_colors[0]},{rbg_colors[1]},{rbg_colors[2]})', end='')
    console.print(character, style=f'rgb({rbg_colors[3]},{rbg_colors[4]},{rbg_colors[5]})', end='')

    purple = [153, 50, 204]
    purple = list(map(lambda x: int(x * (all_levels[6] / 100.0)), purple))
    console.print(character, style=f'rgb({purple[0]},{purple[1]},{purple[2]})', end='')

    effect_useful_info = list(map(lambda x: x[3], curr_effects))
    # console.print(f'Effect: {effect_useful_info}, BPM: {curr_bpm}{" " * 10}', end='\r')
    console.print(f'', end='\r')


all_levels = [0] * LIGHT_COUNT
async def terminal(level, i):
    # if is_windows():
    #     return
    all_levels[i] = level
    if i == LIGHT_COUNT - 1:
        await render_to_terminal(all_levels)


####################################

async def light():
    global beat_index
    local = args.local
    while True:
        light_lock.acquire()

        rate = curr_bpm / 60 * SUB_BEATS
        time_diff = time.perf_counter() - time_start
        beat_index = int(time_diff * rate)
        update = False

        i = 0
        while i < len(curr_effects):
            if not channel_lut[curr_effects[i][0]]["loop"] and beat_index + curr_effects[i][1] >= channel_lut[curr_effects[i][0]]["length"]:
                remove_effect(i)
                update = True
            else:
                i+=1
        for i in range(LIGHT_COUNT):
            level = 0
            for j in range(len(curr_effects)):
                index = beat_index + curr_effects[j][1]
                if index >= 0:
                    index = index % channel_lut[curr_effects[j][0]]["length"]
                    level += channel_lut[curr_effects[j][0]]["beats"][index][i]

            if local:
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

def curr_effect_index(profile, button):
    for i in range(len(curr_effects)):
        if curr_effects[i][2] == profile and curr_effects[i][3] == button:
            return i
    return False

def remove_effect(index):
    profile = curr_effects[index][2]
    button = curr_effects[index][3]
    curr_effects.pop(index)
    if "song" in profiles_json[profile][button]:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

def clear_effects():
    for index, effect in enumerate(curr_effects):
        remove_effect(index)

def add_effect(profile, button):
    global beat_index, time_start, curr_bpm
    if profiles_json[profile][button]["type"] != "toggle" or curr_effect_index(profile, button) is False:
        effect = profiles_json[profile][button]['effect']
        if "bpm" in profiles_json[profile][button]:
            time_start = time.perf_counter() + profiles_json[profile][button]['delay']
            curr_bpm = profiles_json[profile][button]['bpm']
            clear_effects()
            beat_index = int((-profiles_json[profile][button]['delay']) * (curr_bpm / 60 * SUB_BEATS))
            offset = 0
        else:
            offset = (beat_index % round(profiles_json[profile][button]['snap'] * SUB_BEATS)) - beat_index
        if "song" in profiles_json[profile][button]:
            pygame.mixer.music.load('data/' + profiles_json[profile][button]['song'])
            pygame.mixer.music.play()
        curr_effects.append([effect, offset, profile, button])

######################################

def setup_gpio():
    global pca

    import board
    import busio
    import adafruit_pca9685

    i2c = busio.I2C(board.SCL, board.SDA)
    pca = adafruit_pca9685.PCA9685(i2c)

    pca.frequency = 200

    for i in range(len(pca.channels)):
        pca.channels[i].duty_cycle = 0

    pca.channels[0].duty_cycle = 0xFFFF
    pca.channels[1].duty_cycle = 0xFFFF
    pca.channels[2].duty_cycle = 0xFFFF
    pca.channels[3].duty_cycle = 0xFFFF
    pca.channels[4].duty_cycle = 0xFFFF
    pca.channels[5].duty_cycle = 0xFFFF


################################################

effects_json = {}
profiles_json = {}
channel_lut = {}

graph = {}
found = {}
simple_effects = []
complex_effects = []

def effects_json_sort(path):
    curr = path[-1]
    if curr in found:
        return
    found[curr] = True
    for next in graph[curr]:
        if next in path:
            print(f'Cycle Found: {curr} -> {next}')
            exit()
        effects_json_sort(path + [next])
    if len(graph[curr]) == 0:
        simple_effects.append(curr)
    else:
        complex_effects.append(curr)

def update_effects_json():
    global effects_json, profiles_json, channel_lut, graph, found, simple_effects, complex_effects

    effects_json = {}
    profiles_json = {}
    channel_lut = {}

    graph = {}
    found = {}
    simple_effects = []
    complex_effects = []

    effect_dir = python_file_directory.joinpath('effects')
    for file in os.listdir(effect_dir):
        print(file)
        with open(effect_dir.joinpath(file), 'r') as f:
            effects_json.update(json.loads(f.read()))

    profile_dir = python_file_directory.joinpath('profiles')
    for file in os.listdir(profile_dir):
        with open(profile_dir.joinpath(file), 'r') as f:
            profiles_json.update(json.loads(f.read()))

    for effect in effects_json:
        if 'loop' not in effects_json[effect]:
            effects_json[effect]['loop'] = True

        graph[effect] = {}
        for beat in effects_json[effect]["beats"]:
            if type(effects_json[effect]["beats"][beat]) is str:
                effects_json[effect]["beats"][beat] = [[effects_json[effect]["beats"][beat]]]
            elif type(effects_json[effect]["beats"][beat][0]) is str:
                effects_json[effect]["beats"][beat] = [effects_json[effect]["beats"][beat]]
            elif type(effects_json[effect]["beats"][beat][0]) in [int, float]:
                effects_json[effect]["beats"][beat] = [[effects_json[effect]["beats"][beat]]]
            elif type(effects_json[effect]["beats"][beat][0][0]) in [int, float]:
                effects_json[effect]["beats"][beat] = [effects_json[effect]["beats"][beat]]

            if type(effects_json[effect]["beats"][beat][0][0]) is str:
                for entry in effects_json[effect]["beats"][beat]:
                    graph[effect][entry[0]] = True
        graph[effect] = list(graph[effect].keys())


    for profile in profiles_json:
        for button in profiles_json[profile]:
            if 'snap' not in profiles_json[profile][button]:
                profiles_json[profile][button]['snap'] = 1 / SUB_BEATS
            if 'type' not in profiles_json[profile][button]:
                profiles_json[profile][button]['type'] = "toggle"
            if 'bpm' in profiles_json[profile][button]:
                if 'delay' not in profiles_json[profile][button]:
                    profiles_json[profile][button]['delay'] = 0
            profiles_json[profile][button]['length'] = effects_json[profiles_json[profile][button]['effect']]['length']
            profiles_json[profile][button]['loop'] = effects_json[profiles_json[profile][button]['effect']]['loop']

    for effect in graph:
        effects_json_sort([effect])

    for effect in simple_effects:    
        channel_lut[effect] = {
            'length': round(effects_json[effect]['length'] * SUB_BEATS),
            'loop': effects_json[effect]['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(effects_json[effect]['length'] * SUB_BEATS)],
        }
        for beat in effects_json[effect]["beats"]:
            for component in effects_json[effect]["beats"][beat]: # component -> ['name', 1, 0, 8, 0]
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                
                if len(component) == 1:
                    component.append(effects_json[effect]['length'])
                if len(component) == 2:
                    component.append(1)
                if len(component) == 3:
                    component.append(1)

                channels = component[0]
                length = round(min(component[1] * SUB_BEATS, channel_lut[effect]["length"] - start_beat))
                start_mult = component[2]
                end_mult = component[3]

                for i in range(length):
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        channel_lut[effect]["beats"][start_beat + i][x] += channels[x] * mult


    for effect in complex_effects:
        channel_lut[effect] = {
            'length': round(effects_json[effect]['length'] * SUB_BEATS),
            'loop': effects_json[effect]['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(effects_json[effect]['length'] * SUB_BEATS)],
        }
        for beat in effects_json[effect]["beats"]:
            for component in effects_json[effect]["beats"][beat]:
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                name = component[0]

                if len(component) == 1:
                    if effects_json[name]["loop"]:
                        component.append(effects_json[effect]['length'])
                    else:
                        component.append(effects_json[name]['length'])
                if len(component) == 2:
                    component.append(1)
                if len(component) == 3:
                    component.append(1)
                if len(component) == 4:
                    component.append(0)

                length = round(min(component[1] * SUB_BEATS, channel_lut[effect]["length"] - start_beat))
                start_mult = component[2]
                end_mult = component[3]
                offset = round(component[4] * SUB_BEATS)

                for i in range(length):
                    channels = channel_lut[name]["beats"][(i + offset) % channel_lut[name]["length"]]
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        channel_lut[effect]["beats"][start_beat + i][x] += channels[x] * mult
                    
        # for i in range(channel_lut[effect]["length"]):
        #     for x in range(LIGHT_COUNT):
        #         channel_lut[effect]["beats"][i][x] = min(100, max(0, channel_lut[effect]["beats"][i][x]))
    print("effects_json updated")
    # for index, x in enumerate(channel_lut['Musician Show']['beats']):
    #     print(f'index {index / 24}: {x}')

update_effects_json()

##################################################

def kill_in_n_seconds(seconds):
    time.sleep(seconds)
    if is_windows():
        kill_string = f'taskkill /PID {os.getpid()} /F'
    else:
        kill_string = f'kill -9 {os.getpid()}'
    print(f'running to kill: "{kill_string}"')
    os.system(kill_string)

def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    if not args.local:    
        # tries to turn off lights
        x = threading.Thread(target=kill_in_n_seconds, args=(0.5,))
        x.start()
        for i in range(len(pca.channels)):
            pca.channels[i].duty_cycle = 0
    exit()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#################################################


parser = argparse.ArgumentParser(description = '')
parser.add_argument('--local', dest='local', default=False, action='store_true')
parser.add_argument('--starting_show', dest='starting_show', type=str, default='')
args = parser.parse_args()

if args.local:
    from rich.console import Console
    console = Console()
else:
    setup_gpio()


http_thread = threading.Thread(target=http_server, args=[], daemon=True)
http_thread.start()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def start_async():
    asyncio.create_task(light())

    if args.starting_show:
        add_effect('Shows', args.starting_show)

    websocket_server = await websockets.serve(init_client, "0.0.0.0", 8765)
    await websocket_server.wait_closed()

asyncio.run(start_async())