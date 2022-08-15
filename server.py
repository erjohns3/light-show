import socket
import threading
import time
import json
import signal
import importlib
import pathlib
import asyncio
import websockets
import http.server
import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from tinytag import TinyTag
from operator import add

from helpers import *
import sound_helpers


pca = None

SUB_BEATS = 24
LIGHT_COUNT = 7

curr_effects = []
song_queue = []

curr_bpm = 72
time_start = time.perf_counter()
beat_index = 0

light_lock = threading.Lock()
song_lock = threading.Lock()

light_sockets = []
song_sockets = []

song_playing = False
song_time = 0
queue_salt = 0

pygame.mixer.init()


########################################


PORT = 9555
Handler = http.server.SimpleHTTPRequestHandler
local_ip = socket.gethostbyname(socket.gethostname())

def http_server():
    httpd = http.server.ThreadingHTTPServer(('', PORT), Handler)
    print(f'{bcolors.OKGREEN}serving dj set at: http://{local_ip}:{PORT}/dj.html')
    print(f'serving queue at: http://{local_ip}:{PORT}{bcolors.ENDC}', flush=True)
    httpd.serve_forever()


########################################

async def init_dj_client(websocket, path):
    global curr_bpm, time_start, beat_index, song_playing, song_time

    message = {
        'effects': effects_config,
        'songs': songs_config,
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print('socket send failed', flush=True)

    light_sockets.append(websocket)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            for i in range(len(light_sockets)):
                if light_sockets[i] == websocket:
                    light_sockets.pop(i)
                    break
            print('socket recv FAILED - ' + websocket.remote_address[0] + ' : ' + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'type' in msg:
            light_lock.acquire()

            broadcast_song = False

            if msg['type'] == 'add_effect':
                effect_name = msg['effect']
                song_time = 0
                if has_song(effect_name):
                    if song_playing and len(song_queue) > 0:
                        song_queue.pop()
                    song_queue.insert(0, [effect_name, get_queue_salt()])
                    play_song(effect_name)
                    song_playing = True
                    broadcast_song = True
                add_effect(effect_name)

            elif msg['type'] == 'remove_effect':
                effect_name = msg['effect']
                if has_song(effect_name):
                    if song_playing and len(song_queue) > 0:
                        song_queue.pop()
                    stop_song()
                    song_playing = False
                    broadcast_song = True
                index = curr_effect_index(effect_name)
                if index is not False:
                    remove_effect(index)

            elif msg['type'] == 'clear_effects':
                clear_effects()
                stop_song()
                #BROKEN

            elif msg['type'] == 'update_config':
                clear_effects()
                update_config()
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


async def init_queue_client(websocket, path):
    global curr_bpm, time_start, beat_index, song_playing, song_time

    message = {
        'effects': effects_config,
        'songs': songs_config,
        'queue': song_queue,
        'status': {
            'playing': song_playing
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
    except:
        print('socket send failed', flush=True)

    song_sockets.append(websocket)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            for i in range(len(song_sockets)):
                if song_sockets[i] == websocket:
                    song_sockets.pop(i)
                    break
            print('socket recv FAILED - ' + websocket.remote_address[0] + ' : ' + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'type' in msg:
            song_lock.acquire()

            broadcast_light = False

            if msg['type'] == 'add_queue_back':
                effect_name = msg['effect']
                song_queue.append([effect_name, get_queue_salt()])
                if len(song_queue) == 1:
                    song_time = 0
                    play_song(effect_name)
                    song_playing = True
                    add_effect(effect_name)
                    broadcast_light = True
            
            elif msg['type'] == 'add_queue_front':
                effect_name = msg['effect']
                if len(song_queue) == 0:
                    song_queue.append([effect_name, get_queue_salt()])
                else:
                    song_queue.insert(1, [effect_name, get_queue_salt()])
                if len(song_queue) == 1:
                    song_time = 0
                    play_song(effect_name)
                    song_playing = True
                    add_effect(effect_name)
                    broadcast_light = True

            elif msg['type'] == 'remove_queue':
                effect_name = msg['effect']
                num = msg['num']
                for i in range(len(song_queue)):
                    if song_queue[i][0] == effect_name and song_queue[i][1] == num:
                        song_queue.pop(i)
                        if i == 0:
                            stop_song()
                            index = curr_effect_index(effect_name)
                            if index is not False:
                                remove_effect(index)
                            if song_playing and len(song_queue) > 0:
                                song_time = 0
                                new_effect_name = song_queue[0][0]
                                add_effect(new_effect_name)
                                play_song(new_effect_name)
                            broadcast_light = True
                        break
                if len(song_queue) == 0:
                    song_playing = False

            elif msg['type'] == 'play_queue':
                if len(song_queue) > 0 and not song_playing:
                    effect_name = song_queue[0][0]
                    play_song(effect_name)
                    song_playing = True
                    add_effect(effect_name)
                    broadcast_light = True

            elif msg['type'] == 'pause_queue':
                if len(song_queue) > 0 and song_playing:
                    effect_name = song_queue[0][0]
                    #song_queue.pop(0)
                    song_time += max(pygame.mixer.music.get_pos(), 0) / 1000
                    print(song_time)
                    stop_song()
                    index = curr_effect_index(effect_name)
                    if index is not False:
                        remove_effect(index)
                    song_playing = False
                    broadcast_light = True

            song_lock.release()

            if broadcast_light:
                await send_light_status()
            await send_song_status() # we might want to lock this


def get_queue_salt():
    global queue_salt
    queue_salt += 1
    return queue_salt


async def broadcast(sockets, msg):
    for socket in sockets:
        try:
            await socket.send(msg)
        except:
            print('socket send failed', flush=True)


async def send_light_status():
    message = {
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm
        }
    }
    dump = json.dumps(message)
    await broadcast(light_sockets, dump)


async def send_song_status():
    global song_playing
    message = {
        'queue': song_queue,
        'status': {
            'playing': song_playing
        }
    }
    dump = json.dumps(message)
    await broadcast(song_sockets, dump)
    

####################################


my_color_tuple = [254, 0, 0]
terminal_size = os.get_terminal_size().columns
async def render_to_terminal(all_levels):
    terminal_color_scaling = 1
    max_num = pow(2, 16) - 1
    levels_capped = list(map(lambda x: min(max(int(((x * 15) / max_num) * 255), 0), 255), all_levels))

    uv_level_scaling = min(1, (terminal_color_scaling * levels_capped[6]) / 255.0)
    purple = [153, 50, 204]
    purple_scaled = list(map(lambda x: int(x * uv_level_scaling), purple))

    uv_style = f'rgb({purple_scaled[0]},{purple_scaled[1]},{purple_scaled[2]})'    
    top_rgb_style = f'rgb({levels_capped[0]},{levels_capped[1]},{levels_capped[2]})'
    bottom_rgb_style = f'rgb({levels_capped[3]},{levels_capped[4]},{levels_capped[5]})'

    character = '▆'
    dead_space = terminal_size - 15
    console.print(' ' + character * 2, style=uv_style, end='')
    console.print(character * 10, style=top_rgb_style, end='')
    console.print(character * 2 + (' ' * dead_space), style=uv_style, end='')
    console.print('\n', end='')
    console.print(f'{" " * terminal_size}\n' * 3, end='')

    console.print(' ' + character * 14 + (' ' * dead_space), style=bottom_rgb_style, end='')
    console.print('\n', end='')

    # effect_useful_info = list(map(lambda x: x[3], curr_effects))
    
    effect_specific = ''
    if curr_effects:
        effect_name = curr_effects[0][0]
        if has_song(effect_name):
            index = (beat_index + curr_effects[0][1])
            time_diff = time.perf_counter() - time_start
            song_path = effects_config[effect_name]['song_path']
            effect_specific = f"""\
, {round(100 * (index / channel_lut[effect_name]['length']))}% lights\
, {round(100 * (time_diff / songs_config[song_path]['duration']))}% song\
"""

    useful_info = f"""\
BPM: {curr_bpm}, \
Beat: {round((beat_index / SUB_BEATS) + 1, 1)}, \
Seconds: {round(time.perf_counter() - time_start)}\
{effect_specific}\
"""
    extra_lines_up = (len(useful_info) // terminal_size) + 1
    console.print(useful_info + (' ' * (terminal_size - len(useful_info))), end='')
    console.print('', end='\033[F' * (4 + extra_lines_up))


all_levels = [0] * LIGHT_COUNT
async def terminal(level, i):
    all_levels[i] = level
    if i == LIGHT_COUNT - 1:
        await render_to_terminal(all_levels)


####################################

async def light():
    global beat_index, song_playing

    try:
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
                if not channel_lut[effect_name]['loop'] and index >= channel_lut[effect_name]['length']:
                    remove_effect(i)
                    if has_song(effect_name):
                        stop_song()
                        song_queue.pop(0)
                        if song_playing and len(song_queue) > 0:
                            song_time = 0
                            new_effect_name = song_queue[0][0]
                            add_effect(new_effect_name)
                            play_song(new_effect_name)
                        elif len(song_queue) == 0:
                            song_playing = False
                        broadcast_song = True
                    broadcast_light = True
                else:
                    i+=1
            for i in range(LIGHT_COUNT):
                level = 0
                for j in range(len(curr_effects)):
                    index = beat_index + curr_effects[j][1]
                    if index >= 0 and (channel_lut[effect_name]['loop'] or index < channel_lut[curr_effects[j][0]]['length']):
                        index = index % channel_lut[curr_effects[j][0]]['length']
                        level += channel_lut[curr_effects[j][0]]['beats'][index][i]

                # level = max(0, min(0xFFFF, round(level * 0xFFFF / 100)))
                level = max(0, min(0xFFFF, level * 0xFFFF / 100))
                between_0_and_1 = level / 0xFFFF
                level = round(pow(between_0_and_1, 2.2) * 0xFFFF)

                if args.local:
                    await terminal(level, i)
                else:
                    pca.channels[i].duty_cycle = level

            if broadcast_light:
                await send_light_status()
            if broadcast_song:
                await send_song_status()

            if args.print_beat and not args.local and beat_index % SUB_BEATS == 0:
                print(f'Beat: {(beat_index // SUB_BEATS) + 1}, Seconds: {time_diff:.2f}')

            time_diff = time.perf_counter() - time_start
            time_delay = ((beat_index + 1) / rate) - time_diff

            light_lock.release()
            await asyncio.sleep(time_delay)
    except Exception:
        import traceback
        print(traceback.format_exc())

#################################################

def has_song(name):
    return 'song_path' in effects_config[name]

def curr_effect_index(name):
    for i in range(len(curr_effects)):
        if curr_effects[i][0] == name:
            return i
    return False

def remove_effect(index):
    curr_effects.pop(index)

def clear_effects():
    for index, effect in enumerate(curr_effects):
        remove_effect(index)

def add_effect(name):
    global beat_index, time_start, curr_bpm

    effect = effects_config[name]
    if (effect['trigger'] == 'toggle' or effect['trigger'] == 'hold') and curr_effect_index(name) is not False:
        return

    if 'bpm' in effect:
        clear_effects()
        time_start = time.perf_counter() + effect['delay_lights'] - song_time
        curr_bpm = effect['bpm']
        beat_index = int((-effect['delay_lights']) * (curr_bpm / 60 * SUB_BEATS))
        offset = 0
    else:
        # offset = (beat_index % round(effect['snap'] * SUB_BEATS)) - beat_index
        snap = round(effect['snap'] * SUB_BEATS)
        offset = beat_index % snap
        if offset > snap * 0.5:
            offset -= snap
        offset -= beat_index
    curr_effects.append([name, offset])


def play_song(effect_name):
    song_path = effects_config[effect_name]['song_path']
    skip = effects_config[effect_name]['skip_song'] + song_time
    pygame.mixer.music.set_volume(args.volume)

    # if type(song) == pathlib.Path:
    # if os.sep in song:
    pygame.mixer.music.load(pathlib.Path(song_path))
    # else:
        # pygame.mixer.music.load(pathlib.Path('songs').joinpath(song))

    # ffmpeg -i songs/musician2.mp3 -c:a libvorbis -q:a 4 songs/musician2.ogg
    # python server.py --local --show "shelter" --skip 215
    # ffplay songs/shelter.mp3 -ss 215 -nodisp -autoexit
    print(f'{bcolors.OKBLUE}Starting music "{song_path}" at {skip} seconds at {round(args.volume * 100)}% volume{bcolors.ENDC}')
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


################################################

effects_config = {}
songs_config = {}

channel_lut = {}

graph = {}
found = {}
simple_effects = []
complex_effects = []

def effects_config_sort(path):
    curr = path[-1]
    if curr in found:
        return
    found[curr] = True
    for next in graph[curr]:
        if next in path:
            print(f'Cycle Found: {curr} -> {next}')
            exit()
        effects_config_sort(path + [next])
    if len(graph[curr]) == 0:
        simple_effects.append(curr)
    else:
        complex_effects.append(curr)

all_globals = globals()

def update_config(autogenerated_effects=None):
    global effects_config, songs_config, channel_lut, graph, found, simple_effects, complex_effects

    begin = time.perf_counter()
    channel_lut = {}

    graph = {}
    found = {}
    simple_effects = []
    complex_effects = []

    effects_config = {}
    if autogenerated_effects:
        effects_config.update(autogenerated_effects)
    for name, path in get_all_paths('effects', only_files=True):
        module = 'effects.' + path.stem
        if module in all_globals:
            importlib.reload(all_globals[module])
        else:
            all_globals[module] = importlib.import_module(module)
        effects_config.update(all_globals[module].effects)
    print(f'finishing up to imports took {time.perf_counter() - begin:.2f} seconds')

    songs_config = {}
    song_dir = pathlib.Path('songs')
    for filename in os.listdir(song_dir):
        filepath = pathlib.Path(song_dir.joinpath(filename))
        if filepath.suffix in ['.mp3', '.ogg', '.wav']:
            tags = TinyTag.get(filepath)
            artist = tags.artist
            duration = tags.duration

            if not duration:
                print(f'{bcolors.WARNING}No tag found for file: "{filepath}", ffprobing, but this is slow {bcolors.ENDC}')
                duration = sound_helpers.get_audio_clip_length(filepath)
            songs_config[str(filepath)] = {
                'name': filepath.stem,
                'artist': artist,
                'duration': duration
            }
    print(f'finishing up to getting song detail lengths {time.perf_counter() - begin:.2f} seconds')

    for effect_name, effect in effects_config.items():
        graph[effect_name] = {}
        beats = effect['beats']
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
    print(f'finishing up to beat reading took {time.perf_counter() - begin:.2f} seconds')


    for effect_name in graph:
        effects_config_sort([effect_name])
    print(f'finishing up the graph sorting took {time.perf_counter() - begin:.2f} seconds')

    for effect_name, effect in effects_config.items():
        if 'snap' not in effect:
            effect['snap'] = 1 / SUB_BEATS
        else:
            effect['snap'] = max(effect['snap'], 1 / SUB_BEATS)
        if 'trigger' not in effect:
            effect['trigger'] = 'toggle'
        if 'profiles' not in effect:
            effect['profiles'] = []
        if 'song_path' in effect and effect['song_path'] in songs_config:
            if 'bpm' not in effect:
                print('song effects must have bpm')
                exit()
            effect['delay_lights'] = effect.get('delay_lights', 0)
            if not args.local:
                effect['delay_lights'] += 0.1
            if 'length' not in effect:
                effect['length'] = songs_config[effect['song_path']]['duration'] * effect['bpm'] / 60
            if 'loop' not in effect:
                effect['loop'] = False
        else:
            if 'length' not in effect:
                max_length = 0
                beats = effect['beats']
                for beat in beats:
                    for component in beats[beat]: # component -> ['name', 1, 0, 8, 0]
                        max_length = max(max_length, (eval(beat) - 1) + component[1])  
                effect['length'] = max_length
            if 'loop' not in effect:
                effect['loop'] = True
    print(f'(done with update_config) finishing up to effect defaults took {time.perf_counter() - begin:.2f} seconds')

    for effect_name in effects_config:
        effects_config[effect_name]['profiles'].append('All Effects')
    print(f'finishing up to setting all_effects defaults took {time.perf_counter() - begin:.2f} seconds')

    for effect_name in simple_effects:
        effect = effects_config[effect_name]
        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(effect['length'] * SUB_BEATS)],
        }
        beats = effect['beats']
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
                    if length == 1:
                        mult = start_mult
                    else:
                        mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    for x in range(LIGHT_COUNT):
                        channel_lut[effect_name]['beats'][start_beat + i][x] += channels[x] * mult
                    if args.invert:
                        tmp = channel_lut[effect_name]['beats'][start_beat + i]
                        tmp[0], tmp[3] = tmp[3], tmp[0]
                        tmp[1], tmp[4] = tmp[4], tmp[1]
                        tmp[2], tmp[5] = tmp[5], tmp[2]
    print(f'finishing up to simple effects took {time.perf_counter() - begin:.2f} seconds')

    amt = 0
    for effect_name in complex_effects:
        effect = effects_config[effect_name]
        beats = effect['beats']

        # if length isn't specified, generate a length
        calced_effect_length = 0
        for beat in beats:
            for component in beats[beat]:
                name = component[0]
                if len(component) == 1:
                    if effects_config[name]['loop']:
                        component.append(effect['length'])
                    else:
                        component.append(effects_config[name]['length'])
                if len(component) == 2:
                    component.append(1)
                if len(component) == 3:
                    component.append(1)
                if len(component) == 4:
                    component.append(0)
                calced_effect_length = max(calced_effect_length, float(beat) + component[1] - 1)
        if 'length' not in effect:
            effect['length'] = calced_effect_length

        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * 7] * round(effect['length'] * SUB_BEATS)],
        }

        for beat in beats:
            for component in beats[beat]:
                start_beat = round((eval(beat) - 1) * SUB_BEATS)
                name = component[0]

                length = round(min(component[1] * SUB_BEATS, channel_lut[effect_name]['length'] - start_beat))
                start_mult = component[2]
                end_mult = component[3]
                offset = round(component[4] * SUB_BEATS)

                for i in range(length):
                    channels = channel_lut[name]['beats'][(i + offset) % channel_lut[name]['length']]

                    if length == 1:
                        mult = start_mult
                    else:
                        mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    
                    final_channel = channel_lut[effect_name]['beats'][start_beat + i]
                    for x in range(LIGHT_COUNT):
                        final_channel[x] += channels[x] * mult


        # for i in range(channel_lut[effect_name]['length']):
        #     for x in range(LIGHT_COUNT):
        #         channel_lut[effect_name]['beats'][i][x] = min(100, max(0, channel_lut[effect_name]['beats'][i][x]))
    print(f'finishing up to complex effects took {time.perf_counter() - begin:.2f} seconds')


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
    if args.reload:
        observer.stop()
        observer.join()
    exit()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

#################################################


parser = argparse.ArgumentParser(description = '')
parser.add_argument('--local', dest='local', default=False, action='store_true')
parser.add_argument('--show', dest='show', type=str, default='')
parser.add_argument('--skip', dest='skip_show', type=float, default=0)
parser.add_argument('--volume', dest='volume', type=int, default=100)
parser.add_argument('--print_beat', dest='print_beat', default=False, action='store_true')
parser.add_argument('--reload', dest='reload', default=False, action='store_true')
parser.add_argument('--jump_back', dest='jump_back', type=int, default=0)
parser.add_argument('--speed', dest='speed', type=float, default=1)
parser.add_argument('--invert', dest='invert', default=False, action='store_true')
parser.add_argument('--autogen', dest='autogen', default=False, action='store_true')
args = parser.parse_args()

args.volume = args.volume / 100
if args.local:
    from rich.console import Console
    console = Console()
else:
    setup_gpio()

update_config()

if args.autogen:
    autogenerated_effects = {}
    import generate_show

    # does all
    # for song_path in songs_config:
    for song_path in {'songs/musician2.ogg'}:
        song_path = pathlib.Path(song_path)
        new_effect = generate_show.generate_show(song_path)
        autogenerated_effects.update(new_effect)
        effect_name = list(new_effect.keys())[0]
    update_config(autogenerated_effects)


if args.reload:
    from watchdog.observers import Observer
    from watchdog.events import Fileffects_configeSystemEventHandler

    class FilesystemHandler(FileSystemEventHandler):
        last_updated = 0

        @staticmethod
        def on_any_event(event):
            if event.is_directory or event.event_type not in ['modified', 'created'] or '__pycache__' in event.src_path or not event.src_path.endswith('.py'):
                return None
            if FilesystemHandler.last_updated > (time.time() - .05):
                print('not updating not enough time!!!')
            print(f'Reloading json because: "{event.src_path}" was modified')
            FilesystemHandler.last_updated = time.time()            
            if curr_effects:
                # remove effect
                index = beat_index + curr_effects[0][1]
                effect_name = curr_effects[0][0]
                remove_effect(0)
                if has_song(effect_name):
                    time_in_effect = (time.perf_counter() - time_start) - args.jump_back
                    if not args.jump_back and args.skip_show:
                        time_in_effect = args.skip_show
                    print('Stopped effect')
                    stop_song()

                update_config()

                # add effect
                if has_song(effect_name):
                    if args.speed != 1 and 'song_path' in effects_config[args.show]:
                        effects_config[args.show]['bpm'] *= args.speed
                        effects_config[args.show]['song_path'] = sound_helpers.change_speed_audio_asetrate(effects_config[args.show]['song_path'], args.speed)
                    # adding a delay here stopped a crash for some reason
                    time_in_effect = max(-effects_config[args.show]['skip_song'], time_in_effect)
                    effects_config[args.show]['skip_song'] += time_in_effect
                    effects_config[args.show]['delay_lights'] -= time_in_effect
                    play_song(effect_name)
                add_effect(effect_name)
            else:
                update_config()


    observer = Observer()
    observer.schedule(FilesystemHandler(), python_file_directory, recursive = True)
    observer.start()


http_thread = threading.Thread(target=http_server, args=[], daemon=True)
http_thread.start()
# allows prints from http_server to finish to not mess up terminal output
if args.local:
    time.sleep(.03)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def start_async():
    dj_socket_server = await websockets.serve(init_dj_client, '0.0.0.0', 1337)
    queue_socket_server = await websockets.serve(init_queue_client, '0.0.0.0', 7654)

    if args.show:
        print('Starting show from CLI')
        if args.show in effects_config:
            if args.speed != 1 and 'song_path' in effects_config[args.show]:
                effects_config[args.show]['bpm'] *= args.speed
                effects_config[args.show]['song_path'] = sound_helpers.change_speed_audio_asetrate(effects_config[args.show]['song_path'], args.speed)
                args.skip_show *= 1 / args.speed
                effects_config[args.show]['skip_song'] *= 1 / args.speed
                effects_config[args.show]['delay_lights'] *= 1 / args.speed
            if args.skip_show:
                effects_config[args.show]['skip_song'] += args.skip_show
                effects_config[args.show]['delay_lights'] -= args.skip_show
            song_queue.append([args.show, get_queue_salt()])
            add_effect(args.show)
            play_song(args.show)
        else:
            print(f'{bcolors.FAIL}Couldnt find effect named "{args.show}" in any profile{bcolors.ENDC}')
    asyncio.create_task(light())

    await dj_socket_server.wait_closed() and queue_socket_server.wait_closed()

asyncio.run(start_async())