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


# rubberband -D 843 deadmau5\ \&\ Kaskade\ -\ I\ Remember\ \(HQ\).ogg slowed_deadmau.ogg
def change_speed_audio_rubberband(input_filepath, speed):
    output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}_rubberband_{speed}{input_filepath.suffix}')
    if os.path.exists(output_filepath):
        return output_filepath

    print(f'{bcolors.OKGREEN}Converting "{input_filepath} to speed {speed} using rubberband{bcolors.ENDC}"')
    run_command_blocking([
        'rubberband',
        '-t',
        1 / speed,
        str(input_filepath),
        str(output_filepath),
    ], debug=True)
    return output_filepath

def convert_to_wav(input_filepath):
    if type(input_filepath) != pathlib.Path:
        input_filepath = pathlib.Path(input_filepath)

    output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}.wav')
    if os.path.exists(output_filepath):
        return output_filepath

    print(f'{bcolors.OKGREEN}Converting "{input_filepath} to wav{bcolors.ENDC}"')
    run_command_blocking([
        'ffmpeg',
        '-i',
        str(input_filepath),
        str(output_filepath),
    ], debug=True)
    return output_filepath


def change_speed_audio_asetrate(input_filepath, speed):
    if type(input_filepath) != pathlib.Path:
        input_filepath = pathlib.Path(input_filepath)
    import tinytag

    output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}_asetrate_{speed}{input_filepath.suffix}')
    if os.path.exists(output_filepath):
        return output_filepath

    print(f'{bcolors.OKGREEN}Converting "{input_filepath} to speed {speed} using asetrate{bcolors.ENDC}"')
    run_command_blocking([
        'ffmpeg',
        '-i',
        str(input_filepath),
        '-filter:a',
        f'asetrate={tinytag.TinyTag.get(input_filepath).samplerate * speed}',
        '-y',
        str(output_filepath),
    ], debug=True)
    return output_filepath


#   ffmpeg -i input.mkv -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" output.mkv
# def change_speed_audio_atempo(input_filepath, speed):
#     output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}_{speed}{input_filepath.suffix}')
#     if os.path.exists(output_filepath):
#         return output_filepath
#     print(f'{bcolors.OKGREEN}Converting "{input_filepath} to speed {speed}{bcolors.ENDC}"')
#     run_command_blocking([
#         'ffmpeg',
#         '-i',
#         str(input_filepath),
#         '-filter_complex',
#         f'[0:a]atempo={speed}[a]',
#         '-map',
#         '[a]', 
#         str(output_filepath),
#     ], debug=True)
#     return output_filepath

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

def get_audio_clip_length(filepath):
    returncode, stdout, stderr = run_command_blocking([
        'ffprobe',
        '-v', 
        'error', 
        '-show_entries', 
        'format=duration', 
        '-of', 
        'default=noprint_wrappers=1:nokey=1', 
        str(filepath)
    ])
    return float(stdout)
