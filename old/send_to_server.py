import websockets
import asyncio
import json
import time
import argparse
import pathlib

from helpers import *
import sound_helpers


# https://github.com/chrvadala/music-beat-detector
# https://github.com/shunfu/python-beat-detector




shows_filepath = pathlib.Path(__file__).parent.joinpath('shows.json')
with open(shows_filepath) as f:
    shows = json.loads(f.read())


def precise_wait(time_to_wait):
    time_start = time.perf_counter()
    buffer = .005
    if time_to_wait > buffer:
        time.sleep(time_to_wait - buffer)
    while time.perf_counter() < time_start + time_to_wait:
        pass
    return

websocket_delay = .002

async def show(websocket, show_name):
    show_obj = shows[show_name]

    if '/' in show_obj['song_name'] or '\\' in show_obj['song_name']:
        song_filepath = pathlib.Path(show_obj['song_name'])
    else:
        song_filepath = pathlib.Path(__file__).parent.joinpath('data').joinpath(show_obj['song_name'])
    if not sound_helpers.is_audio_running():
        sound_helpers.play_audio_async(song_filepath, volume=100, paused=True)
        time.sleep(.5)


    msg = {
        'type': 'set_bpm',
        'bpm': show_obj['bpm'],
    }
    await websocket.send(json.dumps(msg))
    msg_from_server = await websocket.recv()
    print(f'{msg_from_server=}')

    sound_helpers.toggle_pause_async_mpv()

    precise_wait(show_obj.get('delay', 0))

    time_start = time.perf_counter()
    show_index = 0
    beats_per_second = 60 / show_obj['bpm']
    beats_so_far_after_pattern = 0
    show_arr = show_obj['show']
    last_target_time = 0
    
    while show_index < len(show_arr):
        await clear_modes(websocket)

        for mode_to_add in show_arr[show_index][:-1]:
            await add_mode(websocket, mode_to_add)

        if show_obj.get('show_timing_type', None) == 'seconds':
            target_time = time_start + show_arr[show_index][-1]
            print(f'time since last beat {target_time - last_target_time}')
            last_target_time = target_time
        else:
            beats_so_far_after_pattern += show_arr[show_index][-1]
            time_to_play_beats = (beats_per_second * beats_so_far_after_pattern)
            target_time = time_start + time_to_play_beats
        time_to_wait = (target_time - time.perf_counter()) - websocket_delay
        precise_wait(time_to_wait)
        show_index += 1


async def clear_modes(websocket):
    msg = {
        'type': 'clear_modes',
    }
    await websocket.send(json.dumps(msg))
    msg_from_server = await websocket.recv()
    print(f'{msg_from_server=}')

async def add_mode(websocket, mode_name):
    msg = {
        'type': 'add_mode',
        'mode': mode_name
    }
    await websocket.send(json.dumps(msg))
    msg_from_server = await websocket.recv()
    print(f'{msg_from_server=}')


async def loop():
    async with websockets.connect(f'ws://{args.ip_to_connect_to}:8765') as websocket:
        msg = {}
        await websocket.send(json.dumps(msg))
        effects_json = await websocket.recv()
        effects_json = json.loads(effects_json)['effects_json']
        index_of_effects_json = 0
        keys_of_effects_json = list(effects_json.keys())
        old_mode = None

        await show(websocket, 'musician')

        while True:
            stuff = input('enter "j" or ";", or a name, or a show: ')
            if stuff in ['j', 'a']:
                index_of_effects_json -= 1
                index_of_effects_json %= len(keys_of_effects_json)
                stuff = keys_of_effects_json[index_of_effects_json]
            elif stuff in [';', 'd']:
                index_of_effects_json += 1
                index_of_effects_json %= len(keys_of_effects_json)
                stuff = keys_of_effects_json[index_of_effects_json]
            elif stuff in shows:
                await show(websocket, stuff)
                continue
            elif stuff in effects_json:
                pass
            else:
                print('that wasnt anything...')
                continue

            await clear_modes(websocket)
            await add_mode(websocket, stuff)


parser = argparse.ArgumentParser()
parser.add_argument('--ip', dest='ip_to_connect_to', default='localhost', type=str)
args = parser.parse_args()

if args.ip_to_connect_to == 'rpi0':
    args.ip_to_connect_to = '192.168.86.224'

asyncio.run(loop())
