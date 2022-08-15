import pathlib
import json
import re
import sys

import numpy as np
from essentia import *
from essentia.standard import *
from pydub import AudioSegment
# import librosa

from helpers import * 




def generate_show(song_filepath):
    print(f'{bcolors.OKGREEN}Generating show for "{song_filepath}"{bcolors.ENDC}')
    audio = MonoLoader(filename=str(song_filepath))()

    # rhythm_extractor = BeatsLoudness()
    # something1, something2 = rhythm_extractor(audio)
    # print('something1', something1)
    # print('somehting2', something2)
    # exit()

    rhythm_extractor = RhythmExtractor2013(method="multifeature")
    bpm, model_beat_seconds, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

    rounded_bpm = int(round(bpm, 0))
    print(f'BPM: real: {bpm}, rounded: {rounded_bpm}',)
    print(f'Beat estimation confidence: {beats_confidence}')

    # Write to an audio file in a temporary directory.
    beats_filepath = get_temp_dir().joinpath(f'{song_filepath.stem}_beat_data.dat')
    with open(beats_filepath, 'w') as f:
        f.writelines([' '.join(map(str, model_beat_seconds))])


    # Mark beat positions in the audio with beeps and write it to a file.
    marker = AudioOnsetsMarker(onsets=model_beat_seconds, type='beep')
    marked_audio = marker(audio)
    click_filepath = get_temp_dir().joinpath(f'{song_filepath.stem}_beeps{song_filepath.suffix}')
    MonoWriter(filename=str(click_filepath))(marked_audio)


    show = {
        'bpm': rounded_bpm,
        'song_path': str(song_filepath),
        'delay_lights': 0.0,
        'skip_song': 0.0,
        'profiles': ['Generated Shows'],
        'beats': {}
    }

    # Finding proper delay
    static_beat_times = []
    second_medians = []
    for beat, second_predicted in enumerate(model_beat_seconds):
        seconds_passed = beat * (60 / rounded_bpm)
        second_medians.append(second_predicted - seconds_passed)


    # this stuff sucks for some reason. the model is prob just trash
    # delay_amount = sum(second_medians) / len(second_medians)
    # show['delay_lights'] = delay_amount
    show['delay_lights'] = 0

    # applying lights
    modes_to_cycle = ['Red top', 'Green top']
    total_beats = 1 + int(model_beat_seconds[-1] * (rounded_bpm / 60))
    for beat in range(1, total_beats):
        # beat = str(round(second * (rounded_bpm / 60), 3))
        mode = modes_to_cycle[beat % len(modes_to_cycle)]
        show['beats'][str(int_or_float(beat))] = [mode, .25]
    return {
        f'generated_{song_filepath.stem}': show
    }




def eliminate(string, matches):
    found = set()
    for match in matches:
        if match in found:
            continue
        found.add(match)
        string = string.replace(match, '')
    return string


def int_or_float(i):
    i = float(i)
    if abs(i - round(i)) < .0001:
        return round(i)
    return i

if __name__ == '__main__':
    song_name = 'musician2.ogg'
    song_filepath = pathlib.Path('songs').joinpath(song_name)
    output_filepath = get_temp_dir().joinpath(f'generated_show_{song_filepath.stem}.py')

    effect_dict = generate_show(song_filepath)
    
    print(f'{bcolors.OKGREEN}Outputting generated show to "{output_filepath}"{bcolors.ENDC}')
    with open(output_filepath, 'w') as f:
        for effect in effect_dict.values():
            effect['beats'] = {int_or_float(i):v for i, v in effect['beats'].items()}
        effects_str = json.dumps(effect_dict, indent=4, sort_keys=True)

        # jank formatting
        before_string_matches = re.findall(r"\[(\s+)\"", effects_str)
        effects_str = eliminate(effects_str, before_string_matches)
        effects_str = effects_str.replace('],"', '],\n            "')
        effects_str = effects_str.replace('"beats": {"', '"beats": {\n            "')
        effects_str = effects_str.replace('"Generated Shows"\n        ],', '"Generated Shows"],')

        effects_str = 'effects = ' + effects_str
        f.writelines([effects_str])





# old stuff
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