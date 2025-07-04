import time
first_start_time = time.time()
import threading
import json
import signal
import importlib
import pathlib
import asyncio
import argparse
import copy
import os
import colorsys
import random
import sys

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
import winamp.winamp_wrapper # must be loaded first because of MESA forcing

# https://wiki.libsdl.org/SDL2/FAQUsingSDL os.environ['SDL_AUDIODRIVER'] = 'jack'
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import numpy as np
import pygame
import pigpio
import websockets
print(f'Up to pip import: {time.time() - first_start_time:.3f}')

from helpers import *
from users import users
import sound_video_helpers
import youtube_download_helpers
import joystick_and_keyboard_helpers
print_cyan(f'After cheap custom imports import: {time.time() - first_start_time:.3f}')
import grid_helpers
print_cyan(f'Half the custom imports: {time.time() - first_start_time:.3f}')
import effects.compiler
from effects.compiler import GridInfo
print_cyan(f'After custom import: {time.time() - first_start_time:.3f}')



parser = argparse.ArgumentParser(description = '')
parser.add_argument('--local', dest='local', default=None, action='store_true')
parser.add_argument('--show', dest='show_name', type=str, default='')
parser.add_argument('--skip', dest='skip_show_beats', type=float, default=1)
parser.add_argument('--skip_seconds', dest='skip_show_seconds', type=float, default=0)
parser.add_argument('--volume', dest='volume', type=int, default=100)
parser.add_argument('--jump_back', dest='jump_back', type=int, default=0)
parser.add_argument('--speed', dest='speed', type=float, default=1)
parser.add_argument('--autogen', dest='autogen', nargs="?", type=str, const='all')
parser.add_argument('--autogen_mode', dest='autogen_mode', default='both')
parser.add_argument('--delay', dest='absolute_delay_seconds', type=float, default=0.0)
    # https://nullvoxpopuli.github.io/latency-tester/
        # qc35 on arch linux:  395ms
        # wired on arch linux: 110ms
        # 0.285 second difference
        # OLD was .189
        # anecdoteadley the best is .225 though
parser.add_argument('--watch', dest='load_new_rekordbox_shows_live', default=True, action='store_false')
parser.add_argument('--rotate', dest='rotate_grid_terminal', default=False, action='store_true')
parser.add_argument('--skip_autogen', dest='load_autogen_shows', default=True, action='store_false')
parser.add_argument('--no_winamp', dest='winamp', default=None, action='store_false')
parser.add_argument('--fake_winamp', dest='fake_winamp', default=False, action='store_true')
parser.add_argument('--terminal', dest='force_terminal', default=False, action='store_true')
parser.add_argument('--no_curve', dest='no_curve', default=True, action='store_false')
parser.add_argument('--full_grid', dest='full_grid', default=False, action='store_true')
parser.add_argument('--print_info_terminal_lines', dest='should_print_info_terminal_lines', default=False, action='store_true')
parser.add_argument('--skip_render', default=False, action='store_true')
args = parser.parse_args()

if is_doorbell():
    if args.local is None:
        args.local = False
    args.keyboard = False
else:
    args.local = True
    args.keyboard = True

if is_windows():
    args.fake_winamp = True
    args.winamp = False
    print_yellow(f'Since this is windows defaulted to --fake_winamp and --no_winamp')

if args.winamp == None:
    args.winamp = True

this_file_directory = pathlib.Path(__file__).parent.resolve()
effects_dir = this_file_directory.joinpath('effects')





beat_sens_string = 'Beat Sens: N/A'
if args.fake_winamp:
    effects.compiler.winamp_grid = effects.compiler.twinkle
    winamp.winamp_wrapper.winamp_visual_loaded = True

elif args.winamp:
    if not grid_helpers.try_load_winamp():
        print_red(f'Failed to load winamp, exiting')
        exit()
    # put this in for eager load of winamp
    # if not grid_helpers.try_setup_winamp():
    #     print_red(f'Failed to setup winamp, exiting')
    #     exit()
    # result = winamp.winamp_wrapper.get_beat_sensitivity()
    # if result is not None:
    #     beat_sens_string = f'Beat Sens: {result}'


    needs_to_save_winamp_offsets = False
    def save_all_winamp_offsets():
        with open(grid_helpers.winamp.winamp_wrapper.winamp_offsets_filepath, 'w') as f:            
            json.dump(grid_helpers.winamp.winamp_wrapper.winamp_offsets, f, indent=4)

    # spawn a thread to save winamp offsets every 30 seconds
    def save_winamp_offsets_thread():
        global needs_to_save_winamp_offsets
        the_f = grid_helpers.winamp.winamp_wrapper.winamp_offsets_filepath
        while True:
            time.sleep(30)
            # print(f'{cyan(f"Saving winamp offsets to {the_f}")}')
            if needs_to_save_winamp_offsets:
                save_all_winamp_offsets()
                needs_to_save_winamp_offsets = False
    threading.Thread(target=save_winamp_offsets_thread, daemon=True).start()


pi = None


# these are guessed by andrew:
# I think the first 3 are officially unused, commenting out 
LED_PINS = [
    None, None, None, 
    19, 24, 25, # floor vertical (r g b)
    8, 7, 26, # floor horizontal (r g b)
    16, 2, 3, 
    4, 17, 27, 
    22,
    None, None, None, # Uh buffer for math? This is bad 
]

LED_FREQ = 500
LED_RANGE = 200000 // LED_FREQ
LIGHT_COUNT = len(LED_PINS)

SUB_BEATS = 24

curr_effects = []
song_queue = []

curr_bpm = 121
time_start = time.time()
beat_index = 0
last_effect_change_in_beats = None

light_lock, song_lock = threading.Lock(), threading.Lock() 
light_sockets, song_sockets, dev_sockets = [], [], []

song_playing = False
song_time = 0
queue_salt = 0

broadcast_light_status, broadcast_song_status, broadcast_dev_status, broadcast_winamp_offset_update = False, False, False, False
download_queue, search_queue = [], []

def setup_gpio():
    global pi
    pi = pigpio.pi()
    if not pi.connected:
        exit()
    for pin in LED_PINS:
        if pin != None:
            pi.set_PWM_frequency(pin, LED_FREQ)
            pi.set_PWM_range(pin, LED_RANGE)
            pi.set_PWM_dutycycle(pin, 0)

########################################

def add_effect_from_dj(effect_name):
    global song_time, broadcast_song_status
    song_time = 0
    add_effect(effect_name)


laser_mode = False
rekordbox_bpm = None
rekordbox_time = None
rekordbox_original_bpm = None
take_rekordbox_input = False
rekordbox_effect_name = None
async def init_rekordbox_bridge_client(websocket, path=None):
    global rekordbox_bpm, rekordbox_original_bpm, rekordbox_time, time_start, curr_bpm, song_time, take_rekordbox_input, song_playing, broadcast_song_status, song_name_to_show_names, rekordbox_effect_name
    print('rekordbox made connection to new client')
    rekordbox_title = None
    while True:
        try:
            msg = json.loads(await websocket.recv())
            # print('rekordbox msg', msg)
        except:
            if websocket.remote_address and len(websocket.remote_address) == 2:
                addy_1, addy_2 = websocket.remote_address
                print('DJ Client: socket recv FAILED - ' + addy_1 + ' : ' + str(addy_2), flush=True)
            else:
                print('DJ Client: socket recv FAILED - ' + str(websocket.remote_address), flush=True)
            return
        if 'title' in msg and 'original_bpm' in msg:
            stop_song()
            broadcast_song_status = True

            print_blue('Switching to taking rekordbox input')
            take_rekordbox_input = True
            rekordbox_title = msg['title']
            rekordbox_original_bpm = float(msg['original_bpm'])

            handmade_song_found = False
            possible_generated_shows_for_title = []
            print(f'{len(song_name_to_show_names)=}')
            if rekordbox_title in song_name_to_show_names:
                for effect_name in song_name_to_show_names[rekordbox_title]:
                    print_green(f'Found: {len(song_name_to_show_names[rekordbox_title])} effects from "{rekordbox_title=}", they are {song_name_to_show_names[rekordbox_title]}\n')
                    if effect_name.startswith('g_'):
                        possible_generated_shows_for_title.append(effect_name)
                    else:
                        print_green(f'Using handmade effect "{effect_name}"\n')
                        rekordbox_effect_name = effect_name
                        handmade_song_found = True
            if not handmade_song_found:
                if len(possible_generated_shows_for_title) == 0:
                    print_red('Couldnt find any generated effects for this song\n')
                else:
                    if len(possible_generated_shows_for_title) > 1:
                        print_yellow(f'WARNING found multiple shows, {possible_generated_shows_for_title=}, choosing first\n')
                    rekordbox_effect_name = possible_generated_shows_for_title[0]

            if rekordbox_effect_name is not None:
                print_green(f'Playing light show effect from rekordbox: {rekordbox_effect_name}\n')
                clear_effects()
                song_time = 0
                add_effect(rekordbox_effect_name)

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

                to_delay = effects_config[rekordbox_effect_name]['delay_lights']
                if args.absolute_delay_seconds:
                    to_delay += args.absolute_delay_seconds
                if not args.local:
                    to_delay += 0.08
                time_start = time.time() - ((rekordbox_time - to_delay) * (rekordbox_original_bpm / rekordbox_bpm))


async def init_dj_client(websocket, path=None):
    global curr_bpm, time_start, song_playing, beat_sens_string, broadcast_light_status, broadcast_song_status, broadcast_dev_status, broadcast_winamp_offset_update, laser_mode, needs_to_save_winamp_offsets
    print('DJ Client: made connection to new client')

    message = {
        'effects': effects_config_dj_client,
        'songs': songs_config,
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm,
            'laser_mode': laser_mode,
            'beat_sens_string': beat_sens_string,
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
            msg = json.loads(await websocket.recv())
        except:
            light_sockets.remove(websocket)
            if websocket in dev_sockets:
                dev_sockets.remove(websocket)
            if websocket.remote_address and len(websocket.remote_address) == 2:
                addy_1, addy_2 = websocket.remote_address
                print('DJ Client: socket recv FAILED - ' + addy_1 + ' : ' + str(addy_2), flush=True)
            else:
                print('DJ Client: socket recv FAILED - ' + str(websocket.remote_address), flush=True)
            break

        beat_sens_number = 'N/A'
        if 'type' in msg:
            if msg['type'] == 'accel':
                # print(f'Recieved accel: {msg}' * 20)
                # last_accel = [msg['x'], msg['y']]
                effects.compiler.set_accel([msg['x'], msg['y']])


            elif msg['type'] == 'add_effect':
                add_effect_from_dj(msg['effect'])

            elif msg['type'] == 'remove_effect':
                effect_name = msg['effect']
                remove_effect_name(effect_name)

            elif msg['type'] == 'beat_sens_up':
                result = winamp.winamp_wrapper.increase_beat_sensitivity()
                if result is not None:
                    beat_sens_number = f'{result:.2f}'
                beat_sens_string = f'Beat Sens: {beat_sens_number}'
                # print(f'recieved beat_sens_up, {beat_sens_string=}')
                broadcast_light_status = True

            elif msg['type'] == 'beat_sens_down':
                result = winamp.winamp_wrapper.decrease_beat_sensitivity()
                if result is not None:
                    beat_sens_number = f'{result:.2f}'
                beat_sens_string = f'Beat Sens: {beat_sens_number}'
                # print(f'recieved beat_sens_down, {beat_sens_string=}')
                broadcast_light_status = True

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
                broadcast_dev_status = True

            elif msg['type'] == 'toggle_laser_mode':
                laser_mode = not laser_mode
                print(f'Toggled laser mode, now in state: {laser_mode}\n')
                if curr_effects:
                    maybe_new_effect_name = maybe_get_laser_version(curr_effects[0][0])
                    if maybe_new_effect_name not in channel_lut:
                        print_green(f'late lut compiling {maybe_new_effect_name}')
                        compile_lut({maybe_new_effect_name: effects_config[maybe_new_effect_name]})
                    curr_effects[0][0] = maybe_new_effect_name

            elif msg['type'] == 'winamp_offset_update':
                slider_id, slider_value = msg['id'], msg['value']
                # print(f'Recieved winamp offset update: {slider_id} = {slider_value}')
                curr_winamp_effect = None
                for i in range(len(curr_effects)):
                    effect_name = curr_effects[i][0]
                    effect = effects_config[effect_name]
                    for p in effect.get('profiles', []):
                        if 'winamp' in p.lower():
                            curr_winamp_effect = (effect_name, effect)
                            break
                if curr_winamp_effect is None:
                    print_red('No winamp effect found, skipping winamp offset update')
                    continue

                effect = curr_winamp_effect[1]
                winamp_offsets = effect.get('winamp_offsets', {
                    'winamp_bright_shift': 0,
                    'winamp_hue_shift': 0,
                    'winamp_sat_shift': 0,
                    'winamp_beat_sensitivity': 1,
                    'rating': 0,
                })
                if slider_id == 'lightness':
                    winamp_offsets['winamp_bright_shift'] = float(slider_value) / 100
                elif slider_id == 'hue':
                    winamp_offsets['winamp_hue_shift'] = float(slider_value) / 360
                elif slider_id == 'saturation':
                    winamp_offsets['winamp_sat_shift'] = float(slider_value) / 100
                elif slider_id == 'sensitivity':
                    winamp_offsets['winamp_beat_sensitivity'] = float(slider_value)
                elif slider_id == 'rating':
                    winamp_offsets['rating'] = int(slider_value)
                effect['winamp_offsets'] = winamp_offsets

                effects_config_dj_client[effect_name]['winamp_offsets'] = winamp_offsets
                broadcast_winamp_offset_update = [effect_name]
                needs_to_save_winamp_offsets = True
                grid_helpers.winamp.winamp_wrapper.winamp_offsets[effect_name] = winamp_offsets


                # from the current effect remove all profiles that have "winamp rated" in them
                if 'profiles' in effect:
                    new_profiles = []
                    for profile in effect['profiles']:
                        if 'winamp rated' not in profile.lower():
                            new_profiles.append(profile)
                    if winamp_offsets['rating'] > 0:
                        new_profiles.append(f'winamp rated {winamp_offsets["rating"]}')
                    new_profiles = list(set(new_profiles))
                    effect['profiles'] = new_profiles
                    effects_config_dj_client[effect_name]['profiles'] = new_profiles

            broadcast_light_status = True


def download_song(url, uuid):
    download_start_time = time.time()
    import autogen

    if 'search_query' in url:
        return print_yellow(f'user {uuid_to_user(uuid)} entered a url with search_query in it, returning')

    max_length_seconds = None
    if not is_admin(uuid):
        max_length_seconds = 15 * 60
    
    # TODO add caching here
    filepath = youtube_download_helpers.download_youtube_url(url=url, dest_path=this_file_directory.joinpath('songs'), max_length_seconds=max_length_seconds)
    if filepath is None:
        return print_yellow('Couldnt download video, returning')
    print(f'finished downloading {url} to {filepath} in {time.time() - download_start_time} seconds')

    add_song_to_config(filepath)
    # !TODO i think we need to prep_loaded_effects here, we are getting saved by the rekordbox watcher?

    added = False
    src_bpm_offset_cache = autogen.get_src_bpm_offset_multiprocess(filepath, use_boundaries=True) 
    for mode in [None, 'lasers']:
        show_name, show, _ = autogen.generate_show(filepath, overwrite=True, mode=mode, src_bpm_offset_cache=copy.deepcopy(src_bpm_offset_cache))
        if show is None:
            print_red(f'Autogenerator failed to create effect for {url}')
            return

        effects_config[show_name] = show
        add_dependancies({show_name: show})

        set_effect_defaults(show_name, show) # !TODO idk if this is needed
        compile_lut({show_name: show})

        print(f'created show for: {show_name}')

        effects_config_queue_client[show_name] = {}
        for key, value in show.items():
            if key != 'beats':
                effects_config_queue_client[show_name][key] = value

        if not added and ((mode == None and not laser_mode) or mode == 'lasers'):
            added = True
            print(f'should be adding {show.get("song_path")}\n' * 10)
            if 'song_path' in show:
                print(f'Auto adding "{show_name}" to queue')
                add_queue_balanced(show_name, uuid)


async def init_queue_client(websocket, path=None):
    global curr_bpm, song_playing, song_time, broadcast_light_status, broadcast_song_status
    print('Song Queue: made connection to new client')

    # !TODO here and the other place we need to gzip effects_config_queue_client i think
    message = {
        'effects': effects_config_queue_client,
        'songs': songs_config,
        'queue': song_queue,
        'users': users,
        'status': {
            'playing': song_playing,
            'time': song_time + (max(pygame.mixer.music.get_pos(), 0) / 1000)
        }
    }
    dump = json.dumps(message)
    # !TODO shouldn't this just error and fail if it fails?????? maybe preventing same client from reconnecting
    try:
        print('Song Queue: sent config to new client')
        await websocket.send(dump)
    except:
        print('Song Queue: socket send failed', flush=True)

    song_sockets.append(websocket)
    while True:
        try:
            print('Song Queue: waiting for message')
            msg = json.loads(await websocket.recv())
        except:
            song_sockets.remove(websocket)
            if websocket.remote_address and len(websocket.remote_address) == 2:
                addy_1, addy_2 = websocket.remote_address
                print('DJ Client: socket recv FAILED - ' + addy_1 + ' : ' + str(addy_2), flush=True)
            else:
                print('DJ Client: socket recv FAILED - ' + str(websocket.remote_address), flush=True)
            break

        print('Song Queue: message recieved:', msg)
        if 'uuid' not in msg:
            print_red(f'uuid not in msg: {msg}')
            continue
        uuid = msg['uuid']
        username = uuid_to_user(uuid)
        
        if 'type' in msg:
            if msg['type'] == 'add_queue_balanced':
                print(f'Song Queue: added to queue by {username}')
                add_queue_balanced(msg['effect'], uuid)

            elif msg['type'] == 'remove_queue':
                print(f'Song Queue: removed from queue by {username}')
                effect_name = msg['effect']
                salt = msg['salt']
                # TODO share this code with light() probably
                for i in range(len(song_queue)):
                    if song_queue[i][0] == effect_name and song_queue[i][1] == salt and (song_queue[i][2] == uuid or is_admin(uuid)):
                        song_queue.pop(i)
                        if i == 0:
                            song_was_playing = stop_song()
                            song_time = 0
                            remove_effect_name(effect_name)
                            if song_was_playing and len(song_queue) > 0:
                                new_effect_name = song_queue[0][0]
                                add_effect(new_effect_name)
                                play_song(new_effect_name)
                            broadcast_light_status = True
                        break
                if len(song_queue) == 0: # is this possible?
                    song_playing = False

            elif msg['type'] == 'play_queue':
                print(f'Song Queue: Play requested ----UUID: {username}')
                if is_admin(uuid):
                    if len(song_queue) > 0 and not song_playing:
                        effect_name = song_queue[0][0]
                        add_effect(effect_name)
                        broadcast_light_status = True
                        play_song(effect_name)

            elif msg['type'] == 'pause_queue':
                print(f'Song Queue: Pause requested ----UUID: {username}')
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

            elif msg['type'] == 'download_song' and 'url' in msg:
                url = msg['url']
                print_blue(f'Song Queue: Adding "{url}" to youtube downloading queue from {username}')
                download_queue.append([url, uuid])
                try:
                    await websocket.send(json.dumps({ 'notification': 'Download Started...' }))
                except:
                    print_red('socket send failed on download_song response', flush=True)

            elif msg['type'] == 'search_song':
                search = msg.get('search', None)
                print(f'Song Queue: searching youtube "{search}" from {username}')
                search_queue.append([search, websocket, False])
            broadcast_song_status = True


def search_youtube():
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
    return True or (uuid in users and users[uuid]['admin'])


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


async def send_client_queue_config():
    queue_message = {
        'effects': effects_config_queue_client,
        'songs': songs_config,
    }
    await broadcast(song_sockets, json.dumps(queue_message))


async def send_light_status():
    global broadcast_light_status, beat_sens_string
    message = {
        'status': {
            'effects': curr_effects,
            'rate': curr_bpm,
            'laser_mode': laser_mode,
            'beat_sens_string': beat_sens_string,
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


async def send_winamp_offsets():
    global broadcast_winamp_offset_update

    if broadcast_winamp_offset_update:
        effect_names = [x for x in broadcast_winamp_offset_update]

        my_arr = []
        for effect_name in effect_names:
            # print(f'UPDATING {effect_name=}, {winamp_offsets}' * 50)
            effect = effects_config[effect_name]
            winamp_offsets = effect.get('winamp_offsets', {
                'winamp_bright_shift': 0,
                'winamp_hue_shift': 0,
                'winamp_sat_shift': 0,
                'winamp_beat_sensitivity': 1,
                'rating': 0,
            })
            my_arr.append({
                'effect_name': effect_name,
                'winamp_bright_shift': winamp_offsets['winamp_bright_shift'] * 100,
                'winamp_hue_shift': winamp_offsets['winamp_hue_shift'] * 360,
                'winamp_sat_shift': winamp_offsets['winamp_sat_shift'] * 100,
                'winamp_beat_sensitivity': winamp_offsets['winamp_beat_sensitivity'],
                'rating': winamp_offsets['rating'],
            })
        print(my_arr)
        await broadcast(light_sockets, json.dumps({
            'update_winamp_offsets': my_arr
        }))
        broadcast_winamp_offset_update = False




async def send_dev_status():
    global broadcast_dev_status
    sub_effect_names = []
    for effect in curr_effects:
        sub_effect_names += get_sub_effect_names(effect[0], (beat_index / SUB_BEATS) + 1)

    message = {
        'status': {
            'effects': [[x, 0] for x in sub_effect_names] + curr_effects,
            'dev_mode': True,
        }
    }
    await broadcast(dev_sockets, json.dumps(message))

    if broadcast_dev_status:
        tmp_sockets = []
        for sock in light_sockets:
            if sock not in dev_sockets:
                tmp_sockets.append(sock)

        message = {
            'status': {
                'effects': curr_effects,
                'dev_mode': False,
            }
        }
        await broadcast(tmp_sockets, json.dumps(message))
        broadcast_dev_status = False

def uuid_to_user(uuid):
    if uuid in users:
        return users[uuid]['name'] + f' ({uuid})'
    return uuid

####################################

def get_sub_effect_names(effect_name, beat):
    sub_effect_names = []
    for effect in effects_config[effect_name]['beats']:
        if type(effect[1]) == str: # probably isn't needed?
            if effect[0] <= beat <= effect[0] + effect[2]:
                sub_effect_names.append(effect[1])
            elif sub_effect_names:
                break
    return sub_effect_names


previous_sub_effect_names = None
def print_info_terminal_lines():
    global last_effect_change_in_beats, previous_sub_effect_names
    curr_beat = (beat_index / SUB_BEATS) + 1
    try:
        terminal_size = os.get_terminal_size().columns
    except:
        terminal_size = 45

    show_specific = ''
    all_effect_names = []
    for effect in curr_effects:
        effect_name = effect[0]

        if has_song(effect_name):
            channel_lut_index = (beat_index + effect[1])
            show_specific = f"""\
, Show {round(100 * (channel_lut_index / channel_lut[effect_name]['length']))}%\
"""     
            new_sub_effect_names = get_sub_effect_names(effect_name, curr_beat)
            all_effect_names += new_sub_effect_names
            if previous_sub_effect_names is None:
                last_effect_change_in_beats = None
            elif new_sub_effect_names != previous_sub_effect_names:
                last_effect_change_in_beats = beat_index
            previous_sub_effect_names = new_sub_effect_names
            
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

    # TODO do this right based on the actual effects dictionary...
    change_str = 'BSL ?'
    if last_effect_change_in_beats is not None:
        change_str = f'BSL {(beat_index - last_effect_change_in_beats) / SUB_BEATS:.1f}'
    useful_info += f"""\
BPM {curr_bpm:.1f}, \
Beat {curr_beat:.1f}, \
{change_str}\
"""
    useful_info += f'{show_specific}'
    useful_info = useful_info[:terminal_size]

    effect_string = f'Effects: {", ".join(all_effect_names)}'
    effect_string = effect_string[:terminal_size]

    to_fill = terminal_size - len(effect_string)
    effect_print = ''.join([effect_string, (' ' * to_fill)])
    print(effect_print)

    to_fill = terminal_size - len(useful_info)
    print(useful_info + (' ' * to_fill))
    return 2


laser_representation = '.,-~:;=!*#$@'
laser_motor_stage = random.randint(0, 1000)
laser_motor_max_acceleration = 10
laser_motor_min_deceleration = 10
laser_motor_velocity = 0

laser_intensity_max_acceleration = 70
laser_intensity_min_deceleration = 70
laser_intensity = 0

max_num = pow(2, 16) - 1
purple = [153, 50, 204]
disco_speed = .15
disco_pos = 0
# !TODO remove the 0-5 indexes
@profile
def render_terminal(light_levels):
    global laser_motor_stage, disco_pos, laser_motor_velocity, laser_intensity

    character = '▆'
    try:
        terminal_size = os.get_terminal_size().columns
    except:
        terminal_size = 45
    line_length = terminal_size - 1

    levels_255 = list(map(lambda x: int(x * 2.55), light_levels))
    # bottom_rgb_complete = levels_255[6:9]
    bottom_rgb_hori_complete = levels_255[6:9]
    uv_value = levels_255[9]
    target_laser_color_rgb = levels_255[10:12]
    target_laser_motor_value = min(100, max(0, levels_255[12] / 2.55))
    disco_color_rgb = levels_255[13:16]
    bottom_rgb_vert_complete = levels_255[16:19]


    purple_scaled = list(map(lambda x: int(x * (uv_value / 255)), purple))
 
    if any(target_laser_color_rgb):
        laser_chars = list(f'{" " * line_length}\n' * 3)
        for i in range(3):
            for j in range(15):
                if j > 1 and (j + i + (laser_motor_stage // 100)) % 4 == 0: # this was // 90 for some reason idk why
                    laser_chars[j + (line_length * i)] = laser_representation[laser_motor_stage // 100]
        laser_string = ''.join(laser_chars)
        laser_style = [target_laser_color_rgb[1], target_laser_color_rgb[0], 0]
    else:
        laser_string = f'{" " * (terminal_size - 1)}\n' * 3
        laser_style = [0, 0, 0]

    if any(disco_color_rgb):
        disco_chars = [' '] * grid_helpers.GRID_HEIGHT
        for rgb_index in range(3):
            if disco_color_rgb[rgb_index]:
                style_for_color = [0, 0, 0]
                style_for_color[rgb_index] = disco_color_rgb[rgb_index]
                for pos_offset in [0, 5, 10, 15, 20, 25]:
                    position = (int(disco_pos) + pos_offset + rgb_index) % grid_helpers.GRID_HEIGHT
                    disco_chars[position] = rgb_ansi('o', style_for_color)
    else:
        disco_chars = ' ' * grid_helpers.GRID_HEIGHT

    if laser_motor_velocity < target_laser_motor_value:
        laser_motor_velocity += min(laser_motor_max_acceleration, target_laser_motor_value - laser_motor_velocity)
    elif laser_motor_velocity > target_laser_motor_value:
        laser_motor_velocity -= min(laser_motor_min_deceleration, laser_motor_velocity - target_laser_motor_value)
    laser_motor_stage += int(laser_motor_velocity)
    laser_motor_stage %= 1000

    disco_pos += disco_speed
    if disco_pos > grid_helpers.GRID_HEIGHT:
        disco_pos -= grid_helpers.GRID_HEIGHT    

    # laser_intensity will be 0-1
    # if laser_intensity < 1:

    top_uv_row = rgb_ansi(character * grid_helpers.GRID_HEIGHT, purple_scaled)
    bottom_light_row = rgb_ansi(character * (grid_helpers.GRID_HEIGHT // 2), bottom_rgb_hori_complete)
    bottom_light_row += rgb_ansi(character * (grid_helpers.GRID_HEIGHT // 2), bottom_rgb_vert_complete)
    laser_row = rgb_ansi(laser_string, laser_style)
    disco_row = ''.join([char for char in disco_chars])

    top_lines_to_reset = print_info_terminal_lines()

    # actually i bet this really doesn't work because of invisible ansi characters... and cutting off doesnt work because they have length, we need to just keep track
    print(top_uv_row)
    grid_rows_to_reset = grid_helpers.render(terminal=True, reset_terminal=False)
    print(laser_row)
    print(bottom_light_row)
    print(disco_row, end='')
    sys.stdout.write('\033[F' * (6 + grid_rows_to_reset + top_lines_to_reset))

####################################

pin_light_levels = [0] * LIGHT_COUNT

last_guys = None
@profile
async def light():
    global beat_index, song_playing, song_time, broadcast_song_status, broadcast_light_status, last_called_grid_render, curr_effects, last_guys

    download_thread = None
    search_thread = None 
    while True:
        infos_for_this_sub_beat = {}
        grid_fill_from_old = True
        clear_grid_at_start = True

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

        rebuild_effects = False
        for effect_name, start_index in curr_effects: 
            index = beat_index + start_index
            if not channel_lut[effect_name]['loop'] and index >= channel_lut[effect_name]['length']:
                rebuild_effects = True
                break

        if rebuild_effects:
            broadcast_light_status = True
            curr_effects = [ # list comp is fastest
                effect for effect in curr_effects 
                if channel_lut[effect_name]['loop'] or beat_index + start_index < channel_lut[effect_name]['length']
            ]

        # For the grid function effects
        for effect_name, start_index in curr_effects:
            info_arr = channel_lut[effect_name].get('info', None)
            if info_arr is not None:
                index = beat_index + start_index
                looped = False
                if index >= 0 and channel_lut[effect_name]['loop']:
                    # !idk about this
                    if index >= channel_lut[effect_name]['length']:
                        looped = True
                    index = index % channel_lut[effect_name]['length']

                # print(f'Looking at {len(info_arr)} info_arrs for {effect_name}\n' * 8)
                # !TODO i think this is the slowest part for lots of grid effects, take a look, probably can be smart about start beat
                for start_b, end_b, info in info_arr:
                    # print(f'{index=}\n' * 8)
                    if start_b <= index < end_b:
                        info.length = end_b - start_b
                        info.curr_sub_beat = index - start_b
                        info.percent_done = info.curr_sub_beat / info.length
                        info.bpm = curr_bpm
                        info.time_diff = time_diff
                        info.looped = looped
                        
                        priority = getattr(info, 'priority', 0)
                        if priority not in infos_for_this_sub_beat:
                            infos_for_this_sub_beat[priority] = []
                        infos_for_this_sub_beat[priority].append(info)

                        clear_grid_at_start = clear_grid_at_start and getattr(info, 'clear', True)
                        grid_fill_from_old = grid_fill_from_old and getattr(info, 'grid_fill_from_old', True)

        # Preparing the pin light values (laser, laser motor, disco, floor lights, old grid)
        for light_index in range(LIGHT_COUNT):
            level = 0
            for effect_name, start_index in curr_effects:
                modified_beat_index = beat_index + start_index # what is this variable??
                if 'beats' in channel_lut[effect_name] and modified_beat_index >= 0 and (channel_lut[effect_name]['loop'] or modified_beat_index < channel_lut[effect_name]['length']):
                    modified_beat_index = modified_beat_index % channel_lut[effect_name]['length']
                    level += channel_lut[effect_name]['beats'][modified_beat_index][light_index]
            pin_light_levels[light_index] = max(0, min(100, level))

        # Preparing new grid_helpers.grid for display
        if clear_grid_at_start:
            grid_helpers.reset()
        
        if grid_fill_from_old:
            grid_levels_from_front_back = pin_light_levels[:6]
            if args.full_grid:
                # full fill (overbearing because entire grid)
                grid_helpers.grid[:, grid_helpers.GRID_HEIGHT // 2:] = [grid_levels_from_front_back[0], grid_levels_from_front_back[1], grid_levels_from_front_back[2]] # front
                grid_helpers.grid[:, :grid_helpers.GRID_HEIGHT // 2] = [grid_levels_from_front_back[3], grid_levels_from_front_back[4], grid_levels_from_front_back[5]] # back        
            else:
                def grid_fill_fancy(rgbs, centerpoint):
                    # bright_to_go is initally brightness percentage out of 100.
                    bright_to_go = max(rgbs)
                    rgbs = [rgbs[0], rgbs[1], rgbs[2]]
                    # max_per_bucket determines what percent each bucket can contribute.
                    # ideally would add to 100%
                    max_per_bucket = [14.25, 13.75, 13.25, 12.75, 12.25, 11.75, 11.25, 10.75] # there are 8 rows available, including center
                    rgb_outs = []
                    # center is special case:
                    row_bright = min(bright_to_go, max_per_bucket[0])
                    bright_to_go -= row_bright
                    rgb_outs.append([x*row_bright/14.25 for x in rgbs])
                    counter = 1
                    while bright_to_go > 0:
                        row_bright = min(bright_to_go, max_per_bucket[counter])
                        bright_to_go -= row_bright*2
                        rgb_outs.append([x*row_bright/14.25 for x in rgbs])
                        counter += 1
                    extra = 0
                    if centerpoint == 3:
                        extra = -1
                    for i, rgb in enumerate(rgb_outs):
                        if i == 0:
                            grid_helpers.grid[:, int(centerpoint * (grid_helpers.GRID_HEIGHT / 4)) + extra] = [rgb[0], rgb[1], rgb[2]] # front
                        else:
                            grid_helpers.grid[:, (int(centerpoint * (grid_helpers.GRID_HEIGHT / 4))+i) + extra] = [rgb[0], rgb[1], rgb[2]] # front
                            grid_helpers.grid[:, (int(centerpoint * (grid_helpers.GRID_HEIGHT / 4))-i) + extra] = [rgb[0], rgb[1], rgb[2]] # front
                grid_fill_fancy([grid_levels_from_front_back[0], grid_levels_from_front_back[1], grid_levels_from_front_back[2]], 3)
                grid_fill_fancy([grid_levels_from_front_back[3], grid_levels_from_front_back[4], grid_levels_from_front_back[5]], 1)
                
            # semi fill (looks like pre-grid)
            # grid_helpers.grid[:, int(3 * (grid_helpers.GRID_HEIGHT / 4))] = [grid_levels_from_front_back[0]-50, grid_levels_from_front_back[1]-50, grid_levels_from_front_back[2]-50] # front
            # grid_helpers.grid[:, grid_helpers.GRID_HEIGHT // 4] = [grid_levels_from_front_back[3], grid_levels_from_front_back[4], grid_levels_from_front_back[5]] # back

        # !TODO stable sort it so that winamps are always first in the current effects? Then it'll only apply the winamp offsets once to just the winamp effects 
        has_played_winamp = False
        for priority, info_arr in sorted(list(infos_for_this_sub_beat.items())):
            for info in info_arr:
                if getattr(info, 'is_winamp', None) is True:
                    if has_played_winamp:
                        continue
                    has_played_winamp = True
                
                try:
                    info.grid_function(info)
                except Exception:
                    print_stacktrace()
                    print_yellow(f'TRIED TO CALL {info=}, but it DIDNT work, stacktrace above')
                
                if getattr(info, 'is_winamp', None) is True:
                    effects = [effects_config[effect_name] for effect_name, _ in curr_effects]
                    for effect in effects:
                        if effect.get('winamp_offsets'):
                            lightness_shift = effect['winamp_offsets'].get('winamp_bright_shift', 0)
                            hue_shift = effect['winamp_offsets'].get('winamp_hue_shift', 0)
                            sat_shift = effect['winamp_offsets'].get('winamp_sat_shift', 0)
                            sensitivity = effect['winamp_offsets'].get('winamp_beat_sensitivity', 1.0)
                            winamp.winamp_wrapper.set_beat_sensitivity(sensitivity)
                            for i in range(grid_helpers.GRID_WIDTH):
                                for j in range(grid_helpers.GRID_HEIGHT):
                                    r, g, b = grid_helpers.grid[i, j]

                                    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0

                                    h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
                                    h = (h + hue_shift) % 1.0
                                    l += lightness_shift
                                    s += sat_shift

                                    l = max(0.0, min(1.0, l))
                                    s = max(0.0, min(1.0, s))

                                    r_new_norm, g_new_norm, b_new_norm = colorsys.hls_to_rgb(h, l, s)

                                    r_new = int(r_new_norm * 255)
                                    g_new = int(g_new_norm * 255)
                                    b_new = int(b_new_norm * 255)

                                    grid_helpers.grid[i, j] = [r_new, g_new, b_new]

        grid_helpers.grid = np.clip(grid_helpers.grid, a_min=0, a_max=100)

        # Render the grid to the terminal
        if args.local or args.force_terminal:
            if not args.skip_render:
                # grid_helpers.apply_bezier_to_grid() # for testing
                render_terminal(pin_light_levels) # this also renders the grid to the terminal


        # Send relevant pin light levels to the pi. Pins 6-8 are the floor
        if not args.local:
            # just scale 0-500 to 0-100 for pin_light_levels [6, 7, 8, 16, 17, 18]
            order_to_color = {
                0: grid_helpers.grid_red_bezier,
                1: grid_helpers.grid_green_bezier,
                2: grid_helpers.grid_blue_bezier
            }
            for index, pin_index in enumerate([6, 7, 8, 16, 17, 18]):
                bezier_color = order_to_color[index % 3]
                pin_light_levels[pin_index] = round(pin_light_levels[pin_index])
                pin_light_levels[pin_index] = bezier_color[pin_light_levels[pin_index]]

                pin_light_levels[pin_index] = round((pin_light_levels[pin_index] / 600) * 100)
                pin_light_levels[pin_index] = max(0, min(100, pin_light_levels[pin_index])) 



            # pin_light_levels[6] = grid_helpers.bottom_red_bezier[pin_light_levels[6]]
            # pin_light_levels[7] = grid_helpers.bottom_green_bezier[pin_light_levels[7]]
            # pin_light_levels[8] = grid_helpers.bottom_blue_bezier[pin_light_levels[8]]

            # All the pin light levels and the pins are lined up except for the floor vertical floor lights
            for index in range(6, len(pin_light_levels) - 3):
                send_num_to_pi = round((pin_light_levels[index] / 100) * LED_RANGE)
                pi.set_PWM_dutycycle(LED_PINS[index], send_num_to_pi)

            # vertical floor
            for light_level_index, pin_index in zip([16, 17, 18], [3, 4, 5]):
                send_num_to_pi = round((pin_light_levels[light_level_index] / 100) * LED_RANGE)
                pi.set_PWM_dutycycle(LED_PINS[pin_index], send_num_to_pi)

        if args.should_print_info_terminal_lines:
            if last_guys:
                print('\033[F' * last_guys, end='')
            last_guys = print_info_terminal_lines()
            
        # Sends the grid to the pi 
        if not args.local:
            if args.no_curve:
                grid_helpers.apply_bezier_to_grid()
            grid_helpers.render()

        # check on youtube downloads
        if download_thread is not None:
            if not download_thread.is_alive():
                await send_client_queue_config()
                await send_song_status()
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

        # if anything's changed we need to resend info to clients
        if broadcast_light_status:
            await send_light_status()
        if broadcast_song_status:
            await send_song_status()
        if broadcast_dev_status or (dev_sockets and beat_index % SUB_BEATS == 0):
            await send_dev_status()
        if broadcast_winamp_offset_update:
            await send_winamp_offsets()
        
        # math for the next beat
        time_diff = time.time() - time_start

        direction = 1 
        if rate < 0:
            direction = -1
        time_delay = ((beat_index + direction) / rate) - time_diff

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

    # if new_effect_name in effects_config and 'song_path' in effects_config[new_effect_name]:
    #     print(f'Adding effect with song named {new_effect_name}')

    if new_effect_name not in channel_lut:
        print_green(f'late lut compiling {new_effect_name}')
        compile_lut({new_effect_name: effects_config[new_effect_name]})

    effect = effects_config[new_effect_name]
    if (effect['trigger'] == 'toggle' or effect['trigger'] == 'hold') and get_effect_index(new_effect_name) is not False:
        return

    if new_effect_name in winamp.winamp_wrapper.preset_name_to_filepath:
        index = 0
        while index < len(curr_effects):
            existing_name = curr_effects[index][0]
            if existing_name in winamp.winamp_wrapper.preset_name_to_filepath:
                curr_effects.pop(index)
            else:
                index += 1

    if 'bpm' in effect:
        if 'downloaded_songs' in str(effect.get('song_path', 'downloaded_songs')):
            print_yellow('Only clearing other effects with songs because i think this is a rekordbox switch')
            for effect_name, start_index in curr_effects:
                if effects_config[effect_name].get('was_autogenerated', False):
                    remove_effect_name(effect_name)
        else:
            clear_effects()

        curr_bpm = effect['bpm']

        to_delay = effect['delay_lights']
        if args.absolute_delay_seconds:
            to_delay += args.absolute_delay_seconds
        if not args.local:
            to_delay += 0.08
        
        time_start = time.time() + to_delay - song_time
        beat_index = int((-to_delay) * (curr_bpm / 60 * SUB_BEATS))
        offset = 0
    else:
        snap = round(effect['snap'] * SUB_BEATS)
        offset = beat_index % snap
        if offset > snap * 0.5:
            offset -= snap
        offset -= beat_index
    curr_effects.append([new_effect_name, offset])


def play_song(effect_name, quiet=False): # disabled rekordbox input
    global take_rekordbox_input, song_playing
    take_rekordbox_input = False
    song_path = effects_config[effect_name]['song_path']
    start_time = effects_config[effect_name]['skip_song'] + song_time
    
    print(f'start_time: {start_time:,.2f}, skip_song: {effects_config[effect_name]["skip_song"]:.2f}, song_time: {song_time:.2f}')
    if not quiet: print_blue(f'Starting music from {effect_name}: "{song_path}" at {start_time} seconds at {round(args.volume * 100)}% volume')

    pygame.mixer.music.set_volume(args.volume)
    pygame.mixer.music.load(pathlib.Path(song_path))
    pygame.mixer.music.play(start=start_time)
    song_playing = True

def stop_song():
    global song_playing
    pygame.mixer.music.stop()
    song_was_playing_before = song_playing
    song_playing = False
    return song_was_playing_before


######################################

effects_config = {}
effects_config_dj_client = {}
effects_config_queue_client = {}
songs_config = {}
song_name_to_show_names = {}

channel_lut = {}

graph = {}
found = {}
simple_effects = []
complex_effects = []


all_infos = []
def effects_config_sort(all_nodes):
    curr_node = all_nodes[-1]
    
    if curr_node in found:
        return
    
    found[curr_node] = True
    if isinstance(curr_node, GridInfo):
        all_infos.append(curr_node)
        complex_effects.append(curr_node)
        return

    for needed_node in graph[curr_node]:
        if needed_node in all_nodes:
            raise Exception(f'Cycle Found: {curr_node} -> {needed_node}')
        effects_config_sort(all_nodes + [needed_node])
    
    if curr_node:
        if len(graph[curr_node]) == 0:
            simple_effects.append(curr_node)
        else:
            complex_effects.append(curr_node)
        

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


def add_dependancies(effect_names):
    for effect_name in effect_names:
        effect = effects_config[effect_name]
        # optimized from below
        graph[effect_name] = list({component[1] for component in effect['beats'] if not isinstance(component[1], list)})
        # for component in effect['beats']:
        #     if not isinstance(component[1], list):
        #         graph[effect_name].add(component[1])
        # graph[effect_name] = list(graph[effect_name])


def add_song_to_config(song_path, quiet=True):
    song_path = pathlib.Path(str(song_path).replace('\\', '/'))
    relative_path = song_path
    if relative_path.is_absolute():
        relative_path = relative_path.relative_to(this_file_directory)
        if not quiet: print(f'relative_path is {relative_path}')

    if song_path.suffix in ['.mp3', '.ogg', '.wav']:
        name, artist, duration, samplerate, _song_path = sound_video_helpers.get_song_metadata_info(song_path)
        if samplerate != 48000:
            print_red(f'This song file is not 48000hz sample rate, {song_path}. This introduces weird bugs, delete the file.')
            return False

        songs_config[str(relative_path.as_posix())] = {
            'name': name,
            'artist': artist,
            'duration': duration
        }
        if not quiet: print(f'Added song to config: {relative_path}, {str(relative_path.as_posix())}')
        return str(relative_path.as_posix())
    else:
        print_red(f'add_song_to_config: CANNOT READ FILETYPE {song_path.suffix} in {song_path}')


def prep_loaded_effects(effect_names):
    global effects_config
    for effect_name in effect_names:
        effect = effects_config[effect_name]
        if effect.get('not_done'):
            del effects_config[effect_name]
            continue
        if 'song_path' in effect:
            effect['song_path'] = effect['song_path'].replace('\\', '/')

    updated_effect_names = []
    temp_stuff = []
    for effect_name in effect_names:
        if effect_name not in effects_config:
            continue
        updated_effect_names.append(effect_name)
        effect = effects_config[effect_name]
        if effect_name.startswith('g_lasers'):
            continue
        if 'song_path' in effect:
            song_name = pathlib.Path(effect['song_path']).stem              
            if song_name not in song_name_to_show_names:
                song_name_to_show_names[song_name] = []
            song_name_to_show_names[song_name].append(effect_name)
            if effect['song_path'] in songs_config:
                if not effect_name.startswith('g_'):
                    if 'profiles' not in effect:
                        effect['profiles'] = []
                    effect['profiles'].append('Shows')
                # print(effect_name, song_name_to_show_names[song_name])
            elif effect.get('song_not_avaliable', True):
                if not effect_name.startswith('g_'): # !TODO replace with "was_autogenerated"
                    print(yellow('handmade song not avaliable') + f' "{effect["song_path"]=}"')
                if args.show_name:
                    effect['song_not_avaliable'] = True
                # else:
                #     del effect['song_path']
                    # print_red('deleted', _effect_name)
    print(f'{len(song_name_to_show_names)=}, {len(effect_names)=:,}, {len(temp_stuff)=}')
    add_dependancies(updated_effect_names)


def load_effects_config_from_disk():
    global effects_config, effects_config_queue_client, effects_config_dj_client, graph, found, song_name_to_show_names
    update_config_and_lut_time = time.time()

    effects_config = {}
    effects_config_dj_client = {}
    effects_config_queue_client = {}

    graph = {}
    found = {}

    song_name_to_show_names = {}

    effects_dir = this_file_directory.joinpath('effects')

    import_time = 0
    found_paths = list(get_all_paths(effects_dir, only_files=True))
    if args.load_autogen_shows:
        found_paths += list(get_all_paths(effects_dir.joinpath('rekordbox_effects'), quiet=True, only_files=True)) + list(get_all_paths(effects_dir.joinpath('autogen_shows'), quiet=True, only_files=True))

    for name, filepath in found_paths:
        if name == 'compiler.py':
            continue
    
        relative_path = filepath.relative_to(this_file_directory)
        # print(f'LOADING: {relative_path} \n ' * 10)
        without_suffix = relative_path.parent.joinpath(relative_path.stem)
        module_name = str(without_suffix).replace(os.sep, '.')
        t1 = time.time()
        globals()[module_name] = importlib.import_module(module_name) # to reload: importlib.reload(globals()[module_name])
        effects.compiler.next_beat = None
        import_time += time.time() - t1
        
        for effect_name in globals()[module_name].effects:
            if globals()[module_name].effects.get('was_autogenerated'): # IDK WHY THIS WAS HERE BUT IT KINDA WAS?
                if effect_name in effects_config:
                    print_red(f'ERROR: Effect name collision "{effect_name}"\n    File 1:   {effects_config[effect_name]["from_python_file"]}\n    File 2: {relative_path}')
                    exit()
        
        effects_config.update(globals()[module_name].effects)
        for effect_name in globals()[module_name].effects:
            effects_config[effect_name]['from_python_file'] = str(relative_path)

    prep_loaded_effects(list(effects_config.keys()))
    print_blue(f'load_effects_config_from_disk took {time.time() - update_config_and_lut_time:.3f}, import modules time: {import_time:.3f}, imported {len(found_paths)} modules')


def set_effect_defaults(effect_name, effect): # this must be safe to run multiple times
    if 'hue_shift' not in effect:
        effect['hue_shift'] = 0
    if 'sat_shift' not in effect:
        effect['sat_shift'] = 0
    if 'bright_shift' not in effect:
        effect['bright_shift'] = 0
    if 'grid_bright_shift' not in effect:
        effect['grid_bright_shift'] = 0
    if 'snap' not in effect:
        effect['snap'] = 1 / SUB_BEATS
    else:
        effect['snap'] = max(effect['snap'], 1 / SUB_BEATS)
    if 'trigger' not in effect:
        effect['trigger'] = 'toggle'
    if 'profiles' not in effect:
        effect['profiles'] = []
    if effect.get('autogen') and 'Autogen effects' not in effect['profiles']:
        effect['profiles'].append('Autogen effects')

    if 'song_path' in effect:
        effect['song_path'] = str(pathlib.Path(effect['song_path'])).replace('\\', '/')
        effect['loop'] = False # !todo verify this is a correct assumption

        if 'delay_lights' not in effect:
            effect['delay_lights'] = 0

        if effect['song_path'] in songs_config: # song file has been successfully loaded
            if 'bpm' not in effect:
                print_red(f'Show "{effect_name}" must have bpm. Song path found: {effect["song_path"]}\n' * 10)
                exit()

            if 'length' not in effect:
                effect['length'] = songs_config[effect['song_path']]['duration'] * effect['bpm'] / 60
    if 'loop' not in effect:
        effect['loop'] = True

    if args.winamp and effect_name in grid_helpers.winamp.winamp_wrapper.winamp_offsets:
        effect['winamp_offsets'] = grid_helpers.winamp.winamp_wrapper.winamp_offsets[effect_name]
        rating = effect['winamp_offsets'].get('rating', 0)
        if rating > 0:
            effect['profiles'].append(f'winamp rated {rating}')
    else:
        if args.winamp and 'from_python_file' in effect and effect['from_python_file'] == 'effects/winamp_effects.py':
            effect['winamp_offsets'] = {
                'winamp_bright_shift': 0,
                'winamp_hue_shift': 0,
                'winamp_sat_shift': 100,
                'winamp_beat_sensitivity': 1.0,
                'rating': 0,
            }
            grid_helpers.winamp.winamp_wrapper.winamp_offsets[effect_name] = effect['winamp_offsets']


def precompile_some_luts_effects_config():
    compile_all_luts_start_time = time.time()

    effects_config_to_compile = {}
    if args.show_name:
        effects_config_to_compile[args.show_name] = effects_config[args.show_name]

    for effect_name, effect in effects_config.items():
        set_effect_defaults(effect_name, effect)
        if effect.get('profiles', None) or effect.get('song_path', None) in songs_config:
            effects_config_clients = [effects_config_dj_client, effects_config_queue_client]
            # commenting this is a perf test, comment to slow down the dj client
            if effect.get('was_autogenerated', False):
                effects_config_clients = [effects_config_queue_client]
            
            needed_fields = ['profiles', 'loop', 'trigger', 'bpm', 'length', 'song_path', 'was_autogenerated', 'winamp_offsets']
            for effects_config_client in effects_config_clients:
                effects_config_client[effect_name] = {key: value for key, value in effect.items() if key in needed_fields}

                # for key, value in effect.items():
                #     if key == 'winamp_offsets':
                #         print(f'OK HERE {value}')
                        # exit()

    # print(effects_config_dj_client)
    # from pympler import asizeof
    # print(f'Size of effects_config_client: {bytes_to_human_readable_string(asizeof.asizeof(effects_config_dj_client))}')
    # exit()

    if is_doorbell():
        for effect_name, effect in effects_config.items(): # eager compile all normal effects
            if 'bpm' not in effect and not effect.get('winamp') and effect.get('profiles'):
                effects_config_to_compile[effect_name] = effect

    compile_lut(effects_config_to_compile)
    print_blue(f'precompile_some_luts_effects_config took: {time.time() - compile_all_luts_start_time:.3f} to compile {len(effects_config_to_compile):,} effects, and did preliminary setup on {len(effects_config):,} effects')


def set_complex_effect_defaults(effect):
    for component in effect['beats']:
        start_beat = component[0] - 1
        reference_effect_name = component[1]
        
        # !todo look if this is right
        # if isinstance(reference_effect_name, GridInfo):
        #     return
        
        if len(component) == 2:
            if effects_config[reference_effect_name]['loop']:
                component.append(effect['length'] - start_beat)
            else:
                component.append(effects_config[reference_effect_name]['length'])
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


def calculate_complex_effect_length(effect):
    calced_effect_length = 0
    for component in effect['beats']:
        start_beat = component[0] - 1
        calced_effect_length = max(calced_effect_length, start_beat + component[2])
    return calced_effect_length


def compile_lut(local_effects_config):
    global channel_lut, simple_effects, complex_effects

    simple_effects = []
    complex_effects = []

    sort_perf_timer = time.time()
    for name, effect in local_effects_config.items():
        set_effect_defaults(name, effect)
        missing_effect = dfs(name)
        if missing_effect is not None:
            raise Exception(red(f'dfs: while trying to find dependencies of effect {name}, we found sub complex effect "{missing_effect}" missing from effects_config, probably you changed an effect name.'))
    print_blue(f'Sort took: {time.time() - sort_perf_timer:.3f} seconds')
    
    simple_effect_perf_timer = time.time()
    for effect_name in simple_effects:
        effect = effects_config[effect_name]

        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * LIGHT_COUNT] * round(effect['length'] * SUB_BEATS)],
        }
        for component in effect['beats']:
            start_beat = round((component[0] - 1) * SUB_BEATS)
            channels = component[1]

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
    print_blue(f'Simple effects took: {time.time() - simple_effect_perf_timer:.3f} seconds')

    complex_effect_perf_timer = time.time()
    for effect_name_or_info in complex_effects:
        if isinstance(effect_name_or_info, GridInfo):
            # !TODO i think this length thing might be wrong...
            channel_lut[effect_name_or_info] = {
                # 'length': 0,
                'length': effect_name_or_info.length,
                'info': effect_name_or_info,
            }
            continue

        effect_name = effect_name_or_info
        effect = effects_config[effect_name]
        set_complex_effect_defaults(effect)

        if 'length' not in effect:
            effect['length'] = calculate_complex_effect_length(effect)

        channel_lut[effect_name] = {
            'length': round(effect['length'] * SUB_BEATS),
            'loop': effect['loop'],
            'beats': [x[:] for x in [[0] * LIGHT_COUNT] * round(effect['length'] * SUB_BEATS)],
        }
        curr_channel = channel_lut[effect_name]
        beats = channel_lut[effect_name]['beats']

        for component in effect['beats']:
            start_beat = round((component[0] - 1) * SUB_BEATS)
            reference_name = component[1]
            if reference_name not in channel_lut:
                raise Exception(f'complex effect {effect_name} references effect {reference_name} which does not exist')

            length = round(min(component[2] * SUB_BEATS, channel_lut[effect_name]['length'] - start_beat))

            start_mult = component[3]
            end_mult = component[4]
            offset = round(component[5] * SUB_BEATS)
            hue_shift = component[6]
            sat_shift = component[7]
            bright_shift = component[8]


            reference_channel = channel_lut[reference_name]
            reference_length = channel_lut[reference_name]['length']
            if 'info' in reference_channel:
                if 'info' not in curr_channel:
                    curr_channel['info'] = []
                ref_channel_all_infos = reference_channel['info']
                # print_red(f'we are on effect {effect_name}, {start_beat=}, {length=} and we are adding info from {reference_name}, {ref_channel_all_infos=}')
            
                if isinstance(ref_channel_all_infos, GridInfo):
                    ref_grid_info = ref_channel_all_infos
                    if ref_grid_info.copy:
                        ref_grid_info = copy.deepcopy(ref_grid_info)
                    curr_channel['info'].append(
                        [
                            start_beat,
                            start_beat + length,
                            ref_grid_info,
                        ],
                    )
                else:
                    for (ref_start_beat, ref_end_beat, ref_grid_info) in ref_channel_all_infos:
                        if ref_grid_info.copy:
                            ref_grid_info = copy.deepcopy(ref_grid_info)
                        # !TODO idk if this is right...
                        if offset:
                            # print_cyan(f'  offsetting by {offset=}')
                            ref_start_beat += offset
                            ref_end_beat += offset


                        ref_info_length = ref_end_beat - ref_start_beat
                        # print(f'taking a look at {(ref_start_beat, ref_end_beat, ref_info)}')
                        for calced_start_beat in range(start_beat + ref_start_beat, start_beat + length, reference_length):
                            # print_green(f'  info compiler: {effect_name=}, {start_beat=}, {ref_start_beat=}, {calced_start_beat=}, {length=}, {reference_length=}, {ref_info_length=}, and we are adding info from {reference_name}, {ref_channel_all_infos=}')
                            calced_end_beat = min(calced_start_beat + ref_info_length, start_beat + length)
                            curr_channel['info'].append(
                                [
                                    calced_start_beat,
                                    calced_end_beat,
                                    ref_grid_info,
                                ],
                            )
                            # print(f'added {curr_channel["info"][-1]}')

            if 'beats' not in channel_lut[reference_name]:
                continue
            reference_beats = channel_lut[reference_name]['beats']
            
            grid_bright_shift = 0
            if len(component) > 9:
                grid_bright_shift = component[9]

            for i in range(length):
                reference_channel = reference_beats[(i + offset) % reference_length]
                if any(reference_channel):
                    final_channel = beats[start_beat + i]

                    if length == 1:
                        mult = start_mult
                    else:
                        mult = (start_mult * ((length-1-i)/(length-1))) + (end_mult * ((i)/(length-1)))
                    

                    # !TODO these next two lines are by far the slowest, the thing right below is an optimization, but only speeds up ~25%
                    # for x in range(LIGHT_COUNT):
                    #     final_channel[x] += reference_channel[x] * mult
                    beats[start_beat + i] = [fin + (ref * mult) for fin, ref in zip(final_channel, reference_channel)]


                    if hue_shift or sat_shift or bright_shift or grid_bright_shift:
                        for index, channel_index in enumerate([0, 3, 6, 16]):
                            rd, gr, bl = beats[start_beat + i][channel_index:channel_index + 3]

                            hue, sat, bright = colorsys.rgb_to_hsv(max(0, rd / 100.), max(0, gr / 100.), max(0, bl / 100.))
                            new_hue = (hue + hue_shift) % 1
                            new_sat = min(1, max(0, sat + sat_shift))
                            # bright shift is relative to initial brightness
                            new_bright = min(1, max(0, bright + bright*bright_shift))
                            if index < 2: # tbd
                                new_bright = min(1, max(0, new_bright + new_bright*grid_bright_shift))
                            beats[start_beat + i][channel_index:channel_index + 3] = colorsys.hsv_to_rgb(new_hue, new_sat, new_bright)

                            beats[start_beat + i][channel_index] *= 100
                            beats[start_beat + i][channel_index + 1] *= 100
                            beats[start_beat + i][channel_index + 2] *= 100

    print_blue(f'Complex effects took: {time.time() - complex_effect_perf_timer:.3f} seconds')

##################################################

def signal_handler(sig, frame):
    print('SIG Handler inside light_server.py: ' + str(sig), flush=True)
    close_connections_to_doorbell()
    if 'multiprocessing' in sys.modules:
        import multiprocessing
        active_children = multiprocessing.active_children()        
        if active_children:
            print_yellow(f'Module multiprocessing was imported! Killing active_children processes, PIDS: {[x.pid for x in active_children]}')
            for child in active_children:
                print_yellow(f'killing {child.pid}')
                child.kill()
    if not args.local or is_windows():
        threading.Thread(target=kill_self, args=(0.5,)).start()
    
    if not args.local:
        grid_helpers.reset()
        grid_helpers.render()
        for pin in LED_PINS:
            if pin != None:
                pi.set_PWM_dutycycle(pin, 0)
    sys.exit()

#################################################

def fuzzy_find(search, collection):
    import thefuzz.process
    choices = thefuzz.process.extractBests(query=search, choices=collection, limit=3)
    # sort so that g_ is deprioritized by 20
    deprioed_choices = []
    for name, rating in choices:
        if name.startswith('g_'):
            deprioed_choices.append((name, max(rating - 20, 0)))
        else:
            deprioed_choices.append((name, rating))
    deprioed_choices.sort(key=lambda x: x[1], reverse=True)
    print_cyan(f'top 3 choices: {deprioed_choices}, returning top no matter what')
    return deprioed_choices[0][0]


def restart_show(skip=0, abs_time=None, quiet=False):
    global song_time
    time_to_skip_to = max(0, (time.time() - time_start) + skip)
    if abs_time is not None:
        time_to_skip_to = abs_time
    song_time = time_to_skip_to

    if not quiet: print(f'restarting show at {time_to_skip_to:.3f} seconds')
    if curr_effects:
        effect_name = curr_effects[0][0]
        if not has_song(effect_name):
            return
        remove_effect_index(0)
        stop_song()
        add_effect(effect_name)
        try:
            play_song(effect_name, quiet=False)
        except:
            print_red('play_song errored, running stop_song + clear_effects and continuing')
            clear_effects()
            stop_song()


#################################################

def try_download_video(show_name):
    just_filename = pathlib.Path(effects_config[show_name]['song_path']).stem
    print(f'Searching with phrase "{just_filename}"')
    youtube_search_result = youtube_download_helpers.youtube_search(just_filename)
    if not youtube_search_result:
        print('Couldnt find relevant video on youtube, exiting...')
        exit()

    url = youtube_search_result['webpage_url']
    downloaded_path = youtube_download_helpers.download_youtube_url(url, dest_path='songs')
    if not downloaded_path:
        raise Exception('Couldnt download youtube video')
    
    add_song_to_config(downloaded_path)
    return downloaded_path


def debug_effect_or_grid(effect_name):
    if effect_name not in effects_config:
        print_red(f'Couldnt find effect {effect_name}')
        return
    channel = channel_lut[effect_name]

    if 'info' not in channel:
        print_red('No info found')
        return
    all_infos = channel['info']

    print_blue(f'{effect_name=}, number of infos: {len(all_infos)}, {channel["length"]=}')
    for info in all_infos:
        print_cyan(f'  info: {info}')


def print_current_beat():
    curr_beat = (beat_index / SUB_BEATS) + 1
    print(f'Beat: {curr_beat:.1f}\n' * 25)


tap_beat_file_path = get_temp_dir().joinpath(f'beat_output_file_{random_letters(8)}.dat')
def output_current_beat():
    print_red(f'OUTPUTTING BEATS TO: {tap_beat_file_path}\n' * 10)
    with open(tap_beat_file_path, 'a') as f:
        curr_beat = (beat_index / SUB_BEATS) + 1
        f.writelines([str(round(curr_beat, 2)), '\n'])


print_cyan(f'Up till main: {time.time() - first_start_time:.3f}')
if __name__ == '__main__':
    if args.local:
        joystick_and_keyboard_helpers.invert_left_right_joystick()

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
    if not args.local:
        setup_gpio()
    
    # import songs
    before_song_config_import = time.time()
    for _, filepath in get_all_paths('songs', only_files=True):
        add_song_to_config(filepath)
    print_blue(f'add_song_to_configs took {time.time() - before_song_config_import:.3f}')

    if args.autogen is not None:
        import autogen

        autogen_song_directory = pathlib.Path(__file__).resolve().parent.joinpath('songs')
        if args.autogen == 'all':
            autogen.generate_all_songs_in_directory(autogen_song_directory)
            sys.exit()
        else:
            all_song_name_and_paths = list(get_all_paths(autogen_song_directory, allowed_extensions=set(['.ogg', '.mp3']), only_files=True))

            all_song_names = [name for name, _path in all_song_name_and_paths]
            song_path = pathlib.Path('songs').joinpath(fuzzy_find(args.autogen, all_song_names))
            args.show_name, _, song_path = autogen.generate_show(song_path, overwrite=True, mode=args.autogen_mode)
            if args.autogen_mode == 'lasers':
                laser_mode = True

    load_effects_config_from_disk()

    if args.load_new_rekordbox_shows_live:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler

        class RekordboxFilesystemHandler(FileSystemEventHandler):
            @staticmethod
            def on_any_event(event):
                filepath = event.src_path
                if not isinstance(filepath, pathlib.Path):
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

                time.sleep(0.05)
                print(f'Loading in new light show because: "{filepath}" was created')
                relative_path = filepath.relative_to(this_file_directory)
                without_suffix = relative_path.parent.joinpath(relative_path.stem)
                module_name = str(without_suffix).replace(os.sep, '.')
                if module_name not in globals():
                    globals()[module_name] = importlib.import_module(module_name)
                else:
                    print_red('Somehow this path was already in globals, doing nothing.')
                effects_config.update(globals()[module_name].effects)
                prep_loaded_effects(list(globals()[module_name].effects.keys()))

        observer = Observer()
        dir_to_watch = make_if_not_exist(effects_dir.joinpath('rekordbox_effects'))
        print_cyan(f'Watchdog for rekordbox song additions: {dir_to_watch}')
        observer.schedule(RekordboxFilesystemHandler(), dir_to_watch, recursive=True)
        observer.start()

    if args.keyboard and not is_doorbell():
        import joystick_and_keyboard_helpers
        skip_time = 5
        def if_is_macos_then_kill_self(delay=0.5):
            if is_macos():
                kill_self(delay)
        joystick_and_keyboard_helpers.add_keyboard_events({
            'p': output_current_beat,
            'b': lambda: print(winamp.winamp_wrapper.get_beat_sensitivity()),
            'u': lambda: winamp.winamp_wrapper.increase_beat_sensitivity(),
            'i': lambda: winamp.winamp_wrapper.decrease_beat_sensitivity(),
            'up': lambda: restart_show(skip=2),
            'down': lambda: restart_show(skip=-2),
            'left': lambda: restart_show(skip=-skip_time),
            'right': lambda: restart_show(skip=skip_time),
            'esc': lambda: if_is_macos_then_kill_self(0.5),
        })
        joystick_and_keyboard_helpers.listen_to_keyboard()

    import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile='fullchain.pem', keyfile='privkey.pem')

    https_server_async(9555, this_file_directory, ssl_context=ssl_context, for_printing= ['', 'dj.html'])

    async def light_show_event_loop_start():
        print_cyan(f'Up to light_show_event_loop_start: {time.time() - first_start_time:.3f}')

        # keeping as non FOR NOW
        rekordbox_bridge_server = await websockets.serve(init_rekordbox_bridge_client, '0.0.0.0', 1567)

        dj_socket_server = await websockets.serve(init_dj_client, '0.0.0.0', 1337, ssl=ssl_context)
        queue_socket_server = await websockets.serve(init_queue_client, '0.0.0.0', 7654, ssl=ssl_context)

        print(f'Websocket servers started, {dj_socket_server.sockets[0].getsockname()=}, {queue_socket_server.sockets[0].getsockname()=}, {rekordbox_bridge_server.sockets[0].getsockname()=}')

        if args.show_name:
            print('Starting show from CLI:', args.show_name)
            only_shows = list(filter(lambda x: has_song(x), effects_config.keys()))
            if args.show_name in only_shows:
                print_blue(f'Found "{args.show_name}" in shows')
            else:
                args.show_name = fuzzy_find(args.show_name, only_shows)

            if effects_config[args.show_name].get('song_not_avaliable'):
                print_yellow(f'Song isnt availiable for effect "{args.show_name}", press enter to try downloading?')
                input()
                try_download_video(args.show_name)
                time.sleep(.01)

            if args.show_name not in effects_config:
                print_red(f'Couldnt find effect named "{args.show_name}"')
                exit()
            show = effects_config[args.show_name]

            if args.skip_show_beats > 1:
                if args.skip_show_seconds:
                    raise Exception('You cant set both skip_show_beats and skip_show_seconds')
                args.skip_show_seconds = (args.skip_show_beats - 1) * (60 / show['bpm'])
            elif args.skip_show_beats != 1.0:
                print_red(f'I dont think a value of {args.skip_show_beats} makes sense for skip_show_beats, skipping...')

            if args.speed != 1:
                ratio = 1 / args.speed
                print_yellow(f'Speed was set to {args.speed}, ratio: {ratio:.3f} changing...')
                print_cyan(f'    Old - {args.skip_show_seconds=:.2f}, skip_song: {show["skip_song"]:.2f}, delay_lights: {show["delay_lights"]:.2f}, {show["bpm"]=}')
                show['song_path'] = add_song_to_config(str(sound_video_helpers.change_speed_audio_asetrate(show['song_path'], args.speed, quiet=True)))
                show['bpm'] *= args.speed
                show['skip_song'] *= ratio
                show['delay_lights'] *= ratio
                args.skip_show_seconds *= ratio
                print_cyan(f'    New - {args.skip_show_seconds=:.2f}, skip_song: {show["skip_song"]:.2f}, delay_lights: {show["delay_lights"]:.2f}, path: {show["song_path"]}, {show["bpm"]=}')
                
            if args.skip_show_seconds:
                global song_time
                song_time = args.skip_show_seconds

        print_cyan(f'Up to precompile_some_luts_effects_config: {time.time() - first_start_time:.3f}')
        precompile_some_luts_effects_config()
        # debug_effect_or_grid('5 hours intro') and exit()

        if args.show_name:
            print_blue('Found in CLI:', args.show_name)
            song_queue.append([args.show_name, get_queue_salt(), 'CLI'])
            add_effect(args.show_name)
            play_song(args.show_name)

        print_cyan(f'Whole startup took total: {time.time() - first_start_time:.3f}')

        asyncio.create_task(light())
        await dj_socket_server.wait_closed() and queue_socket_server.wait_closed() and rekordbox_bridge_server.wait_closed()

    asyncio.run(light_show_event_loop_start())
