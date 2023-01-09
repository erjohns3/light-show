import pathlib
import json
import math
import os
import importlib
import time
from collections import Counter
from multiprocessing import Queue, Process
from copy import deepcopy
import colorsys
import random

from scipy.stats import circmean
from scipy.signal import find_peaks
from aubio import source, pvoc, filterbank
import aubio
import pandas as pd
import numpy as np

from effects.compiler import b
import sound_helpers
from helpers import *


def eliminate(string, matches):
    found = set()
    for match in matches:
        if match in found:
            continue
        found.add(match)
        string = string.replace(match, '')
    return string

def write_effect_to_file_pretty(output_filepath, dict_to_dump, write_compiler=False):
    print(f'writing effect/show to {output_filepath}')

    show_name = list(dict_to_dump.keys())[0]    
    if is_windows() and 'song_path' in dict_to_dump[show_name]:
        dict_to_dump[show_name]['song_path'] = dict_to_dump[show_name]['song_path'].replace('\\\\', '/').replace('\\', '/')
    with open(output_filepath, 'w') as file:
        shows_json_str = json.dumps(dict_to_dump, indent=4)
        shows_json_str = shows_json_str.replace(': true', ': True')

        shows_json_str = shows_json_str.replace('\n            ]', ']')
        shows_json_str = shows_json_str.replace('\n                ', ' ')
        
        final_str = 'effects = ' + shows_json_str
        if write_compiler:
            final_str = 'from effects.compiler import b\n\n' + final_str
        file.writelines([final_str])

def get_src_bpm_offset(song_filepath, use_boundaries):
    queue = Queue()
    proc = Process(target=get_src_bpm_offset_multiprocess, args=(song_filepath, use_boundaries, queue,))
    proc.start()     # prints "[42, None, 'hello']"
    return queue.get()


def get_src_bpm_offset_multiprocess(song_filepath, use_boundaries, queue=None):
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
    f_one = filterbank(40, win_s)
    f_one.set_mel_coeffs_slaney(src.samplerate)
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

    bpm_guess = 60
    offset_guess = 0
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
        # doubling the BPM should double the hits.  Let's consider it a square root factor to be safe
        hit_count = hit_count / bpm**.5
        hits[bpm] = hit_count
        if hit_count > best_seen:
            bpm_guess = bpm
            offset_guess = choice
            best_seen = hit_count
    beat_length = 60.0/bpm_guess
    delay = beat_length - offset_guess if offset_guess > 0 else -offset_guess
    if use_boundaries:
        boundary_beats, chunk_levels = get_boundary_beats(energies, beat_length, delay, total_frames / src.samplerate)
    else:
        boundary_beats, chunk_levels = 'DISABLED', []
    print(f'Guessing BPM as {bpm_guess} delay as {delay} beat_length as {beat_length}, boundary_beats as {boundary_beats}')
    if queue:
        queue.put([total_frames / src.samplerate, bpm_guess, delay, boundary_beats, chunk_levels])
    else:
        return total_frames / src.samplerate, bpm_guess, delay, boundary_beats, chunk_levels


def get_boundary_beats(energies_in, beat_length, delay, length_s):
    song_beats = length_s/beat_length
    n_for_beat = round(len(energies_in)/song_beats)
    print(f'n for beat: {n_for_beat}')
    n = round(n_for_beat/4) # average over beat/4
    look_size = 4*4 # look at 4 beats
    # move_size = 2 # on every beat/2
    levels = []
    variances = []
    for i in range(len(energies_in.T)): # window average
        band = energies_in.T[i]
        pad = np.array([0]*(n-len(band)%n))
        band = np.concatenate((band, pad))
        simple = np.sum(band.reshape(-1, n), axis=1)
        levels.append(simple)
        variance = np.var(band.reshape(-1, n), axis=1)
        variances.append(variance)

    energies = np.array(levels)
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

    peaks_to_use = sorted(sorted_peaks[:num_peaks])
    prev = 0    
    iter = 0

    #ensure 1 change per 40s
    while iter < len(peaks_to_use):
        peak = peaks_to_use[iter]
        if peak-prev > 40:
            add = next((x for x in sorted_peaks if x > prev+6 and x < prev+40))
            peaks_to_use.insert(iter, add) # = peak, next iteration
            prev = add
            iter+=1
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
    peaks_to_use=out

    # get levels
    chunk_levels = []
    prev = 0
    for i, peak in enumerate(peaks_to_use+[length_s]):
        peak_i = int(peak/(length_s/len(diffed)))
        end = peak_i
        chunk_level=0
        for i, band in enumerate(levels):
            summed = sum(band[prev: end])
            if i < 6:
                summed *= 5
            chunk_level+=summed
        chunk_levels.append(chunk_level/(end-prev))
        prev = end
    print(chunk_levels)
    min_chunk = min(chunk_levels)
    max_chunk = max(chunk_levels)
    # essentially using percentile to cap the quantity in each bucket
    chunk_levels_lo =  min(np.percentile(chunk_levels, q=10), (max_chunk - min_chunk)*.1 + min_chunk)
    chunk_levels_hi = max(np.percentile(chunk_levels, q=80), (max_chunk - (max_chunk - min_chunk)*.2))
    # chunk_levels_lo = np.percentile(chunk_levels, q=10)
    # chunk_levels_hi = np.percentile(chunk_levels, q=70)

    chunk_levels_out = []
    for level in chunk_levels:
        if level > chunk_levels_hi:
            chunk_levels_out.append('hi')
        elif level < chunk_levels_lo:
            chunk_levels_out.append('low')
        else:
            chunk_levels_out.append('mid')


    matches = []
    for peak in peaks_to_use:
        matches.append(round((peak-delay)/beat_length)) # beats are 1 indexed, but off-by-one is intentional

    return matches, chunk_levels_out


# only works to 10 decimal places
def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return round(int( n/precision+correction ) * precision, 10)


new_effects_made = set()
def make_new_effect(effects_config, effect_name, hue_shift=0, sat_shift=0, bright_shift=0):
    hue_shift = round_to(hue_shift, 0.05)
    sat_shift = round_to(sat_shift, 0.05)
    bright_shift = round_to(bright_shift, 0.01)
    
    new_effect_name = effect_name + f' hue {hue_shift} sat {sat_shift} bright {bright_shift}'.replace('.', '_dot_')
    if new_effect_name in new_effects_made:
        return new_effect_name
    new_effects_made.add(new_effect_name)

    output_directory = pathlib.Path(__file__).parent.joinpath('effects', 'generated_effects')
    if not os.path.exists(output_directory):
        print(f'making directory {output_directory}')
        os.mkdir(output_directory)

    output_filepath = output_directory.joinpath(new_effect_name + '.py')

    effects_config[new_effect_name] = {
        'beats': [
            [1, effect_name, effects_config[effect_name]['length']],
        ],
        'hue_shift': hue_shift,
        'sat_shift': sat_shift,
        'bright_shift': bright_shift,
    }


    # effects_config[new_effect_name] = deepcopy(effects_config[effect_name])
    # effects_config[new_effect_name]['hue_shift'] = 90
    # del effects_config[new_effect_name]['autogen']
    # del effects_config[new_effect_name]['cache_dirty']
    write_effect_to_file_pretty(output_filepath, {new_effect_name: effects_config[new_effect_name]})
    return new_effect_name


avg_hue_cache = {}
def get_avg_hue(channel_lut, effect_name):
    if effect_name in avg_hue_cache:
        return avg_hue_cache[effect_name]
    all_hues = []
    for compiled_channel in channel_lut[effect_name]['beats']:
        for i in range(3):
            rd, gr, bl = compiled_channel[i * 3:(i * 3) + 3]
            hue, sat, bright = colorsys.rgb_to_hsv(max(0, rd / 100.), max(0, bl / 100.), max(0, gr / 100.))
            all_hues.append(hue)
    avg_hue_cache[effect_name] = circmean(all_hues, low=0, high=1)
    # print(all_hues, avg_hue_cache[effect_name])
    # exit()
    return avg_hue_cache[effect_name]


last_song_filepath = None
last_song_data = None

def generate_show(song_filepath, channel_lut, effects_config, overwrite=True, mode=None, include_song_path=True, output_directory=None, random_color=True):
    global last_song_filepath, last_song_data

    start_time = time.time()
    use_boundaries = True and mode != 'simple'
    if mode == 'lasers':
        show_name = f'g_lasers_{pathlib.Path(song_filepath).stem}'
    else:
        show_name = f'g_{pathlib.Path(song_filepath).stem}'

    if output_directory is None:
        output_directory = pathlib.Path(__file__).parent.joinpath('effects', 'autogen_shows')
    if not os.path.exists(output_directory):
        print(f'making directory {output_directory}')
        os.mkdir(output_directory)

    show_name = ''.join([x if x.isalpha() else '_' for x in show_name])
    output_filepath = output_directory.joinpath(show_name + '.py')
    if os.path.exists(output_filepath):
        if overwrite:
            print(f'{bcolors.WARNING}overwrite is set to True, and {output_filepath} exists, generating and overwriting{bcolors.ENDC}')
        else:
            print(f'{bcolors.WARNING}overwrite is set to False, and {output_filepath} exists, so returning without generating show{bcolors.ENDC}')
            return None
    
    
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')

    if last_song_filepath == song_filepath:
        song_length, bpm_guess, delay, boundary_beats, chunk_levels = last_song_data
        print_green(f'autogen: had cached data, using...')
    else:
        song_length, bpm_guess, delay, boundary_beats, chunk_levels = get_src_bpm_offset(song_filepath, use_boundaries)
        last_song_data = [song_length, bpm_guess, delay, deepcopy(boundary_beats), chunk_levels]
        print_blue(f'autogen: time taken up to get_src_bpm_offset_multiprocess: {time.time() - start_time} seconds')
        last_song_filepath = song_filepath


    show = {
        'bpm': bpm_guess,
        'delay_lights': delay,
        'generated_boundaries': boundary_beats,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': [],
        'was_autogenerated': True,
    }
    if include_song_path:
        relative_path = song_filepath
        if relative_path.is_absolute():
            relative_path = relative_path.relative_to(pathlib.Path(__file__).parent)

        show['song_path'] = str(relative_path)



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
        [8, ['downbeat top', 'downbeat bottom']],
        [8, ['downbeat top', 'downbeat bottom', 'disco']],
        [8, ['downbeat top']],
        [8, ['downbeat top']],
        [8, ['downbeat bottom']],
        [8, ['downbeat mixed']],
        [8, ['downbeat mixed']],
        [8, ['downbeat mixed', 'UV pulse']],
        [8, ['downbeat mixed', 'UV']],
        [8, ['downbeat top', 'downbeat bottom', 'UV']],
        [8, ['downbeat top', 'UV']],
        [8, ['downbeat bottom', 'UV']],
        [8, ['rainbow top', 'downbeat bottom']],
        [8, ['disco']],
        [2, ['filler']],
        [1, ['filler']],
        [2, ['UV pulse']],
        [1, ['UV pulse single']],
    ]

    if mode == 'lasers':
        for _ in range(5):
            scenes += [
                [8, ['laser long', 'disco strobe']],
            ]
        for _ in range(5):
            scenes += [
                [8, ['laser long']],
            ]

        scenes += [
            [2, ['filler laser']],
            [1, ['filler laser']],
        ]


    # if chunk is high intensity: at least one effect must be mid or high
    # if chunk is low: no effects should be high
    # if chunk is silence: show UV pulse at half time


    # apply lights
    total_beats = int((song_length / 60) * bpm_guess)
    beat = 1  
    if mode == 'simple': # Only RBBB timing
        while beat < total_beats:
            # effect_name = make_new_effect(effects_config, effect_name, hue_shift=random.random(), sat_shift=0, bright_shift=0)
            # avg_hue = get_avg_hue(channel_lut, effect_name)
            # print(f'avg hue of {effect_name}: {avg_hue}')
            show['beats'].append([beat, 'RBBB 1 bar', 4])
            beat += 4
    elif use_boundaries==True: # Based on scenes
        boundary_beats.append(total_beats+1) # add beats up to ending (maybe off by 1)
        prev_bound = 0
        prev_scene = None
        prev_effects = []
        for iter, bound in enumerate(boundary_beats):
            chunk_level = chunk_levels[iter] #TODO use this for filtering
            length_left = bound-prev_bound
            while length_left>0:
                new_prev_effects = []
                candidates = []
                if length_left > 16:
                    candidates = [x for x in scenes if x[0] >= 4 and  x[0] <= length_left]# and x[1] != prev_scene]
                else:
                    candidates = [x for x in scenes if x[0] <= length_left]# and x[1] != prev_scene]
                    if length_left > 2:
                        candidates = [x for x in candidates if x[1] != ['flash']]

                if not candidates:
                    candidates = [1, ['UV pulse']] # bugfix for case that seems impossible

                length, effect_types = random.choice([x for x in candidates])
                while length_left >= length:
                    for effect_type in effect_types:
                        effect_candidates = deepcopy(effect_types_to_name[effect_type])

                        if chunk_level == "hi":
                            effect_candidates = [x for x in effect_candidates if not (
                                "intensity" in effects_config_filtered[x] and effects_config_filtered[x]["intensity"] == "low"
                                )]
                            # effect_candidates = effect_types_to_name['flash'] #DEBUG
                        elif chunk_level == "low":
                            effect_candidates = [x for x in effect_candidates if not (
                                "intensity" in effects_config_filtered[x] and effects_config_filtered[x]["intensity"] == "high"
                                )]
                            # effect_candidates = effect_types_to_name['UV pulse'] # DEBUG
                        if not effect_candidates: # it's low intensity but all candidates are high
                            effect_candidates = ['a_UV pulse']
                        effect_name = random.choice(effect_candidates)

                        # shift by a random color
                        # dimmer doesn't play well with hue shifter
                        hue_shift, sat_shift, bright_shift = 0, 0, 0
                        # if random_color and effect_type != 'dimmers':
                        if effect_type != 'dimmers':
                            hue_shift=random.random()
                            bright_shift = -.2
                            # effect_name = make_new_effect(effects_config, effect_name, hue_shift=random.random(), sat_shift=0, bright_shift=-.2)

                        new_prev_effects.append(effect_name)
                        the_length = length
                        if length_left >= length*4 and length==8:
                            the_length = length * 4
                        elif length_left >= length*2 and length==8:
                            the_length = length * 2
                        show['beats'].append(b(beat, name=effect_name, length=the_length, hue_shift=hue_shift, sat_shift=sat_shift, bright_shift=bright_shift))
                    
                    if length_left >= length*4 and length==8:
                        beat += length*4
                        length_left -= length*4
                    elif length_left >= length*2 and length==8:
                        beat += length*2
                        length_left -= length*2
                    else:
                        beat += length
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
    
    ending_beat = 0
    for index in range(len(show['beats'])):
        beat = show['beats'][index][0]
        length = show['beats'][index][2]
        ending_beat = max(ending_beat, beat + length)
    show['length'] = ending_beat

    the_show = {
        show_name: show
    }

    if '.' in show_name:
        print_red(f'Cannot generate show for {show_name} because it has a dot before the file extension')
        return None
    write_effect_to_file_pretty(output_filepath, the_show)
    print_blue(f'autogen: time taken to finish: {time.time() - start_time} seconds')
    
    return the_show, output_filepath

def get_effect_files_jsons():
    all_globals = globals()
    effects_config = {}
    for name, path in get_all_paths('effects', only_files=True):
        if name == 'compiler.py':
            continue
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