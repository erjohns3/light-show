import websockets
import asyncio
import json
import time
import argparse

from helpers import *
import sound_helpers


# https://github.com/chrvadala/music-beat-detector
# https://github.com/shunfu/python-beat-detector




shows_filepath = python_file_directory.joinpath('shows.json')
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

    song_filepath = python_file_directory.joinpath('data').joinpath(show_obj['song_name'])
    if not sound_helpers.is_audio_running():
        sound_helpers.play_audio_async(song_filepath, volume=55, paused=True)
        time.sleep(.5)


    msg = {
        'type': 'set_bpm',
        'bpm': show_obj['bpm'],
    }
    await websocket.send(json.dumps(msg))
    msg_from_server = await websocket.recv()
    print(f'{msg_from_server=}')

    sound_helpers.toggle_pause_async_mpv()

    precise_wait(show_obj['delay'])

    time_start = time.perf_counter()
    show_index = 0

    while show_index < len(show_obj['show']):
        msg = {
            'type': 'clear_modes',
        }
        await websocket.send(json.dumps(msg))
        msg_from_server = await websocket.recv()
        print(f'{msg_from_server=}')

        for mode_to_add in show_obj['show'][show_index]:
            msg = {
                'type': 'add_mode',
                'mode': mode_to_add,
            }
            await websocket.send(json.dumps(msg))
            msg_from_server = await websocket.recv()
            print(f'{msg_from_server=}')


        beats_per_second = 60 / show_obj['bpm']
        time_to_wait = (beats_per_second * show_obj['show'][show_index][-1]) - websocket_delay

        precise_wait(time_to_wait)
        show_index += 1



async def loop():
    async with websockets.connect(f'ws://{args.ip_to_connect_to}:8765') as websocket:
        msg = {}
        await websocket.send(json.dumps(msg))
        config = await websocket.recv()
        config = json.loads(config)['config']
        index_of_config = 0
        keys_of_config = list(config.keys())
        old_mode = None

        while True:
            stuff = input('enter "j" or ";", or a name, or a show: ')
            if stuff in ['j', 'a']:
                index_of_config -= 1
                index_of_config %= len(keys_of_config)
                stuff = keys_of_config[index_of_config]
            elif stuff in [';', 'd']:
                index_of_config -= 1
                index_of_config %= len(keys_of_config)
                stuff = keys_of_config[index_of_config]
            elif stuff in shows:
                await show(websocket, stuff)
                continue
            elif stuff in config:
                pass
            else:
                print('that wasnt anything...')
                continue

            msg = {
                'type': 'clear_modes',
            }
            await websocket.send(json.dumps(msg))
            msg_from_server = await websocket.recv()
            print(f'{msg_from_server=}')

            old_mode = stuff
            msg = {
                'type': 'add_mode',
                'mode': stuff
            }

            await websocket.send(json.dumps(msg))
            msg_from_server = await websocket.recv()
            print(f'{msg_from_server=}')

parser = argparse.ArgumentParser()
parser.add_argument('--ip', dest='ip_to_connect_to', default='localhost', type=str)
args = parser.parse_args()

if args.ip_to_connect_to == 'rpi0':
    args.ip_to_connect_to = '192.168.86.224'

asyncio.run(loop())
