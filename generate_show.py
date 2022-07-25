import pathlib
import json
import re
import sys

import numpy as np
from essentia import *
from essentia.standard import *
from pydub import AudioSegment
import librosa
# from pylab import *

from helpers import * 


song_name = 'musician.mp3'
song_filepath = python_file_directory.joinpath('data').joinpath(song_name).resolve().relative_to(python_file_directory)



audio = MonoLoader(filename=str(song_filepath))()

rhythm_extractor = RhythmExtractor2013(method="multifeature")
bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

rounded_bpm = int(round(bpm, 0))
print(f'BPM: real: {bpm}, rounded: {rounded_bpm}',)
print(f'Beat estimation confidence: {beats_confidence}')

# Write to an audio file in a temporary directory.
beats_filepath = pathlib.Path('data').joinpath('nonsense').joinpath('temp_beats_output.dat')
with open(beats_filepath, 'w') as f:
    f.writelines([' '.join(map(str, beats))])


# Mark beat positions in the audio and write it to a file.
# Use beeps instead of white noise to mark them, as it is more distinctive.


marker = AudioOnsetsMarker(onsets=beats, type='beep')
marked_audio = marker(audio)
click_filepath = pathlib.Path('data').joinpath('nonsense').joinpath('click_file_for_essentia.mp3')
MonoWriter(filename=str(click_filepath))(marked_audio)


new_show = {
    'song_name': str(song_filepath),
    'bpm': rounded_bpm,
    'show_timing_type': 'seconds',
    # 'delay': 0.0,
    'show': [],
}


# making inteligent decicions or something
# sound = AudioSegment.from_file(song_filepath, format='mp3')


# y, sr = librosa.load(librosa.ex('nutcracker'))
# hop_length = 512
# y_harmonic, y_percussive = librosa.effects.hpss(y)
# Beat track on the percussive signal
# tempo, beat_frames = librosa.beat.beat_track(y=y_percussive, sr=sr)
# Compute MFCC features from the raw signal
# mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
# print(mfcc)

# mfcc_delta = librosa.feature.delta(mfcc)
# print(mfcc_delta)

# output = np.mean(librosa.feature.rms(audio, center=True).T, axis=0)
# print(output)
# exit()

modes_to_cycle = ['Red Top', 'Green Top']
for index, second in enumerate(beats):
    mode = modes_to_cycle[index % len(modes_to_cycle)]
    new_show['show'].append([mode, float(second)])
    

# writing into a show
with open('shows.json') as f:
    shows_json = json.loads(f.read())



shows_json[os.path.splitext(song_name)[0]] = new_show





def eliminate(string, matches):
    found = set()
    for match in matches:
        if match in found:
            continue
        found.add(match)
        string = string.replace(match, '')
    return string

with open('shows.json', 'w') as f:
    shows_json_str = json.dumps(shows_json, indent=4, sort_keys=True)

    before_string_matches = re.findall(r"\[(\s+)\"", shows_json_str)
    shows_json_str = eliminate(shows_json_str, before_string_matches)

    after_digit = re.findall(r"\d(\s+)\]", shows_json_str)
    shows_json_str = eliminate(shows_json_str, after_digit)
    shows_json_str = shows_json_str.replace('[[', '[\n            [')
    shows_json_str = shows_json_str.replace('],[', '],\n            [')
    
    f.writelines([shows_json_str])

