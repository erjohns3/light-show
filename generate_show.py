import pathlib
import json
import re
import sys
import math
import statistics
import os
import importlib
import sys

from scipy.signal import find_peaks
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


def generate_show(song_filepath):
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')

    src, bpm_guess, delay = get_src_bpm_offset(song_filepath)

    show = {
        'bpm': int(bpm_guess),
        'song_path': str(song_filepath),
        'delay_lights': delay,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': []
    }

    # apply lights
    modes_to_cycle = ['Red top', 'Green top']
    length_s = src.duration / src.samplerate
    total_beats = int(length_s/60*bpm_guess)
    for beat in range(1, total_beats):
        mode = modes_to_cycle[beat % len(modes_to_cycle)]
        show['beats'].append([beat, mode, .25])
    return {
        f'generated_{pathlib.Path(song_filepath).stem}_show': show
    }



if __name__ == '__main__':
    real_std_out = sys.stdout
    all_globals = globals()

    effects_config = {}
    for name, path in get_all_paths('effects', only_files=True):
        module = 'effects.' + path.stem
        all_globals[module] = importlib.import_module(module)
        effects_config.update(all_globals[module].effects)

    configs_with_bpm = {}
    for effect_name, effect in effects_config.items():
        if 'bpm' in effect and 'song_path' in effect:
            configs_with_bpm[effect['song_path']] = effect['bpm']
    

    all_calculated_bpms = {}
    for name, song_filepath in get_all_paths('songs', only_files=True):
        src, bpm_guess, delay = get_src_bpm_offset(song_filepath)        
        all_calculated_bpms[str(song_filepath)] = bpm_guess

    for song_filepath, guess_bpm in all_calculated_bpms.items():
        if song_filepath in configs_with_bpm:
            config_bpm = configs_with_bpm[song_filepath]            
            if config_bpm == guess_bpm:
                print(f'{bcolors.OKGREEN}guess_bpm: {guess_bpm} == config_bpm: {config_bpm}, {song_filepath}{bcolors.ENDC}')
            else:
                print(f'{bcolors.FAIL}guess_bpm: {guess_bpm} == config_bpm: {config_bpm}, {song_filepath}{bcolors.ENDC}')
        else:
            print(f'{bcolors.OKCYAN}BPM: {bpm_guess}, no config_bpm found, {song_filepath}{bcolors.ENDC}')



# BPM: 128, songs/deadmau5 feat. Rob Swire - Ghosts N Stuff.ogg
# BPM: 90, songs/luigi.ogg
# BPM: 128, songs/deadmau5 & Kaskade - I Remember (HQ).ogg
# BPM: 130, songs/Brett Kavanaugh Hearing Automatic x Levels Remix.ogg
# BPM: 120, songs/Porter Robinson - Musician (Official Music Video).ogg
# BPM: 112, songs/Not Butter.ogg
# BPM: 157, songs/Everything Goes On.ogg
# BPM: 110, songs/KSLV - Pimp Slap.ogg
# BPM: 120, songs/Radiohead - Everything in Its Right Place (Sam Goku Edit).ogg
# BPM: 124, songs/cnam_slander_said_the_sky_cut.ogg
# BPM: 122, songs/BoonDocks - A Pimp Named Slickback Funny Moment's.ogg
# BPM: 144, songs/Porter Robinson x Illenium x Said the Sky Mix by C-Nam.ogg
# BPM: 100, songs/shelter.ogg
# BPM: 146, songs/mo_bamba.ogg
# BPM: 128, songs/Telepathic Love.ogg
# BPM: 136, songs/Mad Zach - The Visitor.ogg
# BPM: 118, songs/Joywave • Tongues (lyrics).ogg
# BPM: 90, songs/slowed_deadmau.ogg
# BPM: 176, songs/Sakamoto Maaya - Okaerinasai (tomatomerde Remix).ogg
# BPM: 138, songs/Superhumanoids - Too Young For Love.ogg
# BPM: 96, songs/Cheesecake.ogg
# BPM: 128, songs/Notion - Hooked.ogg