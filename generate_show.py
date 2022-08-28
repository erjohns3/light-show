import pathlib
import json
import re
import sys
import math
import statistics

import aubio
import numpy as np
from helpers import *


def generate_show(song_filepath):
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')


    # -------------- tempo and offset -------------------
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size

    print(f'song_filepath: {song_filepath}')
    src = aubio.source(str(song_filepath), 0, hop_s)

    print(src.uri, src.samplerate, src.channels, src.duration)
    o = aubio.tempo("default", win_s, hop_s, src.samplerate)
    delay = 4. * hop_s

    beats = []

    # total number of frames read
    total_frames = 0
    bpms = []
    while True:
        samples, read = src()
        is_beat = o(samples)
        if is_beat:
            this_beat = total_frames - delay + is_beat[0] * hop_s
            human_readable = (this_beat / float(src.samplerate))
            # print("%f" % human_readable)
            beats.append(human_readable)
            bpms.append(o.get_bpm())
        total_frames += read
        if read < hop_s:
            break

    bpm = int(round(statistics.median(bpms)))

    distances = []
    beat_length = 60/bpm
    for i, value in enumerate(beats):
        if (bpms[i]-bpm)/bpm < .05:
            match = round(value/beat_length)*beat_length
            distances.append(beat_length-(match-value))
    med = np.median(distances)
    print(distances)
    length_int = 60.0/bpm
    delay = length_int - med if med < 0 else med

    print(
        f'Guessing BPM as {bpm} delay as {delay} beat_length as {length_int}')

    show = {
        'bpm': int(bpm),
        'song_path': str(song_filepath),
        'delay_lights': delay,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': []
    }

    # -------------- output ---------------------
    modes_to_cycle = ['Red top', 'Green top']
    length_s = src.duration/src.samplerate
    total_beats = int(length_s/60*bpm)
    for beat in range(1, total_beats):
        mode = modes_to_cycle[beat % len(modes_to_cycle)]
        show['beats'].append([beat, mode, .25])
    return {
        f'generated_{pathlib.Path(song_filepath).stem}_show': show
    }
