# example call
# python play_some_sound_ffmpeg.py data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 42 8

import os
import shutil
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
        print_red(f'You are running as root, this probably will cause problems with audio, continuing anyway')

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
def change_speed_audio_rubberband(input_filepath, speed, output_directory=get_temp_dir(), cache=False, quiet=False):
    input_filepath = pathlib.Path(input_filepath)

    if speed == 1.0 or speed == 1:
        return input_filepath
    
    output_filepath = output_directory.joinpath(f'{input_filepath.stem}_rubberband_{speed}{input_filepath.suffix}')
    if cache and output_filepath.exists():
        return output_filepath

    if not quiet:
        print_green(f'Converting "{input_filepath}" to speed {speed} using rubberband')
        
    retcode, _stdout, stderr = run_command_blocking([
        'rubberband',
        '-t',
        str(1 / speed),
        input_filepath,
        output_filepath,
    ])
    if retcode:
        return print_red(f'change_speed_audio_rubberband: Couldnt change speed due to: {stderr}')
    return output_filepath


def convert_to_wav(input_filepath, output_directory=get_temp_dir(), cache=True, quiet=False):
    input_filepath = pathlib.Path(input_filepath)
    output_filepath = output_directory.joinpath(f'{input_filepath.stem}.wav')
    if input_filepath.suffix == '.wav' or (cache and output_filepath.exists()):
        return output_filepath

    if not quiet:
        print(f'Converting "{input_filepath}" to wav')
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg',
        '-i',
        input_filepath,
        output_filepath,
    ])
    if retcode:
        return print_red(f'convert_to_wav: Couldnt convert to wav due to: {stderr}')
    return output_filepath  


# ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
def combine_video_audio(video_path, audio_path, output_directory=get_temp_dir(), cache=True):
    output_filepath = output_directory.joinpath(f'{video_path.stem}_combined_audio_video{video_path.suffix}')
    if cache and output_filepath.exists():
        return output_filepath
    
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg', '-y', '-hide_banner',
        '-i', str(video_path),
        '-i', str(audio_path),
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '1:a:0',
        output_filepath,
    ])
    if retcode:
        return print_red(f'combine_video_audio: Couldnt combine video and audio due to: {stderr}')
    return output_filepath

# ffmpeg -i input.mp4 -c copy -an output.mp4
def remove_audio(path, output_directory=get_temp_dir(), cache=True):
    path = pathlib.Path(path)
    output_filepath = output_directory.joinpath(f'{path.stem}_no_audio_{path.suffix}')
    if cache and output_filepath.exists():
        return output_filepath
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg',
        '-i', str(path),
        '-c', 'copy',
        '-an', '-y',
        output_filepath,
    ])
    if retcode:
        return print_red(f'remove_audio: Couldnt remove audio due to: {stderr}')
    return output_filepath


def slowed_video_ffmpeg_setpts(path, speed, output_directory=get_temp_dir(), cache=True, quiet=False):
    path = pathlib.Path(path)
    if speed == 1.0 or speed == 1:
        return path

    output_filepath = output_directory.joinpath(f'{path.stem}_filter_setpts_{speed}{path.suffix}')
    if cache and output_filepath.exists():
        return output_filepath

    if not quiet:
        print_green(f'Converting "{path}" to speed {speed} using filter setpts')
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg',
        '-i', str(path),
        '-filter:v', f'setpts={1 / speed}*PTS',
        '-y',
        output_filepath,
    ])
    if retcode:
        return print_red(f'slowed_video: Couldnt slow video due to: {stderr}')
    return output_filepath


# [STREAM]
    # index=0
    # codec_type=video
    # codec_name=h264
    # profile=High
    # codec_tag_string=avc1
    # width=1920
    # height=800
    # sample_aspect_ratio=1:1
    # display_aspect_ratio=12:5
    # pix_fmt=yuv420p
    # level=40
    # is_avc=true
    # r_frame_rate=24000/1001
    # avg_frame_rate=24000/1001
    # time_base=1/24000
    # start_pts=0
    # start_time=0.000000
    # duration_ts=482482
    # duration=20.103417
    # bit_rate=2213745
    # bits_per_raw_sample=8
    # nb_frames=482

# [STREAM]
    # index=1
    # codec_type=audio
    # codec_name=aac
    # codec_tag_string=mp4a
    # sample_fmt=fltp
    # sample_rate=48000
    # channels=2
    # channel_layout=stereo
    # time_base=1/48000
    # duration_ts=960720
    # duration=20.015000
    # bit_rate=128475
    # max_bit_rate=N/A
    # bits_per_raw_sample=N/A
    # nb_frames=940
def get_ffmpeg_streams(path):
    retcode, stdout, stderr = run_command_blocking([
        'ffprobe', '-hide_banner',
        '-show_streams',
        str(path),
    ])
    if retcode:
        return print_red(f'get_ffmpeg_streams: Couldnt get stream info: {stderr}')
    
    streams = []
    for line in stdout.split('\n'):
        line = line.strip()
        if not line or line == '[/STREAM]':
            continue
        if line == '[STREAM]':
            streams.append({})
        elif len(streams):
            key, val = line.split('=')
            streams[-1][key] = val
    return streams


def get_audio_streams(path):
    streams = get_ffmpeg_streams(path)
    return list(filter(lambda x: x['codec_type'] == 'audio', streams))


def get_video_streams(path):
    streams = get_ffmpeg_streams(path)
    return list(filter(lambda x: x['codec_type'] == 'video', streams))


codec_to_suffix = {
    'aac': '.aac',
    'mp3': '.mp3',
    'opus': '.opus',
    'vorbis': '.ogg',
    'flac': '.flac',
}
# checks to only extract 1 audio stream for now
def extract_audio(input_filepath, output_directory=get_temp_dir(), cache=False, quiet=True):
    input_filepath = pathlib.Path(input_filepath)
    audio_streams = get_audio_streams(input_filepath)
    if len(audio_streams) == 0:
        return print_red(f'extract_audio: No audio stream found: {audio_streams}')
    if len(audio_streams) > 1:
        return print_red(f'extract_audio: More than one audio stream found: {audio_streams}')
    output_filepath = output_directory.joinpath(f'only_audio_{input_filepath.name}')

    codec = audio_streams[0]['codec_name']
    if codec in codec_to_suffix:
        output_filepath = output_filepath.with_suffix(codec_to_suffix[codec])
    else:
        print_yellow(f'Dont know correct suffix for {codec=}, keeping original suffix')
    if cache and output_filepath.exists():
        return output_filepath

    if not quiet:
        print_green(f'Extracting audio from "{input_filepath}"')
    
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg', '-y', '-hide_banner',
        '-i', input_filepath,
        '-vn',
        '-c:a', 'copy', 
        output_filepath
    ])
    if retcode:
        return print_red(f'extract_audio: Couldnt extract audio clip due to: {stderr}')
    return output_filepath


def convert_to_mp3(input_filepath, output_directory=get_temp_dir(), cache=False, quiet=False):
    input_filepath = pathlib.Path(input_filepath)
    if input_filepath.suffix == '.mp3':
        print(f'convert_to_mp3: {input_filepath} already has mp3 suffix')
        return input_filepath

    output_filepath = output_directory.joinpath(f'{input_filepath.stem}.mp3')    
    if cache and output_filepath.exists():
        print(f'convert_to_mp3: {output_filepath} already exists')
        return output_filepath

    audio_streams = get_audio_streams(input_filepath)
    if len(audio_streams) == 0:
        return print_red(f'extract_mp3: No audio stream found: {audio_streams}')
    
    if len(audio_streams) > 1:
        return print_red(f'extract_mp3: More than one audio stream found: {audio_streams}')
    
    if audio_streams[0]['codec_name'] == 'mp3':
        print(f'convert_to_mp3: Audio codec is {audio_streams[0]["codec_name"]} so no need to convert')
        return extract_audio(input_filepath, output_directory, cache=cache, quiet=quiet)

    if not quiet:
        print_green(f'Audio codec is {audio_streams[0]["codec_name"]} so slow converting (encoding) "{input_filepath}" to mp3"')

    cmd = [
        'ffmpeg', '-y', '-hide_banner',
        '-i', input_filepath,
        '-vn',
        '-ab', '128k', 
        '-ar', '44100',
        '-f', 'mp3',
        output_filepath,
    ]
    retcode, _stdout, stderr = run_command_blocking(cmd)
    if retcode:
        return print_red(f'convert_to_mp3: Couldnt extract due to stderr: {stderr}')
    return output_filepath


def change_speed_audio_asetrate(input_filepath, speed, quiet=False):
    input_filepath = pathlib.Path(input_filepath)

    if speed == 1.0 or speed == 1:
        return input_filepath
    output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}_asetrate_{speed}{input_filepath.suffix}')
    if output_filepath.exists():
        return output_filepath
    
    import tinytag
    if not quiet:
        print(f'{bcolors.OKGREEN}Converting "{input_filepath} to speed {speed} using asetrate{bcolors.ENDC}"')
    run_command_blocking([
        'ffmpeg',
        '-i',
        input_filepath,
        '-filter:a',
        f'asetrate={tinytag.TinyTag.get(input_filepath).samplerate * speed}',
        '-y',
        output_filepath,
    ], debug=False)
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
#         input_filepath,
#         '-filter_complex',
#         f'[0:a]atempo={speed}[a]',
#         '-map',
#         '[a]', 
#         output_filepath,
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

def get_length(filepath):
    returncode, stdout, stderr = run_command_blocking([
        'ffprobe',
        '-v', 
        'error', 
        '-show_entries', 
        'format=duration', 
        '-of', 
        'default=noprint_wrappers=1:nokey=1', 
        filepath,
    ])
    return float(stdout.strip())


allowed_song_extensions = set(['.mp3', '.ogg', '.wav'])
def get_song_metadata_info(song_path):
    from tinytag import TinyTag

    if song_path.suffix in allowed_song_extensions:
        # song_metadata_start_time = time.time()
        tags = TinyTag.get(song_path)
        # print(f'get_song_metadata_info(): took {time.time() - song_metadata_start_time} seconds')
        name, duration = tags.title, tags.duration

        if name == None:
            name = song_path.stem

        if not duration:
            print_yellow(f'No tag found for file: "{song_path}", ffprobing, but this is slow.')
            duration = get_length(song_path)
        return name, tags.artist, duration, tags.samplerate, song_path
    else:
        print_red(f'File type not in: {allowed_song_extensions}, {song_path}')

def generateFrequencyVideo(input_audio, quiet=False):
    output_path = get_temp_dir().joinpath(f'{input_audio.stem}_freq.mp4')

    if output_path.exists() and (output_path.stat().st_mtime > pathlib.Path(__file__).stat().st_mtime):
        return output_path

    if not quiet:
        print_blue('Generating frequency video...')

    from scipy.signal import find_peaks, medfilt
    import librosa
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt
    import numpy as np

    n_fft = 2048*4
    y, sr = librosa.load(input_audio, sr=44100*2)
    if len(y) % n_fft:
        y = np.pad(y, (0, (len(y)//n_fft+1)*n_fft - len(y)), 'constant', constant_values=0) # pad to be divisible by n_fft

    frequencies = np.linspace(0, sr/2, int(1 + n_fft//2))

    NOTE_NAMES = [
        "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4"
    ]
    FREQ_VALUES = [librosa.note_to_hz(n) for n in NOTE_NAMES]
    NOTE_NAMES = [n.replace('#', "'") for n in NOTE_NAMES]

    fig, ax = plt.subplots()
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Amplitude")
    Y_LIM = 600
    ax.set_xlim(40, 400)
    ax.set_ylim(0, Y_LIM)
    ax.set_xscale('log')
    for i in range(len(NOTE_NAMES)):
        colors = ('cyan', 'magenta', 'green')
        ax.axvline(x=FREQ_VALUES[i], color=colors[i%3], linestyle='--', linewidth=.5, alpha=.5)
        ax.annotate(NOTE_NAMES[i], (FREQ_VALUES[i], Y_LIM - (i%3 * 30)), color=colors[i%3])
    line_original, = ax.plot([], [], label='Original Spectrum', color='blue')
    #line_smoothed, = ax.plot([], [], label='Smoothed Spectrum', color='orange')

    def animate(i):
        start_sample = i * n_fft
        end_sample = (i + 1) * n_fft

        fft_result = librosa.stft(y[start_sample:end_sample], n_fft=n_fft, hop_length=sr, window='hann', center=False)
        d = np.abs(fft_result)
        #Smooth data into wave
        freq_content = np.mean(d, axis=1)

        line_original.set_data(frequencies, freq_content)
        #line_smoothed.set_data(frequencies, medfilt(freq_content, kernel_size=3))

        #return [line_original,line_smoothed]
        return line_original,

    num_frames = len(y)/n_fft
    frame_duration = n_fft/sr
    print(f'sample rate: {sr}, num_frames: {num_frames}, frame_duration: {frame_duration}')
    ani = FuncAnimation(fig, animate, frames=int(num_frames), interval=int(frame_duration * 1000), blit=True, repeat=False)
    
    tmp_path = get_temp_dir().joinpath(f'{random_letters(15)}.mp4')
    ani.save(tmp_path, writer='ffmpeg', fps=1/frame_duration)
    shutil.move(tmp_path, output_path)
    
    return output_path