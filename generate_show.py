import pathlib
import json
import re
import sys
import math
import statistics
import os
import importlib
import sys
import sound_helpers

# from scipy.signal import find_peaks
import pandas as pd 
import aubio
import numpy as np

from helpers import *


def get_src_bpm_offset(song_filepath):
    # internet copypasta from here ...
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    
    src = aubio.source(str(song_filepath), 0, hop_s)

    print(src.uri, src.samplerate, src.channels, src.duration)
    o = aubio.tempo("default", win_s, hop_s, src.samplerate)

    delay = 4. * hop_s

    beats = []

    # total number of frames read
    total_frames = 0
    while True:
        samples, read = src()
        is_beat = o(samples)
        if is_beat:
            this_beat = total_frames - delay + is_beat[0] * hop_s
            human_readable = (this_beat / float(src.samplerate))
            # print("%f" % human_readable)
            beats.append(human_readable)
        total_frames += read
        if read < hop_s: break
    # ...to here
    bpm_guess = -1
    offset_guess = -1
    best_seen = math.inf
    beats = np.array(beats)
    errors = {}
    for bpm in range(70, 180):
        distances = []
        beat_length = 60/bpm
        error = 0
        for value in beats:
            match = round(value/beat_length)*beat_length
            distances.append(match-value)
        bins = np.linspace(-beat_length, beat_length, 40) # group bins into 5% intervals of beat length (on either side)
        df = pd.DataFrame(distances, columns=['cnt']).groupby(pd.cut(np.array(distances), bins)).count().sort_values('cnt', ascending=False).reset_index()
        choice = (df.iloc[0][0].left+df.iloc[0][0].right)/2
        for distance in distances:
            if abs(distance-choice)/(beat_length) > .05: # match to 10% of beat length (could be tuned)
                error+=1

        errors[bpm] = error
        if error < best_seen:
            bpm_guess = bpm
            offset_guess = choice
            best_seen = error

    length_int = 60.0/bpm_guess
    delay = length_int - offset_guess if offset_guess > 0 else -offset_guess

    print(f'Guessing BPM as {bpm_guess} delay as {delay} beat_length as {length_int}')
    return src, bpm_guess, delay


def generate_show(song_filepath, effects_config):
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')

    if is_windows():
        src, bpm_guess, delay = get_src_bpm_offset(sound_helpers.convert_to_wav(song_filepath))
    else:
        src, bpm_guess, delay = get_src_bpm_offset(song_filepath)

    show = {
        'bpm': bpm_guess,
        'song_path': str(song_filepath),
        'delay_lights': delay,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': []
    }



    effect_files_json = get_effect_files_jsons()

    # counting number of times effect is used
    effect_usages = {}
    for effect_name, effect in effect_files_json.items():
        for beats in effect['beats']:
            if type(beats[1]) == str:
                if beats[1] not in effect_usages:
                    effect_usages[beats[1]] = 0
                effect_usages[beats[1]] += 1

    # filtering to only ones in between 4 and 16
    # effects_config_4_16 = dict(filter(lambda x: 4 <= x[1]['length'] <= 16, effects_config.items()))
    # effect_usages_4_16 = dict(filter(lambda x: x[0] in effects_config_labeled, effect_usages.items()))


    # making probability distribution
    # effect_probabilities = {}
    # total = sum(effect_usages_4_16.values())
    # for effect_name, times_used in effect_usages_4_16.items():
    #     effect_probabilities[effect_name] = times_used / total

    # print('frequency of potential effects used')
    # for times_used, effect_name in sorted([(x, y) for y, x in effect_usages_4_16.items()]):
    #     print(f'times_used: {times_used}, {effect_name}')



    effects_config_labeled = dict(filter(lambda x: x[1].get('autogen', False), effects_config.items()))
    effect_usages_labeled = dict(filter(lambda x: x[0] in effects_config_labeled, effect_usages.items()))

    print(effects_config_labeled)
    print(effect_usages_labeled)

    # apply lights
    length_s = src.duration / src.samplerate
    total_beats = int((length_s / 60) * bpm_guess)

    beat = 1    
    while beat < total_beats:
        # chosen_effect_names = random.choices(list(effect_probabilities.keys()), weights=effect_probabilities.values(), k=2)
        chosen_effect_names = random.choices(list(effect_usages_labeled.keys()), k=2)
        
        all_lengths = []
        for effect_name in chosen_effect_names:
            length = effect_files_json[effect_name]['length']
            all_lengths.append(length)
            show['beats'].append([beat, effect_name, length])
        beat += max(all_lengths)
    
    the_show = {
        f'generated_{pathlib.Path(song_filepath).stem}_show': show
    }
    
    # dump show to temp output
    # with 
    # print()

    return the_show


def get_effect_files_jsons():
    all_globals = globals()
    effects_config = {}
    for name, path in get_all_paths('effects', only_files=True):
        module = 'effects.' + path.stem
        all_globals[module] = importlib.import_module(module)
        effects_config.update(all_globals[module].effects)
    return effects_config


if __name__ == '__main__':
    effect_files_jsons = get_effect_files_jsons()

    configs_with_bpm = {}
    for effect_name, effect in effect_files_jsons.items():
        if 'bpm' in effect and 'song_path' in effect:
            configs_with_bpm[effect['song_path']] = {
                'bpm': effect['bpm'],
                'delay': effect['delay_lights'] + effect['skip_song'],
            }
    

    guess_bpm_delay = {}
    for name, song_filepath in get_all_paths('songs', only_files=True):
        src, guess_bpm, guess_delay = get_src_bpm_offset(song_filepath)        
        guess_bpm_delay[str(song_filepath)] = (guess_bpm, guess_delay)

    for song_filepath, (guess_bpm, guess_delay) in guess_bpm_delay.items():
        if song_filepath in configs_with_bpm:
            config_bpm = configs_with_bpm[song_filepath]['bpm']
            config_delay = configs_with_bpm[song_filepath]['delay']
            
            delay_string = f'config_delay: {config_delay}, guess_delay: {guess_delay}'
            if config_bpm == guess_bpm:
                print(f'{bcolors.OKGREEN}BPM match: {guess_bpm}, {delay_string}, {song_filepath}{bcolors.ENDC}')
            else:
                print(f'{bcolors.FAIL}config_bpm: {config_bpm} != guess_bpm: {guess_bpm}, {delay_string}, {song_filepath}{bcolors.ENDC}')
        else:
            print(f'{bcolors.OKCYAN}BPM: {guess_bpm}, no config_bpm found, {song_filepath}{bcolors.ENDC}')
