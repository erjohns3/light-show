import pathlib
import json
import re
import sys
import math
import os
import importlib
import sys
import sound_helpers
import time
from collections import Counter
from scipy.signal import find_peaks
from aubio import source, pvoc, filterbank
from numpy import vstack, zeros, hstack

from multiprocessing import Queue, Process
import pandas as pd 
import aubio
import numpy as np

from helpers import *


def eliminate(string, matches):
    found = set()
    for match in matches:
        if match in found:
            continue
        found.add(match)
        string = string.replace(match, '')
    return string

def write_show_file_pretty(output_filepath, dict_to_dump):
    with open(output_filepath, 'w') as file:
        shows_json_str = json.dumps(dict_to_dump, indent=4)
        shows_json_str = shows_json_str.replace(': true', ': True')

        shows_json_str = shows_json_str.replace('\n            ]', ']')
        shows_json_str = shows_json_str.replace('\n                ', ' ')
        
        file.writelines(['effects = ' + shows_json_str])

def get_src_bpm_offset(song_filepath, use_boundaries, queue=None, debug=True):
    if is_windows():
        song_filepath = sound_helpers.convert_to_wav(song_filepath)

    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    src = aubio.source(str(song_filepath), 0, hop_s)
    # print(src.uri, src.samplerate, src.channels, src.duration)
    o = aubio.tempo("default", win_s, hop_s, src.samplerate)

    pv = pvoc(win_s, hop_s)
    f = filterbank(40, win_s)
    f.set_mel_coeffs_slaney(src.samplerate)
    energies = [[0.0]*40]

    delay = 4. * hop_s
    beats = []
    total_frames = 0
    bpms = []
    print_green("Started aubio loop fft samples for energy")
    while True:
        samples, read = src()
        is_beat = o(samples)
        # boundaries
        fftgrain = pv(samples)
        new_energies = f(fftgrain)
        # print(new_energies)
        energies.append(new_energies.copy())
        # print(energies)
        if is_beat:
            this_beat = total_frames - delay + is_beat[0] * hop_s
            human_readable = (this_beat / float(src.samplerate))
            beats.append(human_readable)
            bpms.append(int(o.get_bpm()))
        total_frames += read
        if read < hop_s: break
    print_green("Finished aubio loop")
    energies = np.array(energies)
    # print(energies)
    common_bpms = [x for x, cnt in Counter(bpms).most_common(10) if x>80 and x<190]
    if not common_bpms:
        common_bpms = [x for x, cnt in Counter(bpms).most_common(10)]

    bpm_candidates = set()
    for bpm in common_bpms:
        for plus in [-2,-1,0,1]:
            bpm_candidates.add(bpm+plus)

    bpm_guess = -1
    offset_guess = -1
    best_seen = -math.inf
    hits = {} 
    for bpm in bpm_candidates:
        distances = []
        beat_length = 60/bpm
        hit_count = 0
        for value in beats:
            match = round(value/beat_length)*beat_length
            distances.append(match-value)
        # todo.  the bins could be replaced with a sliding window to improve accuracy
        bins = np.linspace(-beat_length, beat_length, 40) # group bins into 5% intervals of beat length (on either side)
        df = pd.DataFrame(distances, columns=['cnt']).groupby(pd.cut(np.array(distances), bins)).count().sort_values('cnt', ascending=False).reset_index()
        choice = (df.iloc[0][0].left+df.iloc[0][0].right)/2
        for distance in distances: 
            if abs(distance-choice)/(60/max(bpm_candidates)) < .05: # match to 5% of beat length
                hit_count+=1
        # doubling the BPM should double the hits.  Scale it down a bit though
        hit_count = hit_count / bpm**.5
        hits[bpm] = hit_count
        if hit_count > best_seen:
            bpm_guess = bpm
            offset_guess = choice
            best_seen = hit_count
    beat_length = 60.0/bpm_guess
    delay = beat_length - offset_guess if offset_guess > 0 else -offset_guess
    if use_boundaries:
        boundary_beats = get_boundary_beats(energies, beat_length, delay, total_frames / src.samplerate)
    else:
        boundary_beats = 'DISABLED'
    if debug:
        print(f'Guessing BPM as {bpm_guess} delay as {delay} beat_length as {beat_length}, boundary_beats as {boundary_beats}')
    if queue:
        queue.put([total_frames / src.samplerate, bpm_guess, delay, boundary_beats])
    else:
        return total_frames / src.samplerate, bpm_guess, delay, boundary_beats


def get_boundary_beats(energies, beat_length, delay, length_s):
    song_beats = length_s/beat_length
    n_for_beat = round(len(energies)/song_beats)
    print(f'n for beat: {n_for_beat}')
    n = round(n_for_beat/4) # average over beat/4
    look_size = 4*4 # look at 4 beats
    move_size = 2 # on every beat/2
    todo = []
    for i in range(len(energies.T)): # window average
        band = energies.T[i]
        pad = np.array([0]*(n-len(band)%n))
        band = np.concatenate((band, pad))
        simple = np.sum(band.reshape(-1, n), axis=1)
        todo.append(simple)

    energies = np.array(todo)
    diffed = [0 for i in range(look_size)]
    for i in range(len(energies[0]))[look_size:-look_size*2]:
        # for each band: find difference in value between left_i and right_i
        diff = 0
        for band_i, band in enumerate(energies): # np.concatenate((energies[:5],energies[-5:]))
            left = np.sum(band[i-look_size:i])
            right = np.sum(band[i:i+look_size])
            this = right-left
            if band_i < 6:
                diff += abs(this)*3
            diff += abs(this)
        diffed.append(diff)

    diffed+= [0 for i in range(look_size*2)]
    peaks = find_peaks(diffed, height=1, width=1)

    sorted_peaks = [x*length_s/len(diffed) for _, x in sorted(zip(peaks[1]['peak_heights'], peaks[0]), reverse=True)]

    num_peaks = int(2*length_s/60)

    peaks_to_use = sorted_peaks[:num_peaks]
    prev = 0    
    iter = 0
    #ensure 1 change per 40s
    while iter < len(peaks_to_use):
        peak = sorted(peaks_to_use)[iter]
        if peak-prev > 40:
            add = next((x for x in sorted_peaks if x > prev+6 and x < prev+40))
            peaks_to_use.append(add) # = peak, next iteration
        else:
            prev = peak
            iter+=1
        

    out = []
    # combine within 16 beats
    for peak in peaks_to_use:
        new_out = []
        todo = peak
        for prev in out:
            if abs(prev-peak) < beat_length*18:
                peak = max(prev, peak)
            else:
                new_out.append(prev)
        new_out.append(peak)
        out = new_out

    # print(sorted(out))
    matches = []
    for peak in out:
        matches.append(round((peak-delay)/beat_length)) # beats are 1 indexed
    # print(matches)

    return sorted(set(list(matches)))

def generate_show(song_filepath, effects_config, overwrite=True, simple=False, debug=True):
    start_time = time.time()
    use_boundaries = True and not simple
    show_name = f'g_{pathlib.Path(song_filepath).stem}'

    output_directory = python_file_directory.joinpath('effects', 'autogen_shows')
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    show_name_without_spaces = show_name.replace(' ', '_')
    output_filepath = output_directory.joinpath(show_name_without_spaces + '.py')
    if os.path.exists(output_filepath):
        if overwrite:
            print(f'{bcolors.WARNING}overwrite is set to True, and {output_filepath} exists, generating and overwriting{bcolors.ENDC}')
        else:
            print(f'{bcolors.WARNING}overwrite is set to False, and {output_filepath} exists, so returning without generating show{bcolors.ENDC}')
            return None
    
    
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')
    queue = Queue()
    proc = Process(target=get_src_bpm_offset, args=(song_filepath, use_boundaries, queue,))
    proc.start()
    song_length, bpm_guess, delay, boundary_beats = queue.get()    # prints "[42, None, 'hello']"

    print_blue(f'autogen: time taken up to get_src_bpm_offset: {time.time() - start_time} seconds')

    relative_path = song_filepath
    if relative_path.is_absolute():
        relative_path = relative_path.relative_to(python_file_directory)
    show = {
        'bpm': bpm_guess,
        'song_path': str(relative_path),
        'delay_lights': delay,
        'generated_boundaries': boundary_beats,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': [],
        'was_autogenerated': True,
    }

    effect_files_json = get_effect_files_jsons()
    effects_config_filtered = dict(filter(lambda x: x[1].get('autogen', False), effect_files_json.items()))
    
    effect_names = list(effects_config_filtered.keys())
    effect_types_to_name = {}
    for name, effect in effects_config_filtered.items():
        if type(effect['autogen']) == str:
            if effect['autogen'] not in effect_types_to_name:
                effect_types_to_name[effect['autogen']] = []
            effect_types_to_name[effect['autogen']].append(name)
    
    scenes = [
        [16, ['downbeat top', 'downbeat bottom']],
        [16, ['downbeat top']],
        [16, ['downbeat top']],
        [16, ['downbeat bottom']],
        [16, ['downbeat mixed']],
        [16, ['downbeat mixed']],
        [16, ['downbeat mixed', 'UV pulse']],
        [16, ['downbeat mixed', 'UV']],
        [16, ['downbeat top', 'downbeat bottom', 'UV']],
        [16, ['downbeat top', 'UV']],
        [16, ['downbeat bottom', 'UV']],
        [16, ['rainbow top', 'downbeat bottom']],
        [2, ['filler']],
        [1, ['filler']],
        [4, ['UV pulse']],
        [2, ['UV pulse']],
        [1, ['UV pulse']],
        [1, ['flash']],
    ]

    # apply lights
    total_beats = int((song_length / 60) * bpm_guess)
    beat = 1    
    if simple: # Only RBBB timing
        while beat < total_beats:
            show['beats'].append([beat, 'RBBB 1 bar', 4])
            beat += 4
    elif use_boundaries==True: # Based on scenes
        boundary_beats.append(total_beats+1) # add beats up to ending (maybe off by 1)
        prev_bound = 0
        prev_scene = None
        prev_effects = []
        for bound in boundary_beats:
            length_left = bound-prev_bound
            while length_left>0:
                new_prev_effects = []
                if length_left > 16:
                    candidates = [x for x in scenes if x [0] >= 4 and  x[0] <= length_left and x[1] != prev_scene]
                else:
                    if bound == boundary_beats[-1]:
                        candidates = [x for x in candidates if x[1] == 'UV pulse']
                    candidates = [x for x in scenes if x[0] <= length_left and x[1] != prev_scene]
                    if length_left > 2:
                        candidates = [x for x in candidates if x[1] != ['flash']]

                length, effect_types = random.choice([x for x in candidates])
                while length_left >= length:
                    for effect_type in effect_types:
                        candidates = effect_types_to_name[effect_type]
                        if len(candidates) > 1:
                            candidates = [x for x in candidates if x not in prev_effects]
                        effect_name = random.choice(effect_types_to_name[effect_type])
                        new_prev_effects.append(effect_name)
                        show['beats'].append([beat, effect_name, length])
                        if length_left > length*2 and length==16:
                            show['beats'].append([beat+length, effect_name, length])
                    beat += length
                    if length_left > length*2 and length==16:
                        beat += length
                        length_left -= length
                    length_left -= length
                prev_effects = new_prev_effects
                prev_scene = effect_types
            prev_bound = bound
    else: # Based on scenes
        while beat < total_beats:
            length, effect_types = random.choices(scenes, k=1)[0]
            for effect_type in effect_types:
                effect_name = random.choices(effect_types_to_name[effect_type], k=1)[0]
                show['beats'].append([beat, effect_name, length])
            beat += length
                
    
    the_show = {
        show_name: show
    }
    
    if '.' in show_name:
        print_red(f'Cannot generate show for {show_name} because it has a dot before the file extension')
        return None
    print(f'writing "{show_name}" to {output_filepath}')
    write_show_file_pretty(output_filepath, the_show)
    print_blue(f'autogen: time taken to finish: {time.time() - start_time} seconds')
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
        length, guess_bpm, guess_delay = get_src_bpm_offset(song_filepath)        
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




# old shit to look thru effects:

# counting number of times effect is used
# effect_usages = {}
# for effect_name, effect in effect_files_json.items():
#     for beats in effect['beats']:
#         if type(beats[1]) == str:
#             if beats[1] not in effect_usages:
#                 effect_usages[beats[1]] = 0
#             effect_usages[beats[1]] += 1

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