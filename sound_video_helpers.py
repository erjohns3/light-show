# example call
# python play_some_sound_ffmpeg.py data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 42 8

import time
import os
import pathlib
import json
import re

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


def slowed_audio(path, speed, cache=True, quiet=False):
    if is_windows():
        wav_path = convert_to_wav(path)
        path = wav_path
    
    slowed_path = change_speed_audio_rubberband(path, speed, cache=cache, quiet=quiet)
    
    # if is_windows():
        # wav_path.unlink()

    if is_windows():
        slowed_mp3_path = convert_to_mp3(slowed_path)
        # slowed_path.unlink()
        slowed_path = slowed_mp3_path
    
    return slowed_path

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


# https://trac.ffmpeg.org/wiki/Seeking
# def cut_video(video_path, start_second, end_second, output_directory=get_temp_dir(), cache=False, timing=False, quiet=True):
#     start_time = time.time()

#     output_video_path = output_directory.joinpath(f'extracted_{start_second:.2f}_{end_second:.2f}' + video_path.suffix)

#     cmd = [
#         'ffmpeg', '-hide_banner', '-y',
#         '-ss', seconds_to_fmmpeg_ms_string(start_second),
#         # '-t', seconds_to_fmmpeg_ms_string(end_second - start_second),
#         '-i', video_path,
#         '-map_chapters', '-1',
#         '-c', 'copy',
#         '-to', seconds_to_fmmpeg_ms_string(end_second),
#         '-copyts',
#         output_video_path,
#     ]
#     retcode, _stdout, stderr = run_command_blocking(cmd)
#     print_blue(f'{video_path=}')
#     print_blue(f'{output_video_path=}')
#     if timing:
#         length = sound_video_helpers.get_length(output_video_path)
#         wanted = end_second - start_second
#         print(f'cut_video took: {time.time() - start_time:.2f}. Wanted {wanted:.2f} length, got {length:.2f} length')
#     if retcode:
#         return print_red(f'ERROR cut_video ^^^ stderr: {stderr}')
#     return output_video_path



# THIS WORKS + FAST BUT SCREWS UP TIMESTAMPS?
    # cmd = [
    #     'ffmpeg', '-hide_banner', '-y',
    #     '-ss', seconds_to_fmmpeg_ms_string(start_second),
    #     '-i', video_path,
    #     '-map_chapters', '-1',
    #     '-c', 'copy',
    #     '-to', seconds_to_fmmpeg_ms_string(end_second),
    #     '-copyts',
    #     output_video_path,
    # ]

def slowed_video_ffmpeg_setpts(path, speed, output_directory=get_temp_dir(), cache=True, quiet=False):
    path = pathlib.Path(path)
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
def get_ffprobe_streams(path):
    retcode, stdout, stderr = run_command_blocking([
        'ffprobe', '-hide_banner',
        '-show_streams',
        str(path),
    ])
    if retcode:
        return print_red(f'get_ffprobe_streams: Couldnt get stream info: {stderr}')
    
    track = False
    streams = []
    try:
        for line in stdout.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line == '[STREAM]':
                streams.append({})
                track = True
            elif line == '[/STREAM]':
                track = False            
            elif line == '[SIDE_DATA]':
                track = False            
            elif track:
                key, val = line.split('=')
                streams[-1][key] = val
    except Exception as e:
        print_blue(f'{stdout}')
        print_yellow(f'{stderr}')
        print(f'{line=}')
        print_red(f'get_ffprobe_streams: Couldnt parse stream info: {get_stack_trace()}')
        exit()
    return streams


def get_audio_streams(path):
    streams = get_ffprobe_streams(path)
    return list(filter(lambda x: x['codec_type'] == 'audio', streams))


def get_video_streams(path):
    streams = get_ffprobe_streams(path)
    return list(filter(lambda x: x['codec_type'] == 'video', streams))


def ensure_single_stream(stream):
    if len(stream) == 0:
        return print_red(f'get_single_stream: No streams found: {stream=}')
    if len(stream) > 1:
        return print_red(f'get_single_stream: More than one stream found: {stream=}')
    return stream[0]


def get_audio_codec_name(filepath):
    audio_stream = ensure_single_stream(get_audio_streams(filepath))
    return audio_stream['codec_name']


codec_to_suffix = {
    'ac3': '.ac3',
    'aac': '.aac',
    'mp3': '.mp3',
    'opus': '.opus',
    'vorbis': '.ogg',
    'flac': '.flac',
}
# checks to only extract 1 audio stream for now
def extract_audio(input_filepath, output_directory=get_temp_dir(), start_second=None, end_second=None, cache=False, timing=False, quiet=True):
    start_time = time.time()
    input_filepath = pathlib.Path(input_filepath)
    existing_codec = get_audio_codec_name(input_filepath)
    
    extra_string = ''
    if start_second is not None:
        extra_string = f'start_{start_second:.3f}_end_{end_second:.3f}_'
    output_filepath = output_directory.joinpath(f'only_audio_{extra_string}{input_filepath.name}')

    if existing_codec in codec_to_suffix:
        output_filepath = output_filepath.with_suffix(codec_to_suffix[existing_codec])
    else:
        print_yellow(f'Dont know correct suffix for {existing_codec=}, keeping original suffix')
    if cache and output_filepath.exists():
        return output_filepath

    if not quiet:
        print(f'extract_audio: From "{input_filepath}", {existing_codec=}, extracting audio to "{output_filepath}"')

    cmd = ['ffmpeg', '-y', '-hide_banner']

    if start_second is None:
        cmd += [
            '-i', input_filepath,
            '-vn',
            '-c:a', 'copy', 
        ]
    else:
        cmd += [
            '-i', input_filepath,
            '-ss', seconds_to_fmmpeg_ms_string(start_second),
            '-to', seconds_to_fmmpeg_ms_string(end_second),
            '-vn',
            '-c:a', 'copy', 
            '-copyts',
        ]
    cmd.append(output_filepath)
    retcode, _stdout, stderr = run_command_blocking(cmd)
    if retcode:
        return print_red(f'extract_audio: Couldnt extract audio clip due to: {stderr}')
    if timing:
        print(f'extract_audio took: {time.time() - start_time:.2f}')
    if not quiet and start_second is not None:
        output_length = get_length(output_filepath, exact=True)
        print(f'output length is {output_length:.4f} seconds, wanted {end_second - start_second:.4f} seconds')
    return output_filepath


def convert_to_aac(input_filepath, output_directory=get_temp_dir(), cache=False, quiet=False):
    input_filepath = pathlib.Path(input_filepath)
    if input_filepath.suffix == '.aac':
        print(f'convert_to_aac: {input_filepath} already has aac suffix')
        return input_filepath

    output_filepath = output_directory.joinpath(f'{input_filepath.stem}.aac')    
    if cache and output_filepath.exists():
        print(f'convert_to_aac: {output_filepath} already exists')
        return output_filepath

    existing_codec = get_audio_codec_name(input_filepath)
    if existing_codec == 'aac':
        print(f'convert_to_aac: {existing_codec=} so no need to convert')
        return extract_audio(input_filepath, output_directory, cache=cache, quiet=quiet)

    if not quiet:
        print_green(f'{existing_codec=} so slow converting (encoding) "{input_filepath}" to aac and storing in {output_filepath}')

    cmd = [
        'ffmpeg', '-y', '-hide_banner',
        '-i', input_filepath,
        '-vn',
        # '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-f', 'adts',
        output_filepath,
    ]
    retcode, _stdout, stderr = run_command_blocking(cmd)
    if retcode:
        return print_red(f'convert_to_aac: Couldnt extract due to stderr: {stderr}')
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

    existing_codec = get_audio_codec_name(input_filepath)
    if existing_codec == 'mp3':
        print(f'convert_to_mp3: {existing_codec=} so no need to convert')
        return extract_audio(input_filepath, output_directory, cache=cache, quiet=quiet)

    if not quiet:
        print_green(f'{existing_codec=} so slow converting (encoding) "{input_filepath}" to mp3"')

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


def change_speed_audio_asetrate(input_filepath, speed, cache=True, quiet=False):
    input_filepath = pathlib.Path(input_filepath)

    if speed == 1.0 or speed == 1:
        return input_filepath
    
    output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}_asetrate_{speed}{input_filepath.suffix}')
    if cache and output_filepath.exists():
        return output_filepath
    
    import tinytag
    input_samplerate = tinytag.TinyTag.get(input_filepath).samplerate
    if not quiet: print_green(f'Converting "{input_filepath}" to speed {speed} using asetrate')
    retcode, stdout, stderr = run_command_blocking([
        'ffmpeg', '-hide_banner', '-y',
        '-copyts',
        '-i', input_filepath,
        '-filter:a',
        f'asetrate={input_samplerate * speed},aresample={input_samplerate}:resampler=soxr',
        # !TODO fix
        '-b:a', '499821',
        output_filepath,
    ])

    if retcode:
        return print_red(f'change_speed_audio_asetrate: Couldnt change speed due to: {stderr}')
    input_length = get_length(input_filepath, exact=True)
    output_length = get_length(output_filepath, exact=True)
    print_yellow(f'change_speed_audio_asetrate: {input_length=}, {output_length=}, ratio is {input_length / output_length:.4f}')
    print_yellow(f'Samplerate before {tinytag.TinyTag.get(input_filepath).samplerate}, samplerate after: {tinytag.TinyTag.get(output_filepath).samplerate}')

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

# ffmpeg -i input.mp3 -f null -
# The second to the last line of the console output will show something like:
# size=N/A time=00:03:49.12 bitrate=N/A


def get_length(filepath, exact=False):
    if exact:
        returncode, stdout, stderr = run_command_blocking([
            'ffmpeg', '-hide_banner', 
            '-i', filepath,
            '-f', 'null',
            '-',
        ])
        if returncode:
            return print_red(f'get_length: Couldnt get length due to: {stderr}')

        lines = stderr.strip().splitlines()
        # regex for "time=00:00:19.96" and get the time in seconds
        matches = re.findall(r'time=(\d\d:\d\d:\d\d.\d\d)', lines[-2])
        return hmsm_string_to_seconds(matches[0])

    else:
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
        if returncode:
            return print_red(f'get_length: Couldnt get length due to: {stderr}')
        return float(stdout.strip())

def guess_video_metadata_from_path(video_path, quiet=False):
    import re
    file_name = video_path.stem.lower()
    title = None
    season_number = None
    episode_number = None
    year = None
    if (re.fullmatch(r'[^.]+\.[^.]+(\.[^.]+)*', file_name)):
        import PTN
        info = PTN.parse(file_name)
        if 'title' in info: title = info['title']
        if 'season' in info: season_number = info['season']
        if 'episode' in info: episode_number = info['episode']
        if 'year' in info: year = info['year']
    else:
        if (season_ep_info := re.search(r's\d+\w*e\d+', file_name)):
            season_number, episode_number = re.split('s|e',season_ep_info.group())[1:]
            file_name = re.sub(season_ep_info.re, '', file_name)
        else:
            if (season_info := re.search(r'(season|s)\s*\d+', file_name)):
                season_number = re.search(r'\d+', season_info.group()).group()
                file_name = re.sub(season_info.re, '', file_name)
            elif (season_info := re.search(r'(season|s)\s*\d+', file_name.parent.stem)):
                season_number = re.search(r'\d+', season_info.group()).group()
            if (ep_info := re.search(r'(episode|ep|e)\s*\d+', file_name)):
                episode_number = re.search(r'\d+', ep_info.group()).group()
                file_name = re.sub(ep_info.re, '', file_name)
        if (year_info := re.search(r'\((19|20)\d{2}\)', file_name)):
            year =  re.search(r'\d+', year_info.group()).group()
            file_name = re.sub(year_info.re, '', file_name)
    file_name.strip()
    # Fuzz match and see if we can find a match
    if not title:
        from thefuzz import fuzz
        title_scores = [(x, fuzz.partial_ratio(file_name, x)) for x in video_path.relative_to(video_path.anchor).parts[0:-1] if fuzz.partial_ratio(file_name, x) > 80]
        if title_scores:
            title_scores.sort(key=lambda x: x[1], reverse=True)
            best_title = title_scores[0][0] 
            title = (re.search(best_title, file_name, flags=re.IGNORECASE) or re.search(file_name, best_title, flags=re.IGNORECASE)).group()
    # giveup and grab parent
    if not title:
        video_path_stepper = video_path
        while video_path_stepper.parent != video_path_stepper:
            if re.sub(r'-|_', ' ', video_path_stepper.parent.stem.lower()) in ['movies', 'tv', 'tv shows', 'tv show', 'tv series']:
                title = video_path_stepper.stem
                break
            video_path_stepper = video_path_stepper.parent
    # just give up
    if not title:
        print_red(f'guess_video_metadata_from_path: Couldnt guess title for "{video_path}"')
    if title and not year:
        if (year_info := re.search(r'\((19|20)\d{2}\)', title)):
            year =  re.search(r'\d+', year_info.group()).group()
            title = re.sub(year_info.re, '', title)
    output = {'title': title, 'season': season_number, 'episode': episode_number, 'year': year}
    if not quiet: print_green(f'guess_video_metadata_from_path: Metadata inferred for {json.dumps(output, indent=4)}\n')
    return output

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