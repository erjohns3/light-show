# example call
# python play_some_sound_ffmpeg.py data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 42 8

import os
import subprocess
import threading
import multiprocessing
import pathlib

from helpers import *


audio_procs = []
def is_audio_running():
    return any(map(lambda x: x.is_alive(), audio_procs))

def stop_audio():
    while audio_procs:
        proc = audio_procs[-1]
        proc.terminate()
        audio_procs.pop()

# example call: ffplay -i data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 -autoexit -nodisp -af 'dynaudnorm=n=0:c=1'
async def play_sound_with_ffplay(audio_path, start_time=0, volume=100):
    if is_linux_root():
        print(f'{bcolors.FAIL}WARNING: you are running as root, this probably will cause problems with audio{bcolors.ENDC}')

    extra_args = []
    if False: # normalize_peak_volume_decibals
        extra_args += ['-af', 'loudnorm=I=-16:LRA=11:TP=-1.5'] # or -af 'dynaudnorm=n=0:c=1'

    process = run_command_async([
        'ffplay',
        '-autoexit',
        '-nodisp',
        '-volume',
        str(volume),
        '-ss',
        seconds_to_hmsm_string(start_time),
        str(audio_path)
    ] + extra_args, debug=True)

    audio_procs.append(process)

def create_mp3(input_filepath, output_directory, seconds_seek_to, seconds_to_play):
    output_filepath = os.path.join(output_directory, f'{random_letters(10)}.mp3')
    ffmpeg_args = [
        '-i',
        input_filepath,
        '-ss',
        seconds_to_hmsm_string(seconds_seek_to),
        '-to',
        seconds_to_hmsm_string(seconds_seek_to + seconds_to_play),
        output_filepath
    ]
    run_command_blocking(['ffmpeg'] + ffmpeg_args)
    return output_filepath

def get_audio_clip_length(filename):
    ffprobe_args = ['-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename]
    return float(run_command_blocking(['ffprobe'] + ffprobe_args))
