import time
first_start_time = time.time()
import socket
import threading
import json
import signal
import importlib
import pathlib
import asyncio
import argparse
import os
import colorsys
import random
import traceback
import sys
print(f'Up to stdlib import: {time.time() - first_start_time:.3f}')

from helpers import *

# https://wiki.libsdl.org/SDL2/FAQUsingSDL
# os.environ['SDL_AUDIODRIVER'] = 'jack'

# also i tried
    # sudo apt-get update
    # sudo apt-get install alsa-utils
    # sudo modprobe snd_bcm2835
    # sudo apt-get install avahi-utils
    # sudo reboot
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import websockets
print(f'Up to pip import: {time.time() - first_start_time:.3f}')

print_cyan(f'Up to custom import: {time.time() - first_start_time:.3f}')
import sound_helpers
import youtube_helpers
from users import users
print_cyan(f'Up to custom import: {time.time() - first_start_time:.3f}')


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
parser.add_argument('--autogen', dest='autogen', nargs="?", type=str, const='all')
parser.add_argument('--autogen_mode', dest='autogen_mode', default='both')
parser.add_argument('--delay', dest='delay_seconds', type=float, default=0.0) #bluetooth qc35 headphones are .189 latency
parser.add_argument('--watch', dest='load_new_rekordbox_shows_live', default=False, action='store_true')
args = parser.parse_args()


this_file_directory = pathlib.Path(__file__).parent.resolve()
effects_dir = this_file_directory.joinpath('effects')

pca = None

SUB_BEATS = 24
LIGHT_COUNT = 16

curr_effects = []
song_queue = []

originals = {}

curr_bpm = 121
time_start = time.time()
beat_index = 0

light_lock, song_lock = threading.Lock(), threading.Lock() 
light_sockets, song_sockets, dev_sockets = [], [], []

song_playing = False
song_time = 0
queue_salt = 0

broadcast_light_status = False 
broadcast_song_status = False

download_queue, search_queue = [], []

printed_http_info = False


########################################

# class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def end_headers(self):
#         self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
#         self.send_header("Pragma", "no-cache")
#         self.send_header("Expires", "0")
#         self.send_header('Access-Control-Allow-Origin', '*')
#         http.server.SimpleHTTPRequestHandler.end_headers(self)
        
PORT = 9555
try:
    local_ip = socket.gethostbyname(socket.gethostname())
except:
    local_ip = 'cant_resolve_hostbyname'

def run_http_server_forever():
    global printed_http_info
    import http.server
    httpd = http.server.ThreadingHTTPServer(('', PORT), http.server.SimpleHTTPRequestHandler)
    print_green(f'Dj interface: http://{local_ip}:{PORT}/dj.html\nQueue: http://{local_ip}:{PORT}', flush=True)
    printed_http_info = True
    httpd.serve_forever()


########################################

def add_effect_from_dj(effect_name):
    global song_time, broadcast_song_status
    song_time = 0
    add_effect(effect_name)
    if has_song(effect_name):
        song_path = this_file_directory.joinpath(pathlib.Path(effects_config[effect_name]['song_path']))
        if not os.path.exists(song_path):
            print_red(f'Client wanted to play {effect_name}, but the song_path: {song_path} doesnt exist')
            return
        if song_playing and len(song_queue) > 0:
            song_queue.pop()
        song_queue.insert(0, [effect_name, get_queue_salt(), 'DJ'])
        play_song(effect_name)
        broadcast_song_status = True


laser_mode = False
rekordbox_bpm = None
rekordbox_time = None
rekordbox_original_bpm = None
take_rekordbox_input = False
rekordbox_effect_name = None
async def init_rekordbox_bridge_client(websocket, path):
    global rekordbox_bpm, rekordbox_original_bpm, rekordbox_time, time_start, curr_bpm, song_time, take_rekordbox_input, song_playing, broadcast_song_status, song_name_to_show_names, rekordbox_effect_name
    print('rekordbox made connection to new client')
    rekordbox_title = None
    while True:
        try:
            msg_string = await websocket.recv()
        except:
            print('socket recv FAILED - ' + websocket.remote_address[0] + ' : ' + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'title' in msg and 'original_bpm' in msg:
            stop_song()
            broadcast_song_status = True

            print('Taking rekordbox input')
            take_rekordbox_input = True
            rekordbox_title = msg['title']
            rekordbox_original_bpm = float(msg['original_bpm'])

            # !TODO change all this nonsense so we dont have to have rekordbox and autogenerated folders
            handmade_song_found = False
            if rekordbox_title in song_name_to_show_names:
                for effect_name in song_name_to_show_names[rekordbox_title]:
                    if not effect_name.startswith('g_'):
                        print_green(f'Found: {len(song_name_to_show_names[rekordbox_title])} effects with the song "{rekordbox_title}"\n')
                        print_green(f'Picked first non "g_" from: {song_name_to_show_names[rekordbox_title]}, aka "{effect_name}"\n')
                        rekordbox_effect_name = effect_name
                        handmade_song_found = True
                        break
            if not handmade_song_found:
                rekordbox_effect_name = 'g_' + rekordbox_title
                print(f'Couldnt find handmade song "{rekordbox_title}", looking for an effect named "{rekordbox_effect_name}"\n')
                if rekordbox_effect_name not in effects_config:
                    print_yellow(f'Cant play autogenerated light show effect from rekordbox! Missing effect {rekordbox_effect_name}\n')
                    rekordbox_effect_name = None
            

            if rekordbox_effect_name is not None:
                print_green(f'Playing light show effect from rekordbox: {rekordbox_effect_name}\n')
                clear_effects()
                song_time = 0
                add_effect(rekordbox_effect_name)

        # print(f'{list(msg.keys())}\n' * 10)

        # !TODO this still gets SPAMMMED by the rekordbox bridge, just iffing around it
        if take_rekordbox_input:
            if rekordbox_effect_name is None:
                print_yellow(f'Cant update rekordbox time and bpm! Missing effect {rekordbox_title}\n' * 8)  
                continue


            if 'master_time' in msg and 'master_bpm' in msg and 'timestamp' in msg:
                # print(f'Time delay from bridge: {time.time() - float(msg["timestamp"])}')
                rekordbox_time, rekordbox_bpm = float(msg['master_time']), float(msg['master_bpm'])
                # print(f'master_bpm recieved: {rekordbox_bpm}, master_time recieved: {rekordbox_time}')
                if rekordbox_bpm >= 0:
                    rekordbox_bpm = max(.1, rekordbox_bpm)
                else:
                    rekordbox_bpm = min(-.1, rekordbox_bpm)
                curr_bpm = rekordbox_bpm
                time_start = time.time() - ((rekordbox_time - effects_config[rekordbox_effect_name]['delay_lights']) * (rekordbox_original_bpm / rekordbox_bpm))
                            


async def init_dj_client(websocket, path):
    global curr_bpm, time_start, song_playing, song_time, broadcast_light_status, broadcast_song_status, laser_mode
    print('DJ Client: made connection to new client')

    message = {
        'effects': effects_config_client,
        'songs': songs_config,
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm,
            'laser_mode': laser_mode,
        }
    }
    dump = json.dumps(message)
    try:
        await websocket.send(dump)
        print('DJ Client: sent config to new client')
    except:
        print('DJ Client: socket send failed', flush=True)

    light_sockets.append(websocket)

    while True:
        try:
            msg_string = await websocket.recv()
        except:
            light_sockets.remove(websocket)
            if websocket in dev_sockets:
                dev_sockets.remove(websocket)
            print('DJ Client: socket recv FAILED - ' + websocket.remote_address[0] + ' : ' + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        if 'type' in msg:
            if msg['type'] == 'add_effect':
                add_effect_from_dj(msg['effect'])

            elif msg['type'] == 'remove_effect':
                effect_name = msg['effect']
                # if has_song(effect_name):
                #     if song_playing and len(song_queue) > 0:
                #         song_queue.pop()
                #     stop_song()
                #     broadcast_song_status = True
                remove_effect_name(effect_name)

            elif msg['type'] == 'clear_effects':
                clear_effects()
                stop_song()

            elif msg['type'] == 'toggle_dev_mode':
                if websocket in dev_sockets:
                    print(f'Turned dev mode off')
                    dev_sockets.remove(websocket)
                else:
                    print(f'Turned dev mode on')
                    dev_sockets.append(websocket)

            elif msg['type'] == 'toggle_laser_mode':
                laser_mode = not laser_mode
                print(f'Toggled laser mode, now in state: {laser_mode}\n')
                if curr_effects:
                    maybe_new_effect_name = maybe_get_laser_version(curr_effects[0][0])
                    if maybe_new_effect_name not in channel_lut:
                        print_green(f'late lut compiling {maybe_new_effect_name}')
                        compile_lut({maybe_new_effect_name: effects_config[maybe_new_effect_name]})
                    curr_effects[0][0] = maybe_new_effect_name

            # elif msg['type'] == 'set_bpm':
            #     time_start = time.time()
            #     curr_bpm = float(msg['bpm'])
            #     for effect in curr_effects:
            #         effect[1] = 0

            broadcast_light_status = True


def download_song(url, uuid):
    from copy import deepcopy

    download_start_time = time.time()
    import autogen

    if 'search_query' in url:
        print_yellow(f'user {uuid_to_user(uuid)} entered a url with search_query in it, returning')
        return None

    max_length_seconds = None
    if not is_admin(uuid):
        max_length_seconds = 15 * 60
    
    # TODO add caching here
    filepath = youtube_helpers.download_youtube_url(url=url, dest_path=this_file_directory.joinpath('songs'), max_length_seconds=max_length_seconds)
    if filepath is None:
        print_yellow('Couldnt download video, returning')
        return
    print(f'finished downloading {url} to {filepath} in {time.time() - download_start_time} seconds')

    add_song_to_config(filepath)

    added = False
    # !TODO testing this for the audio glitch
    src_bpm_offset_cache = autogen.get_src_bpm_offset_multiprocess(filepath, use_boundaries=True) 
    # src_bpm_offset_cache = autogen.get_src_bpm_offset(filepath, use_boundaries=True) 
    for mode in [None, 'lasers']:
        show_name, show, _ = autogen.generate_show(filepath, overwrite=True, mode=mode, src_bpm_offset_cache=deepcopy(src_bpm_offset_cache))
        if show is None:
            print_red(f'Autogenerator failed to create effect for {url}')
            return

        print(f'passing filepath: {filepath}')
        effects_config[show_name] = show
        add_dependancies({show_name: show})

        compile_lut({show_name: show})
        print(f'created show for: {show_name}')

        effects_config_client[show_name] = {}
        for key, value in show.items():
            if key != 'beats':
                effects_config_client[show_name][key] = value

        if not added and ((mode == None and not laser_mode) or mode == 'lasers'):
            added = True
            if 'song_path' in effect:
                print(f'Auto adding "{show_name}" to queue')
                add_queue_balanced(show_name, uuid)


async def init_queue_client(websocket, path):
    global curr_bpm, song_playing, song_time, broadcast_light_status, broadcast_song_status
    print('Song Queue: made connection to new client')

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
        print('Song Queue: sent config to new client')
        await websocket.send(dump)
    except:
        print('Song Queue: socket send failed', flush=True)

    song_sockets.append(websocket)

    while True:
        try:
            print('Song Queue: waiting for message')
            msg_string = await websocket.recv()
        except:
            song_sockets.remove(websocket)
            print('socket recv FAILED - ' + websocket.remote_address[0] + ' : ' + str(websocket.remote_address[1]), flush=True)
            break

        msg = json.loads(msg_string)

        print('Song Queue: message recieved:', msg)
        if 'type' in msg:
            if msg['type'] == 'add_queue_balanced' and 'uuid' in msg:
                print(f'Song Queue: added to queue by {uuid_to_user(msg["uuid"])}')
                add_queue_balanced(msg['effect'], msg['uuid'])

            elif msg['type'] == 'remove_queue' and 'uuid' in msg:
                uuid = msg['uuid']
                print(f'Song Queue: removed from queue by {uuid_to_user(msg["uuid"])}')
                effect_name = msg['effect']
                salt = msg['salt']
                # TODO share this code with light() probably
                for i in range(len(song_queue)):
                    if song_queue[i][0] == effect_name and song_queue[i][1] == salt and (song_queue[i][2] == uuid or is_admin(uuid)):
                        song_queue.pop(i)
                        if i == 0:
                            # andrew: oops, this is ew
                            song_was_playing = song_playing
                            stop_song()
                            song_playing = song_was_playing
                            song_time = 0
                            remove_effect_name(effect_name)
                            if song_playing and len(song_queue) > 0:
                                new_effect_name = song_queue[0][0]
                                add_effect(new_effect_name)
                                play_song(new_effect_name)
                            broadcast_light_status = True
                        break
                if len(song_queue) == 0:
                    song_playing = False

            elif msg['type'] == 'play_queue' and 'uuid' in msg:
                uuid = msg['uuid']
                print(f'Song Queue: Play requested ----UUID: {uuid_to_user(uuid)}')
                if is_admin(uuid):
                    if len(song_queue) > 0 and not song_playing:
                        effect_name = song_queue[0][0]
                        add_effect(effect_name)
                        broadcast_light_status = True
                        play_song(effect_name)

            elif msg['type'] == 'pause_queue' and 'uuid' in msg:
                uuid = msg['uuid']
                print(f'Song Queue: Pause requested ----UUID: {uuid_to_user(uuid)}')
                if is_admin(uuid):
                    if len(song_queue) > 0 and song_playing:
                        effect_name = song_queue[0][0]
                        song_time += max(pygame.mixer.music.get_pos(), 0) / 1000
                        stop_song()
                        remove_effect_name(effect_name)
                        broadcast_light_status = True

            elif msg['type'] == 'set_time':
                restart_show(abs_time=msg['time'])
                broadcast_light_status = True

            elif msg['type'] == 'download_song' and 'uuid' in msg:
                uuid = msg['uuid']
                url = msg.get('url', None)
                print_blue(f'Song Queue: Adding "{url}" to youtube downloading queue from {uuid_to_user(uuid)}')
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
                print(f'Song Queue: searching youtube "{search}" from {uuid_to_user(uuid)}')
                search_queue.append([search, websocket, False])
            broadcast_song_status = True


def search_youtube():
    import subprocess
    from urllib.parse import quote

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
        with open(get_temp_dir().joinpath('search_parse.html'), 'w', encoding="utf-8") as f:
            f.write(out[start:end])
        with open(get_temp_dir().joinpath('search_full.html'), 'w', encoding="utf-8") as f:
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
                    except Exception as e:
                        print_yellow(f'parsing 4 failed, aborting youtube search, exception: {e}')
            except Exception as e:
                print_yellow(f'parsing 3 failed, aborting youtube search, exception: {e}')
    else:
        print('--- WARNING: JSON NOT FOUND ---')

    message = {
        'search': videos
    }
    search_queue[0][2] = json.dumps(message)


def add_queue_balanced(effect_name, uuid):
    global song_playing, song_time, broadcast_light_status, broadcast_song_status

    # TODO Eric, is this code useless now? i just commented it out
    # if False: # is_admin(uuid):
    #     index = 1
    #     while index < len(song_queue):
    #         if song_queue[index][2] != uuid:
    #             break
    #         index += 1
    # else:
    index = 0
    count = 0
    user_counts = {}
    for entry in song_queue:
        user_counts[entry[2]] = 0
        if entry[2] == uuid:
            count += 1
    while index < len(song_queue):
        if user_counts[song_queue[index][2]] > count:
            break
        user_counts[song_queue[index][2]] += 1
        index += 1
    song_queue.insert(index, [effect_name, get_queue_salt(), uuid])

    if len(song_queue) == 1:
        song_time = 0
        add_effect(effect_name)
        broadcast_light_status = True
        play_song(effect_name)
        broadcast_song_status = True


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
    global broadcast_light_status
    message = {
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm,
            'laser_mode': laser_mode,
        }
    }
    await broadcast(light_sockets, json.dumps(message))
    broadcast_light_status = False


async def send_song_status():
    global broadcast_song_status
    # print((str(song_queue) + '\n') * 10)
    message = {
        'queue': song_queue,
        'status': {
            'playing': song_playing,
            'time': song_time + (max(pygame.mixer.music.get_pos(), 0) / 1000)
        }
    }
    await broadcast(song_sockets, json.dumps(message))
    broadcast_song_status = False


async def send_dev_status():
    if not curr_effects:
        return
    print('sent dev status')

    sub_effect_names = []
    for effect in curr_effects:
        sub_effect_names += get_sub_effect_names(effect[0], (beat_index / SUB_BEATS) + 1)
    if not sub_effect_names:
        return

    message = {
        'status': {
            'effects': [[x, 0] for x in sub_effect_names],
            'dev_mode': True,
        }
    }
    await broadcast(dev_sockets, json.dumps(message))


####################################


def get_sub_effect_names(effect_name, beat):
    sub_effect_names = []
    effect_beats = effects_config[effect_name]['beats']
    for effect in effect_beats:
        if type(effect[1]) == str:
            if effect[0] <= beat <= effect[0] + effect[2]:
                sub_effect_names.append(effect[1])
            elif sub_effect_names:
                break
    return sub_effect_names


stage_chars = '.,-~:;=!*#$@'
max_num = pow(2, 16) - 1
purple = [153, 50, 204]
laser_stage = random.randint(0, 110)
disco_stage = random.randint(0, 100)
disco_style = 'rgb(0,0,0)'
async def render_to_terminal(all_levels):
    global rekordbox_time, rekordbox_bpm, laser_stage, disco_stage, disco_style, printed_http_info

    while not printed_http_info:
        time.sleep(.01)

    curr_beat = (beat_index / SUB_BEATS) + 1
    terminal_size = os.get_terminal_size().columns
    dead_space = terminal_size - 15

    show_specific = ''
    all_effect_names = []
    for effect in curr_effects:
        effect_name = effect[0]

        if has_song(effect_name):
            channel_lut_index = (beat_index + effect[1])
            show_specific = f"""\
, Show {round(100 * (channel_lut_index / channel_lut[effect_name]['length']))}%\
"""
            all_effect_names += get_sub_effect_names(effect_name, curr_beat)
        else:
            all_effect_names.append(effect[0])

    useful_info = ''
    if laser_mode:
        useful_info += f'L1, '
    else:
        useful_info += f'L0, '
    if rekordbox_bpm is not None:
        useful_info += f', r_bpm {round(rekordbox_bpm, 1)}'
    if rekordbox_time is not None:
        useful_info += f', r_time {round(rekordbox_time, 1)}, '
    if rekordbox_effect_name is not None:
        useful_info += f', r: {rekordbox_effect_name}, '

    useful_info += f"""\
BPM {curr_bpm:.1f}, \
Beat {curr_beat:.1f}\
"""
    useful_info += f'{show_specific}'

    size_of_current_line = len(useful_info) % (terminal_size + 1)
    chars_until_end_of_line = terminal_size - size_of_current_line
    useful_info += ' ' * chars_until_end_of_line

    levels_255 = list(map(lambda x: int((x / max_num) * 255), all_levels))


    top_front_values = levels_255[0:3]
    top_back_values = levels_255[3:6]
    bottom_values = levels_255[6:9]
    uv_value = levels_255[9]
    laser_color_values = levels_255[10:12]
    laser_motor_value = levels_255[12] / 2.55
    disco_color_values = levels_255[13:16]

    purple_scaled = list(map(lambda x: int(x * (uv_value / 255)), purple))

    uv_style = f'rgb({purple_scaled[0]},{purple_scaled[1]},{purple_scaled[2]})'    
    top_front_rgb_style = f'rgb({top_front_values[0]},{top_front_values[1]},{top_front_values[2]})'
    top_back_rgb_style = f'rgb({top_back_values[0]},{top_back_values[1]},{top_back_values[2]})'
    bottom_rgb_style = f'rgb({bottom_values[0]},{bottom_values[1]},{bottom_values[2]})'

    # print(f'{top_front_values=}, {top_back_values=}, {bottom_values=}, {uv_value=}, {laser_color_values=}, {laser_motor_value=}')
    # print(f'{laser_color_values=}, {laser_motor_value=}')
    if any(laser_color_values):
        line_length = terminal_size - 1
        laser_arr = list(f'{" " * line_length}\n' * 3)
        for i in range(3):
            for j in range(terminal_size - 1):
                if j > 1 and j < 15 and (j + i + (laser_stage // 9)) % 4 == 0:
                    laser_arr[j + (line_length * i)] = stage_chars[laser_stage // 10]
        laser_string = ''.join(laser_arr)
        laser_style = f'rgb({laser_color_values[1]},{laser_color_values[0]},0)'
    else:
        laser_string = f'{" " * (terminal_size - 1)}\n' * 3
        laser_style = 'default'

    if any(disco_color_values):
        disco_string = ''
        for i in range(14):
            thing = (i + (disco_stage // 10))
            if thing % 4 == 0 or thing % 6 == 0:
                disco_string += 'o'
            else:
                disco_string += ' '
        disco_style = f'rgb({disco_color_values[0]},{disco_color_values[1]},{disco_color_values[2]})'
    else:
        disco_string = ' ' * 14


    if all_levels[12] != 0:
        laser_stage += int(max(1, laser_motor_value // 10))
        laser_stage %= 110

    disco_stage = (disco_stage + 1) % 10000

    effect_string = f'Effects: {", ".join(all_effect_names)}'
    remaining = terminal_size - len(effect_string)
    console.print(effect_string + (' ' * max(0, remaining)), no_wrap=True, overflow='ellipsis', end='\n')
    console.print(useful_info, no_wrap=True, overflow='ellipsis', end='\n')

    character = '▆'
    console.print(' ' + character * 2, style=uv_style, end='')
    console.print(character * 5, style=top_front_rgb_style, end='')
    console.print(character * 5, style=top_back_rgb_style, end='')
    console.print(character * 2 + (' ' * dead_space), style=uv_style, end='')
    console.print('\n', style=top_back_rgb_style, end='')
    console.print(laser_string, style=laser_style, end='')
    console.print(' ' + character * 14 + (' ' * dead_space), style=bottom_rgb_style, end='')
    console.print(' ', style='default', end='')
    for char in disco_string:
        console.print(char, style=disco_style, end='')
    console.print(' ' * dead_space, style='default', end='')
    console.print('', end='\033[F' * 7)


all_levels = [0] * LIGHT_COUNT
async def terminal(level, i):
    all_levels[i] = level
    if i == LIGHT_COUNT - 1:
        await render_to_terminal(all_levels)


####################################

def uuid_to_user(uuid):
    if uuid in users:
        return users[uuid]['name'] + f' ({uuid})'
    return uuid

async def light():
    global beat_index, song_playing, song_time, broadcast_song_status, broadcast_light_status

    download_thread = None
    search_thread = None

    while True:

        rate = curr_bpm / 60 * SUB_BEATS
        time_diff = time.time() - time_start
        beat_index = int(time_diff * rate)

        if song_playing and not pygame.mixer.music.get_busy():
            remove_effect_name(song_queue[0][0])
            song_queue.pop(0)
            song_time = 0
            if len(song_queue) > 0:
                new_effect_name = song_queue[0][0]
                add_effect(new_effect_name)
                play_song(new_effect_name)
            elif len(song_queue) == 0:
                song_playing = False
            broadcast_song_status = True

        i = 0
        while i < len(curr_effects):
            index = beat_index + curr_effects[i][1]
            effect_name = curr_effects[i][0]
            if not channel_lut[effect_name]['loop'] and index >= channel_lut[effect_name]['length']:
                remove_effect_index(i)
                broadcast_light_status = True
            else:
                i+=1

        for i in range(LIGHT_COUNT):
            level = 0
            for j in range(len(curr_effects)):
                effect_name = curr_effects[j][0]
                index = beat_index + curr_effects[j][1]

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
            print_blue(f'Starting download of {url} from client {uuid_to_user(uuid)}')
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

        if broadcast_light_status:
            await send_light_status()
        if broadcast_song_status:
            await send_song_status()

        if dev_sockets and beat_index % SUB_BEATS == 0:
            await send_dev_status()
            if args.print_beat and not args.local:
                print(f'Beat: {(beat_index // SUB_BEATS) + 1}, Seconds: {time_diff:.3f}')

        time_diff = time.time() - time_start

        direction = 1 
        if rate < 0:
            direction = -1
        time_delay = ((beat_index + direction) / rate) - time_diff

        # if beat_index % SUB_BEATS == 0:
        #     print(f'{beat_index=}, {time_diff=}')
            # avg = 0
        # else:
        #     print(beat_index)
        #     avg += time_diff

        await asyncio.sleep(min(0.05, time_delay))

#################################################

def has_song(name):
    return 'song_path' in effects_config[name]

def get_effect_index(name):
    for i in range(len(curr_effects)):
        if curr_effects[i][0] == name:
            return i
    return False

def remove_effect_name(name):
    for i in range(len(curr_effects)):
        if curr_effects[i][0] == name:
            curr_effects.pop(i)
            return True
    return False

def remove_effect_index(index):
    curr_effects.pop(index)

def clear_effects():
    global curr_effects
    curr_effects = []

def maybe_get_laser_version(effect_name):
    if effect_name.startswith('g_lasers_'):
        if not laser_mode:
            return 'g_' + effect_name[9:]
    elif effect_name.startswith('g_') and laser_mode:
        laser_name = 'g_lasers_' + effect_name[2:]
        print(f'Since it is an autogen effect, and laser mode is on, searching for {laser_name}\n' * 5)
        if laser_name in effects_config:
            print_green(f'Found "{laser_name}"\n' * 5)
            return laser_name
        else:
            print_yellow(f'Could not find laser effect, using normal effect instead\n' * 5)
    return effect_name

def add_effect(new_effect_name):
    global beat_index, time_start, curr_bpm

    new_effect_name = maybe_get_laser_version(new_effect_name)

    if new_effect_name in effects_config and 'song_path' in effects_config[new_effect_name]:
        print(f'Adding effect with song named {new_effect_name}')

    if new_effect_name not in channel_lut:
        print_green(f'late lut compiling {new_effect_name}')
        compile_lut({new_effect_name: effects_config[new_effect_name]})

    effect = effects_config[new_effect_name]
    if (effect['trigger'] == 'toggle' or effect['trigger'] == 'hold') and get_effect_index(new_effect_name) is not False:
        return

    if 'bpm' in effect:
        clear_effects()
        time_start = time.time() + effect['delay_lights'] - song_time
        print('effect will have time_start of:', effect['delay_lights'] - song_time)
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
    curr_effects.append([new_effect_name, offset])


def play_song(effect_name, print_out=True):
    global take_rekordbox_input, song_playing
    print('Disabling rekordbox input')
    take_rekordbox_input = False
    print(f'Going to play music from effect: {effect_name}')
    song_path = effects_config[effect_name]['song_path']
    start_time = effects_config[effect_name]['skip_song'] + song_time
    if print_out:
        print(f'{bcolors.OKBLUE}Starting music "{song_path}" at {start_time} seconds at {round(args.volume * 100)}% volume{bcolors.ENDC}')

    pygame.mixer.music.set_volume(args.volume)
    pygame.mixer.music.load(pathlib.Path(song_path))

    # ffmpeg -i songs/musician2.mp3 -c:a libvorbis -q:a 4 songs/musician2.ogg
    # python server.py --local --show "shelter" --skip 215
    # ffplay songs/shelter.mp3 -ss 215 -nodisp -autoexit
    pygame.mixer.music.play(start=start_time)
    song_playing = True

def stop_song():
    global song_playing
    pygame.mixer.music.stop()
    song_playing = False


######################################

def setup_gpio():
    global pca

    try:
        import board
    except Exception as e:
        print_red(f'{traceback.format_exc()}')
        print_yellow(f'you need to add --local probably')        
        sys.exit()

    
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
song_name_to_show_names = {}

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
    
    for node in graph[curr]:
        if node in path:
            raise Exception(f'Cycle Found: {curr} -> {node}')
        effects_config_sort(path + [node])
    if len(graph[curr]) == 0 and curr:
        simple_effects.append(curr)
    elif curr:
        complex_effects.append(curr)


def dfs(effect_name):
    if effect_name not in found:
        if effect_name not in effects_config:
            return effect_name
        for component in effects_config[effect_name]['beats']:
            if type(component[1]) == str:
                missing_effect = dfs(component[1])
                if missing_effect:
                    return missing_effect
        effects_config_sort([effect_name])


# def add_dependancies(effects_config):
#     for effect_name, effect in effects_config.items():
#         graph[effect_name] = {}
#         for component in effect['beats']:
#             if type(component[1]) is str:
#                 graph[effect_name][component[1]] = True
#         graph[effect_name] = list(graph[effect_name].keys())

def add_dependancies(effect_names):
    for effect_name in effect_names:
        effect = effects_config[effect_name]
        graph[effect_name] = {}
        for component in effect['beats']:
            if type(component[1]) is str:
                graph[effect_name][component[1]] = True
        graph[effect_name] = list(graph[effect_name].keys())


def add_song_to_config(song_path):
    song_path = pathlib.Path(str(song_path).replace('\\', '/'))
    relative_path = song_path
    if relative_path.is_absolute():
        relative_path = relative_path.relative_to(this_file_directory)

    if song_path.suffix in ['.mp3', '.ogg', '.wav']:
        name, artist, duration, samplerate, _song_path = sound_helpers.get_song_metadata_info(song_path)
        if samplerate != 48000:
            print_red(f'This song file is not 48000hz sample rate, {song_path}. This introduces weird bugs, delete the file.')
            return False

        songs_config[str(relative_path.as_posix())] = {
            'name': name,
            'artist': artist,
            'duration': duration
        }
    else:
        print_red(f'add_song_to_config: CANNOT READ FILETYPE {song_path.suffix} in {song_path}')


# def prep_loaded_effects(loaded_effects):
#     for effect_name, effect in list(loaded_effects.items()):
#         if effect.get('not_done'):
#             del loaded_effects[effect_name]
#             continue
#         if 'song_path' in effect:
#             effect['song_path'] = effect['song_path'].replace('\\', '/')

#     before_song_config_import = time.time()
#     if not songs_config:
#         for name, filepath in get_all_paths('songs', only_files=True):
#             add_song_to_config(filepath)
#     print_blue(f'add_song_to_configs took {time.time() - before_song_config_import:.3f}')
    
#     for effect_name, effect in loaded_effects.items():
#         if 'song_path' in effect:
#             if effect['song_path'] in songs_config:
#                 song_name = pathlib.Path(effect['song_path']).stem                    
#                 if song_name not in song_name_to_show_names:
#                     song_name_to_show_names[song_name] = []
#                 song_name_to_show_names[song_name].append(effect_name)
#                 # print(effect_name, song_name_to_show_names[song_name])
#             elif effect.get('song_not_avaliable', True):
#                 print_yellow(f'song not avaliable, effect_name: "{effect_name}", song_path "{effect["song_path"]}"')
#                 if args.show:
#                     effect['song_not_avaliable'] = True
#                 else:
#                     del effect['song_path']
#                     # print_red('deleted', _effect_name)
#     add_dependancies(loaded_effects)

def prep_loaded_effects(effect_names):
    global effects_config
    for effect_name in effect_names:
        effect = effects_config[effect_name]
        if effect.get('not_done'):
            del effects_config[effect_name]
            continue
        if 'song_path' in effect:
            effect['song_path'] = effect['song_path'].replace('\\', '/')

    before_song_config_import = time.time()
    if not songs_config:
        for name, filepath in get_all_paths('songs', only_files=True):
            add_song_to_config(filepath)
    print_blue(f'add_song_to_configs took {time.time() - before_song_config_import:.3f}')

    updated_effect_names = []
    for effect_name in effect_names:
        if effect_name not in effects_config:
            continue
        updated_effect_names.append(effect_name)
        effect = effects_config[effect_name]
        if 'song_path' in effect:
            if effect['song_path'] in songs_config:
                song_name = pathlib.Path(effect['song_path']).stem                    
                if song_name not in song_name_to_show_names:
                    song_name_to_show_names[song_name] = []
                song_name_to_show_names[song_name].append(effect_name)
                # print(effect_name, song_name_to_show_names[song_name])
            elif effect.get('song_not_avaliable', True):
                print_yellow(f'song not avaliable, effect_name: "{effect_name}", song_path "{effect["song_path"]}"')
                if args.show:
                    effect['song_not_avaliable'] = True
                else:
                    del effect['song_path']
                    # print_red('deleted', _effect_name)
    add_dependancies(updated_effect_names)



def load_effects_config_from_disk():
    global effects_config, effects_config_client, graph, found, song_name_to_show_names
    update_config_and_lut_time = time.time()

    effects_config = {}
    effects_config_client = {}

    graph = {}
    found = {}

    song_name_to_show_names = {}

    effects_dir = this_file_directory.joinpath('effects')

    total_time = 0
    for name, filepath in get_all_paths(effects_dir, only_files=True) + \
                          get_all_paths(effects_dir.joinpath('generated_effects'), only_files=True, quiet=True) + \
                          get_all_paths(effects_dir.joinpath('rekordbox_effects'), only_files=True, quiet=True) + \
                          get_all_paths(effects_dir.joinpath('autogen_shows'), only_files=True, quiet=True):
        if name == 'compiler.py':
            continue
    
        t1 = time.time()
        relative_path = filepath.relative_to(this_file_directory)
        without_suffix = relative_path.parent.joinpath(relative_path.stem)
        module_name = str(without_suffix).replace(os.sep, '.')
        if module_name in globals():
            importlib.reload(globals()[module_name])
        else:
            globals()[module_name] = importlib.import_module(module_name)
        effects_config.update(globals()[module_name].effects)
        total_time += time.time() - t1

    prep_loaded_effects(list(effects_config.keys()))
    print_blue(f'load_effects_config_from_disk took {time.time() - update_config_and_lut_time:.3f}, {total_time:.3f} to import modules')


def set_effect_defaults(name, effect):
    if 'hue_shift' not in effect:
        effect['hue_shift'] = 0
    if 'sat_shift' not in effect:
        effect['sat_shift'] = 0
    if 'bright_shift' not in effect:
        effect['bright_shift'] = 0
    if 'snap' not in effect:
        effect['snap'] = 1 / SUB_BEATS
    else:
        effect['snap'] = max(effect['snap'], 1 / SUB_BEATS)
    if 'trigger' not in effect:
        effect['trigger'] = 'toggle'
    if 'profiles' not in effect:
        effect['profiles'] = []
    if effect.get('autogen') and 'Autogen effects' not in effect['profiles']:
        effect['profiles'].append(['Autogen effects'])
    if 'song_path' in effect:
        effect['song_path'] = str(pathlib.Path(effect['song_path'])).replace('\\', '/')
    if 'song_path' in effect and effect['song_path'] in songs_config:
        if 'bpm' not in effect:
            print_red(f'song effects must have bpm {effect["song_path"]}\n' * 10)
            exit()
        
        if name in originals:
            effect['delay_lights'] = originals[name]['delay_lights']

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
    # if 'song_path' not in effect:
    #     effect['profiles'].append('All Effects')



def compile_all_luts_from_effects_config():
    global channel_lut
    start_time = time.time()

    channel_lut = {}

    effects_config_to_compile = {}
    if args.show:
        effects_config_to_compile[args.show] = effects_config[args.show]

    for name, effect in effects_config.items():
        set_effect_defaults(name, effect)

        # if not name.startswith('g_lasers_'):
        if effect['profiles'] or 'song_path' in effect and effect['song_path'] in songs_config:
            if 'Generated Shows' in effect['profiles']:
                continue
            
            effects_config_client[name] = {}
            for key, value in effect.items():
                if key != 'beats':
                    effects_config_client[name][key] = value

    # TODO andrew: replace with is_doorbell()
    if is_linux() and not is_andrews_main_computer():
        # eager compile all normal effects
        for effect_name, effect in effects_config.items():
            if 'bpm' not in effect:
                effects_config_to_compile[effect_name] = effect

    compile_lut(effects_config_to_compile)
    print_blue(f'compile_all_luts_from_effects_config took: {time.time() - first_start_time:.3f}')



def compile_lut(local_effects_config):
    global channel_lut, simple_effects, complex_effects

    simple_effects = []
    complex_effects = []

    sort_perf_timer = time.time()
    for name, effect in local_effects_config.items():
        set_effect_defaults(name, effect)
        missing_effect = dfs(name)
        if missing_effect is not None:
            print_red(f'dfs: while trying to find dependancies of effect {name}, we found sub complex effect "{missing_effect}" missing from effects_config, probably you changed an effect name.')
            sys.exit()
    print_blue(f'Sort took: {time.time() - sort_perf_timer:.3f} seconds')
    
    simple_effect_perf_timer = time.time()
    for effect_name in simple_effects:
        effect = effects_config[effect_name]

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
            if len(channels) == 10:
                channels += [0,0,0]
            if len(channels) == 13:
                channels += [0,0,0]

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
    print_blue(f'Simple effects took: {time.time() - simple_effect_perf_timer:.3f} seconds')

    complex_effect_perf_timer = time.time()
    for effect_name in complex_effects:
        effect = effects_config[effect_name]

        # if length isn't specified, generate a length
        calced_effect_length = 0
        for component in effect['beats']:
            start_beat = component[0] - 1
            name = component[1]
            if len(component) == 2:
                if effects_config[name]['loop']:
                    component.append(effect['length'] - start_beat)
                else:
                    component.append(effects_config[name]['length'])
            if len(component) == 3:
                component.append(1)
            if len(component) == 4:
                component.append(component[-1])
            if len(component) == 5:
                component.append(0)
            if len(component) == 6:
                component.append(0)
            if len(component) == 7:
                component.append(0)
            if len(component) == 8:
                component.append(0)
            calced_effect_length = max(calced_effect_length, start_beat + component[2])

        if 'length' not in effect:
            effect['length'] = calced_effect_length

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
            hue_shift = component[6]
            sat_shift = component[7]
            bright_shift = component[8]

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
                    if hue_shift or sat_shift or bright_shift:
                        for i in range(3):
                            rd, gr, bl = final_channel[i * 3:(i * 3) + 3]
                            hue, sat, bright = colorsys.rgb_to_hsv(max(0, rd / 100.), max(0, gr / 100.), max(0, bl / 100.))
                            new_hue = (hue + hue_shift) % 1
                            new_sat = min(1, max(0, sat + sat_shift))
                            # bright shift is relative to initial brightness
                            new_bright = min(1, max(0, bright + bright*bright_shift))
                            final_channel[i * 3:(i * 3) + 3] = colorsys.hsv_to_rgb(new_hue, new_sat, new_bright)
                            final_channel[i * 3] *= 100
                            final_channel[i * 3 + 1] *= 100
                            final_channel[i * 3 + 2] *= 100

    print_blue(f'Complex effects took: {time.time() - complex_effect_perf_timer:.3f} seconds')

##################################################

def kill_in_n_seconds(seconds):
    time.sleep(seconds)
    import atexit
    atexit._run_exitfuncs()

    if is_windows():
        kill_string = f'taskkill /PID {os.getpid()} /F'
    else:
        kill_string = f'kill -9 {os.getpid()}'
    print(f'running to kill: "{kill_string}"')
    os.system(kill_string)


def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    close_connections_to_doorbell()
    if 'multiprocessing' in sys.modules:
        import multiprocessing
        active_children = multiprocessing.active_children()        
        if active_children:
            print_yellow(f'Module multiprocessing was imported! Killing active_children processes, PIDS: {[x.pid for x in active_children]}')
            for child in active_children:
                print_yellow(f'killing {child.pid}')
                child.kill()
    if not args.local:
        threading.Thread(target=kill_in_n_seconds, args=(0.5,)).start()
        for i in range(len(pca.channels)):
            pca.channels[i].duty_cycle = 0
    if args.reload:
        observer.stop()
        observer.join()
    sys.exit()

#################################################


def fuzzy_find(search, collection):
    from thefuzz import process
    print_yellow('Warning: fuzzy_find doesnt prune any results based on probablity and will return a show no matter what')
    return process.extractOne(search, collection)[0]


def restart_show(skip=0, abs_time=None, reload=False):
    global song_time
    if curr_effects:
        effect_name = curr_effects[0][0]
        if not has_song(effect_name):
            return
        remove_effect_index(0)
        
        stop_song()
        time_to_skip_to = max(0, (time.time() - time_start) + skip)
        if abs_time is not None:
            time_to_skip_to = abs_time
        song_time = time_to_skip_to
        print(f'skipping to {time_to_skip_to}')

        if reload:
            print('RELOAD REFRESHING')
            load_effects_config_from_disk()
            compile_all_luts_from_effects_config()

        effect = effects_config[effect_name]

        if args.reload:
            effect['bpm'] = originals[effect_name]['bpm']
            effect['song_path'] = originals[effect_name]['song_path']

            # song time controls these now, maybe just for autogen?
            # effect['skip_song'] = originals[effect_name]['skip_song'] + time_to_skip_to
            # effect['delay_lights'] = originals[effect_name]['delay_lights'] - time_to_skip_to
        add_effect(effect_name)
        try:
            play_song(effect_name, print_out=False)
        except:
            print_red('play_song errored, running stop_song + clear_effects and continuing')
            clear_effects()
            stop_song()
    elif reload:
        print('RELOAD REFRESHING NO EFFECT')
        load_effects_config_from_disk()
        compile_all_luts_from_effects_config()


#################################################

def get_channel_lut():
    return channel_lut

def get_effects_config():
    return effects_config

def try_download_video(show_name):
    just_filename = pathlib.Path(effects_config[show_name]['song_path']).stem
    print(f'Searching with phrase "{just_filename}"')
    youtube_search_result = youtube_helpers.youtube_search(just_filename)
    if not youtube_search_result:
        print('Couldnt find relevant video on youtube, exiting...')
        exit()

    url = youtube_search_result['webpage_url']
    if youtube_helpers.download_youtube_url(url, dest_path='songs'):
        print('downloaded video, continuing to try to recover')
        return
    raise Exception('Couldnt download video')



print_cyan(f'Up till main: {time.time() - first_start_time:.3f}')
if __name__ == '__main__':
    make_if_not_exist(pathlib.Path(__file__).resolve().parent.joinpath('songs'))
    try:
        # pygame.mixer.pre_init(48000, 16, 2, 4096)
        pygame.mixer.init(frequency=48000)
    except:
        print_stacktrace()
        print_red('PYGAME COULDNT INITIALIZE, NO SOUND WILL WORK')
    print_cyan(f'Up through pygame init: {time.time() - first_start_time:.3f}')

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


    args.volume = args.volume / 100
    if args.local:
        from rich.console import Console
        console = Console()
    else:
        setup_gpio()
    
    if args.autogen is not None:
        import autogen

        autogen_song_directory = pathlib.Path(__file__).resolve().parent.joinpath('songs')
        if args.autogen == 'all':
            autogen.generate_all_songs_in_directory(autogen_song_directory)
            sys.exit()
        else:
            all_song_name_and_paths = get_all_paths(autogen_song_directory, only_files=True, allowed_extensions=set(['.ogg', '.mp3']))

            all_song_names = [name for name, _path in all_song_name_and_paths]
            song_path = pathlib.Path('songs').joinpath(fuzzy_find(args.autogen, all_song_names))
            args.show, _, _ = autogen.generate_show(song_path, overwrite=True, mode=args.autogen_mode)
            if args.autogen_mode == 'lasers':
                laser_mode = True


    load_effects_config_from_disk()

    for effect_name, effect in effects_config.items():
        if 'song_path' in effect:
            originals[effect_name] = {
                'skip_song': effects_config[effect_name]['skip_song'],
                'delay_lights': effects_config[effect_name]['delay_lights'],
                'bpm': effects_config[effect_name]['bpm'],
                'song_path': effects_config[effect_name]['song_path'],
            }
    print_cyan(f'Up through copying effects to originals: {time.time() - first_start_time:.3f}')


    def detailed_output_on_enter():
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



                # if RekordboxFilesystemHandler.last_updated > (time.time() - .05):
                #     return

    if args.load_new_rekordbox_shows_live:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class RekordboxFilesystemHandler(FileSystemEventHandler):
            @staticmethod
            def on_any_event(event):
                filepath = event.src_path
                if type(filepath) != pathlib.Path:
                    filepath = pathlib.Path(filepath)

                print_cyan(f'Filesystem event detected, new "{filepath}"')
                if event.is_directory:
                    return print_yellow('skipping: event.is_directory')
                if event.event_type != 'created':
                    return print_yellow('skipping: event.event_type != created')
                if '__pycache__' in event.src_path:
                    return print_yellow('skipping: __pycache__ in event.src_path')
                if not event.src_path.endswith('.py'):
                    return print_yellow('skipping: not event.src_path.endswith(".py")')

                rekordbox_effect_dir = effects_dir.joinpath('rekordbox_effects')
                if filepath.resolve() in rekordbox_effect_dir.parents:
                    print_yellow(f'skipping: Not a child of {rekordbox_effect_dir}')

                print(f'Loading in new light show because: "{filepath}" was created')
                relative_path = filepath.relative_to(this_file_directory)
                without_suffix = relative_path.parent.joinpath(relative_path.stem)
                module_name = str(without_suffix).replace(os.sep, '.')
                if module_name not in globals():
                    globals()[module_name] = importlib.import_module(module_name)
                else:
                    print_red('Somehow this path was already in globals, doing nothing.')
                effects_config.update(globals()[module_name].effects)
                # prep_loaded_effects(effects_config)
                prep_loaded_effects(list(globals()[module_name].effects.keys()))

        observer = Observer()
        observer.schedule(RekordboxFilesystemHandler(), effects_dir, recursive = True)
        observer.start()
        print_green(f'WATCHING {effects_dir} for rekordbox additions')


    if args.reload:
        if not args.show:
            raise Exception('you need to define --show in order to use --reload')
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class FilesystemHandler(FileSystemEventHandler):
            last_updated = 0

            @staticmethod
            def on_any_event(event):
                global downloaded
                if event.is_directory or event.event_type not in ['modified', 'created'] or '__pycache__' in event.src_path or not event.src_path.endswith('.py'):
                    return None
                if FilesystemHandler.last_updated > (time.time() - .05):
                    return
                time_before_restart = time.time()
                print(f'Reloading json because: "{event.src_path}" was modified')
                FilesystemHandler.last_updated = time.time()            
                
                if args.skip_show_seconds and not args.jump_back:
                    restart_show(reload=True, abs_time=args.skip_show_seconds)
                else:
                    restart_show(reload=True, skip=-args.jump_back)
                print_cyan(f'Time to reload: {time.time() - time_before_restart:.3f}')

        observer = Observer()
        observer.schedule(FilesystemHandler(), effects_dir, recursive = True)
        observer.start()
        print_green(f'WATCHING {effects_dir} for all effects additions')

    if args.keyboard:
        from pynput.keyboard import Listener, KeyCode

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
            'j': lambda: restart_show(skip=-skip_time),
            ';': lambda: restart_show(skip=skip_time),
            'left': lambda: restart_show(skip=-skip_time),
            'right': lambda: restart_show(skip=skip_time),
            # 'space': 'UV',
        }
        # https://stackoverflow.com/questions/24072790/how-to-detect-key-presses how to check window name (not global)

        def window_focus():
            if is_linux():
                return_code, stdout, _stderr = run_command_blocking([
                    'xdotool',
                    'getwindowfocus',
                ])
                if return_code != 0:
                    return False
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
                    remove_effect_name(keyboard_dict[key_name])

        def listen_for_keystrokes():
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()

        keyboard_thread = threading.Thread(target=listen_for_keystrokes, args=[], daemon=True)
        keyboard_thread.start()
        if is_macos():
            time.sleep(.05)


    http_thread = threading.Thread(target=run_http_server_forever, args=[], daemon=True)
    http_thread.start()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start_async():
        print_cyan(f'Up to start_async: {time.time() - first_start_time:.3f}')
        rekordbox_bridge_server = await websockets.serve(init_rekordbox_bridge_client, '0.0.0.0', 1567)
        dj_socket_server = await websockets.serve(init_dj_client, '0.0.0.0', 1337)
        queue_socket_server = await websockets.serve(init_queue_client, '0.0.0.0', 7654)
        print(f'{bcolors.OKGREEN}started websocket servers{bcolors.ENDC}')

        if args.show:
            print('Starting show from CLI:', args.show)

            only_shows = list(filter(lambda x: has_song(x), effects_config.keys()))
            args.show = fuzzy_find(args.show, only_shows)

            if effects_config[args.show].get('song_not_avaliable'):
                # print(list(effects_config.keys()))
                print_yellow(f'Song isnt availiable for effect "{args.show}", press enter to try downloading?')
                input()
                try_download_video(args.show)
                time.sleep(.02)

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
                    global song_time
                    song_time = args.skip_show_seconds
                    # effects_config[args.show]['skip_song'] += args.skip_show_seconds
                    # effects_config[args.show]['delay_lights'] -= args.skip_show_seconds
            else:
                print(f'{bcolors.FAIL}Couldnt find effect named "{args.show}" in any profile{bcolors.ENDC}')

        compile_all_luts_from_effects_config()
        if args.show:
            print_blue('Found in CLI:', args.show)
            song_queue.append([args.show, get_queue_salt(), 'CLI'])
            add_effect(args.show)
            play_song(args.show)

        asyncio.create_task(light())

        print_cyan(f'Whole startup: {time.time() - first_start_time:.3f}')
        await dj_socket_server.wait_closed() and queue_socket_server.wait_closed() and rekordbox_bridge_server.wait_closed()

    asyncio.run(start_async())





        # if msg['type'] == 'add_effect':
        #     add_effect_from_dj(msg['effect'])

        # 'key': stuff[0],
        # 'master_total_time': stuff[3],

            # TODO we gotta check above and all the songs
            # if rekordbox_title not in effects_config:
            #     print(f'Couldnt find handmade {rekordbox_title}\n' * 8)
            #     rekordbox_title = 'g_' + rekordbox_title
            #     if rekordbox_title not in effects_config:
            #         print_yellow(f'Cant play light show effect from rekordbox! Missing effect {rekordbox_title}\n' * 8)
            #         continue
            # else:
            #     print(f'FOUND handmade {rekordbox_title}\n' * 8)