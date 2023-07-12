# start_beat: this is the beat that the pattern will start on
# effect_name: this is the effect that will play
# len: the length in beats
# offset: how many beats in to skip to in the pattern
# hue_shift: -1 - 1
# sat_shift: -1 - 1
# bright_shift: -1 - 1
# rgb: 0 - 100
# green laser: 0 - 100
# red laser: 0 - 100
# laser motor: 0 - 100

import pathlib
import time
import sys

import numpy as np

import grid_helpers
from helpers import *

useful_attrs = set([
    'text',
])
class GridInfo:
    def __init__(self):
        self.grid_function = None
        self.grid_skip_top_fill = False

    def reset(self):
        pass

    def all_attr_values(self):
        building = []
        for attr, value in self.__dict__.items():
            building.append(f'{attr}: {value}')
        return ', '.join(building)
    
    def __repr__(self):
        building = []
        for attr, value in self.__dict__.items():
            if attr not in useful_attrs:
                continue
            building.append(f'{attr}: {value}')
        
        return f'GridInfo({self.grid_function.__name__}, attrs: {", ".join(building)})'



# ==== grid_info effects ====

spectogram_cache = {}
# this is part of the reason load slow is bad
# https://librosa.org/blog/2019/07/17/resample-on-load/
def get_whole_spectogram_librosa(filepath, size=(20, 32), times_a_second=1/48):
    import librosa
    the_hash = (filepath, size, times_a_second)
    if the_hash not in spectogram_cache:
        start_time_specto = time.time()
        y, sr = librosa.load(filepath, sr=48000)
        print_cyan(f'loaded {filepath} in {time.time() - start_time_specto} seconds')
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=size[1], hop_length=int(sr * times_a_second))
        S_db = librosa.power_to_db(S, ref=np.max)
        S_db_norm = np.interp(S_db, (S_db.min(), S_db.max()), (0, size[0] - 1))
        spectogram_cache[the_hash] = S_db_norm.T
        spectogram_cache[the_hash] = spectogram_cache[the_hash].astype(int)
        print_cyan(f'computed spectogram for {filepath} in {time.time() - start_time_specto} seconds')
    return spectogram_cache[the_hash]


# idk this code just doesn't work
def get_whole_spectogram_aubio(filepath, size=(20, 32), times_a_second=1/48):
    import aubio
    the_hash = (filepath, size, times_a_second)
    # frequency bins is 32
    if the_hash not in spectogram_cache:
        start_time_specto = time.time()
    
        sr = 48000
        win_size = 512 # fft size
        hop_size = win_size // 2 # hop size
        
        try:
            src = aubio.source(str(filepath), 0, hop_size)
        except:
            print_red(f'failed to load {filepath} with aubio')
            return
        print(f'loaded {filepath} in {time.time() - start_time_specto} seconds')

        n_filters = size[1]
        n_coeffs = size[1]

        pv = aubio.pvoc(win_size, hop_size)
        f = aubio.filterbank(n_coeffs, win_size)
        f.set_mel_coeffs_slaney(sr)

        S = []
        total_frames = 0
        while True:
            samples, read = src()
            specgram = pv(samples)
            mfcc_bands = f(specgram)
            S.append(mfcc_bands)
            total_frames += read
            if read < hop_size:
                break

        S = np.array(S).T
        S_db = 20 * np.log10(S / np.max(S))
        S_db_norm = np.interp(S_db, (S_db.min(), S_db.max()), (0, size[0]))

        spectogram_cache[the_hash] = S_db_norm.T.astype(int)
        print(f'computed spectogram for {filepath} in {time.time() - start_time_specto} seconds')
        print(spectogram_cache[the_hash].shape)
    return spectogram_cache[the_hash]


def grid_visualizer(grid_info):
    grid_helpers.reset()
    # spectogram = get_whole_spectogram_aubio(grid_info.song_path)
    spectogram = get_whole_spectogram_librosa(grid_info.song_path)
    spectogram_at_time = spectogram[grid_info.curr_sub_beat]
    
    if getattr(grid_info, 'flip', None):
        for y in range(grid_helpers.GRID_HEIGHT):
            for x in range(spectogram_at_time[(grid_helpers.GRID_HEIGHT - 1) - y]):
                grid_helpers.grid[x][y] = grid_info.color
    else:
        for y in range(grid_helpers.GRID_HEIGHT):
            for x in range(spectogram_at_time[y]):
                grid_helpers.grid[x][y] = grid_info.color


def get_smallest_equivilent_vectors(vector):
    all_vectors = []
    sign_x = 1 if vector[0] > 0 else -1
    sign_y = 1 if vector[1] > 0 else -1
    needed_x, needed_y = list(map(abs, vector))
    for _ in range(max(needed_x, needed_y)):
        should_x = sign_x if needed_x > 0 else 0
        should_y = sign_y if needed_y > 0 else 0
        all_vectors.append((should_x, should_y))
        needed_x -= should_x
        needed_y -= should_y
    return all_vectors


def move_until_y_occupy(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1
    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        for vector in get_smallest_equivilent_vectors(grid_info.vector):
            for x in range(grid_helpers.GRID_WIDTH):
                if grid_helpers.grid[x][grid_info.y].any():
                    return
            grid_helpers.move(vector)


def clear_grid(grid_info):
    grid_helpers.reset()

def spawn_row_then_move(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1

    if grid_info.curr_sub_beat == 0:
        if getattr(grid_info, 'clear', None):
            grid_helpers.reset()
        grid_info.last_y = None
    
    if not (0 <= grid_info.y < grid_helpers.GRID_HEIGHT):
        if getattr(grid_info, 'bounce', None):
            grid_info.vector = (-grid_info.vector[0], -grid_info.vector[1])
            grid_info.y = max(0, min(grid_info.y, grid_helpers.GRID_HEIGHT - 1))
        else:
            if getattr(grid_info, 'stop_at_edge', None):
                return
            if grid_info.last_y is not None:
                add_color_row(grid_info.last_y, list(map(lambda i: -i, grid_info.color)))
                grid_info.last_y = None
            return

    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        if grid_info.last_y is not None:
            add_color_row(grid_info.last_y, list(map(lambda i: -i, grid_info.color)))
        grid_info.last_y = grid_info.y
        add_color_row(grid_info.y, grid_info.color)
        grid_info.y += grid_info.vector[1]


def spawn_col_then_move(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1

    if grid_info.curr_sub_beat == 0:
        if getattr(grid_info, 'clear', None):
            grid_helpers.reset()
        grid_info.last_x = None
    
    if not (0 <= grid_info.x < grid_helpers.GRID_WIDTH):
        if getattr(grid_info, 'bounce', None):
            grid_info.vector = (-grid_info.vector[0], -grid_info.vector[1])
            grid_info.x = max(0, min(grid_info.x, grid_helpers.GRID_WIDTH - 1))
        else:
            if getattr(grid_info, 'stop_at_edge', None):
                return
            if grid_info.last_x is not None:
                add_color_col(grid_info.last_x, list(map(lambda i: -i, grid_info.color)))
                grid_info.last_x = None
            return

    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        if grid_info.last_x is not None:
            add_color_col(grid_info.last_x, list(map(lambda i: -i, grid_info.color)))
        grid_info.last_x = grid_info.x
        add_color_col(grid_info.x, grid_info.color)
        grid_info.x += grid_info.vector[0]


def add_color_row(y, rgb):
    for x in range(grid_helpers.GRID_WIDTH):
        grid_helpers.grid[x][y] = np.clip(grid_helpers.grid[x][y] + rgb, a_min=0, a_max=100)

def add_color_col(x, rgb):
    for y in range(grid_helpers.GRID_HEIGHT):
        grid_helpers.grid[x][y] = np.clip(grid_helpers.grid[x][y] + rgb, a_min=0, a_max=100)


def move_grid(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1
    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        if grid_info.wrap:
            grid_helpers.move_wrap(grid_info.vector)
        else:
            grid_helpers.move(grid_info.vector)


def spawn_row(grid_info):
    if getattr(grid_info, 'clear', None):
        grid_helpers.reset()
    for x in range(grid_helpers.GRID_WIDTH):
        grid_helpers.grid[x][grid_info.y] = grid_info.color


def spawn_col(grid_info):
    if getattr(grid_info, 'clear', None):
        grid_helpers.reset()
    for y in range(grid_helpers.GRID_HEIGHT):
        grid_helpers.grid[grid_info.x][y] = grid_info.color


# === image, animation and text grid_info effects ===
this_file_directory = pathlib.Path(__file__).parent.resolve()
directory_above_this_file = this_file_directory.parent.resolve()
def fill_grid_from_image_filepath(grid_info):
    from light_server import SUB_BEATS
    # print(f'GridInfo: {grid_info.all_attr_values()}')

    bpm = grid_info.bpm
    curr_beat = grid_info.curr_sub_beat / SUB_BEATS

    relative_beat = grid_info.length - curr_beat

    time_in_pattern = relative_beat * (60 / bpm)

    dimensions = (grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT)
    if grid_info.rotate_90:
        dimensions = (dimensions[1], dimensions[0])

    cached_filepath = grid_helpers.get_cached_converted_filepath(grid_info.filename, dimensions, use_cache=False)
    if grid_helpers.is_animated(cached_filepath):
        grid_helpers.seek_to_animation_time(cached_filepath, time_in_pattern)
    grid_helpers.fill_grid_from_image_filepath(cached_filepath, rotate_90=grid_info.rotate_90)


def fill_grid_from_text(grid_info):
    filepath = grid_helpers.create_image_from_text_pilmoji(grid_info.text, font_size=grid_info.font_size, rotate_90=grid_info.rotate_90, use_cache=False)    
    grid_helpers.fill_grid_from_image_filepath(filepath, rotate_90=grid_info.rotate_90)


def grid_f(start_beat=None, length=None, function=None, filename=None, rotate_90=None, text=None, font_size=12, **kwargs):
    grid_info = GridInfo()
    if filename is not None:
        grid_info.filename = filename
        grid_info.rotate_90 = rotate_90
        function = fill_grid_from_image_filepath

    if text is not None:
        grid_info.text = text
        grid_info.font_size = font_size
        grid_info.rotate_90 = rotate_90
        function = fill_grid_from_text

    if function is None:
        print_red(f'function is None, filename: {filename}, text: {text}')
        exit()
    grid_info.grid_function = function
    grid_info.length = length
    if kwargs:
        for key, value in kwargs.items():
            setattr(grid_info, key, value)
    return [start_beat, grid_info, length]



following_beat = None
def b(start_beat=None, name=None, length=None, intensity=None, offset=None, hue_shift=None, sat_shift=None, bright_shift=None, top_rgb=None, front_rgb=None, back_rgb=None, bottom_rgb=None, uv=None, green_laser=None, red_laser=None, laser_motor=None, disco_rgb=None, grid_bright_shift=None):
    global following_beat

    if length is None:
        raise Exception('length must be defined')

    if start_beat is None:
        if following_beat is None:
            raise Exception('needed to specify last beat first')
        start_beat = following_beat
    
    following_beat = start_beat + length 

    if (name or intensity or offset or hue_shift or sat_shift or bright_shift) and (disco_rgb or top_rgb or front_rgb or back_rgb or bottom_rgb or uv or green_laser or red_laser or laser_motor):
        raise Exception(f'Anything between the sets "name intensity offset hue_shift sat_shift bright_shift" and "disco_rgb top_rgb front_rgb back_rgb bottom_rgb uv,  green_laser red_laser laser_motor" cannot be used together, dont use them in the same call')
    
    if (back_rgb or front_rgb) and top_rgb:
        raise Exception('Cannot define back_rgb or front_rgb if top_rgb is defined')

    if disco_rgb is None:
        disco_rgb = [0, 0, 0]


    if name is None:
        if top_rgb is None:
            top_rgb = [0, 0, 0]
        if bottom_rgb is None:
            bottom_rgb = [0, 0, 0]
        if uv is None:
            uv = 0
        if green_laser is None:
            green_laser = 0
        if red_laser is None:
            red_laser = 0
        if laser_motor is None:
            laser_motor = 0

        if top_rgb:
            front_rgb = top_rgb
            back_rgb = top_rgb
        channel = back_rgb[:] + front_rgb[:] + bottom_rgb[:] + [uv, green_laser, red_laser, laser_motor] + disco_rgb[:]
        return [start_beat, channel, length]

    if intensity is None:
        intensity = 1

    if type(intensity) == int or type(intensity) == float:
        intensity = (intensity, intensity)

    if offset is None:
        offset = 0

    if hue_shift is None:
        hue_shift = 0

    if sat_shift is None:
        sat_shift = 0

    if bright_shift is None:
        bright_shift = 0
    if grid_bright_shift is None:
        grid_bright_shift = 0

    final = [
        start_beat,
        name,
        length,
    ] + list(intensity[:]) + [
        offset,
        hue_shift,
        sat_shift,
        bright_shift,
        grid_bright_shift,
    ]
    return final


# beat(1, 'porter flubs phrase', length=16, intensity=(1, 1), skip=2, hue_shift=, sat_shift=, bright_shift=),
