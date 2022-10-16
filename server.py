import socket
import threading
import time
import json
import signal
import importlib
import pathlib
import asyncio
import http.server
import argparse
import os
import subprocess
from urllib.parse import quote
import hashlib
from copy import deepcopy
import pickle

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import websockets
from tinytag import TinyTag

from helpers import *
import sound_helpers
import youtube_helpers
from users import users

print_blue('Done importing')

parser = argparse.ArgumentParser(description = '')
parser.add_argument('--local', dest='local', default=False, action='store_true')
parser.add_argument('--show', dest='show', type=str, default='')
parser.add_argument('--skip', dest='skip_show_beats', type=float, default=0)
parser.add_argument('--skip_seconds', dest='skip_show_seconds', type=float, default=0)
parser.add_argument('--volume', dest='volume', type=int, default=100)
parser.add_argument('--print_beat', dest='print_beat', default=False, action='store_true')
parser.add_argument('--reload', dest='reload', default=False, action='store_true')
parser.add_argument('--jump_back', dest='jump_back', type=int, default=0)
parser.add_argument('--speed', dest='speed', type=float, default=1)
parser.add_argument('--invert', dest='invert', default=False, action='store_true')
parser.add_argument('--keyboard', dest='keyboard', default=False, action='store_true')
parser.add_argument('--enter', dest='enter', default=False, action='store_true')
parser.add_argument('--autogen', dest='autogen', default=False, action='store_true')
parser.add_argument('--autogen_simple', dest='autogen_simple', default=False, action='store_true')
# bluetooth qc35 headphones are .189 latency
parser.add_argument('--delay', dest='delay_seconds', type=float, default=0.0)


args = parser.parse_args()
if args.autogen_simple:
    args.autogen = True


pca = None

SUB_BEATS = 24
LIGHT_COUNT = 10

curr_effects = []
song_queue = []

curr_bpm = 121
time_start = time.time()
beat_index = 0

light_lock = threading.Lock()
song_lock = threading.Lock()

light_sockets = []
song_sockets = []

song_playing = False
song_time = 0
queue_salt = 0

broadcast_light = False 
broadcast_song = False

download_queue = []
search_queue = []

# pygame.init()
pygame.mixer.init(frequency=48000)


########################################

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)
        
PORT = 9555
local_ip = socket.gethostbyname(socket.gethostname())

def http_server():
    httpd = http.server.ThreadingHTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler)
    print(f'{bcolors.OKGREEN}Dj interface: http://{local_ip}:{PORT}/dj.html')
    print(f'Queue: http://{local_ip}:{PORT}{bcolors.ENDC}', flush=True)
    httpd.serve_forever()


########################################

def add_effect_from_dj(msg):
    global song_time, song_playing, broadcast_song
    effect_name = msg['effect']
    song_time = 0
    if has_song(effect_name):
        song_path = python_file_directory.joinpath(pathlib.Path(effects_config[effect_name]['song_path']))
        if not os.path.exists(song_path):
            print_red(f'Client wanted to play {effect_name}, but the song_path: {song_path} doesnt exist')
            return
        if song_playing and len(song_queue) > 0:
            song_queue.pop()
        song_queue.insert(0, [effect_name, get_queue_salt(), 'DJ'])
        play_song(effect_name)
        song_playing = True
        broadcast_song = True
    add_effect(effect_name)



async def init_dj_client(websocket, path):
    global curr_bpm, time_start, beat_index, song_playing, song_time, broadcast_light, broadcast_song
    print('dj made connection to new client')

    message = {
        'effects': effects_config_client,
        'songs': songs_config,
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
        print('dj sent config to new client')
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

            if msg['type'] == 'add_effect':
                add_effect_from_dj(msg)

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
                update_config_and_lut_from_disk
                #BROKEN

            elif msg['type'] == 'set_bpm':
                time_start = time.time()
                curr_bpm = float(msg['bpm'])
                for effect in curr_effects:
                    effect[1] = 0

            elif msg['type'] == 'inc_time':
                time_start += 0.1

            elif msg['type'] == 'dec_time':
                time_start -= 0.1

            elif msg['type'] == 'inc_time':
                time_start += 0.1

            broadcast_light = True


songs_downloaded_this_process = set()
def download_song(url, uuid):
    download_start_time = time.time() 
    import generate_show

    # time.sleep(20)

    if 'search_query' in url:
        print_yellow(f'user {uuid} entered a url with search_query in it, exiting')
        return None

    max_length_seconds = None
    if not is_admin(uuid):
        max_length_seconds = 15 * 60
    filepath = youtube_helpers.download_youtube_url_to_ogg(url=url, dest_path=python_file_directory.joinpath('songs'), max_length_seconds=max_length_seconds)
    if filepath is None:
        print_yellow('Couldnt download video, returning')
        return
    print(f'finished downloading {url} to {filepath} in {time.time() - download_start_time} seconds')

    add_song_to_config(filepath)
    new_effects = generate_show.generate_show(filepath, channel_lut, effects_config, overwrite=True, simple=False, debug=True)
    if new_effects is None:
        print_red(f'Autogenerator failed to create effect for {url}')
        return

    print(f'passing filepath: {filepath}')
    compile_lut(new_effects)
    effects_config.update(new_effects)
    print(f'created show for: {list(new_effects.keys())}')

    for name, effect in new_effects.items():
        effects_config_client[name] = {}
        for key, value in effect.items():
            if key != 'beats':
                effects_config_client[name][key] = value
        if 'song_path' in effect:
            add_queue_balanced(name, uuid)


async def init_queue_client(websocket, path):
    global curr_bpm, time_start, beat_index, song_playing, song_time, broadcast_light, broadcast_song
    print('queue made connection to new client')

    # this is a lot going over the wire, should we minimize?
    message = {
        'effects': effects_config_client,
        'songs': songs_config,
        'queue': song_queue,
        'users': users,
        'status': {
            'playing': song_playing,
            'time': song_time + (max(pygame.mixer.music.get_pos(), 0) / 1000)
        }
    }
    dump = json.dumps(message)
    try:
        print('queue sent config to new client')
        await websocket.send(dump)
    except:
        print('socket send failed', flush=True)

    song_sockets.append(websocket)

    while True:
        try:
            print('queue waiting for message')
            msg_string = await websocket.recv()
            print('queue waiting for message')
        except:
            for i in range(len(song_sockets)):
                if song_sockets[i] == websocket:
                    song_sockets.pop(i)
                    break
            print('socket recv FAILED - ' + websocket.remote_address[0] + ' : ' + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        print(msg)
        if 'type' in msg:

            if msg['type'] == 'add_queue_back' and 'uuid' in msg:
                uuid = msg['uuid']
                effect_name = msg['effect']
                song_queue.append([effect_name, get_queue_salt(), uuid])
                if len(song_queue) == 1:
                    song_time = 0
                    play_song(effect_name)
                    song_playing = True
                    add_effect(effect_name)
                    broadcast_light = True
            
            elif msg['type'] == 'add_queue_front' and 'uuid' in msg:
                uuid = msg['uuid']
                effect_name = msg['effect']
                if len(song_queue) == 0:
                    song_queue.append([effect_name, get_queue_salt(), uuid])
                else:
                    song_queue.insert(1, [effect_name, get_queue_salt(), uuid])
                if len(song_queue) == 1:
                    song_time = 0
                    play_song(effect_name)
                    song_playing = True
                    add_effect(effect_name)
                    broadcast_light = True

            elif msg['type'] == 'add_queue_balanced' and 'uuid' in msg:
                add_queue_balanced(msg['effect'], msg['uuid'])

            elif msg['type'] == 'remove_queue' and 'uuid' in msg:
                uuid = msg['uuid']
                effect_name = msg['effect']
                salt = msg['salt']
                for i in range(len(song_queue)):
                    if song_queue[i][0] == effect_name and song_queue[i][1] == salt and (song_queue[i][2] == uuid or is_admin(uuid)):
                        song_queue.pop(i)
                        if i == 0:
                            stop_song()
                            song_time = 0
                            index = curr_effect_index(effect_name)
                            if index is not False:
                                remove_effect(index)
                            if song_playing and len(song_queue) > 0:
                                new_effect_name = song_queue[0][0]
                                add_effect(new_effect_name)
                                play_song(new_effect_name)
                            broadcast_light = True
                        break
                if len(song_queue) == 0:
                    song_playing = False

            elif msg['type'] == 'play_queue' and 'uuid' in msg:
                uuid = msg['uuid']
                print(f'----UUID: {uuid}')
                if is_admin(uuid):
                    if len(song_queue) > 0 and not song_playing:
                        effect_name = song_queue[0][0]
                        play_song(effect_name)
                        song_playing = True
                        add_effect(effect_name)
                        broadcast_light = True

            elif msg['type'] == 'pause_queue' and 'uuid' in msg:
                uuid = msg['uuid']
                print(f'----UUID: {uuid}')
                if is_admin(uuid):
                    if len(song_queue) > 0 and song_playing:
                        effect_name = song_queue[0][0]
                        song_time += max(pygame.mixer.music.get_pos(), 0) / 1000
                        stop_song()
                        index = curr_effect_index(effect_name)
                        if index is not False:
                            remove_effect(index)
                        song_playing = False
                        broadcast_light = True

            elif msg['type'] == 'set_time':
                song_time = msg['time']
                if len(song_queue) > 0 and song_playing:
                    effect_name = song_queue[0][0]
                    play_song(effect_name)
                    song_playing = True
                    add_effect(effect_name)
                    broadcast_light = True

            elif msg['type'] == 'download_song' and 'uuid' in msg:
                uuid = msg['uuid']
                url = msg.get('url', None)
                print_blue(f'Adding "{url}" to youtube downloading queue')
                download_queue.append([url, uuid])
                message = {
                    'notification': 'Download Started...'
                }
                dump = json.dumps(message)
                try:
                    await websocket.send(dump)
                except:
                    print('socket send failed', flush=True)

            elif msg['type'] == 'search_song' and 'uuid' in msg:
                uuid = msg['uuid']
                search = msg.get('search', None)
                search_queue.append([search, websocket, False])
            
            broadcast_song = True


def search_youtube():
    search = quote(search_queue[0][0])
    print(f'Query: {search}')
    url = 'https://www.youtube.com/results?search_query=' + search
    print(f'URL: {url}')
    curl = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
    out = curl.stdout.read().decode("utf-8") 
    start = out.find("var ytInitialData = ") + 20
    end = out.find(";</script>", start)
    videos = []
    print(f'start: {start}, end {end}')
    if start >= 0 and end >= 0:
        from os import path
        loc = pathlib.Path(__file__).parent.absolute()
        drink_io_folder = str(loc)
        with open(path.join(drink_io_folder, 'parse.html'), 'w') as f:
            f.write(out[start:end])
        with open(path.join(drink_io_folder, 'full.html'), 'w') as f:
            f.write(out)

        list1 = []
        try:
            dict = json.loads(out[start:end])
            list1 = dict["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]
        except:
            print(f'loading json failed', flush=True)
        for item1 in list1:
            try:
                list2 = item1["itemSectionRenderer"]["contents"]
                for item2 in list2:
                    try:
                        info = item2['videoRenderer']
                        print(info['title']['runs'][0]['text'])
                        videos.append({
                            'title': info['title']['runs'][0]['text'],
                            'channel': info["ownerText"]['runs'][0]['text'],
                            'thumbnail': info['thumbnail']['thumbnails'][0]['url'],
                            'length': info['lengthText']['simpleText'],
                            'views': info['viewCountText']['simpleText'],
                            'id': info['videoId']
                        })
                    except:
                        print(f'parsing 4 failed', flush=True)
            except:
                    print(f'parsing 3 failed', flush=True)
    else:
        print('--- WARNING: JSON NOT FOUND ---')

    message = {
        'search': videos
    }
    search_queue[0][2] = json.dumps(message)


def add_queue_balanced(effect_name, uuid):
    global song_playing, song_time, broadcast_light, broadcast_song
    
    if False: # is_admin(uuid):
        index = 1
        while index < len(song_queue):
            if song_queue[index][2] != uuid:
                break
            index += 1
    else:
        index = 0
        count = 0
        user_counts = {}
        for entry in song_queue:
            user_counts[entry[2]] = 0
            if entry[2] == uuid:
                count += 1
        while index < len(song_queue):
            # ERIC THIS CRASHED IM PUTTIGN IN A CHECK LOL. Should be fixed now
            # if song_queue[index][2] not in user_counts:
            #     print('saving a crash')
            #     user_counts[song_queue[index][2]] = 0
            if user_counts[song_queue[index][2]] > count:
                break
            user_counts[song_queue[index][2]] += 1
            index += 1
    song_queue.insert(index, [effect_name, get_queue_salt(), uuid])
    
    if len(song_queue) == 1:
        song_time = 0
        play_song(effect_name)
        song_playing = True
        add_effect(effect_name)
        broadcast_light = True
        broadcast_song = True


def is_admin(uuid):
    return True
    return uuid in users and users[uuid]['admin']


def get_queue_salt():
    global queue_salt
    queue_salt += 1
    return queue_salt


async def broadcast(sockets, msg):
    for socket in sockets:
        try:
            await socket.send(msg)
        except:
            print(f'socket send failed. socket: {socket}', flush=True)

async def send_config():
    message = {
        'effects': effects_config_client,
        'songs': songs_config,
    }
    await broadcast(light_sockets, json.dumps(message))
    await broadcast(song_sockets, json.dumps(message))


async def send_light_status():
    global broadcast_light
    message = {
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm
        }
    }
    await broadcast(light_sockets, json.dumps(message))
    broadcast_light = False


async def send_song_status():
    global broadcast_song
    message = {
        'queue': song_queue,
        'status': {
            'playing': song_playing,
            'time': song_time + (max(pygame.mixer.music.get_pos(), 0) / 1000)
        }
    }
    await broadcast(song_sockets, json.dumps(message))
    broadcast_song = False


####################################


# terminal specific
if args.local:
    # straight pow(2, 16) to what i think it should be
    green_vals = {
        1: 1,
        .7: .6,
        .6: .4,
        .4: .2,
        .20: .13,
        0.1: .05,
        0: 0,    
    }
    red_vals = {
        1: 1,
        .7: .6,
        .6: .4,
        .4: .2,
        .20: .13,
        0.1: .05,
        0: 0,    
    }
    blue_vals = {
        1: 1,
        .7: .6,
        .6: .4,
        .4: .2,
        .20: .13,
        0.1: .05,
        0: 0,    
    }
    green_vals = {y:x for x, y in green_vals.items()}
    red_vals = {y:x for x, y in red_vals.items()}
    blue_vals = {y:x for x, y in blue_vals.items()}

    # floor to perceieved
    # green_vals = { 1: 1, .9: .95, .5: .70, .4: .60, .3: .45, .2: .30, .15: .25, .14: .2, .13: .18, .12: .15, .11: .1, .1: 0,  0: 0,  }
    # red_vals = { 1: 1,.9: .95,.5: .70,.4: .60,.3: .40,.25: .25,.2: .20,.14: .12,.13: .11,.12: 0, 0: 0, }
    # blue_vals = { 1: 1, .9: .90, .5: .65, .4: .50, .3: .35, .25: .28, .2: .2, .14: .15, .13: .13, .12: .11, .11: 0,  0: 0,  }

    max_num = pow(2, 16) - 1
    def get_interpolated_value(interpolation_dict, value):
        if value == 0:
            return 0
        if 255 <= value:
            return 255

        # print(f'before scale: {value=}')
        value /= 255
        # print(f'after scale: {value=}')
        pairs = sorted([(i, o) for i, o in interpolation_dict.items()])
        for index, (i1, o1) in enumerate(pairs):
            (i2, o2) = pairs[index + 1]
            if value <= pairs[index + 1][0]:
                difference_in_outputs = o2 - o1
                difference_in_inputs = i2 - i1
                difference_in_value = value - i1
                scaling = difference_in_value / difference_in_inputs
                # print(f'({i1=}, {i2=}), ({o1=}, {o2=}), {scaling=}, {difference_in_outputs=}, {difference_in_inputs=}, {difference_in_value=}')
                final_output = 255 * (o1 + (difference_in_outputs * scaling))
                # print(f'got {value}, returning: {final_output}')
                return int(final_output)

    terminal_lut = {'red': [0] * (255 + 1), 'green': [0] * (255 + 1), 'blue': [0] * (255 + 1)}
    for i in range(255 + 1):
        terminal_lut['red'][i] = get_interpolated_value(red_vals, i)
        terminal_lut['green'][i] = get_interpolated_value(green_vals, i)
        terminal_lut['blue'][i] = get_interpolated_value(blue_vals, i)
    purple = [153, 50, 204]
    terminal_size = os.get_terminal_size().columns


def get_sub_effect_names(effect_name, beat):
    sub_effect_names = []
    effect_beats = effects_config[effect_name]['beats']
    for effect in effect_beats:
        if effect[0] <= beat <= effect[0] + effect[2]:
            sub_effect_names.append(effect[1])
        elif sub_effect_names:
            break
    return sub_effect_names


last_extra_lines = None
async def render_to_terminal(all_levels):
    global last_extra_lines
    curr_beat = (beat_index / SUB_BEATS) + 1
    dead_space = terminal_size - 15

    show_specific = ''
    all_effect_names = []
    for effect in curr_effects:
        effect_name = effect[0]

        # if has_song(effect[0]):
        #     all_effect_names += get_sub_effect_names(effect[0], curr_beat)
        if has_song(effect_name):
            channel_lut_index = (beat_index + effect[1])
            show_specific = f"""\
, Show {round(100 * (channel_lut_index / channel_lut[effect_name]['length']))}%\
"""
            all_effect_names += get_sub_effect_names(effect_name, curr_beat)
        else:
            all_effect_names.append(effect[0])
            # getting duration thru the song
            # time_diff = time.time() - time_start
            # song_path = effects_config[effect_name]['song_path']
            # if 'song_path' in songs_config:
            #     f", {round(100 * (time_diff / songs_config[song_path]['duration']))}% song"

# Seconds: {round(time.time() - time_start, 2):.2f}\

    useful_info = f"""\
BPM {curr_bpm:.1f}, \
Beat {curr_beat:.1f}\
{show_specific}\
"""
    
    # size_of_current_line = len(useful_info) - (terminal_size * (len(useful_info) // terminal_size))
    size_of_current_line = len(useful_info) % (terminal_size + 1)
    chars_until_end_of_line = terminal_size - size_of_current_line
    # print(f'{size_of_current_line=}, {chars_until_end_of_line=}, {terminal_size=}')
    useful_info += ' ' * chars_until_end_of_line
    extra_lines_up = (len(useful_info) // (terminal_size + 1)) + 1
    # if last_extra_lines is not None and last_extra_lines > extra_lines_up:
    #     print(f'{" " * dead_space}\n' * (last_extra_lines - extra_lines_up))
        # print(f'last_extra_lines: {last_extra_lines}, extra_lines_up: {extra_lines_up}')
        # exit()

    last_extra_lines = extra_lines_up


    # print('pre 255:', list(map(lambda x: x / max_num, all_levels)))
    levels_255 = list(map(lambda x: int((x / max_num) * 255), all_levels))
    # print('after 255:', levels_255)
    levels_255[0] = terminal_lut['red'][levels_255[0]]
    levels_255[1] = terminal_lut['green'][levels_255[1]]
    levels_255[2] = terminal_lut['blue'][levels_255[2]]
    levels_255[3] = terminal_lut['red'][levels_255[3]]
    levels_255[4] = terminal_lut['green'][levels_255[4]]
    levels_255[5] = terminal_lut['blue'][levels_255[5]]
    # print('after terminal lut', levels_255)

    # uv_level_scaling = min(1, levels_255[6] / 255.0)
    purple_scaled = list(map(lambda x: int(x * (levels_255[9] / 255)), purple))

    uv_style = f'rgb({purple_scaled[0]},{purple_scaled[1]},{purple_scaled[2]})'    
    top_front_rgb_style = f'rgb({levels_255[0]},{levels_255[1]},{levels_255[2]})'
    top_back_rgb_style = f'rgb({levels_255[3]},{levels_255[4]},{levels_255[5]})'
    bottom_rgb_style = f'rgb({levels_255[6]},{levels_255[7]},{levels_255[8]})'


    # print(useful_info)
    #  + (' ' * (terminal_size - len(useful_info)))

    effect_string = f'Effects: {", ".join(all_effect_names)}'
    remaining = terminal_size - len(effect_string) 
    console.print(effect_string + (' ' * max(0, remaining)), no_wrap=True, overflow='ellipsis', end='\n')
    console.print(useful_info, no_wrap=True, overflow='ellipsis', end='\n')

    character = '▆'
    console.print(' ' + character * 2, style=uv_style, end='')
    console.print(character * 5, style=top_front_rgb_style, end='')
    console.print(character * 5, style=top_back_rgb_style, end='')
    console.print(character * 2 + (' ' * dead_space), style=uv_style, end='')
    console.print('\n', end='')
    console.print(f'{" " * (terminal_size - 1)}\n' * 3, end='')

    console.print(' ' + character * 14 + (' ' * dead_space), style=bottom_rgb_style, end='')

    console.print('', end='\033[F' * 6)


all_levels = [0] * LIGHT_COUNT
async def terminal(level, i):
    all_levels[i] = level
    if i == LIGHT_COUNT - 1:
        await render_to_terminal(all_levels)


####################################

async def light():
    global beat_index, song_playing, song_time, broadcast_song, broadcast_light

    download_thread = None
    search_thread = None

    while True:

        rate = curr_bpm / 60 * SUB_BEATS
        time_diff = time.time() - time_start
        beat_index = int(time_diff * rate)       
            
        i = 0
        while i < len(curr_effects):
            index = beat_index + curr_effects[i][1]
            effect_name = curr_effects[i][0]
            if not channel_lut[effect_name]['loop'] and index >= channel_lut[effect_name]['length']:
                remove_effect(i)
                if has_song(effect_name):
                    stop_song()
                    song_queue.pop(0)
                    song_time = 0
                    if song_playing and len(song_queue) > 0:
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
                effect_name = curr_effects[j][0]
                index = beat_index + curr_effects[j][1]
                
                # print(effect_name)
                if 'rotate_color' in effects_config[effect_name]:
                    print('rotating!!')
                
                if index >= 0 and (channel_lut[effect_name]['loop'] or index < channel_lut[effect_name]['length']):
                    index = index % channel_lut[effect_name]['length']
                    level += channel_lut[effect_name]['beats'][index][i]

                

            level_bounded = max(0, min(0xFFFF, level * 0xFFFF / 100))
            level_between_0_and_1 = level_bounded / 0xFFFF
            
            # gamma curve
            level_scaled = round(pow(level_between_0_and_1, 2.2) * 0xFFFF)
            # level_scaled = round(level_bounded)

            if args.local:
                await terminal(level_bounded, i)
            else:
                pca.channels[i].duty_cycle = level_scaled


        if download_thread is not None:
            if not download_thread.is_alive():
                await send_config()
                download_thread = None
        elif download_queue:
            url, uuid = download_queue.pop(0)
            print_blue(f'Starting download of {url} from client {uuid}')
            download_thread = threading.Thread(target=download_song, args=(url, uuid))
            download_thread.start()

        if search_thread is not None:
            if not search_thread.is_alive():
                await broadcast([search_queue[0][1]], search_queue[0][2])
                search_queue.pop(0)
                search_thread = None
        elif len(search_queue) > 0:
            search_thread = threading.Thread(target=search_youtube, args=())
            search_thread.start()

        if broadcast_light:
            await send_light_status()
        if broadcast_song:
            await send_song_status()

        if args.print_beat and not args.local and beat_index % SUB_BEATS == 0:
            print(f'Beat: {(beat_index // SUB_BEATS) + 1}, Seconds: {time_diff:.3f}')

        time_diff = time.time() - time_start
        time_delay = ((beat_index + 1) / rate) - time_diff

        # if beat_index % SUB_BEATS == 0:
        #     print(f'{beat_index=}, {time_diff=}')
            # avg = 0
        # else:
        #     print(beat_index)
        #     avg += time_diff

        await asyncio.sleep(time_delay)

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
    while len(curr_effects) > 0:
        remove_effect(0)

def add_effect(name):
    global beat_index, time_start, curr_bpm

    effect = effects_config[name]
    if (effect['trigger'] == 'toggle' or effect['trigger'] == 'hold') and curr_effect_index(name) is not False:
        return

    if 'bpm' in effect:
        clear_effects()
        time_start = time.time() + effect['delay_lights'] - song_time
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


def play_song(effect_name, print_out=True):
    song_path = effects_config[effect_name]['song_path']
    skip = effects_config[effect_name]['skip_song'] + song_time
    pygame.mixer.music.set_volume(args.volume)

    pygame.mixer.music.load(pathlib.Path(song_path))

    # ffmpeg -i songs/musician2.mp3 -c:a libvorbis -q:a 4 songs/musician2.ogg
    # python server.py --local --show "shelter" --skip 215
    # ffplay songs/shelter.mp3 -ss 215 -nodisp -autoexit
    if print_out:
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
effects_config_client = {}
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

def add_song_to_config(filepath):
    if filepath.suffix in ['.mp3', '.ogg', '.wav']:
        tags = TinyTag.get(filepath)
        name = tags.title
        artist = tags.artist
        duration = tags.duration

        if tags.samplerate != 48000:
            print_red(f'this shit song aint 48000 fam, {filepath}')
            return False

        if name == None:
            name = filepath.stem

        if not duration:
            print_yellow(f'No tag found for file: "{filepath}", ffprobing, but this is slow')
            duration = sound_helpers.get_audio_clip_length(filepath)
        relative_path = filepath
        if relative_path.is_absolute():
            relative_path = relative_path.relative_to(python_file_directory)
        
        songs_config[str(relative_path)] = {
            'name': name,
            'artist': artist,
            'duration': duration
        }
    else:
        print_red(f'CANNOT READ FILETYPE {filepath.suffix} in {filepath}')
        return False
    return True

all_globals = globals()
def update_config_and_lut_from_disk():
    global effects_config, effects_config_client, songs_config, channel_lut, graph, found

    channel_lut = {}
    effects_config = {}
    effects_config_client = {}
    songs_config = {}

    graph = {}
    found = {}

    # begin_perf_timer = time.time()
    effects_dir = python_file_directory.joinpath('effects')
    for name, filepath in get_all_paths(effects_dir, only_files=True) + get_all_paths(effects_dir.joinpath('autogen_shows'), only_files=True):
        relative_path = filepath.relative_to(python_file_directory)
        without_suffix = relative_path.parent.joinpath(relative_path.stem)
        module_name = str(without_suffix).replace(os.sep, '.')
        if module_name in all_globals:
            importlib.reload(all_globals[module_name])
        else:
            all_globals[module_name] = importlib.import_module(module_name)

        effects_config.update(all_globals[module_name].effects)

    song_dir = python_file_directory.joinpath('songs')
    for name, filepath in get_all_paths('songs', only_files=True):
        add_song_to_config(filepath)
    compile_lut(effects_config)

    for name, effect in effects_config.items():
        effects_config_client[name] = {}
        for key, value in effect.items():
            if key != 'beats':
                effects_config_client[name][key] = value


def set_effect_defaults(local_effects_config):
    for effect_name, effect in local_effects_config.items():
        if 'snap' not in effect:
            effect['snap'] = 1 / SUB_BEATS
        else:
            effect['snap'] = max(effect['snap'], 1 / SUB_BEATS)
        if 'trigger' not in effect:
            effect['trigger'] = 'toggle'
        if 'profiles' not in effect:
            effect['profiles'] = []
        if 'song_path' in effect:
            effect['song_path'] = str(pathlib.Path(effect['song_path']))
        if 'song_path' in effect and effect['song_path'] not in songs_config:
            del effect['song_path']
        if 'song_path' in effect and effect['song_path'] in songs_config:
            if 'bpm' not in effect:
                print_red('song effects must have bpm\n' * 10)
                exit()
            effect['delay_lights'] = effect.get('delay_lights', 0)
            if not args.local:
                effect['delay_lights'] += 0.1
            if args.delay_seconds:
                effect['delay_lights'] += args.delay_seconds
            if 'length' not in effect:
                effect['length'] = songs_config[effect['song_path']]['duration'] * effect['bpm'] / 60
            if 'loop' not in effect:
                effect['loop'] = False
        else:
            if 'loop' not in effect:
                effect['loop'] = True

    for effect_name in local_effects_config:
        if 'song_path' not in local_effects_config[effect_name]:
            local_effects_config[effect_name]['profiles'].append('All Effects')
    

def get_effect_hash(effect_name, effect):
    copied_effect = {}
    for key, item in effect.items():
        if 'cache' not in key:
            copied_effect[key] = item
    
    the_str = json.dumps(copied_effect, sort_keys=True)
    return hashlib.md5(the_str.encode()).hexdigest()


lut_cache_dir = python_file_directory.joinpath('lut_cache')
def cache_assign_dirty(local_effects_config):
    lmao = 0
    if not os.path.exists(lut_cache_dir):
        print(f'making directory {lut_cache_dir}')
        os.mkdir(lut_cache_dir)

    for effect_name, effect in local_effects_config.items():
        effect_cache_filepath = lut_cache_dir.joinpath(effect_name)
        
        effect['cache_dirty'] = True
        if os.path.exists(effect_cache_filepath):
            with open(effect_cache_filepath, 'r') as f:
                if get_effect_hash(effect_name, effect) == f.read().strip():
                    effect['cache_dirty'] = False
                    with open(str(effect_cache_filepath) + '.pickle', 'r') as pf:
                        effect['cache_lut'] = pickle.load(pf)
                else:
                    print_yellow(f'{effect_name} is dirty')
    
    for effect_name, effect in local_effects_config.items():
        dfs_dirty_cache(effect_name)

    print('timing', lmao)

cache_dfs_seen = {}
def dfs_dirty_cache(effect_name):
    if effect_name in cache_dfs_seen:
        return cache_dfs_seen[effect_name]
    dirty = effects_config[effect_name]['cache_dirty']
    for sub_effect in graph[effect_name]:
        dirty = dirty or dfs_dirty_cache(sub_effect)
    cache_dfs_seen[effect_name] = dirty
    return dirty


def compile_lut(local_effects_config):
    global channel_lut, simple_effects, complex_effects

    simple_effects = []
    complex_effects = []

    cache_and_graph_perf_timer = time.time()
    for effect_name, effect in local_effects_config.items():
        graph[effect_name] = {}
        for component in effect['beats']:
            if type(component[1]) is str:
                graph[effect_name][component[1]] = True
        graph[effect_name] = list(graph[effect_name].keys())

    for effect_name in graph:
        effects_config_sort([effect_name])

    set_effect_defaults(local_effects_config)
    cache_assign_dirty(local_effects_config)
    print_cyan(f'Cache and graph: {time.time() - cache_and_graph_perf_timer:.3f} seconds')

    simple_effect_perf_timer = time.time()
    for effect_name in simple_effects:
        effect = local_effects_config[effect_name]

        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * LIGHT_COUNT] * round(effect['length'] * SUB_BEATS)],
            # 'beats': numpy.zeros((round(effect['length'] * SUB_BEATS), LIGHT_COUNT)),
        }
        for component in effect['beats']:
            start_beat = round((component[0] - 1) * SUB_BEATS)
            channels = component[1]
            
            if len(channels) == 4:
                channels[3:3] = channels[0:3]
            if len(channels) == 7:
                channels[3:3] = channels[0:3]

            if len(component) == 2:
                component.append(effect['length'])
            if len(component) == 3:
                component.append(1)
            if len(component) == 4:
                component.append(1)

            length = round(min(component[2] * SUB_BEATS, channel_lut[effect_name]['length'] - start_beat))
            start_mult = component[3]
            end_mult = component[4]

            for i in range(length):
                if length == 1:
                    mult = start_mult
                else:
                    mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                for x in range(LIGHT_COUNT):
                    channel_lut[effect_name]['beats'][start_beat + i][x] += channels[x] * mult
                if args.invert:
                    tmp = channel_lut[effect_name]['beats'][start_beat + i]
                    tmp[3] = tmp[6]
                    tmp[4] = tmp[7]
                    tmp[5] = tmp[8]
                    tmp[0], tmp[6] = tmp[6], tmp[0]
                    tmp[1], tmp[7] = tmp[7], tmp[1]
                    tmp[2], tmp[8] = tmp[8], tmp[2]
    print_cyan(f'Simple effects: {time.time() - simple_effect_perf_timer:.3f} seconds')

    complex_effect_perf_timer = time.time()
    for effect_name in complex_effects:
        effect = local_effects_config[effect_name]
        if not effect['cache_dirty']:
            channel_lut[effect_name] = effect['cache_lut']
            continue

        og_effect = deepcopy(effect)

        # if length isn't specified, generate a length
        calced_effect_length = 0
        for component in effect['beats']:
            start_beat = component[0] - 1
            name = component[1]
            if len(component) == 2:
                if local_effects_config[name]['loop']:
                    component.append(effect['length'] - start_beat)
                else:
                    component.append(local_effects_config[name]['length'])
            if len(component) == 3:
                component.append(1)
            if len(component) == 4:
                component.append(1)
            if len(component) == 5:
                component.append(0)
            calced_effect_length = max(calced_effect_length, start_beat + component[2])

        if 'length' not in effect:
            effect['length'] = calced_effect_length

        # this is 20% of time
        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * LIGHT_COUNT] * round(effect['length'] * SUB_BEATS)],
            # 'beats': numpy.zeros((round(effect['length'] * SUB_BEATS), LIGHT_COUNT)),
        }
        beats = channel_lut[effect_name]['beats']

        
        for component in effect['beats']:
            start_beat = round((component[0] - 1) * SUB_BEATS)
            reference_name = component[1]
            reference_beats = channel_lut[reference_name]['beats']
            reference_length = channel_lut[reference_name]['length']

            length = round(min(component[2] * SUB_BEATS, channel_lut[effect_name]['length'] - start_beat))
            start_mult = component[3]
            end_mult = component[4]
            offset = round(component[5] * SUB_BEATS)

            for i in range(length):
                reference_channels = reference_beats[(i + offset) % reference_length]
                if any(reference_channels):
                    final_channel = beats[start_beat + i]

                    if length == 1:
                        mult = start_mult
                    else:
                        mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))

                    for x in range(LIGHT_COUNT):
                        final_channel[x] += reference_channels[x] * mult

        effect_cache_filepath = lut_cache_dir.joinpath(effect_name)
        print(f'{effect_name} was dirty, dumping to {effect_cache_filepath.relative_to(python_file_directory)}')
        with open(effect_cache_filepath, 'w') as f:
            f.writelines([get_effect_hash(effect_name, og_effect)])

        with open(str(effect_cache_filepath) + '.pickle', 'w') as f:
            f.dump(get_effect_hash(effect_name, og_effect))


    print_cyan(f'Complex effects: {time.time() - complex_effect_perf_timer:.3f} seconds')


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


#################################################

def fuzzy_find(name, valid_names, filter_words=None):
    name = name.lower()
    all_candidates = []
    if filter_words:
        valid_names = list(filter(lambda x: any([y in x.lower() for y in filter_words]), valid_names))
    valid_names = [x for x in valid_names if x[-5:] != '.webm']
    lower_to_real = {x.lower():x for x in valid_names}
    for show_name in lower_to_real:
        if name in show_name:
            all_candidates.append(lower_to_real[show_name])
    if not all_candidates:
        print(f'{bcolors.FAIL}No shows for "{name}" were found{bcolors.ENDC}')
        exit()
    if len(all_candidates) > 1:
        print(f'{bcolors.FAIL}Too many candidates for show "{name}" {all_candidates}{bcolors.ENDC}')
        exit()
    return all_candidates[0]

#################################################




if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


    args.volume = args.volume / 100
    if args.local:
        from rich.console import Console
        console = Console()
    else:
        setup_gpio()

    update_config_and_lut_from_disk()

    # testing the youtube downloading
    # the_thread = threading.Thread(target=download_song, args=('https://www.youtube.com/watch?v=tAhT6kFWkAo',))
    # the_thread.start()


    if args.autogen:
        autogenerated_effects = {}
        import generate_show

        if args.show:
            song_path = pathlib.Path('songs').joinpath(fuzzy_find(args.show, list(os.listdir('songs'))))
            new_effect = generate_show.generate_show(song_path, channel_lut,  effects_config, overwrite=True, simple=args.autogen_simple)
            autogenerated_effects.update(new_effect)
            effect_name = list(new_effect.keys())[0]
            args.show = effect_name
        else:
            print(f'{bcolors.WARNING}AUTOGENERATING ALL SHOWS IN DIRECTORY{bcolors.ENDC}')
            for name, path in get_all_paths('songs', only_files=True):
                new_effect = generate_show.generate_show(path, channel_lut,  effects_config, overwrite=True, simple=args.autogen_simple, debug=False)
                if new_effect is not None:
                    autogenerated_effects.update(new_effect)    
        update_config_and_lut_from_disk()


    def detailed_output_on_enter():
        global beat_index
        while True:
            input()
            all_effect_names = []

            curr_beat = (beat_index / SUB_BEATS) + 1
            for effect in curr_effects:
                if has_song(effect[0]):
                    all_effect_names += get_sub_effect_names(effect[0], curr_beat)
                else:
                    all_effect_names.append(effect[0])
            
            print(f'beat: {curr_beat:2f}, current_effects playing: {all_effect_names}')


    if args.enter:
        x = threading.Thread(target=detailed_output_on_enter)
        x.start()



    originals = {}
    def restart_show(reload=False, skip=0):
        if curr_effects:
            effect_name = curr_effects[0][0]
            remove_effect(0)
            time_to_skip_to = max(0, (time.time() - time_start) + skip)
            stop_song()


            if effect_name not in originals:
                originals[effect_name] = {
                    'skip_song': effects_config[effect_name]['skip_song'],
                    'delay_lights': effects_config[effect_name]['delay_lights'],
                    'bpm': effects_config[effect_name]['bpm'],
                    'song_path': effects_config[effect_name]['song_path'],
                }
            if reload:
                update_config_and_lut_from_disk()

            effects_config[effect_name]['bpm'] = originals[effect_name]['bpm']
            effects_config[effect_name]['song_path'] = originals[effect_name]['song_path']
            effects_config[effect_name]['skip_song'] = originals[effect_name]['skip_song'] + time_to_skip_to
            effects_config[effect_name]['delay_lights'] = originals[effect_name]['delay_lights'] - time_to_skip_to
            # original_delays[effect_name] = effects_config[effect_name]['delay_lights']
            # effects_config[effect_name]['skip_song'] = time_to_skip_to
            # effects_config[effect_name]['delay_lights'] = time_to_skip_to - originals[effect_name]
            play_song(effect_name, print_out=False)
            add_effect(effect_name)
        elif reload:
            update_config_and_lut_from_disk()


    if args.reload:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

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
                restart_show(True, -args.jump_back)

        observer = Observer()
        observer.schedule(FilesystemHandler(), python_file_directory, recursive = True)
        observer.start()



    if args.keyboard:
        from pynput.keyboard import Key, Listener, KeyCode

        if is_linux():
            _return_code, stdout, _stderr = run_command_blocking([
                'xdotool',
                'getactivewindow',
            ])
            process_window_id = int(stdout.strip())

        skip_time = 5
        keyboard_dict = {
            # 'd': 'Red top',
            # 'f': 'Cyan top',
            # 'j': 'Blue bottom',
            # 'k': 'Green bottom',
            'left': lambda: restart_show(False, -skip_time),
            'right': lambda: restart_show(False, skip_time),
            # 'space': 'UV',
        }
        # https://stackoverflow.com/questions/24072790/how-to-detect-key-presses how to check window name (not global)

        def window_focus():
            if is_linux():
                _return_code, stdout, _stderr = run_command_blocking([
                    'xdotool',
                    'getwindowfocus',
                ])
                other = int(stdout.strip())
                return process_window_id == other
            return True

        def on_press(key):
            if not window_focus():
                return

            if type(key) == KeyCode:
                key_name = key.char
            else:
                key_name = key.name
            if key_name in keyboard_dict:
                if type(keyboard_dict[key_name]) == str:
                    add_effect(keyboard_dict[key_name])
                else:
                    keyboard_dict[key_name]()

        def on_release(key):
            if not window_focus():
                return

            if type(key) == KeyCode:
                key_name = key.char
            else:
                key_name = key.name
            if key_name in keyboard_dict:
                if type(keyboard_dict[key_name]) == str:
                    remove_effect(curr_effect_index(keyboard_dict[key_name]))

        def listen_for_keystrokes():
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

        keyboard_thread = threading.Thread(target=listen_for_keystrokes, args=[], daemon=True)
        keyboard_thread.start()



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
        print(f'{bcolors.OKGREEN}started websocket servers{bcolors.ENDC}')

        if args.show:
            args.show = fuzzy_find(args.show, list(effects_config.keys()), filter_words=['show', 'g_'])
            print('Starting show from CLI')
            if args.show in effects_config:
                if args.speed != 1 and 'song_path' in effects_config[args.show]:
                    effects_config[args.show]['bpm'] *= args.speed
                    effects_config[args.show]['song_path'] = str(sound_helpers.change_speed_audio_asetrate(effects_config[args.show]['song_path'], args.speed))
                    args.skip_show_seconds *= 1 / args.speed
                    args.delay_seconds *= 1 / args.speed
                    effects_config[args.show]['skip_song'] *= 1 / args.speed
                    effects_config[args.show]['delay_lights'] *= 1 / args.speed
                if args.skip_show_beats:
                    args.skip_show_seconds = (args.skip_show_beats - 1) * (60 / effects_config[args.show]['bpm'])
                if args.skip_show_seconds:
                    effects_config[args.show]['skip_song'] += args.skip_show_seconds
                    effects_config[args.show]['delay_lights'] -= args.skip_show_seconds
                song_queue.append([args.show, get_queue_salt(), 'CLI'])
                add_effect(args.show)
                play_song(args.show)
            else:
                print(f'{bcolors.FAIL}Couldnt find effect named "{args.show}" in any profile{bcolors.ENDC}')
        asyncio.create_task(light())

        await dj_socket_server.wait_closed() and queue_socket_server.wait_closed()

    asyncio.run(start_async())







# old compile stuff

# numpy stuff
# final_channel += channels
# final_channel *= mult
# trying to optimize
# final_channel = list((x + y) * mult for x, y in zip(final_channel, channels))



# starter = time.time()
# block += time.time() - starter
# print(f'time spent in block: {block}')