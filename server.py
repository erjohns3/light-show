import profile
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
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import eyed3
import pygame

from helpers import *
import sound_helpers


pygame.init()
pygame.mixer.init()

pca = None

SUB_BEATS = 24
LIGHT_COUNT = 7

curr_effects = []
song_queue = []

curr_bpm = 120.5
time_start = time.perf_counter()
beat_index = 0

light_lock = threading.Lock()
song_lock = threading.Lock()

light_sockets = []
song_sockets = []

song_playing = False
queue_autoplay = False
show_num = 0

pygame.init()
pygame.mixer.init()

########################################


PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
local_ip = socket.gethostbyname(socket.gethostname())

def http_server():
    httpd = http.server.ThreadingHTTPServer(("", PORT), Handler)
    print(f'serving at: http://{local_ip}:{PORT}', flush=True)
    httpd.serve_forever()


########################################

async def init_light_client(websocket, path):
    global curr_bpm, time_start, beat_index, queue_autoplay

    message = {
        'shows': shows_json,
        'songs': songs_json,
        'status': {
            'shows': curr_effects,
            'rate': curr_bpm
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print("socket send failed", flush=True)

    light_sockets.append(websocket)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            for i in range(len(light_sockets)):
                if light_sockets[i] == websocket:
                    light_sockets.pop(i)
                    break
            print("socket recv FAILED - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'type' in msg:
            light_lock.acquire()

            broadcast_song = False

            if msg['type'] == 'add_show':
                show_name = msg['show']

                if has_song(show_name):
                    if queue_autoplay and len(song_queue) > 0:
                        song_queue.pop()
                    song_queue.insert(0, [show_name, get_show_num()])
                    play_song(show_name)
                    queue_autoplay = True
                    broadcast_song = True
                add_effect(show_name)

            elif msg['type'] == 'remove_show':
                show_name = msg['show']
                if has_song(show_name):
                    if queue_autoplay and len(song_queue) > 0:
                        song_queue.pop()
                    stop_song()
                    queue_autoplay = False
                    broadcast_song = True
                index = curr_effect_index(show_name)
                if index is not False:
                    remove_effect(index)

            elif msg['type'] == 'clear_shows':
                clear_effects()
                stop_song()
                #BROKEN

            elif msg['type'] == 'update_json':
                clear_effects()
                update_json()
                #BROKEN

            elif msg['type'] == 'set_bpm':
                time_start = time.perf_counter()
                curr_bpm = float(msg['bpm'])
                clear_effects()
                #BROKEN

            light_lock.release()

            if broadcast_song:
                await send_song_status()
            await send_light_status() # we might want to lock this


async def init_song_client(websocket, path):
    global curr_bpm, time_start, beat_index, queue_autoplay

    message = {
        'shows': shows_json,
        'songs': songs_json,
        'queue': song_queue,
        'status': {
            'playing': song_playing,
            'autoplay': queue_autoplay
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print("socket send failed", flush=True)

    song_sockets.append(websocket)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            for i in range(len(song_sockets)):
                if song_sockets[i] == websocket:
                    song_sockets.pop(i)
                    break
            print("socket recv FAILED - " + websocket.remote_address[0] + " : " + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'type' in msg:
            song_lock.acquire()

            broadcast_light = False

            if msg['type'] == 'add_queue_back':
                show_name = msg['show']
                song_queue.append([show_name, get_show_num()])
                if len(song_queue) == 1:
                    play_song(show_name)
                    queue_autoplay = True
                    add_effect(show_name)
                    broadcast_light = True
            
            elif msg['type'] == 'add_queue_front':
                show_name = msg['show']
                if len(song_queue) == 0:
                    song_queue.append([show_name, get_show_num()])
                else:
                    song_queue.insert(1, [show_name, get_show_num()])
                if len(song_queue) == 1:
                    play_song(show_name)
                    queue_autoplay = True
                    add_effect(show_name)
                    broadcast_light = True

            elif msg['type'] == 'remove_queue':
                show_name = msg['show']
                num = msg['num']
                for i in range(len(song_queue)):
                    if song_queue[i][0] == show_name and song_queue[i][1] == num:
                        song_queue.pop(i)
                        if i == 0:
                            stop_song()
                            index = curr_effect_index(show_name)
                            if index is not False:
                                remove_effect(index)
                            if queue_autoplay and len(song_queue) > 0:
                                new_show_name = song_queue[0][0]
                                add_effect(new_show_name)
                                play_song(new_show_name)
                            broadcast_light = True
                        break
                if len(song_queue) == 0:
                    queue_autoplay = False

            elif msg['type'] == 'play_queue':
                if len(song_queue) > 0:
                    show_name = song_queue[0][0]
                    play_song(show_name)
                    queue_autoplay = True
                    add_effect(show_name)
                    broadcast_light = True

            elif msg['type'] == 'stop_queue':
                if len(song_queue) > 0:
                    show_name = song_queue[0][0]
                    song_queue.pop(0)
                    stop_song()
                    index = curr_effect_index(show_name)
                    if index is not False:
                        remove_effect(index)
                    queue_autoplay = False
                    broadcast_light = True

            song_lock.release()

            if broadcast_light:
                await send_light_status()
            await send_song_status() # we might want to lock this


def get_show_num():
    global show_num
    show_num += 1
    return show_num


async def broadcast(sockets, msg):
    for socket in sockets:
        try:
            await socket.send(msg)
        except:
            print("socket send failed", flush=True)


async def send_light_status():
    message = {
        'status': {
            'shows': curr_effects,
            'rate': curr_bpm
        }
    }
    dump = json.dumps(message)
    await broadcast(light_sockets, dump)


async def send_song_status():
    global queue_autoplay
    message = {
        'queue': song_queue,
        'status': {
            'autoplay': queue_autoplay
        }
    }
    dump = json.dumps(message)
    await broadcast(song_sockets, dump)
    

####################################


my_color_tuple = [254, 0, 0]
async def render_to_terminal(all_levels):
    terminal_color_scaling = 6
    max_num = (pow(2, 16) - 1) / 100
    levels_capped = list(map(lambda x: min(max(terminal_color_scaling * int(x / max_num), 0), 255), all_levels))

    uv_level_scaling = min(1, (terminal_color_scaling * levels_capped[6]) / 255.0)
    purple = [153, 50, 204]
    purple_scaled = list(map(lambda x: int(x * uv_level_scaling), purple))

    uv_style = f'rgb({purple_scaled[0]},{purple_scaled[1]},{purple_scaled[2]})'    
    top_rgb_style = f'rgb({levels_capped[0]},{levels_capped[1]},{levels_capped[2]})'
    bottom_rgb_style = f'rgb({levels_capped[3]},{levels_capped[4]},{levels_capped[5]})'

    character = '▆'
    console.print(' ' + character * 2, style=uv_style, end='')
    console.print(character * 10, style=top_rgb_style, end='')
    console.print(character * 2, style=uv_style, end='')
    console.print('\n' * 3)


    # console.print(' ' + character * 14, style=bottom_rgb_style, end='\n')
    console.print(' ' + character * 14, style=bottom_rgb_style, end='')

    # effect_useful_info = list(map(lambda x: x[3], curr_effects))
    # console.print(f'Effect: {effect_useful_info}, BPM: {curr_bpm}{" " * 10}', end='\r')
    console.print('', end='\033[F' * 4)


all_levels = [0] * LIGHT_COUNT
async def terminal(level, i):
    # if is_windows():
    #     return
    all_levels[i] = level
    if i == LIGHT_COUNT - 1:
        await render_to_terminal(all_levels)


####################################

async def light():
    global beat_index, queue_autoplay

    local = args.local
    while True:
        light_lock.acquire()

        rate = curr_bpm / 60 * SUB_BEATS
        time_diff = time.perf_counter() - time_start
        beat_index = int(time_diff * rate)
        broadcast_light = False
        broadcast_song = False        
            
        i = 0
        while i < len(curr_effects):
            index = beat_index + curr_effects[i][1]
            effect_name = curr_effects[i][0]
            show_name = curr_effects[i][2]
            if (not channel_lut[effect_name]['loop'] and index >= channel_lut[effect_name]['length']) or time_diff >= shows_json[show_name]['duration']:
                remove_effect(i)
                if has_song(show_name):
                    stop_song()
                    song_queue.pop(0)
                    if queue_autoplay and len(song_queue) > 0:
                        new_show_name = song_queue[0][0]
                        add_effect(new_show_name)
                        play_song(new_show_name)
                    elif len(song_queue) == 0:
                        queue_autoplay = False
                    broadcast_song = True
                broadcast_light = True
            else:
                i+=1
        for i in range(LIGHT_COUNT):
            level = 0
            for j in range(len(curr_effects)):
                index = beat_index + curr_effects[j][1]
                if index >= 0:
                    index = index % channel_lut[curr_effects[j][0]]['length']
                    level += channel_lut[curr_effects[j][0]]["beats"][index][i]
            level = max(0, min(0xFFFF, round(level * 0xFFFF / 100)))

            if local:
                await terminal(level, i)
            else:
                pca.channels[i].duty_cycle = level

        if broadcast_light:
            await send_light_status()
        if broadcast_song:
            await send_song_status()

        time_diff = time.perf_counter() - time_start
        time_delay = ((beat_index + 1) / rate) - time_diff

        light_lock.release()
        # print(beat_index)
        await asyncio.sleep(time_delay)

#################################################

def has_song(show_name):
    return "song" in shows_json[show_name]

def curr_effect_index(show_name):
    for i in range(len(curr_effects)):
        if curr_effects[i][2] == show_name:
            return i
    return False

def remove_effect(index):
    curr_effects.pop(index)

def clear_effects():
    for index, effect in enumerate(curr_effects):
        remove_effect(index)


def add_effect(show_name):
    global beat_index, time_start, curr_bpm

    show = shows_json[show_name]
    if (show['trigger'] == 'toggle' or show['trigger'] == 'hold') and curr_effect_index(show_name) is not False:
        return

    effect = show['effect']

    if "bpm" in show:
        clear_effects()
        time_start = time.perf_counter() + show['delay_lights']
        curr_bpm = show['bpm']
        beat_index = int((-show['delay_lights']) * (curr_bpm / 60 * SUB_BEATS))
        offset = 0
    else:
        offset = (beat_index % round(show['snap'] * SUB_BEATS)) - beat_index
    curr_effects.append([effect, offset, show_name])


def play_song(show_name):
    song = shows_json[show_name]['song']
    skip = shows_json[show_name]['skip_song']
    pygame.mixer.music.set_volume(args.volume)
    pygame.mixer.music.load(pathlib.Path('songs').joinpath(song))
    channel = pygame.mixer.music.play(start=skip)


def stop_song():
    pygame.mixer.music.stop()

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

    # pca.channels[0].duty_cycle = 0x0AFF
    # pca.channels[1].duty_cycle = 0x0AFF
    # pca.channels[2].duty_cycle = 0x0AFF
    # pca.channels[3].duty_cycle = 0x0AFF
    # pca.channels[4].duty_cycle = 0x0AFF
    # pca.channels[5].duty_cycle = 0x0AFF


################################################

shows_json = {}
effects_json = {}
songs_json = {}

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


def update_json():
    global effects_json, shows_json, songs_json, channel_lut, graph, found, simple_effects, complex_effects

    effects_json = {}
    shows_json = {}
    songs_json = {}

    channel_lut = {}

    graph = {}
    found = {}
    simple_effects = []
    complex_effects = []

    effect_dir = python_file_directory.joinpath('effects')
    for file in os.listdir(effect_dir):
        with open(effect_dir.joinpath(file), 'r') as f:
            effects_json.update(json.loads(f.read()))

    profile_dir = python_file_directory.joinpath('shows')
    for file in os.listdir(profile_dir):
        with open(profile_dir.joinpath(file), 'r') as f:
            shows_json.update(json.loads(f.read()))

    song_dir = python_file_directory.joinpath('songs')
    for file in os.listdir(song_dir):
        if file[-4:] == '.mp3':
            filepath = song_dir.joinpath(file)
            metadata = eyed3.load(filepath)
            if metadata.tag.title != None:
                name = metadata.tag.title
            else:
                name = pathlib.Path(file).stem
            songs_json[file] = {
                'name': name,
                'artist': metadata.tag.artist,
                'duration': metadata.info.time_secs
            }

    for effect_name, effect in effects_json.items():
        if 'loop' not in effect:
            effect['loop'] = True

        graph[effect_name] = {}
        beats = effect["beats"]
        for beat in beats:
            if type(beats[beat]) is str:
                beats[beat] = [[beats[beat]]]
            elif type(beats[beat][0]) is str:
                beats[beat] = [beats[beat]]
            elif type(beats[beat][0]) in [int, float]:
                beats[beat] = [[beats[beat]]]
            elif type(beats[beat][0][0]) in [int, float]:
                beats[beat] = [beats[beat]]

            if type(beats[beat][0][0]) is str:
                for entry in beats[beat]:
                    graph[effect_name][entry[0]] = True
        graph[effect_name] = list(graph[effect_name].keys())
    
    for show_name, show in shows_json.items():
        if 'snap' not in show:
            show['snap'] = 1 / SUB_BEATS
        if 'trigger' not in show:
            show['trigger'] = "toggle"
        if 'bpm' in show:
            show['delay_lights'] = show.get('delay_lights', 0)
            if not args.local:
                show['delay_lights'] += 0
            print('show: ', show['delay_lights'])
        loop = False
        duration = 1000000
        if 'effect' in show:
            loop = effects_json[show['effect']]['loop']
            length = effects_json[show['effect']]['length']
        if 'song' in show:
            duration = songs_json[show['song']]['duration']
        if 'duration' in show:
            duration = min(duration, show['duration'])
        show['length'] = length
        show['duration'] = duration
        show['loop'] = loop


    for effect_name in graph:
        effects_json_sort([effect_name])

    for effect_name in simple_effects:
        effect = effects_json[effect_name]
        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(effect['length'] * SUB_BEATS)],
        }
        beats = effect["beats"]
        for beat in beats:
            for component in beats[beat]: # component -> ['name', 1, 0, 8, 0]
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                
                if len(component) == 1:
                    component.append(effect['length'])
                if len(component) == 2:
                    component.append(1)
                if len(component) == 3:
                    component.append(1)

                channels = component[0]
                length = round(min(component[1] * SUB_BEATS, channel_lut[effect_name]['length'] - start_beat))
                start_mult = component[2]
                end_mult = component[3]

                for i in range(length):
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        channel_lut[effect_name]["beats"][start_beat + i][x] += channels[x] * mult

    for effect_name in complex_effects:
        effect = effects_json[effect_name]
        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(effect['length'] * SUB_BEATS)],
        }
        beats = effect["beats"]
        for beat in beats:
            for component in beats[beat]:
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                name = component[0]

                if len(component) == 1:
                    if effects_json[name]['loop']:
                        component.append(effect['length'])
                    else:
                        component.append(effects_json[name]['length'])
                if len(component) == 2:
                    component.append(1)
                if len(component) == 3:
                    component.append(1)
                if len(component) == 4:
                    component.append(0)

                length = round(min(component[1] * SUB_BEATS, channel_lut[effect_name]['length'] - start_beat))
                start_mult = component[2]
                end_mult = component[3]
                offset = round(component[4] * SUB_BEATS)

                for i in range(length):
                    channels = channel_lut[name]["beats"][(i + offset) % channel_lut[name]['length']]
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        channel_lut[effect_name]["beats"][start_beat + i][x] += channels[x] * mult
                    
        # for i in range(channel_lut[effect_name]['length']):
        #     for x in range(LIGHT_COUNT):
        #         channel_lut[effect_name]["beats"][i][x] = min(100, max(0, channel_lut[effect_name]["beats"][i][x]))
    print("effects_json updated")
    # for index, x in enumerate(channel_lut['Musician Show']['beats']):
    #     print(f'index {index / 24}: {x}')

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
parser.add_argument('--show', dest='show', type=str, default='')
parser.add_argument('--skip', dest='skip_show', type=int, default=0)
parser.add_argument('--volume', dest='volume', type=int, default=100)
args = parser.parse_args()

args.volume = args.volume / 100

if args.local:
    from rich.console import Console
    console = Console()
else:
    setup_gpio()

update_json()

http_thread = threading.Thread(target=http_server, args=[], daemon=True)
http_thread.start()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

async def start_async():

    light_socket_server = await websockets.serve(init_light_client, "0.0.0.0", 1337)
    song_socket_server = await websockets.serve(init_song_client, "0.0.0.0", 7654)

    if args.show:
        if args.show in shows_json:
            if args.skip_show:
                shows_json[args.show]['skip_song'] += args.skip_show
                shows_json[args.show]['delay_lights'] -= args.skip_show
            add_effect(args.show)
            play_song(args.show)
        else:
            print(f'Couldnt find effect named "{args.show}" in any profile')
    asyncio.create_task(light())

    await light_socket_server.wait_closed()

asyncio.run(start_async())