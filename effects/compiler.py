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
from PIL import Image

import grid_helpers
from helpers import *

useful_attrs = set([
    'text',
])
class GridInfo:
    def __init__(self):
        self.grid_function = None

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




# ==== eric and andrews transformation matrix stuff


def get_rectangle_numpy(width, height, color=(100, 100, 100)):
    rectangle = np.array(np.zeros((grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT, 3)), np.double)

    mid_x = (grid_helpers.GRID_WIDTH - 1) / 2
    mid_y = (grid_helpers.GRID_HEIGHT - 1) / 2
    
    start_x = int(mid_x - width / 2)
    start_y = int(mid_y - height / 2)
    for x in range(width):
        for y in range(height):
            rectangle[x + start_x][y + start_y] = color
    return rectangle




def interpolate_float(f1, f2, percent_done):
    return (1 - percent_done) * f1 + percent_done * f2


def interpolate_int(i1, i2, percent_done):
    interpolated_float = interpolate_float(i1, i2, percent_done)
    return round(interpolated_float)


# v1: (-2, 4) # v2: (3, 1)  # percent_done: 0-1
def interpolate_vectors_float(v1, v2, percent_done):
    return tuple((1 - percent_done) * v1[i] + percent_done * v2[i] for i in range(len(v1)))


def interpolate_vectors_int(v1, v2, percent_done):
    mids = interpolate_vectors_float(v1, v2, percent_done)
    return tuple(map(round, mids))



def create_transform_matrix(midpoint, scale, rot, pos):
    # Step 1: Translate midpoint to (0, 0)
    tx1 = -midpoint[0]
    ty1 = -midpoint[1]
    # tx1 = -midpoint[0]
    # ty1 = -midpoint[1]

    # Step 2: Rotate & Scale
    # Convert degrees to radians and negate it due to PIL's coordinate system
    rot_rad = -rot
    a = scale[0]*np.cos(rot_rad)
    b = -scale[0]*np.sin(rot_rad)
    d = scale[1]*np.sin(rot_rad)
    e = scale[1]*np.cos(rot_rad)

    # Step 3: Translate back the (0, 0) to the midpoint
    tx2 = midpoint[0] + pos[0]
    ty2 = midpoint[1] + pos[1]
    return [
        a, b, a*tx1 + b*ty1 + tx2,
        d, e, d*tx1 + e*ty1 + ty2
    ]


def scale_rotate_matrix(midpoint, scale, rot):
    # Step 1: Translate midpoint to (0, 0)
    tx1 = -midpoint[0]
    ty1 = -midpoint[1]

    # Step 2: Rotate & Scale
    rot_rad = -rot
    a = scale[0]*np.cos(rot_rad)
    b = -scale[0]*np.sin(rot_rad)
    d = scale[1]*np.sin(rot_rad)
    e = scale[1]*np.cos(rot_rad)

    # Step 3: Translate back the (0, 0) to the midpoint
    tx2 = midpoint[0]
    ty2 = midpoint[1]
    return [
        a, b, a*tx1 + b*ty1 + tx2,
        d, e, d*tx1 + e*ty1 + ty2
    ]


def transform_scale_rotation_and_translation(object_image, size, midpoint, scale, rot, pos):
    scale_rot_matrix = create_transform_matrix(midpoint, scale, rot, (0, 0))
    between = object_image.transform(size, Image.AFFINE, scale_rot_matrix, Image.NEAREST)
    translation_matrix = create_transform_matrix(midpoint, (1, 1), 0, pos)
    return between.transform(size, Image.AFFINE, translation_matrix, Image.NEAREST)


def load_object(info):
    if isinstance(info.object, str): # is a previous object
        info.name = info.object
        if info.name not in object_memory:
            raise Exception(f'object name "{info.name}" not found in memory')
        info.object, (loaded_pos, loaded_scale, loaded_rot) = object_memory[info.name]

        info.start_pos = getattr(info, 'start_pos', loaded_pos)
        info.start_scale = getattr(info, 'start_scale', loaded_scale)
        info.start_rot = getattr(info, 'start_rot', loaded_rot)

        info.end_pos = getattr(info, 'end_pos', info.start_pos)
        info.end_scale = getattr(info, 'end_scale', info.start_scale)
        info.end_rot = getattr(info, 'end_rot', info.start_rot)

        object_memory[info.name][1] = (info.end_pos, info.end_scale, info.end_rot)
        # print_blue(f'object name "{info.name}" found in memory, loading {info.start_pos, info.start_scale, info.start_rot=}, {info.end_pos, info.end_scale, info.end_rot=}\n' * 3)
    else:
        info.start_pos = getattr(info, 'start_pos', (0, 0))
        info.start_scale = getattr(info, 'start_scale', (1, 1))
        info.start_rot = getattr(info, 'start_rot', 0)

        info.end_pos = getattr(info, 'end_pos', info.start_pos)
        info.end_scale = getattr(info, 'end_scale', info.start_scale)
        info.end_rot = getattr(info, 'end_rot', info.start_rot)
        if isinstance(info.object, np.ndarray): # is a numpy array            
            object_as_uint8 = info.object.astype(np.uint8)
            object_image = Image.fromarray(object_as_uint8)
            # object_image.save('temp/test.png')
            # print('temp/test.png')
            if getattr(info, 'name', None) is not None:
                object_memory[info.name] = [object_image, (info.end_pos, info.end_scale, info.end_rot)]
            info.object = object_image
        elif isinstance(info.object, Image.Image): # is a PIL image
            object_image = info.object
            # print(f'object is pillow. using {info.start_pos, info.start_scale, info.start_rot=}, {info.end_pos, info.end_scale, info.end_rot=}\n' * 3)
        else:
            raise Exception(f'object type "{type(info.object)}" not supported')


object_memory = {}
@profile
def our_transform(info):
    load_object(info)

    # by this point info.object is a pillow image and start_'s end_'s all are set
    percent_done = info.curr_sub_beat / info.length
    pos = interpolate_vectors_float(info.start_pos, info.end_pos, percent_done)
    scale = interpolate_vectors_float(info.start_scale, info.end_scale, percent_done)
    rot = interpolate_float(info.start_rot, info.end_rot, percent_done)

    size = info.object.size

    # why is this seemingly backwards???
    midpoint = ((grid_helpers.GRID_HEIGHT - 1) / 2, (grid_helpers.GRID_WIDTH - 1) / 2)

    transformed_image = transform_scale_rotation_and_translation(info.object, size, midpoint, scale, rot, pos)
    # print(f'{pos=}, {scale=}, {rot=}, {info.object.size=}, {transformed_image.size=}\n' * 10)

    # !TODO this is rly bad
    arr_version = np.array(transformed_image)
    normalizedData = (arr_version-np.min(arr_version))/(np.max(arr_version)-np.min(arr_version)) * 100

    grid_helpers.grid = normalizedData
    




# ==== info effects ====

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


def grid_visualizer(info):
    grid_helpers.reset()
    # spectogram = get_whole_spectogram_aubio(info.song_path)
    spectogram = get_whole_spectogram_librosa(info.song_path)
    spectogram_at_time = spectogram[info.curr_sub_beat]
    
    if getattr(info, 'flip', None):
        for y in range(grid_helpers.GRID_HEIGHT):
            for x in range(spectogram_at_time[(grid_helpers.GRID_HEIGHT - 1) - y]):
                grid_helpers.grid[x][y] = info.color
    else:
        for y in range(grid_helpers.GRID_HEIGHT):
            for x in range(spectogram_at_time[y]):
                grid_helpers.grid[x][y] = info.color


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


def move_until_y_occupy(info):
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1
    if info.curr_sub_beat % info.beat_divide == 0:
        for vector in get_smallest_equivilent_vectors(info.vector):
            for x in range(grid_helpers.GRID_WIDTH):
                if grid_helpers.grid[x][info.y].any():
                    return
            grid_helpers.move(vector)


def clear_grid(info):
    grid_helpers.reset()

def spawn_row_then_move(info):
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1

    if info.curr_sub_beat == 0:
        if getattr(info, 'clear', None):
            grid_helpers.reset()
        info.last_y = None
    
    if not (0 <= info.y < grid_helpers.GRID_HEIGHT):
        if getattr(info, 'bounce', None):
            info.vector = (-info.vector[0], -info.vector[1])
            info.y = max(0, min(info.y, grid_helpers.GRID_HEIGHT - 1))
        else:
            if getattr(info, 'stop_at_edge', None):
                return
            if info.last_y is not None:
                add_color_row(info.last_y, list(map(lambda i: -i, info.color)))
                info.last_y = None
            return

    if info.curr_sub_beat % info.beat_divide == 0:
        if info.last_y is not None:
            add_color_row(info.last_y, list(map(lambda i: -i, info.color)))
        info.last_y = info.y
        add_color_row(info.y, info.color)
        info.y += info.vector[1]


def spawn_col_then_move(info):
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1

    if info.curr_sub_beat == 0:
        if getattr(info, 'clear', None):
            grid_helpers.reset()
        info.last_x = None
    
    if not (0 <= info.x < grid_helpers.GRID_WIDTH):
        if getattr(info, 'bounce', None):
            info.vector = (-info.vector[0], -info.vector[1])
            info.x = max(0, min(info.x, grid_helpers.GRID_WIDTH - 1))
        else:
            if getattr(info, 'stop_at_edge', None):
                return
            if info.last_x is not None:
                add_color_col(info.last_x, list(map(lambda i: -i, info.color)))
                info.last_x = None
            return

    if info.curr_sub_beat % info.beat_divide == 0:
        if info.last_x is not None:
            add_color_col(info.last_x, list(map(lambda i: -i, info.color)))
        info.last_x = info.x
        add_color_col(info.x, info.color)
        info.x += info.vector[0]


def add_color_row(y, rgb):
    for x in range(grid_helpers.GRID_WIDTH):
        grid_helpers.grid[x][y] = np.clip(grid_helpers.grid[x][y] + rgb, a_min=0, a_max=100)

def add_color_col(x, rgb):
    for y in range(grid_helpers.GRID_HEIGHT):
        grid_helpers.grid[x][y] = np.clip(grid_helpers.grid[x][y] + rgb, a_min=0, a_max=100)


def move_grid(info):
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1
    if info.curr_sub_beat % info.beat_divide == 0:
        if info.wrap:
            grid_helpers.move_wrap(info.vector)
        else:
            grid_helpers.move(info.vector)


def spawn_row(info):
    if getattr(info, 'clear', None):
        grid_helpers.reset()
    for x in range(grid_helpers.GRID_WIDTH):
        grid_helpers.grid[x][info.y] = info.color


def spawn_col(info):
    if getattr(info, 'clear', None):
        grid_helpers.reset()
    for y in range(grid_helpers.GRID_HEIGHT):
        grid_helpers.grid[info.x][y] = info.color


# === image, animation and text info effects ===
this_file_directory = pathlib.Path(__file__).parent.resolve()
directory_above_this_file = this_file_directory.parent.resolve()
def fill_grid_from_image_filepath(info):
    from light_server import SUB_BEATS
    # print(f'GridInfo: {info.all_attr_values()}')

    bpm = info.bpm
    curr_beat = info.curr_sub_beat / SUB_BEATS

    relative_beat = info.length - curr_beat

    time_in_pattern = relative_beat * (60 / bpm)

    dimensions = (grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT)
    if info.rotate_90:
        dimensions = (dimensions[1], dimensions[0])

    cached_filepath = grid_helpers.get_cached_converted_filepath(info.filename, dimensions, use_cache=False)
    if grid_helpers.is_animated(cached_filepath):
        grid_helpers.seek_to_animation_time(cached_filepath, time_in_pattern)
    grid_helpers.fill_grid_from_image_filepath(cached_filepath, rotate_90=info.rotate_90)


def fill_grid_from_text(info):
    filepath = grid_helpers.create_image_from_text_pilmoji(info.text, font_size=info.font_size, rotate_90=info.rotate_90, use_cache=False)    
    grid_helpers.fill_grid_from_image_filepath(filepath, rotate_90=info.rotate_90)


def grid_f(start_beat=None, length=None, function=None, filename=None, rotate_90=None, text=None, font_size=12, **kwargs):
    info = GridInfo()
    if filename is not None:
        info.filename = filename
        info.rotate_90 = rotate_90
        function = fill_grid_from_image_filepath

    if text is not None:
        info.text = text
        info.font_size = font_size
        info.rotate_90 = rotate_90
        function = fill_grid_from_text

    if function is None:
        print_red(f'function is None, filename: {filename}, text: {text}')
        exit()
    info.grid_function = function
    info.length = length
    if kwargs:
        for key, value in kwargs.items():
            setattr(info, key, value)
    return [start_beat, info, length]



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
