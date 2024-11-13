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
import math
import random
from collections import deque
import copy
import joystick_and_keyboard_helpers
import colorsys

import numpy as np
from PIL import Image

import grid_helpers
import winamp.winamp_wrapper
from helpers import *


class GColor:
    negative = (-1000, -1000, -1000)
    white = (100, 100, 100)
    blue = (0, 0, 100)
    seafoam = (0, 100, 50)
    blue_some_green = (0, 30, 100)
    red = (100, 0, 0)
    green = (0, 100, 0)
    purple = (100, 0, 100)
    yellow = (100, 100, 0)
    cyan = (0, 100, 100)
    orange = (100, 50, 0)
    pink = (100, 0, 50)
    light_blue = (0, 50, 100)
    light_green = (50, 100, 0)
    nothing = (0, 0, 0)



useful_attrs = set([
    'text',
])
class GridInfo:
    def __init__(self):
        self.grid_function = None
        self.copy = False

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

grid_copy_for_mask = copy.deepcopy(grid_helpers.grid)
def grid_winamp_mask(grid_info):
    if not grid_helpers.try_setup_winamp():
        print_red(f'Failed to load winamp when args spec, exiting\n' * 10)
        exit()

    if grid_info.curr_sub_beat == 0:
        joystick_and_keyboard_helpers.clear_events()
        
    for event in joystick_and_keyboard_helpers.inputs_since_last_called():
        if event == 'r':
            grid_info.preset = winamp.winamp_wrapper.get_random_preset_path()

    winamp.winamp_wrapper.load_preset(grid_info.preset)
    winamp.winamp_wrapper.compute_frame()
    winamp.winamp_wrapper.load_into_numpy_array(grid_copy_for_mask)

    intensity = getattr(grid_info, 'intensity', 1)

    if type(intensity) not in [list, tuple]:
        start_intensity = intensity
        end_intensity = intensity
    else:
        start_intensity, end_intensity = intensity
    current_intensity = interpolate_float(start_intensity, end_intensity, grid_info.percent_done)
    
    for x, y in grid_helpers.coords():
        if grid_helpers.grid[x][y].any():
            grid_helpers.grid[x][y] = scale_vector(grid_copy_for_mask[x][y], current_intensity)


def randomize_preset_on_object(grid_info):
    grid_info.bobby_jones.preset = winamp.winamp_wrapper.get_random_preset_path()


# relies on there being a named object in our_transform (i think not comprehensive enough)
# def sidechain_grid_shape(grid_info):
#     intensity = getattr(grid_info, 'intensity', 1)

#     if type(intensity) not in [list, tuple]:
#         start_intensity = intensity
#         end_intensity = intensity
#     else:
#         start_intensity, end_intensity = intensity
    
#     current_intensity = interpolate_float(start_intensity, end_intensity, grid_info.percent_done)
    
#     curr_object_box = cached_by_name_last_arr[grid_info.name]
#     for x, y in grid_helpers.coords():
#         if not curr_object_box[x][y].any():
#             grid_helpers.grid[x][y] = scale_vector(grid_helpers.grid[x][y], 1 - current_intensity)


def sidechain_grid(grid_info):
    intensity = getattr(grid_info, 'intensity', 1)

    if type(intensity) not in [list, tuple]:
        start_intensity = intensity
        end_intensity = intensity
    else:
        start_intensity, end_intensity = intensity
    
    current_intensity = interpolate_float(start_intensity, end_intensity, grid_info.percent_done)    
    for x, y in grid_helpers.coords():
        grid_helpers.grid[x][y] = scale_vector(grid_helpers.grid[x][y], current_intensity)


def twinkle(grid_info):
    num_twinkles = getattr(grid_info, 'num_twinkles', 40)
    twinkle_length = getattr(grid_info, 'twinkle_length', 1)
    twinkle_lower_wait = getattr(grid_info, 'twinkle_lower_wait', 1)
    twinkle_upper_wait = getattr(grid_info, 'twinkle_upper_wait', 4)
    overall_color = getattr(grid_info, 'color', GColor.green)
    if getattr(grid_info, 'twinkles', None) is None or (grid_info.curr_sub_beat == 0 and not grid_info.looped):
        grid_info.twinkles = [None] * num_twinkles
        for index in range(len(grid_info.twinkles)):
            grid_info.twinkles[index] = time.time() + (random.random() * (twinkle_upper_wait - twinkle_lower_wait))

    for index, state_or_next_time in enumerate(grid_info.twinkles):
        if isinstance(state_or_next_time, float):
            if time.time() < state_or_next_time:
                continue

            new_x, new_y = grid_helpers.random_coord()
            grid_info.twinkles[index] = (new_x, new_y, time.time(), twinkle_length)
        
        curr_x, curr_y, curr_start_time, curr_length = grid_info.twinkles[index]

        percent_done = (time.time() - curr_start_time) / curr_length
        if percent_done > 1:
            grid_info.twinkles[index] = time.time() + twinkle_lower_wait + (random.random() * twinkle_upper_wait)
            continue

        percent_done * 2
        if percent_done <= .5:
            interpol_color = interpolate_vectors_float((0, 0, 0), overall_color, percent_done * 2)
        else:
            interpol_color = interpolate_vectors_float(overall_color, (0, 0, 0), (percent_done * 2) - 1)
        grid_helpers.grid[curr_x][curr_y] += interpol_color




def bounce_line_y(grid_info):
    if getattr(grid_info, 'curr_y', None) is None:
        grid_info.curr_y = 0

    if getattr(grid_info, 'color', None) is None:
        grid_info.color = GColor.light_green

    if getattr(grid_info, 'dir', None) is None:
        grid_info.dir = 1

    speed = getattr(grid_info, 'speed', 1)

    if (grid_info.curr_sub_beat + getattr(grid_info, 'sub_beat_offset', 0)) % 48 == 0:
        if grid_info.curr_y == grid_helpers.GRID_HEIGHT - 1:
            grid_info.dir = -1
        else:
            grid_info.dir = 1

    # if grid_info.curr_sub_beat % speed == 0:
    grid_info.curr_y += grid_info.dir * speed
    if grid_info.curr_y < 0:
        grid_info.curr_y = 0
    if grid_info.curr_y >= grid_helpers.GRID_HEIGHT:
        grid_info.curr_y = grid_helpers.GRID_HEIGHT - 1

    for x in range(0, grid_helpers.GRID_WIDTH):
        grid_helpers.grid[x][grid_info.curr_y] = grid_info.color


def bounce_line_x(grid_info):
    if getattr(grid_info, 'curr_x', None) is None:
        grid_info.curr_x = 0

    if getattr(grid_info, 'color', None) is None:
        grid_info.color = GColor.light_green

    if getattr(grid_info, 'dir', None) is None:
        grid_info.dir = 1

    speed = int(1 / getattr(grid_info, 'speed', 1))

    if grid_info.curr_sub_beat % 48 == 0:
        if grid_info.curr_x == grid_helpers.GRID_WIDTH - 1:
            grid_info.dir = -1
        else:
            grid_info.dir = 1

    if grid_info.curr_sub_beat % speed == 0:
        grid_info.curr_x += grid_info.dir * 2
        if grid_info.curr_x < 0:
            grid_info.curr_x = 0
        if grid_info.curr_x >= grid_helpers.GRID_WIDTH:
            grid_info.curr_x = grid_helpers.GRID_WIDTH - 1

        for y in range(0, grid_helpers.GRID_HEIGHT):
            grid_helpers.grid[grid_info.curr_x][y] = grid_info.color


# !TODO fix so first cycle isn't bad if upper and lower are too close
def make_twinkle(start_beat=1, length=1, color=GColor.white, twinkle_length=1, num_twinkles=20, twinkle_lower_wait=1, twinkle_upper_wait=4):
    return [grid_f(
        start_beat,
        function=twinkle,
        color=color,
        num_twinkles=num_twinkles,
        twinkle_lower_wait=twinkle_lower_wait,
        twinkle_upper_wait=twinkle_upper_wait, 
        twinkle_length=twinkle_length,
        length=length,
    )]

def get_circle_pulse_beats(start_beat=1, start_color=GColor.white, end_color=None, total=20, reverse=False, length=10):
    if end_color is None:
        end_color = start_color
    arr = []
    to_iter = list(range(total))
    if reverse:
        to_iter = reversed(to_iter)
    for index, i in enumerate(to_iter):
        before_color = interpolate_vectors_float(start_color, end_color, i / total)
        after_color = interpolate_vectors_float(start_color, end_color, (i+1) / total)
        arr.append(grid_f(
            start_beat + (index / length),
            function=our_transform,
            object=get_centered_circle_numpy_nofill(radius=(i+1)),
            start_color=before_color,
            end_color=after_color,
            length=1/length,
        ))
    return arr






def get_circle_pulse_beats_new(start_beat=1, start_color=GColor.white, end_color=None, reverse=False, speed=5, steps=20, start_pos=None, start_radius=0):
    if end_color is None:
        end_color = start_color

    arr = []
    inv_speed = 1 / speed
    beats = list(zip([x * inv_speed for x in range(steps)], [inv_speed for x in range(steps)]))
    if reverse:
        beats = reversed(beats)

    for index, (beat_offset, length_of_step) in enumerate(beats):
        before_color = interpolate_vectors_float(start_color, end_color, index / steps)
        after_color = interpolate_vectors_float(start_color, end_color, (index+1) / steps)
        thing = grid_f(
            start_beat + beat_offset,
            function=our_transform,
            object=get_centered_circle_numpy_nofill(radius=(index+1) + start_radius),
            start_color=before_color,
            end_color=after_color,
            length=length_of_step,
        )
        if start_pos is not None:
            thing[1].start_pos = start_pos
        arr.append(thing)
    return arr


def get_circle_pulse_beats_fade(start_beat=1, start_color=GColor.white, end_color=None, reverse=False, speed=5, steps=20):
    if end_color is None:
        end_color = start_color

    arr = []
    inv_speed = 1 / speed
    beats = list(zip([x * inv_speed for x in range(steps)], [inv_speed for x in range(steps)]))
    if reverse:
        beats = reversed(beats)

    for index, (beat_offset, length_of_step) in enumerate(beats):
        before_color = interpolate_vectors_float(start_color, end_color, index / steps)
        after_color = interpolate_vectors_float(start_color, end_color, (index+1) / steps)

        arr.append(grid_f(
            start_beat + beat_offset,
            function=our_transform,
            object=get_centered_circle_numpy_nofill(radius=(index+1)),
            start_color=before_color,
            end_color=after_color,
            length=length_of_step,
        ))
    return arr


# ==== eric and andrews transformation matrix stuff


def get_centered_circle_numpy(radius, offset_x=0, offset_y=0, color=(100, 100, 100)):
    grid_width, grid_height = grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT
    
    circle = np.zeros((grid_width, grid_height, 3), dtype=np.double)

    mid_x = (grid_width // 2) + offset_x
    mid_y = (grid_height // 2) + offset_y

    for x in range(grid_width):
        for y in range(grid_height):
            if (x - mid_x) ** 2 + (y - mid_y) ** 2 <= radius ** 2:
                circle[x][y] = color
    return circle


def random_color():
    b = random.randint(0, 100)
    g = random.randint(0, 100)
    r = random.randint(0, 100)
    return (b, g, r)

def minus_color(color, amt):
    return (max(color[0] - amt, 0), max(color[1] - amt, 0), max(color[2] - amt, 0))

def trail_ball_fade(grid_info):
    if getattr(grid_info, 'pos', None) is None:
        grid_info.pos = grid_helpers.random_coord()
        grid_info.dir = (1 - (random.randint(0, 1) * 2), 1 - (random.randint(0, 1) * 2))
        grid_info.color = random_color()
        grid_info.trail = deque([])


    grid_helpers.grid[grid_info.pos[0]][grid_info.pos[1]] = grid_info.color
    for index, ((p_x, p_y), p_color) in enumerate(grid_info.trail):        
        grid_helpers.grid[p_x][p_y] += p_color

    speed = int(1 / getattr(grid_info, 'speed', 1))
    if grid_info.curr_sub_beat % speed == 0:
        index = 0
        while index < len(grid_info.trail):
            (p_x, p_y), p_color = grid_info.trail[index]
            p_color = minus_color(p_color, 5)
            grid_info.trail[index][1] = p_color
            if p_color == (0, 0, 0) and index == 0:
                grid_info.trail.popleft()
            else:
                index += 1

        x, y = grid_info.pos
        d_x, d_y = grid_info.dir

        if x + d_x < 0 or x + d_x >= grid_helpers.GRID_WIDTH:
            grid_info.dir = (grid_info.dir[0] * -1, grid_info.dir[1])
            d_x *= -1
            grid_info.color = random_color()

        if y + d_y < 0 or y + d_y >= grid_helpers.GRID_HEIGHT:
            grid_info.dir = (grid_info.dir[0], grid_info.dir[1] * -1)
            d_y *= -1
            grid_info.color = random_color()

        grid_info.pos = (x + d_x, y + d_y)
        grid_info.trail.append([grid_info.pos, grid_info.color])



def get_centered_circle_numpy_nofill(radius, offset_x=0, offset_y=0, color=(100, 100, 100)):
    grid_width, grid_height = grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT
    
    circle = np.zeros((grid_width, grid_height, 3), dtype=np.double)

    mid_x = (grid_width // 2) + offset_x
    mid_y = (grid_height // 2) + offset_y

    inner_radius = radius - 1
    for x in range(grid_width):
        for y in range(grid_height):
            distance = (x - mid_x) ** 2 + (y - mid_y) ** 2
            distance = math.sqrt(distance)
            
            if distance <= radius and distance >= inner_radius:
                circle[x][y] = color
    return circle


def get_centered_circle_numpy_fill(radius, offset_x=0, offset_y=0, color=(100, 100, 100)):
    grid_width, grid_height = grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT

    circle = np.zeros((grid_width, grid_height, 3), dtype=np.double)

    mid_x = (grid_width // 2) + offset_x
    mid_y = (grid_height // 2) + offset_y

    for x in range(grid_width):
        for y in range(grid_height):
            distance = math.sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2)

            if distance <= radius:
                circle[x][y] = color
    return circle



def get_down_line_numpy(length, offset_x=0, offset_y=0, color=(100, 100, 100)):
    grid_width, grid_height = grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT
    
    circle = np.zeros((grid_width, grid_height, 3), dtype=np.double)

    mid_x = (grid_width // 2) + offset_x
    mid_y = (grid_height // 2) + offset_y

    for i in range(length):
        circle[mid_x][mid_y + i] = color

    return circle

def get_point_numpy(point, color=(100, 100, 100)):
    rectangle = np.array(np.zeros((grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT, 3)), np.double)

    mid_x = (grid_helpers.GRID_WIDTH - 1) / 2
    mid_y = (grid_helpers.GRID_HEIGHT - 1) / 2
    
    x = int(mid_x - point[0])
    y = int(mid_y - point[1])
    rectangle[x][y] = color
    return rectangle


def get_rectangle_numpy(width, height, color=(100, 100, 100), offset_x=0, offset_y=0):
    rectangle = np.array(np.zeros((grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT, 3)), np.double)

    mid_x = ((grid_helpers.GRID_WIDTH - 1) / 2) + offset_x
    mid_y = ((grid_helpers.GRID_HEIGHT - 1) / 2) + offset_y
    
    start_x = int(mid_x - width / 2)
    start_y = int(mid_y - height / 2)
    for x in range(width):
        for y in range(height):
            rectangle[x + start_x][y + start_y] = color
    return rectangle


def interpolate_float(f1, f2, percent_done):
    return (1 - percent_done) * f1 + percent_done * f2


def interpolate_vectors_float(v1, v2, percent_done):
    return tuple((1 - percent_done) * v1[i] + percent_done * v2[i] for i in range(len(v1)))


# def add_vecc(v1, v2, percent_done):
#     return tuple((1 - percent_done) * v1[i] + percent_done * v2[i] for i in range(len(v1)))


def scale_vector(vector, scale):
    return tuple(vector[i] * scale for i in range(len(vector)))


def transform_scale_rotation_and_translation(object_image, size, midpoint, scale, rot, pos):
    center_matrix = np.array([[1, 0, midpoint[0]], [0, 1, midpoint[1]], [0,0,1]])
    uncenter_matrix = np.array([[1, 0, -midpoint[0]], [0, 1, -midpoint[1]], [0,0,1]])
    translate_matrix = np.array([[1, 0, pos[1]], [0, 1, pos[0]], [0,0,1]])
    scale_matrix = np.array([[1/scale[0], 0, 0], [0, 1/scale[1], 0], [0,0,1]])
    rotation_matrix = np.array([[math.cos(rot), -math.sin(rot), 0], [math.sin(rot), math.cos(rot), 0], [0,0,1]])

    transform_matrix = (center_matrix @ scale_matrix @ rotation_matrix @ translate_matrix @ uncenter_matrix)[0:2].reshape((6)).tolist()

    return object_image.transform(size, Image.AFFINE, transform_matrix, Image.NEAREST)


def load_object(info):
    if isinstance(info.object, str): # is a previous object
        info.name = info.object
        if info.name not in object_memory:
            print(f'object name "{info.name}" not found in memory')
            return False
        info.object, (loaded_pos, loaded_scale, loaded_rot, loaded_color) = object_memory[info.name]

        info.start_pos = getattr(info, 'start_pos', loaded_pos)
        info.start_scale = getattr(info, 'start_scale', loaded_scale)
        info.start_rot = getattr(info, 'start_rot', loaded_rot)
        info.start_color = getattr(info, 'start_color', loaded_color)

        info.end_pos = getattr(info, 'end_pos', info.start_pos)
        info.end_scale = getattr(info, 'end_scale', info.start_scale)
        info.end_rot = getattr(info, 'end_rot', info.start_rot)
        info.end_color = getattr(info, 'end_color', info.start_color)

        if info.end_color:
            info.color = True

        object_memory[info.name][1] = (info.end_pos, info.end_scale, info.end_rot, info.end_color)
    else:
        info.start_pos = getattr(info, 'start_pos', (0, 0))
        info.start_scale = getattr(info, 'start_scale', (1, 1))
        info.start_rot = getattr(info, 'start_rot', 0)

        if getattr(info, 'color', None) is not None:
            info.start_color = getattr(info, 'start_color', info.color)

        if getattr(info, 'start_color', None) is not None:
            info.start_color = getattr(info, 'start_color', (0, 0, 0))
            info.end_color = getattr(info, 'end_color', info.start_color)
            info.color = True
        info.end_color = getattr(info, 'end_color', None)

        info.end_pos = getattr(info, 'end_pos', info.start_pos)

        info.end_scale = getattr(info, 'end_scale', info.start_scale)
        info.end_rot = getattr(info, 'end_rot', info.start_rot)
        if isinstance(info.object, np.ndarray): # is a numpy array            
            object_as_uint8 = info.object.astype(np.uint8)
            object_image = Image.fromarray(object_as_uint8)
            info.object = object_image
            if getattr(info, 'name', None) is not None:
                object_memory[info.name] = [info.object, (info.end_pos, info.end_scale, info.end_rot, info.end_color)]
        elif not isinstance(info.object, Image.Image): # is a PIL image
            raise Exception(f'object type "{type(info.object)}" not supported')
    return True


def change_numpy_array_to_color(numpy_array, color):
    result_array = np.copy(numpy_array)
    result_array[(result_array != 0).all(axis=-1)] = color
    return result_array


def change_to_color(pillow_image, color):
    color = tuple(map(int, color))

    numpy_array = np.array(pillow_image)
    numpy_array = numpy_array.astype(np.uint8)
    numpy_array = change_numpy_array_to_color(numpy_array, color)
    return Image.fromarray(numpy_array)


object_memory = {}
cached_by_name_last_arr = {}
def our_transform(info):
    if not load_object(info):
        return

    # by this point info.object is a pillow image and start_'s end_'s all are set
    percent_done = info.curr_sub_beat / info.length
    pos = interpolate_vectors_float(info.start_pos, info.end_pos, percent_done)
    scale = interpolate_vectors_float(info.start_scale, info.end_scale, percent_done)
    rot = interpolate_float(info.start_rot, info.end_rot, percent_done)

    size = info.object.size

    # why is this seemingly backwards???
    midpoint = ((grid_helpers.GRID_HEIGHT - 1) / 2, (grid_helpers.GRID_WIDTH - 1) / 2)

    colored_object = info.object
    
    if getattr(info, 'color', None) is not None:
        current_color = interpolate_vectors_float(info.start_color, info.end_color, percent_done)
        colored_object = change_to_color(info.object, current_color)
    
    # if getattr(info, 'negative', None) is not None:

    transformed_image = transform_scale_rotation_and_translation(colored_object, size, midpoint, scale, rot, pos)
    
    arr_version = np.array(transformed_image)

    # if getattr(info, 'name', None) is not None: # old for sidechain_grid_shape (i think was bad)
    #     cached_by_name_last_arr[info.name] = arr_version
    if getattr(info, 'overwrite', None):
        grid_helpers.grid = arr_version
    else:
        grid_helpers.grid += arr_version



# ==== info effects ====




# Set percentage of grid to twinkle
TWINKLE_PERCENT = 0.2

# Find number of random points on grid to make twinkle
NUM_GRID_TWINKLE = int(TWINKLE_PERCENT * (grid_helpers.GRID_WIDTH * grid_helpers.GRID_HEIGHT))

# Total number of beats for twinkle effect
TWINKLE_TIME = 100

# Time for each twinkle to fade
TWINKLE_FADE = 2

# Twinkle speed, higher is slower, lower is faster
TWINKLE_SPEED = 10

# def make_twinkle_beats(color):
#     twinkle_beats = []
#     for beat in range(1, TWINKLE_TIME):
#         for j in range(int(NUM_GRID_TWINKLE)):
#             x, y = grid_helpers.random_coord()
#             # Create random offset for start beat of each twinkle
#             t_offset = random.uniform(0, beat * TWINKLE_SPEED)
#             twinkle_beats.append(
#                     grid_f(
#                         beat + t_offset,
#                         function=our_transform,
#                         object=get_rectangle_numpy(1, 1),
#                         start_pos=(y, x),
#                         start_color=color,
#                         end_color=(0, 0, 0),
#                         length=TWINKLE_FADE,
#                     )
#                 )
#     return twinkle_beats



def fire_ball_fade(grid_info):
    if grid_info.curr_sub_beat == 1 or getattr(grid_info, 'pos', None) is None:
        if random.randint(0, 1) == 0:
            start_x, x_dir = random.sample([(0, 1), (grid_helpers.GRID_WIDTH - 1, -1)], k=1)[0]
            start_y = random.randint(0, grid_helpers.GRID_HEIGHT - 1)
            y_dir = 1 - (random.randint(0, 1) * 2)
        else:
            start_x = random.randint(0, grid_helpers.GRID_WIDTH - 1)
            x_dir = 1 - (random.randint(0, 1) * 2)
            start_y, y_dir = random.sample([(0, 1), (grid_helpers.GRID_HEIGHT - 1, -1)], k=1)[0]

        grid_info.pos = (start_x, start_y)
        grid_info.dir = (x_dir, y_dir)
        # grid_info.pos = (random.randint(0, grid_helpers.GRID_WIDTH - 1), random.randint(0, grid_helpers.GRID_HEIGHT - 1))
        # grid_info.dir = (1 - (random.randint(0, 1) * 2), 1 - (random.randint(0, 1) * 2))
        grid_info.color = random_color()
        grid_info.trail = deque([])

    speed = int(1 / getattr(grid_info, 'speed', 1))

    if grid_info.curr_sub_beat % speed == 0:
        index = 0
        while index < len(grid_info.trail):
            (p_x, p_y), p_color = grid_info.trail[index]
            p_color = minus_color(p_color, 5)
            grid_info.trail[index][1] = p_color
            grid_helpers.grid[p_x][p_y] += p_color
            if p_color == (0, 0, 0) and index == 0:
                grid_info.trail.popleft()
            else:
                index += 1

        x, y = grid_info.pos
        d_x, d_y = grid_info.dir
        if x + d_x < 0 or x + d_x >= grid_helpers.GRID_WIDTH or y + d_y < 0 or y + d_y >= grid_helpers.GRID_HEIGHT:
            return
        grid_info.pos = (x + d_x, y + d_y)

    grid_helpers.grid[grid_info.pos[0]][grid_info.pos[1]] = grid_info.color

    if grid_info.curr_sub_beat % speed == 0:
        grid_info.trail.append([grid_info.pos, grid_info.color])



def rain(grid_info):
    if getattr(grid_info, 'rains', None) is None or (grid_info.curr_sub_beat == 0 and not grid_info.looped):
        grid_info.rains = [None] * grid_info.num_rains
        for index in range(len(grid_info.rains)):
            grid_info.rains[index] = time.time() + (random.random() * grid_info.upper_wait)
        grid_info.explosions = []

    for index, state_or_next_time in enumerate(grid_info.rains):
        if isinstance(state_or_next_time, float):
            if time.time() < state_or_next_time:
                continue

            new_x = random.randint(0, grid_helpers.GRID_WIDTH - 1)
            grid_info.rains[index] = (new_x, 0, time.time(), grid_info.speed)
        
        curr_x, curr_y, curr_start_time, curr_length = grid_info.rains[index]

        percent_done = (time.time() - curr_start_time) / curr_length
        if percent_done > .9:
            grid_info.rains[index] = time.time() + grid_info.lower_wait + (random.random() * grid_info.upper_wait)
            grid_info.explosions.append((curr_x, time.time(), .24))
            continue
        
        curr_y = int(percent_done * grid_helpers.GRID_HEIGHT)

        grid_helpers.grid[curr_x][curr_y] += grid_info.color
        scale = .02
        for i in range(1, 3):
            new_y = curr_y - i
            if new_y < 0:
                break
            grid_helpers.grid[curr_x][new_y] += scale_vector(GColor.blue, scale)
            scale /= 1.2

    index = 0
    while index < len(grid_info.explosions):         
        curr_x, curr_start_time, curr_length = grid_info.explosions[index]

        percent_done = (time.time() - curr_start_time) / curr_length
        if percent_done > 1:
            del grid_info.explosions[index]
            continue
        
        radius = int(percent_done * 4)
        inner_radius = radius - 1

        grid_width, grid_height = grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT
        
        mid_x = curr_x
        mid_y = grid_helpers.GRID_HEIGHT - 1
        for x in range(grid_width):
            for y in range(grid_height):
                if random.randint(1, 5) != 1:
                    continue
                distance = (x - mid_x) ** 2 + (y - mid_y) ** 2
                distance = math.sqrt(distance)
                if distance <= radius and distance >= inner_radius:
                    grid_helpers.grid[x][y] += scale_vector(GColor.blue, .04)
                    grid_helpers.grid[x][y] += scale_vector(GColor.white, .02)
        index += 1


def make_rain(start_beat=1, length=1, speed=1.2, lower_wait=1, upper_wait=6, color=GColor.blue_some_green, num_rains=20):
    return [grid_f(
        start_beat,
        function=rain,
        num_rains=num_rains,
        color=color,
        lower_wait=lower_wait,
        upper_wait=upper_wait, 
        speed=speed,
        length=length,
    )]





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


last_accel = [0, 0]
def set_accel(accel):
    global last_accel
    last_accel = accel


def accel_wrap(info):
    if getattr(info, 'running', None) is None or (info.curr_sub_beat == 1 and not info.looped):
        info.offset_x = 0
        info.offset_y = 0
    grid_helpers.move_wrap([int(last_accel[0]), int(last_accel[1])])

def accel_nowrap(info):
    if getattr(info, 'running', None) is None or (info.curr_sub_beat == 1 and not info.looped):
        info.offset_x = 0
        info.offset_y = 0
    # for row in grid_helpers.grid:
    #     print(row)
    grid_helpers.move([int(last_accel[0]), int(last_accel[1])])


def move_x_wrap(info):
    if getattr(info, 'running', None) is None or (info.curr_sub_beat == 1 and not info.looped):
        info.running = info.by
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1
    if info.curr_sub_beat % info.beat_divide == 0:
        grid_helpers.move_wrap([info.running, 0])
        info.running += info.by

def move_x(info):
    if getattr(info, 'running', None) is None or (info.curr_sub_beat == 1 and not info.looped):
        info.running = info.by
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1
    if info.curr_sub_beat % info.beat_divide == 0:
        grid_helpers.move([info.running, 0])
        info.running += info.by


def move_y_wrap(info):
    if getattr(info, 'running', None) is None or (info.curr_sub_beat == 1 and not info.looped):
        info.running = info.by
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1
    if info.curr_sub_beat % info.beat_divide == 0:
        grid_helpers.move_wrap([0, info.running])
        info.running += info.by

def move_y(info):
    if getattr(info, 'running', None) is None or (info.curr_sub_beat == 1 and not info.looped):
        info.running = info.by
    if getattr(info, 'beat_divide', None) is None:
        info.beat_divide = 1
    if info.curr_sub_beat % info.beat_divide == 0:
        grid_helpers.move([0, info.running])
        info.running += info.by



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
        if getattr(info, 'wrap', None):
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


def fill_color(info):
    grid_helpers.fill(info.color)


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
    grid_helpers.fill_grid_from_image_filepath(cached_filepath, getattr(info, 'color', None), rotate_90=info.rotate_90)


def fill_grid_from_text(info):
    color = getattr(info, 'color', None)
    subtract = getattr(info, 'subtract', None)
    filepath = grid_helpers.create_image_from_text_pilmoji(info.text, font_size=info.font_size, rotate_90=info.rotate_90, use_cache=False)
    grid_helpers.fill_grid_from_image_filepath(filepath, color=color, rotate_90=info.rotate_90, subtract=subtract)


def grid_f(start_beat=None, function=None, filename=None, rotate_90=None, text=None, font_size=12, length=None, **kwargs):
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


# if hue_shift or sat_shift or bright_shift or grid_bright_shift:
#     for part in range(3):
#         rd, gr, bl = final_channel[part * 3:(part * 3) + 3]
#         hue, sat, bright = colorsys.rgb_to_hsv(max(0, rd / 100.), max(0, gr / 100.), max(0, bl / 100.))
#         new_hue = (hue + hue_shift) % 1
#         new_sat = min(1, max(0, sat + sat_shift))
#         # bright shift is relative to initial brightness
#         new_bright = min(1, max(0, bright + bright*bright_shift))
#         if (part == 0 or part == 1): # tbd
#             new_bright = min(1, max(0, new_bright + new_bright*grid_bright_shift))
#         final_channel[part * 3:(part * 3) + 3] = colorsys.hsv_to_rgb(new_hue, new_sat, new_bright)
#         if any([x for x in [rd, gr, bl]]):
#             print(f'Old hue {hue:.2f}, sat {sat:.2f}, bright {bright:.2f}, new hue {new_hue:.2f}, new sat {new_sat:.2f}, new bright {new_bright:.2f}, old final: {[rd, gr, bl]}, new final: {final_channel[part * 3:(part * 3) + 3]}')

#         final_channel[part * 3] *= 100
#         final_channel[part * 3 + 1] *= 100
#         final_channel[part * 3 + 2] *= 100

# like above but simpler and better and no need for grid_bright_shift

def shift(initial, hue_shift=None, sat_shift=None, bright_shift=None):
    # Normalize initial RGB values to 0-1 scale
    r, g, b = [max(0, min(1, c / 100.0)) for c in initial]
    
    # Convert RGB to HSV
    hue, sat, bright = colorsys.rgb_to_hsv(r, g, b)
    
    # Adjust hue if hue_shift is specified
    if hue_shift is not None:
        hue = (hue + hue_shift) % 1
    
    # Adjust saturation if sat_shift is specified
    if sat_shift is not None:
        sat = min(1, max(0, sat + sat_shift))
    
    # Adjust brightness if bright_shift is specified
    if bright_shift is not None:
        bright = min(1, max(0, bright + bright * bright_shift))
    
    # Convert HSV back to RGB
    r_new, g_new, b_new = colorsys.hsv_to_rgb(hue, sat, bright)
    
    # Scale RGB values back to 0-100
    return [c * 100 for c in (r_new, g_new, b_new)]


def s(top_rgb=None, front_rgb=None, back_rgb=None, bottom_rgb=None, bottom_hori_rgb=None, bottom_vert_rgb=None, uv=None, green_laser=None, red_laser=None, laser_motor=None, disco_rgb=None, hue_shift=None, sat_shift=None, bright_shift=None, grid_bright_shift=None):
    if disco_rgb is None:
        disco_rgb = [0, 0, 0]

    if top_rgb:
        front_rgb = top_rgb
        back_rgb = top_rgb

    if bottom_rgb:
        bottom_hori_rgb = bottom_rgb
        bottom_vert_rgb = bottom_rgb

    if uv is None:
        uv = 0
    if green_laser is None:
        green_laser = 0
    if red_laser is None:
        red_laser = 0
    if laser_motor is None:
        laser_motor = 0

    if not back_rgb:
        back_rgb = [0, 0, 0]
    if not front_rgb:
        front_rgb = [0, 0, 0]

    if not bottom_hori_rgb:
        bottom_hori_rgb = [0, 0, 0]
    if not bottom_vert_rgb:
        bottom_vert_rgb = [0, 0, 0]

    bottom_hori_rgb = shift(bottom_hori_rgb, hue_shift, sat_shift, bright_shift)
    bottom_vert_rgb = shift(bottom_vert_rgb, hue_shift, sat_shift, bright_shift)
    front_rgb = shift(front_rgb, hue_shift, sat_shift, bright_shift)
    back_rgb = shift(back_rgb, hue_shift, sat_shift, bright_shift)
    # !TODO might need grid_shift here


    return back_rgb[:] + front_rgb[:] + bottom_hori_rgb[:] + [uv, green_laser, red_laser, laser_motor] + disco_rgb[:] + bottom_vert_rgb[:]


next_beat = None
def b(start_beat=None, name=None, length=None, intensity=None, offset=None, hue_shift=None, sat_shift=None, bright_shift=None, top_rgb=None, front_rgb=None, back_rgb=None, bottom_rgb=None, bottom_hori_rgb=None, bottom_vert_rgb=None, uv=None, green_laser=None, red_laser=None, laser_motor=None, disco_rgb=None, grid_bright_shift=None):
    global next_beat
    if length is None:
        raise Exception('length must be defined')

    if start_beat is None:
        if next_beat is None:
            raise Exception('It looks like you never specified a beat in this song, define at least one')
        start_beat = next_beat
    next_beat = start_beat + length

    if (name or intensity or offset or hue_shift or sat_shift or bright_shift) and (disco_rgb or top_rgb or front_rgb or back_rgb or bottom_rgb or bottom_hori_rgb or bottom_vert_rgb or uv or green_laser or red_laser or laser_motor):
        raise Exception(f'Anything between the sets "name intensity offset hue_shift sat_shift bright_shift" and "disco_rgb top_rgb front_rgb back_rgb bottom_rgb bottom_hori_rgb bottom_vert_rgb uv,  green_laser red_laser laser_motor" cannot be used together, dont use them in the same call')
    
    if (back_rgb or front_rgb) and top_rgb:
        raise Exception('Cannot define back_rgb or front_rgb if top_rgb is defined')
    
    if (bottom_hori_rgb or bottom_vert_rgb) and bottom_rgb:
        raise Exception('Cannot define bottom_hori_rgb or bottom_vert_rgb if bottom_rgb is defined')

    if name is None:
        channel = s(top_rgb, front_rgb, back_rgb, bottom_rgb, bottom_hori_rgb, bottom_vert_rgb, uv, green_laser, red_laser, laser_motor, disco_rgb, hue_shift, sat_shift, bright_shift, grid_bright_shift)
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

def winamp_grid(grid_info):
    if not grid_helpers.try_setup_winamp():
        print_red(f'Failed to load winamp when args spec, exiting\n' * 10)
        exit()
    winamp.winamp_wrapper.load_preset(grid_info.preset)
    winamp.winamp_wrapper.compute_frame()
    winamp.winamp_wrapper.load_into_numpy_array(grid_helpers.grid)







#  FROM 5 HOURS


def get_wub_bounce(beats, colors, speed=1, end_point=112, start_colors_at_beat=None):
    white = (100, 100, 100)
    components = []
    counter = 0
    y_index = 0
    spawn_points = [0, 31]
    vectors = [(0, speed), (0, -speed)]

    for index, beat in enumerate(beats):
        next_beat = beats[index + 1] if index + 1 < len(beats) else end_point
        color = white
        if type(colors[0]) in [int, float]:
            color = colors
        elif start_colors_at_beat is None or beat > start_colors_at_beat:
            color = colors[counter % len(colors)]
            counter += 1
        y_index = 1 - y_index
        # print(f'creating at {beat}, for length {next_beat - beat}')
        # if speed == 1:
        components.append(grid_f(beat, function=spawn_row, clear=True, y=spawn_points[y_index], color=color, length=0.05))    
        # if speed == 3:
        #     sub_or_add = 1
        #     if y_index == 1:
        #         sub_or_add = -1
        #     components.append(grid_f(beat, function=spawn_row, clear=True, y=spawn_points[y_index] + sub_or_add * 2, color=color, length=0.01))
        #     components.append(grid_f(beat, function=spawn_row, y=spawn_points[y_index] + sub_or_add, color=list(map(lambda x: x // 10, color)), length=0.01))
        #     components.append(grid_f(beat, function=spawn_row, y=spawn_points[y_index], color=list(map(lambda x: x // 20, color)), length=0.01))

        components.append(grid_f(beat, function=move_until_y_occupy, y=spawn_points[1-y_index], vector=vectors[y_index], length=next_beat - beat))
    return components