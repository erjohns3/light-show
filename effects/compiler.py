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

import grid_helpers

class GridInfo:
    def __init__(self):
        self.grid_function = None
        self.filename = None
        self.rotate_90 = False


def fill_grid_from_image_filepath_wrapper(grid_info):
    image_filepath = directory_above_this_file.joinpath('images', grid_info.filename)
    grid_helpers.fill_grid_from_image_filepath(image_filepath, rotate_90=grid_info.rotate_90)


this_file_directory = pathlib.Path(__file__).parent.resolve()
directory_above_this_file = this_file_directory.parent.resolve()
following_beat = None
def b(start_beat=None, name=None, length=None, intensity=None, offset=None, hue_shift=None, sat_shift=None, bright_shift=None, top_rgb=None, front_rgb=None, back_rgb=None, bottom_rgb=None, uv=None, green_laser=None, red_laser=None, laser_motor=None, disco_rgb=None, grid_bright_shift=None, grid_function=None, grid_filename=None, grid_rotate_90=None):
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


    grid_info = GridInfo()
    if grid_filename is not None:
        grid_info.filename = grid_filename
        grid_info.rotate_90 = grid_rotate_90
        grid_function = lambda: fill_grid_from_image_filepath_wrapper(grid_info)

    if grid_function is not None:
        grid_info.grid_function = grid_function
        return [start_beat, grid_info, length]

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
