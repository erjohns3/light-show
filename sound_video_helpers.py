# example call
# python play_some_sound_ffmpeg.py data\f538d56c8aa48cea62c35aa01438ff92cde5708ec59c69e9e1be65ff.mp3 42 8

import os
import pathlib
import time
import sys

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

def change_speed_audio_rubberband(input_filepath, speed, output_directory=get_temp_dir(), cache=False, quiet=False, timing=True):
    input_filepath = pathlib.Path(input_filepath)

    if speed == 1.0 or speed == 1:
        return input_filepath
    
    if is_windows():
        converted_path = convert_to_wav(input_filepath, output_directory, cache=cache, quiet=quiet)
    else:
        # !TODO idk if this is needed
        converted_path = convert_to_mp3(input_filepath, output_directory, cache=cache, quiet=quiet)

    start_time = time.time()

    output_filepath = output_directory.joinpath(f'{converted_path.stem}_rubberband_{speed}.mp3')
    intermediary_filepath = output_filepath.with_suffix(converted_path.suffix)
    if cache and output_filepath.exists():
        return output_filepath

    if not quiet:
        print_green(f'Converting "{converted_path}" to speed {speed} using rubberband')

    retcode, _stdout, stderr = run_command_blocking([
        'rubberband',
        '-t', str(1 / speed),
        converted_path,
        intermediary_filepath,
    ])
    if retcode:
        return print_red(f'change_speed_audio_rubberband: Couldnt change speed due to: {stderr}')
    if timing:
        print(f'change_speed_audio_rubberband: took {time.time() - start_time:.2f} seconds')
    if is_windows():
        return convert_to_mp3(intermediary_filepath, output_directory, cache=cache, quiet=quiet)
    return intermediary_filepath


def convert_to_wav(input_filepath, output_directory=get_temp_dir(), cache=True, quiet=False):
    input_filepath = pathlib.Path(input_filepath)
    output_filepath = output_directory.joinpath(f'{input_filepath.stem}.wav')
    if input_filepath.suffix == '.wav' or (cache and output_filepath.exists()):
        return output_filepath

    if not quiet:
        print(f'Converting "{input_filepath}" to wav')
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg', '-y', '-hide_banner',
        '-i',
        # '-b:a', '96k',
        input_filepath,
        output_filepath,
    ])
    if retcode:
        return print_red(f'convert_to_wav: Couldnt convert to wav due to: {stderr}')
    return output_filepath  


# ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 output.mp4
# !TODO WARNING i changed -c:a to copy instead of aac, idk why it was that way before
def combine_video_audio(video_path, audio_path, output_directory=get_temp_dir(), cache=True):
    output_filepath = output_directory.joinpath(f'{video_path.stem}_combined_audio_video{video_path.suffix}')
    if cache and output_filepath.exists():
        return output_filepath
    
    print(f'combine_video_audio: Combining video and audio to {output_filepath}')
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg', '-y', '-hide_banner',
        '-i', str(video_path),
        '-i', str(audio_path),
        '-c:v', 'copy',
        '-c:a', 'copy',
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
    output_filepath = output_directory.joinpath(f'{path.stem}_no_audio{path.suffix}')
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


# !TODO look into http://trac.ffmpeg.org/wiki/How%20to%20speed%20up%20/%20slow%20down%20a%20video
def slowed_video_ffmpeg_setpts(path, speed, output_directory=get_temp_dir(), cache=True, quiet=False):
    path = pathlib.Path(path)
    if speed == 1.0 or speed == 1:
        return path

    output_filepath = output_directory.joinpath(f'{path.stem}_filter_setpts_{speed}{path.suffix}')
    if cache and output_filepath.exists():
        return output_filepath

    if not quiet:
        print_green(f'Converting "{path}" to speed {speed} using filter setpts, final output is {output_filepath}')
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg', '-hide_banner', '-y',
        '-i', str(path),
        '-filter:v', f'setpts={1 / speed}*PTS',
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


def convert_to_mp3(input_filepath, output_directory=get_temp_dir(), cache=True, quiet=False):
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
        # !TODO idk about this, but commenting out for now
        # '-ab', '128k', 
        # '-ar', '44100',
        '-f', 'mp3',
        output_filepath,
    ]
    retcode, _stdout, stderr = run_command_blocking(cmd)
    if retcode:
        return print_red(f'convert_to_mp3: Couldnt extract due to stderr: {stderr}')
    return output_filepath


def change_speed_audio_asetrate(input_filepath, speed, output_samplerate=48000, cache=True, quiet=False):
    input_filepath = pathlib.Path(input_filepath)

    if speed == 1.0 or speed == 1:
        return input_filepath
    output_filepath = get_temp_dir().joinpath(f'{input_filepath.stem}_asetrate_{speed}{input_filepath.suffix}')
    if cache and output_filepath.exists():
        return output_filepath
    
    import tinytag
    if not quiet:
        print_green(f'Converting "{input_filepath} to speed {speed} using asetrate"')
    retcode, _stdout, stderr = run_command_blocking([
        'ffmpeg', '-hide_banner', '-y',
        '-i', input_filepath,
        '-filter:a', f'asetrate={tinytag.TinyTag.get(input_filepath).samplerate * speed},aresample=48000',
        output_filepath,
    ])
    if retcode:
        return print_red(f'change_speed_audio_asetrate: Couldnt change speed due to: {stderr}')
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



# paulstretch
# https://github.com/paulnasca/paulstretch_python/
def load_wav(audio_path):
    import numpy
    import scipy.io.wavfile
    try:
        wavedata = scipy.io.wavfile.read(str(audio_path))
    except:
        return print_red(f'Error loading wav: {audio_path}, stacktrace: {get_stack_trace()}')
    
    samplerate=int(wavedata[0])
    sample_from_wavedata = wavedata[1] * (1.0 / 32768.0)
    sample_from_wavedata = sample_from_wavedata.transpose()
    if len(sample_from_wavedata.shape) == 1: #convert to stereo
        sample_from_wavedata = numpy.tile(sample_from_wavedata, (2, 1))
    return (samplerate, sample_from_wavedata)


# look into this too, has "onset" detection: https://github.com/paulnasca/paulstretch_python/blob/master/paulstretch_newmethod.py
# 1.0 = no strecth
# window size = .25 default
def paulstretch_shared(input_audio_path, speed, windowsize_seconds=.25, output_directory=get_temp_dir(), cache=False):
    input_audio_path = pathlib.Path(input_audio_path)
    stretch = 1 / speed

    if stretch == 1.0 or stretch == 1:
        return input_audio_path
    
    output_audio_path = output_directory.joinpath(f'{input_audio_path.stem}_paulstretch_{stretch}{input_audio_path.suffix}')
    if cache and output_audio_path.exists():
        return output_audio_path

    import wave
    import numpy

    wav_path = convert_to_wav(input_audio_path, output_directory, cache=cache)
    samplerate, smp = load_wav(wav_path)
    nchannels = smp.shape[0]

    temp_wav_output_path = output_audio_path.with_suffix('.wav')
    print(f'paulstretch: wav file will use {temp_wav_output_path}')
    outfile = wave.open(str(temp_wav_output_path), 'wb')
    outfile.setsampwidth(2)
    outfile.setframerate(samplerate)
    outfile.setnchannels(nchannels)

    # make sure that windowsize is even and larger than 16
    windowsize=int(windowsize_seconds * samplerate)
    if windowsize<16:
        windowsize=16
    def optimize_windowsize(n):
        orig_n=n
        while True:
            n=orig_n
            while (n%2)==0:
                n/=2
            while (n%3)==0:
                n/=3
            while (n%5)==0:
                n/=5
            if n<2:
                break
            orig_n+=1
        return orig_n
    windowsize=optimize_windowsize(windowsize)
    windowsize=int(windowsize/2)*2
    half_windowsize=int(windowsize/2)
    print(f'paulstretch: Using windowsize of {windowsize}')

    #correct the end of the smp
    nsamples=smp.shape[1]
    end_size=int(samplerate*0.05)
    if end_size<16:
        end_size=16

    smp[:,nsamples-end_size:nsamples]*=numpy.linspace(1,0,end_size)

    
    #compute the displacement inside the input file
    start_pos=0.0
    displace_pos=(windowsize*0.5)/stretch
    return stretch, windowsize, half_windowsize, smp, output_directory, temp_wav_output_path, outfile, nchannels, nsamples, start_pos, displace_pos


def paulstretch_stereo(input_audio_path, speed, windowsize_seconds=.25, output_directory=get_temp_dir(), cache=False):
    import numpy
    stretch, windowsize, half_windowsize, smp, output_directory, temp_wav_output_path, outfile, nchannels, nsamples, start_pos, displace_pos = paulstretch_shared(input_audio_path, speed, windowsize_seconds=windowsize_seconds, output_directory=output_directory, cache=cache)

    #create Window window
#    window=0.5-cos(arange(windowsize,dtype='float')*2.0*pi/(windowsize-1))*0.5
    window=pow(1.0-pow(numpy.linspace(-1.0,1.0,windowsize),2.0),1.25)

    old_windowed_buf=numpy.zeros((2,windowsize))
#    hinv_sqrt2=(1+sqrt(0.5))*0.5
#    hinv_buf=2.0*(hinv_sqrt2-(1.0-hinv_sqrt2)*cos(arange(half_windowsize,dtype='float')*2.0*pi/half_windowsize))/hinv_sqrt2

    while True:
        #get the windowed buffer
        istart_pos=int(numpy.floor(start_pos))
        buf=smp[:,istart_pos:istart_pos+windowsize]
        if buf.shape[1]<windowsize:
            buf=numpy.append(buf,numpy.zeros((2,windowsize-buf.shape[1])),1)
        buf=buf*window
    
        #get the amplitudes of the frequency components and discard the phases
        freqs=abs(numpy.fft.rfft(buf))

        #randomize the phases by multiplication with a random complex number with modulus=1
        ph=numpy.random.uniform(0,2*numpy.pi,(nchannels,freqs.shape[1]))*1j
        freqs=freqs*numpy.exp(ph)

        #do the inverse FFT 
        buf=numpy.fft.irfft(freqs)

        #window again the output buffer
        buf*=window

        #overlap-add the output
        output=buf[:,0:half_windowsize]+old_windowed_buf[:,half_windowsize:windowsize]
        old_windowed_buf=buf

        #remove the resulted amplitude modulation
        #update: there is no need to the new windowing function
        #output*=hinv_buf
        
        #clamp the values to -1..1 
        output[output>1.0]=1.0
        output[output<-1.0]=-1.0

        #write the output to wav file
        outfile.writeframes(numpy.int16(output.ravel('F')*32767.0).tostring())

        start_pos+=displace_pos
        if start_pos>=nsamples:
            print ("100 %")
            break
        sys.stdout.write ("%d %% \r" % int(100.0*start_pos/nsamples))
        sys.stdout.flush()
    outfile.close()
    mp3_path = convert_to_mp3(temp_wav_output_path, output_directory, cache=False)
    return mp3_path


# onset_level: (0.0=max,1.0=min)",type="float",default=10.0)
def paulstretch_new_method_onset(input_audio_path, speed, windowsize_seconds=.25, onset_level=10.0, output_directory=get_temp_dir(), cache=False):
    import numpy
    stretch, windowsize, half_windowsize, smp, output_directory, temp_wav_output_path, outfile, nchannels, nsamples, start_pos, displace_pos = paulstretch_shared(input_audio_path, speed, windowsize_seconds=windowsize_seconds, output_directory=output_directory, cache=cache)
    #create Hann window
    window=0.5-numpy.cos(numpy.arange(windowsize,dtype='float')*2.0*numpy.pi/(windowsize-1))*0.5

    old_windowed_buf=numpy.zeros((2,windowsize))
    hinv_sqrt2=(1+numpy.sqrt(0.5))*0.5
    hinv_buf=2.0*(hinv_sqrt2-(1.0-hinv_sqrt2)*numpy.cos(numpy.arange(half_windowsize,dtype='float')*2.0*numpy.pi/half_windowsize))/hinv_sqrt2

    freqs=numpy.zeros((2,half_windowsize+1))
    old_freqs=freqs

    num_bins_scaled_freq=32
    freqs_scaled=numpy.zeros(num_bins_scaled_freq)
    old_freqs_scaled=freqs_scaled

    displace_tick=0.0
    displace_tick_increase=1.0/stretch
    if displace_tick_increase>1.0:
        displace_tick_increase=1.0
    extra_onset_time_credit=0.0
    get_next_buf=True
    while True:
        if get_next_buf:
            old_freqs=freqs
            old_freqs_scaled=freqs_scaled

            #get the windowed buffer
            istart_pos=int(numpy.floor(start_pos))
            buf=smp[:,istart_pos:istart_pos+windowsize]
            if buf.shape[1]<windowsize:
                buf=numpy.append(buf,numpy.zeros((2,windowsize-buf.shape[1])),1)
            buf=buf*window
    
            #get the amplitudes of the frequency components and discard the phases
            freqs=abs(numpy.fft.rfft(buf))

            #scale down the spectrum to detect onsets
            freqs_len=freqs.shape[1]
            if num_bins_scaled_freq<freqs_len:
                freqs_len_div=freqs_len//num_bins_scaled_freq
                new_freqs_len=freqs_len_div*num_bins_scaled_freq
                freqs_scaled=numpy.mean(numpy.mean(freqs,0)[:new_freqs_len].reshape([num_bins_scaled_freq,freqs_len_div]),1)
            else:
                freqs_scaled=numpy.zeros(num_bins_scaled_freq)


            #process onsets
            m=2.0*numpy.mean(freqs_scaled-old_freqs_scaled)/(numpy.mean(abs(old_freqs_scaled))+1e-3)
            if m<0.0:
                m=0.0
            if m>1.0:
                m=1.0
            if m>onset_level:
                displace_tick=1.0
                extra_onset_time_credit+=1.0

        cfreqs=(freqs*displace_tick)+(old_freqs*(1.0-displace_tick))

        #randomize the phases by multiplication with a random complex number with modulus=1
        ph=numpy.random.uniform(0,2*numpy.pi,(nchannels,cfreqs.shape[1]))*1j
        cfreqs=cfreqs*numpy.exp(ph)

        #do the inverse FFT 
        buf=numpy.fft.irfft(cfreqs)

        #window again the output buffer
        buf*=window

        #overlap-add the output
        output=buf[:,0:half_windowsize]+old_windowed_buf[:,half_windowsize:windowsize]
        old_windowed_buf=buf

        #remove the resulted amplitude modulation
        output*=hinv_buf
        
        #clamp the values to -1..1 
        output[output>1.0]=1.0
        output[output<-1.0]=-1.0

        #write the output to wav file
        outfile.writeframes(numpy.int16(output.ravel('F')*32767.0).tostring())

        if get_next_buf:
            start_pos+=displace_pos

        get_next_buf=False

        if start_pos>=nsamples:
            print ("100 %")
            break
        sys.stdout.write ("%d %% \r" % int(100.0*start_pos/nsamples))
        sys.stdout.flush()

        
        if extra_onset_time_credit<=0.0:
            displace_tick+=displace_tick_increase
        else:
            credit_get=0.5*displace_tick_increase #this must be less than displace_tick_increase
            extra_onset_time_credit-=credit_get
            if extra_onset_time_credit<0:
                extra_onset_time_credit=0
            displace_tick+=displace_tick_increase-credit_get

        if displace_tick>=1.0:
            displace_tick=displace_tick % 1.0
            get_next_buf=True
    outfile.close()
    mp3_path = convert_to_mp3(temp_wav_output_path, output_directory, cache=False)
    return mp3_path