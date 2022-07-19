# example call
# python play_some_sound_ffmpeg.py data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 42 8

import os
import subprocess
import threading
import multiprocessing
import pathlib

from helpers import *

audio_lock = threading.Lock()
audio_procs = []



if is_macos():
    multiprocessing.set_start_method("fork")


def play_audio_async(filepath, volume=100, paused=False):
    global is_paused
    is_paused = True
    proc = multiprocessing.Process(target=play_sound_with_mpv, args=[filepath, volume, paused])
    with audio_lock:
        audio_procs.append(proc)
    proc.start()

def is_audio_running():
    return any(map(lambda x: x.is_alive(), audio_procs))

def play_audio_seek_normalize_async(filepath, seconds_seek_to, seconds_to_play, normalize_peak_volume_decibals=False):
    proc = multiprocessing.Process(target=play_audio_seek_normalize_blocking, args=(filepath, seconds_seek_to, seconds_to_play, normalize_peak_volume_decibals))
    with audio_lock:
        audio_procs.append(proc)
    proc.start()


def play_audio_seek_normalize_blocking(filepath, seconds_seek_to, seconds_to_play, normalize_peak_volume_decibals=False):
    output_directory = pathlib.Path(__file__).parent.resolve().joinpath('data').joinpath('final_audio_clips')
    altered_mp3_filepath = create_then_normalize_mp3(filepath, output_directory, seconds_seek_to, seconds_to_play)
    play_sound_with_ffplay(altered_mp3_filepath)


def stop_audio():
    with audio_lock:
        while audio_procs:
            proc = audio_procs[-1]
            print(proc.is_alive())
            proc.terminate()
            proc.join()
            audio_procs.pop()

# example call: ffplay -i data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 -autoexit -nodisp -af 'dynaudnorm=n=0:c=1'
def play_sound_with_ffplay(audio_path, normalize_peak_volume_decibals=False, volume=100):
    if is_linux_root():
        print(f'{bcolors.FAIL}WARNING: you are running as root, this probably will cause problems with audio{bcolors.ENDC}')

    extra_args = []
    if normalize_peak_volume_decibals:
        extra_args += ['-af', 'loudnorm=I=-16:LRA=11:TP=-1.5']
        # ffplay_args.append("-af 'dynaudnorm=n=0:c=1'")

    run_command_blocking([
        'ffplay',
        '-autoexit',
        '-nodisp',
        '-volume',
        volume,
        str(audio_path)
    ] + extra_args, debug=True, print_std_out=True)



# i think full list of cmds
# https://mpv.io/manual/master/#json-ipc-client-name
# https://mpv.io/manual/master/#properties
mpv_pause_cmd = '''\
echo '{ "command": ["set_property", "pause", true] }' | socat - /tmp/mpvsocket
'''

mpv_unpause_cmd = '''\
echo '{ "command": ["set_property", "pause", false] }' | socat - /tmp/mpvsocket
'''


global is_paused
is_paused = False

def kill_mpv():
    os.system('killall mpv')

def toggle_pause_async_mpv():
    global is_paused
    if is_paused:
        os.system(mpv_unpause_cmd)
    else:
        os.system(mpv_pause_cmd)
    is_paused = not is_paused


def play_sound_with_mpv(audio_path, volume=100, paused=False):
    print('mpv go')

    if is_linux_root():
        print(f'{bcolors.FAIL}WARNING: you are running as root, this probably will cause problems with audio{bcolors.ENDC}')
    extra_args = []
    if paused:
        extra_args += ['--pause']
    print('mpv later')
    run_command_blocking([
        'mpv',
        '--no-resume-playback',
        f'--volume={volume}',
        '--input-ipc-server=/tmp/mpvsocket',
        'no-osc',
        'use-text-osd=no',
        'osd-level=1',
        'term-osd=force',
        '--no-video',
        str(audio_path)
    ] + extra_args, debug=True, print_std_out=True)
    print('started')





def create_then_normalize_mp3(input_filepath, output_directory, seconds_seek_to, seconds_to_play):
    not_normalized_mp3_filepath = create_mp3(input_filepath, output_directory, seconds_seek_to, seconds_to_play)
    return normalize_mp3(not_normalized_mp3_filepath, output_directory)

def normalize_mp3(input_filepath, output_directory):
    output_filepath = os.path.join(output_directory, f'{random_letters(10)}.mp3')
    ffmpeg_args = [
        '-i',
        input_filepath,
        '-af',
        'loudnorm=I=-16:LRA=11:TP=-1.5',
        output_filepath
    ]
    run_command_blocking(['ffmpeg'] + ffmpeg_args)
    return output_filepath


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
