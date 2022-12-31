# https://www.youtube.com/watch?v=HxG99B8b90w


import json
from rich.console import Console
import re
import asyncio
import time
import random
from threading import Thread

import sound_helpers

from helpers import *
import light3






def set_next_mode_in_sequence(amount):
    global mode_index, bpm
    mode_index += amount
    if mode_index < 0:
        mode_index = len(all_modes) - 1
    elif mode_index >= len(all_modes):
        mode_index = 0
    
    console.print('\r ' * 40, end='\r')
    asyncio.run(light3.set_light([all_modes[mode_index]], bpm, debug=False))

async def print_and_handle_show(all_levels):
    global mode_index, bpm, selected_show, show_light_index, show_starting_time, beat, beats_so_far, show_playing



    rbg_colors = list(map(lambda x: int(x * 2.55), all_levels[:6]))
    character = '▆ '


    console.print('  ' + character, style=f'rgb({rbg_colors[0]},{rbg_colors[1]},{rbg_colors[2]})', end='')
    console.print(character, style=f'rgb({rbg_colors[3]},{rbg_colors[4]},{rbg_colors[5]})', end='')

    purple = [153, 50, 204]
    purple = list(map(lambda x: int(x * (all_levels[6] / 100.0)), purple))
    console.print(character, style=f'rgb({purple[0]},{purple[1]},{purple[2]})', end='')

    console.print(f'Mode: {light3.curr_modes}, BPM: {light3.curr_bpm}, Beat: {beat}{" " * 40}', end='\r')


    if show_playing:
        rate = bpm / 60 * light3.SUB_BEATS
        time_curr = time.perf_counter()
        time_diff = time_curr - show_starting_time
        num = int(time_diff * rate)
        time_delay = ((num + 1) / rate) - time_diff

        the_beat = num // light3.SUB_BEATS
        if beat != the_beat:
            beat = the_beat
        
        if beat - beats_so_far >= shows[selected_show]['show'][show_light_index][-1]:
            beats_so_far += shows[selected_show]['show'][show_light_index][-1]
            show_light_index += 1
            if show_light_index >= len(shows[selected_show]['show']):
                print(f'{bcolors.WARNING}======== Show ended, ran out of lights on beat {beat} ======== {bcolors.ENDC}')
                show_playing = None
            else:
                await light3.set_light(shows[selected_show]['show'][show_light_index][:-1], bpm, debug=False)




def start_song():
    global mode_index, bpm, selected_show, show_playing, show_light_index, show_starting_time, beat, beats_so_far

    show_playing = False
    if sound_helpers.is_audio_running():
        sound_helpers.stop_audio()
        sound_helpers.kill_mpv()
        time.sleep(.5)

    selected_show = 'shelter2'
    bpm = shows[selected_show]['bpm']
    show_light_index = 0
    beat = 0
    beats_so_far = 0
    shelter_filepath = pathlib.Path(__file__).parent.joinpath('data').joinpath(shows[selected_show]['song_name'])
    if not sound_helpers.is_audio_running():
        sound_helpers.play_audio_async(shelter_filepath, volume=30, paused=True)
        time.sleep(.5)
    
    while not sound_helpers.is_audio_running():
        time.sleep(.1)
    sound_helpers.toggle_pause_async_mpv()


    time.sleep(float(shows[selected_show]['delay']))

    print(f'{bcolors.OKBLUE}======== Starting show ======== {bcolors.ENDC}')
    
    show_starting_time = time.perf_counter()
    show_playing = True
    
    asyncio.run(light3.set_light([shows[selected_show]['show'][0][0]], bpm, debug=False))


def press_callback(key_obj):
    pass

def release_callback(key_obj):
    print(key_obj, '\n')
    if key_obj == 'j':
        set_next_mode_in_sequence(-1)
    elif key_obj == ';':
        set_next_mode_in_sequence(1)
    elif key_obj == 'g':
        start_song()
    elif key_obj == 'p':
        sound_helpers.toggle_pause_async_mpv()
    elif key_obj == 'q':
        sound_helpers.stop_audio()
    

# keyboard.KeyCode.from_char('j')
# keyboard.Key.esc
# l = keyboard.Listener(on_press=press_callback,on_release=release_callback)
# l.start()


def write_to_random_file(effects_json):
    output_filename = random_letters(8) + '.json'
    output_filepath = pathlib.Path(__file__).parent.joinpath('data').joinpath(output_filename)


    effects_json_json = json.dumps(effects_json, indent=4, sort_keys=True)
    effects_json_json = re.sub(r'([0-9]),(\n[ ]*)', r'\g<1>, ', effects_json_json)
    effects_json_json = re.sub(r'\[\n[ ]*', r'[', effects_json_json)
    effects_json_json = re.sub(r'\n[ ]*\]', r']', effects_json_json)

    with open(output_filepath, 'w') as f:
        f.write(effects_json_json)

    return output_filepath


def key_input_time():
    while True:
        lol = input()
        release_callback(lol)


console = Console()

thread = Thread(target=key_input_time, args = ())
thread.start()
time.sleep(.05)

shows_filepath = pathlib.Path(__file__).parent.joinpath('shows.json')
with open(shows_filepath) as f:
    shows = json.loads(f.read())


effects_json_filepath = pathlib.Path(__file__).parent.joinpath('effects_json.json')

light_array = light3.read_effects_json(pathlib.Path(__file__).parent.joinpath(effects_json_filepath))

starting_mode = 'Nothing'
starting_bpm = 100

all_modes = [x for x in light_array.keys()]
global mode_index, bpm, selected_show, beat, show_playing
show_playing = False
selected_show = None
beat = None
mode_index = all_modes.index(starting_mode)
bpm = starting_bpm

asyncio.run(light3.set_light([starting_mode], starting_bpm, debug=False))
light_task = asyncio.run(light3.light(light_array, print_and_handle_show))










