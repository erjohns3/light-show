import pathlib
import json
import math
import importlib
import time
from collections import Counter
import multiprocessing
from copy import deepcopy
import random
import traceback
import shutil

from scipy.signal import find_peaks
from aubio import source, pvoc, filterbank
import aubio
import pandas as pd
import numpy as np

from effects.compiler import *
import sound_video_helpers
from helpers import *


def gen_show_worker(song_path, output_directory, include_song_path):
    try:
        src_bpm_offset_cache = get_src_bpm_offset(song_path, use_boundaries=True)
        generate_show(song_path, include_song_path=include_song_path, overwrite=True, mode=None, output_directory=output_directory, src_bpm_offset_cache=deepcopy(src_bpm_offset_cache))
        generate_show(song_path, include_song_path=include_song_path, overwrite=True, mode='lasers', output_directory=output_directory, src_bpm_offset_cache=src_bpm_offset_cache)
        # if is_windows() and song_path.exists() and song_path.suffix == '.wav':
        #     print(f'deleting {song_path} because it is a wav file and we are on windows')
        #     song_path.unlink()
    except Exception as e:
        print_red(f'{traceback.format_exc()}')
        raise e

def generate_all_songs_in_directory(autogen_song_directory, output_directory=None, include_song_path=True):
    # if is_windows():
    #     print_red('this will probably blow up your storage space on windows if you have a lot of songs, so be careful, press enter if you want to continue')
    #     input()
    time_start = time.time()
    import tqdm
    # import concurrent
    from concurrent.futures import ProcessPoolExecutor, as_completed

    all_song_name_and_paths = get_all_paths(autogen_song_directory, recursive=True, allowed_extensions=set(['.ogg', '.mp3', '.wav'], only_files=True))
    all_song_paths = [path for _name, path in all_song_name_and_paths]

    if is_macos():
        import multiprocessing
        multiprocessing.set_start_method('fork')
    print_yellow(f'AUTOGENERATING ALL SHOWS IN DIRECTORY {autogen_song_directory}')

    total_duration = 0
    duration_and_song_paths = []
    print(f'Getting all song metadata info for {len(all_song_paths)} songs...')

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(sound_video_helpers.get_song_metadata_info, song_path) for song_path in all_song_paths]
        for future in as_completed(futures):
            if future.exception() is not None:
                print_red(f'Exception occured in subprocess: {future.exception()}')
                continue
            _, _, duration, _samplerate, song_path = future.result()
            duration_and_song_paths.append((duration, song_path))
            total_duration += duration

    all_song_paths = [song_path for _duration, song_path in sorted(duration_and_song_paths, reverse=True)]
    print(f'finished getting all metadata info for {len(all_song_paths)} songs in {time.time() - time_start} seconds')

    with tqdm.tqdm(total=len(all_song_paths)) as progress_bar:
        with ProcessPoolExecutor() as executor:
            futures = [executor.submit(gen_show_worker, song_path, output_directory, include_song_path) for song_path in all_song_paths]
            for future in as_completed(futures):
                if future.exception() is not None:
                    print_red(f'Exception occured in subprocess: {future.exception()}')
                progress_bar.update(1)
    time_diff = time.time() - time_start
    print(f'finished getting all metadata info for {len(all_song_paths)} songs in {time.time() - time_start} seconds')
    print_green(f'FINISHED AUTOGENERATING ALL ({len(all_song_paths)} songs, {total_duration:.1f} seconds of music) SHOWS IN DIRECTORY {autogen_song_directory} in {time_diff:.1f} seconds ({total_duration / time_diff:.1f} light show seconds per real second)', flush=True)





def write_effect_to_file_pretty(output_filepath, dict_to_dump, write_compiler=False, rip_out_char=None):
    print(f'writing effect to {output_filepath}')

    if '.' in output_filepath.stem:
        old_output_filepath = output_filepath
        output_filepath = output_filepath.parent.joinpath(old_output_filepath.stem.replace('.', '_') + old_output_filepath.suffix)
        print_yellow(f'the dot character cannot be in the output file, old file name: "{old_output_filepath.stem}". renaming the file to "{output_filepath.stem}" and writing')

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
            final_str = 'from effects.compiler import *\n\n' + final_str
        file.writelines([final_str])
    return output_filepath

def get_src_bpm_offset_multiprocess(song_filepath, use_boundaries):
    try:
        queue = multiprocessing.Queue()
        proc = multiprocessing.Process(target=get_src_bpm_offset, args=(song_filepath, use_boundaries, queue,), daemon=True)
        proc.start()
        results = queue.get()
        proc.join()
        return results
    except Exception as e:
        print_red(f'{traceback.format_exc()}')
        raise e


def separate_stem(audio_path, part, model=None, cache=True):
    if not part:
        return audio_path
    
    if model is None:
        if is_andrews_main_computer():
            model = 'htdemucs_ft'
            print(f'separate_stem: Defaulting model to htdemucs_ft. This is highest quality but over 4x slower than the next best')
        else:
            model = 'htdemucs'
            print(f'separate_stem: Defaulting model to htdemucs. This is second highest quality model but fast')

    avail_parts = ['vocals', 'drums', 'bass', 'other']
    if part:
        part = part.lower()
        if part not in avail_parts:
            print_red(f'invalid separation part "{part}", need to choose from {avail_parts}')
            exit()
        separated_dir = make_if_not_exist(get_temp_dir().joinpath('separated')) 
        expected_folder_output = separated_dir.joinpath(model, audio_path.stem)
        if not cache or not expected_folder_output.exists():
            import demucs.separate
            print(f'separating {audio_path.stem}')
            cmd = [
                '--mp3', 
                '-n', model,
                '-o', str(separated_dir),
            ]
            if is_macos(): # apple silicon GPU backend
                cmd += ['-d', 'mps']
            cmd.append(part)
            cmd.append(str(audio_path))
            demucs.separate.main(cmd)
        full_path = expected_folder_output.joinpath(f'{part}.mp3')
        if not full_path.exists():
            print_red(f'expected separated output "{full_path}" doesnt exist, but "{expected_folder_output}" does exist. weird...')
            exit()
        better_named_path = get_temp_dir().joinpath(f'{audio_path.stem}_{part}.mp3')
        if not better_named_path.exists():
            shutil.copy(full_path, better_named_path)
        return better_named_path


def get_src_bpm_offset(song_filepath, use_boundaries=True, queue=None):
    to_delete_after = []
    if is_windows():
        song_filepath_maybe_utf_8 = sound_video_helpers.convert_to_wav(song_filepath)
        clean_name = song_filepath_maybe_utf_8.name.encode('ascii', 'ignore').decode('ascii')
        if clean_name != song_filepath_maybe_utf_8.name:
            song_filepath = song_filepath_maybe_utf_8.with_name(clean_name)
            shutil.move(song_filepath_maybe_utf_8, song_filepath)
        else:
            song_filepath = song_filepath_maybe_utf_8
        to_delete_after.append(song_filepath)

    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    
    try:
        src = aubio.source(str(song_filepath), 0, hop_s)
    except Exception as e:
        print_stacktrace()
        print_yellow(f'failed to open {song_filepath}')
        if not song_filepath.exists():
            print_red(f'since file truly doesnt exist according to python raising again')
            raise Exception('read above exception')

        safe_name = [char if char.isascii() else '_' for char in song_filepath.name]
        safe_filepath = get_temp_dir().joinpath(safe_name)
        shutil.copy(song_filepath, safe_filepath)
        print_yellow(f'moving "{song_filepath}" to safe path: "{safe_filepath}"')
        song_filepath = safe_filepath
        src = aubio.source(str(song_filepath), 0, hop_s)

    # print(src.uri, src.samplerate, src.channels, src.duration)
    o = aubio.tempo('default', win_s, hop_s, src.samplerate)

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
    print_green(f'autogen: {song_filepath.stem} - Started aubio loop fft samples for energy')
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
    print_green(f'autogen: {song_filepath.stem} - Finished aubio loop')
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
    print(f'autogen: {song_filepath.stem} - Guessing BPM as {bpm_guess} delay as {delay} beat_length as {beat_length}, boundary_beats as {boundary_beats}')
    src.close()
    for path in to_delete_after:
        path.unlink()
    if queue:
        queue.put([total_frames / src.samplerate, bpm_guess, delay, boundary_beats, chunk_levels])
    else:
        return total_frames / src.samplerate, bpm_guess, delay, boundary_beats, chunk_levels


def get_boundary_beats(energies_in, beat_length, delay, length_s):
    song_beats = length_s/beat_length
    n_for_beat = round(len(energies_in)/song_beats)
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
    print(f'n_for_beat: {n_for_beat}, chunk_levels: {chunk_levels}')
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


def get_top_level_effect_config():
    all_globals = globals()
    effects_config = {}
    for name, path in get_all_paths('effects', only_files=True):
        if name == 'compiler.py':
            continue
        module = 'effects.' + path.stem
        all_globals[module] = importlib.import_module(module)
        effects_config.update(all_globals[module].effects)
    return effects_config


top_level_effect_config = get_top_level_effect_config()
# print_blue(f'autogen: time taken up through get_top_level_effect_config(): {time.time() - generate_show_start_time} seconds')
def generate_show(song_filepath, overwrite=True, mode=None, include_song_path=True, output_directory=None, src_bpm_offset_cache=None):
    global last_song_filepath, last_song_data

    print_green(f'autogen: {song_filepath.stem} - Generating show...')

    generate_show_start_time = time.time()
    use_boundaries = True and mode != 'simple'
    if mode == 'lasers':
        show_name = f'g_lasers_{pathlib.Path(song_filepath).stem}'
    else:
        show_name = f'g_{pathlib.Path(song_filepath).stem}'

    if output_directory is None:
        output_directory = pathlib.Path(__file__).parent.joinpath('effects', 'autogen_shows')
    make_if_not_exist(output_directory)

    safe_python_filepath_name = ''.join([x if x.isalpha() else '_' for x in show_name])
    output_filepath = output_directory.joinpath(safe_python_filepath_name + '.py')
    if output_filepath.exists():
        if not overwrite:
            print_yellow(f'autogen: overwrite is set to False, and {output_filepath} exists, so returning without generating show')
            return None
    
    song_length, bpm_guess, delay, boundary_beats, chunk_levels = src_bpm_offset_cache or get_src_bpm_offset_multiprocess(song_filepath, use_boundaries)
    print_blue(f'autogen: {song_filepath.stem} - time taken up through get_src_bpm_offset_multiprocess: {time.time() - generate_show_start_time} seconds')


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
            if relative_path.is_relative_to(pathlib.Path(__file__).parent):
                relative_path = relative_path.relative_to(pathlib.Path(__file__).parent)
                print_blue(f'autogen: {song_filepath.stem} - relative_path: {relative_path}')                
        show['song_path'] = str(relative_path)

    
    effects_config_filtered = dict(filter(lambda x: x[1].get('autogen', False), top_level_effect_config.items()))

    effect_names = list(effects_config_filtered.keys())
    effect_types_to_name = {}
    for name, effect in effects_config_filtered.items():
        if type(effect['autogen']) == str:
            if effect['autogen'] not in effect_types_to_name:
                effect_types_to_name[effect['autogen']] = []
            effect_types_to_name[effect['autogen']].append(name)
    
    # TBD.  winamp effects with negative sidechain
    # either just double the ceiling brightness or do something more complex

    scenes = [
        # [8, ['winamp top', 'winamp sidechain', 'downbeat bottom']],
        # [8, ['winamp top', 'winamp sidechain']],
        # [8, ['winamp top', 'winamp sidechain', 'disco strobe']],
        # [8, ['winamp top', 'winamp sidechain', 'UV pulse']],

        [8, ['downbeat top', 'downbeat bottom']],
        [8, ['downbeat top', 'downbeat bottom', 'disco']],
        [8, ['downbeat top']],
        [8, ['downbeat top']],
        [8, ['downbeat top', 'disco strobe']],
        [8, ['downbeat bottom']],
        [8, ['downbeat mixed']],
        [8, ['downbeat mixed']],
        [8, ['downbeat mixed', 'disco']],
        [8, ['downbeat mixed', 'disco strobe']],
        [8, ['downbeat mixed', 'UV pulse']],
        [8, ['downbeat mixed', 'UV']],
        [8, ['downbeat top', 'downbeat bottom', 'UV']],
        [8, ['downbeat top', 'UV']],
        [8, ['downbeat bottom', 'UV']],
        [8, ['downbeat top', 'downbeat bottom']],
        [8, ['downbeat top', 'disco strobe']],
        [8, ['disco strobe']],
        [2, ['filler']],
        [2, ['UV pulse']],
        [2, ['disco']],
        [1, ['filler']],
        [1, ['filler', 'disco strobe']],
        [1, ['UV pulse single']],
    ]

    # from andrew's testing
    # [8, ['complex grid', 'downbeat bottom']],
    # [8, ['complex grid', 'downbeat bottom', 'disco']],
    # [8, ['complex grid']],
    # [1, ['filler']],


    if mode == 'lasers':
        for scene in scenes:
            if scene[0] == 8 and random.random() < .2:
                scene[1].append('laser long')

        for _ in range(2):
            scenes += [
                [5, ['laser long', 'disco strobe']],
            ]
        for _ in range(2):
            scenes += [
                [5, ['laser long']],
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
            show['beats'].append([beat, 'RBBB 1 bar', 4])
            beat += 4
    elif use_boundaries==True: # Based on scenes
        boundary_beats.append(total_beats+1) # add beats up to ending (maybe off by 1)
        prev_bound = 0
        for iter, bound in enumerate(boundary_beats):
            chunk_level = chunk_levels[iter]
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
                        if not effect_candidates: # it's low intensity but all candidates are high TODO
                            effect_candidates = ['UV pulse slow']
                        effect_name = random.choice(effect_candidates)

                        # shift by a random color
                        # dimmer doesn't play well with hue shifter
                        hue_shift, sat_shift, bright_shift = 0, 0, 0
                        # if random_color and effect_type != 'dimmers':
                        if effect_type != 'dimmers': # we never finished the dimming code
                            hue_shift=random.random()
                            bright_shift = 0.0
                            grid_bright_shift = 0.0

                        new_prev_effects.append(effect_name)
                        the_length = length
                        if length_left >= length*4 and length==8:
                            the_length = length * 4
                        elif length_left >= length*2 and length==8:
                            the_length = length * 2
                        show['beats'].append(b(beat, name=effect_name, length=the_length, hue_shift=hue_shift, sat_shift=sat_shift, bright_shift=bright_shift, grid_bright_shift=grid_bright_shift))
                    
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

    output_filepath = write_effect_to_file_pretty(output_filepath, the_show)
    print_blue(f'autogen: {song_filepath.stem} - time taken to finish: {time.time() - generate_show_start_time} seconds')
    
    return show_name, show, output_filepath


if __name__ == '__main__':
    configs_with_bpm = {}
    for effect_name, effect in top_level_effect_config.items():
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
                print_green(f'BPM match: {guess_bpm}, {delay_string}, {song_filepath}')
            else:
                print_red(f'config_bpm: {config_bpm} != guess_bpm: {guess_bpm}, {delay_string}, {song_filepath}')
        else:
            print_cyan(f'BPM: {guess_bpm}, no config_bpm found, {song_filepath}')

