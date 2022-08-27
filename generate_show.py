import pathlib
import json
import re
import sys
import math
import statistics
import numpy as np

import aubio

from helpers import *


def generate_show(song_filepath):
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')


    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size
    
    src = aubio.source(str(song_filepath), 0, hop_s)

    print(src.uri, src.samplerate, src.channels, src.duration)
    o = aubio.tempo("default", win_s, hop_s, src.samplerate)

    delay = 4. * hop_s

    # list of beats, in samples
    beats_samplerate = []
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
            beats_samplerate.append(this_beat)
            beats.append(human_readable)
        total_frames += read
        if read < hop_s: break

    bpm_guess = -1
    offset_guess = -1
    best_seen = math.inf
    beats = np.array(beats)
    errors = {}
    for bpm in range(70, 180):
        distances = []
        beats_possible = [x*60/bpm for x in range(len(beats)+50)]
        error = 0
        for value in beats:
            match = find_nearest(beats_possible, value)
            distances.append(match-value)
        med = np.median(distances)

        for distance in distances:
            if abs(distance-med)/(60/bpm) > .1: # match to 1% of beat length (could be tuned)
                error+=1

        errors[bpm] = error
        if error < best_seen: 
            bpm_guess = bpm
            offset_guess = med
            best_seen = error
    # print(errors)

    length_int = 60.0/bpm_guess
    delay = length_int + offset_guess if offset_guess < 0 else offset_guess

    print(f'Guessing BPM as {bpm_guess} delay as {delay} beat_length as {length_int}')

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
    length_s = src.duration/src.samplerate
    total_beats = int(length_s/60*bpm_guess)
    for beat in range(1, total_beats):
        mode = modes_to_cycle[beat % len(modes_to_cycle)]
        show['beats'].append([beat, mode, .25])
    return {
        f'generated_{song_filepath.stem}_show': show
    }


# fast binary search to nearest value
def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]