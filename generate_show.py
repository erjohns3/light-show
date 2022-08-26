import pathlib
import json
import re
import sys

import amen

from helpers import *


def generate_show(song_filepath):
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')

    rounded_bpm = 2
    model_beat_seconds = [0, 50]
    show = {
        'bpm': rounded_bpm,
        'song_path': str(song_filepath),
        'delay_lights': 0.0,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': []
    }

    # # applying lights
    modes_to_cycle = ['Red top', 'Green top']
    total_beats = 1 + int(model_beat_seconds[-1] * (rounded_bpm / 60))
    for beat in range(1, total_beats):
        # beat = str(round(second * (rounded_bpm / 60), 3))
        mode = modes_to_cycle[beat % len(modes_to_cycle)]
        show['beats'].append([beat, mode, .25])
    return {
        f'generated_{song_filepath.stem}_show': show
    }

