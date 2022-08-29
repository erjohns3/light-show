import pathlib
import json
import re
import sys
import math
import statistics
import numpy as np
from scipy.signal import find_peaks
import pandas as pd 
import aubio

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
    print('lol')
    song_filepath = 'songs/shelter.ogg'
    bpm_guess, delay = get_src_bpm_offset(song_filepath)


