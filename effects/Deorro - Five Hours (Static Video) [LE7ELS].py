import random
from copy import deepcopy

from effects.compiler import *

import grid_helpers

# python light_server.py --local --show "five hours" --rotate --volume 70 --keyboard --skip_autogen --speed 1 --delay .189


intro_beats = [1, 3.79, 6.79, 9.54, 12.12, 14.58, 16.92, 19.08, 21.12, 23.25, 25.33, 27.12, 28.96, 30.67, 32.33, 33.92, 35.46, 37.04, 38.42, 39.83, 41.12, 42.42, 43.79, 45.0, 46.33, 47.46, 48.67, 49.75, 50.88, 51.96, 52.96, 54.04, 55.08, 56.08, 57.04, 57.96, 58.88, 59.79, 60.71, 61.58, 62.42, 63.29, 64.12, 64.92, 65.75, 66.54, 67.29, 68.04, 68.83, 69.54, 70.29, 71.04, 71.71, 72.38, 73.08, 73.79, 74.46, 75.04, 75.71, 76.33, 76.96, 77.58, 78.21, 78.79,              79.42, 80.0, 80.62, 81.21, 81.67, 82.29, 82.88, 83.46, 84.04, 84.58, 85.12, 85.62, 86.17, 86.75, 87.33, 87.88, 88.42, 89.0, 89.5, 90.08, 90.58, 91.17, 91.67, 92.25, 92.79, 93.33, 93.83, 94.38, 94.88, 95.38, 95.92, 96.38,              96.92, 97.46, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 100.96, 101.5, 102.0, 102.5, 103.0, 103.54, 104.04, 104.54, 105.04, 105.54, 106.08, 106.58, 107.04, 107.58, 108.08, 108.58, 109.08, 109.58, 110.08, 110.62, 111.08, 111.62]



def squares_up(info):
    if getattr(info, 'filled_to', None) is None:
        info.filled_to = 0
        info.last_color = [random.randint(0, 30), random.randint(0, 30), random.randint(0, 150)]
    
    coords_length = grid_helpers.total_coords
    percent_done = info.curr_sub_beat / info.length
    fill_to = int(percent_done * coords_length)
    for index, (x, y) in enumerate(grid_helpers.coords_y_first()):
        if info.filled_to <= index <= fill_to:
            grid_helpers.grid[x][y] = white
            grid_helpers.grid[x][y] = info.last_color

            chosen_index = random.randint(0, 2)
            if random.randint(0, 1) == 0:
                info.last_color[chosen_index] = max(info.last_color[chosen_index] - 15, 0)
            else:
                info.last_color[chosen_index] = min(info.last_color[chosen_index] + 15, 254)
    info.filled_to = fill_to

white = (100, 100, 100)
pink = (100, 0, 100)
green_c = (0, 100, 0)
red_c = (100, 0, 0)
blue_c = (0, 0, 100)
note_1 = (100, 0, 100)
note_2 = (0, 0, 100)
note_3 = (100, 0, 0)
note_4 = (0, 100, 0)
note_5 = (0, 100, 100)

hard_colors = [
    (100, 0, 0),
    (0, 100, 0),
    (0, 0, 100),
    (100, 0, 100),
    (0, 100, 100),
    (100, 100, 0),
]


soft_colors = [
    (30, 0, 0),
    (0, 30, 0),
    (0, 0, 30),
    (30, 0, 30),
    (0, 30, 30),
    (30, 30, 0),
]

intro_melody_colors = [
    note_1,
    note_1,
    note_1,
    note_2,
    note_1,
    note_3,
    note_1,
    note_4,
]

chorus_melody_colors = [
    note_1,
    note_2,
    note_3,
    note_4,
]

def get_wub_across(beats, colors):
    components = [
        grid_f(1, function=move_grid, vector=(0, 1), length=111),
    ]
    counter = 0
    for beat in beats:
        # yield grid_f(1, text=🍆, font_size=12, length=0.01)

        color = white
        if beat > 79:
            color = colors[counter % len(colors)]
            counter += 1
        
        components.append(grid_f(beat, function=spawn_row, y=0, color=color, length=0.01))
    return components

def get_wub_bounce(beats, colors, speed=1, end_point=112, start_colors_at_beat=None):
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
        components.append(grid_f(beat, function=spawn_row, clear=True, y=spawn_points[y_index], color=color, length=0.01))    
        # if speed == 3:
        #     sub_or_add = 1
        #     if y_index == 1:
        #         sub_or_add = -1
        #     components.append(grid_f(beat, function=spawn_row, clear=True, y=spawn_points[y_index] + sub_or_add * 2, color=color, length=0.01))
        #     components.append(grid_f(beat, function=spawn_row, y=spawn_points[y_index] + sub_or_add, color=list(map(lambda x: x // 10, color)), length=0.01))
        #     components.append(grid_f(beat, function=spawn_row, y=spawn_points[y_index], color=list(map(lambda x: x // 20, color)), length=0.01))

        components.append(grid_f(beat, function=move_until_y_occupy, y=spawn_points[1-y_index], vector=vectors[y_index], length=next_beat - beat))
    return components


last_object_name = None
def make_transforms(beat, beat_lengths, object=None, poses=None, scales=None, rotations=None):
    global last_object_name

    building = []
    if object is None:
        name = last_object_name
    else:
        name = random_letters(10)
        last_object_name = name

    beats_to_run = 0
    if poses:
        beats_to_run = max(len(poses), beats_to_run)
    elif scales:
        beats_to_run = max(len(scales), beats_to_run)
    elif rotations:
        beats_to_run = max(len(rotations), beats_to_run)

    if not isinstance(beat_lengths, list):
        beat_lengths = [beat_lengths] * beats_to_run

    for index, beat_length in enumerate(beat_lengths):
        if object is None or index > 0:
            object = name
        thing = grid_f(
            beat,
            function=our_transform,
            object=object,
            name=name,
            length=beat_length,
        )
        info = thing[1]
        for part, data in [['pos', poses], ['scale', scales], ['rot', rotations]]:
            if data is None:
                continue
            # print('part', part, 'data', data)
            if len(data) <= index:
                continue
            data = data[index]
            if data is None:
                continue
            start, end = data
            # if part in ['pos', 'scale']:
            #     if not isinstance(start, list):
            #         start = [start, None]
            #     if not isinstance(end, list):
            #         end = [end, None]
            if start is not None:
                setattr(info, f'start_{part}', start)
            if end is not None:
                setattr(info, f'end_{part}', end)
        building.append(thing)
        beat += beat_length
    return building


def get_random_rotate_circles(num, beat_length, colors, circles_angles):
    arr = []
    colors_copy = deepcopy(colors)
    random.shuffle(colors_copy)

    for j, angle in enumerate(circles_angles):
        for i in range(num):
            rand_dist = random.randint(4, 9)
            rand_position = (random.randint(-8, 8), random.randint(-8, 8))
            arr += make_transforms(
                1 + i * beat_length,
                beat_lengths=beat_length,
                # object=get_point_numpy((0, rand_dist), color=colors_copy[(i + j) % len(colors_copy)]),
                object=get_rectangle_numpy(random.randint(1, 5), random.randint(1, 5), color=colors_copy[(i + j) % len(colors_copy)], offset_x=random.randint(-5, 5), offset_y=random.randint(-5, 5)),
                poses=[[rand_position, None]],
                rotations=[(0, angle)],
            )
    return arr


widen_2_beat = [
    [None, (1, 21)],
    [None, (65, 21)],
]
shrink_2_beat = [
    [None, (65, 1)],
    [None, (1, 1)],
]

effects = {
    '5 hours grid intro': {
        'length': 113,
        'beats': [
            grid_f(1, function=lambda x: x, clear=False, length=113),

            # *get_wub_across(intro_beats, intro_melody_colors),
            *get_wub_bounce(intro_beats, intro_melody_colors, end_point=112, start_colors_at_beat=79),
            grid_f(112.5, function=squares_up, length=.5),
        ],
    },

    '5 hours Bottom bass bottom': {
        'length': 1,
        'beats': [
            b(1, name='Blue bottom', length=.8, intensity=[.1, 0], hue_shift=.9),
        ]
    },


    '5 hours grid chorus': {
        'length': 4,
        'beats': [
            grid_f(1, function=lambda x: x, clear=False, length=4),
            b(1, name='5 hours Bottom bass bottom', length=4),
            b(1, name='Red disco pulse', length=3, offset=.5),
            b(4, name='Green disco pulse', length=1, offset=.5),
            *get_wub_bounce(
                [x + .5 for x in range(1, 5)],
                colors=chorus_melody_colors, 
                speed=3,
                end_point=5,
            ),
        ]
    },
    '5 hours box combine color 1': {
        'length': 4, 
        'beats': [
            *make_transforms(
                1, 
                beat_lengths=1,
                object=get_rectangle_numpy(1, 1, color=(0, 100, 0)),
                poses=[
                    [(15, 0), None],
                    None,
                ],
                scales=widen_2_beat,
            ),
            *make_transforms(
                3, 
                beat_lengths=1,
                scales=shrink_2_beat,
            ),
            *make_transforms(
                1,
                object=get_rectangle_numpy(1, 1, color=(0, 0, 100)),
                beat_lengths=1,
                poses=[
                    [(-16, 0), None],
                    None,
                ],
                scales=widen_2_beat,
            ),
            *make_transforms(
                3, 
                beat_lengths=1,
                scales=shrink_2_beat,
            ),
        ]
    },
    '5 hours box combine color 2': {
        'length': 4, 
        'beats': [
            *make_transforms(
                1, 
                beat_lengths=1,
                object=get_rectangle_numpy(1, 1, color=(100, 0, 0)),
                poses=[
                    [(15, 0), None],
                    None,
                ],
                scales=widen_2_beat,
            ),
            *make_transforms(
                3, 
                beat_lengths=1,
                scales=shrink_2_beat,
            ),
            *make_transforms(
                1,
                object=get_rectangle_numpy(1, 1, color=(0, 0, 100)),
                beat_lengths=1,
                poses=[
                    [(-16, 0), None],
                    None,
                ],
                scales=widen_2_beat,
            ),
            *make_transforms(
                3, 
                beat_lengths=1,
                scales=shrink_2_beat,
            ),
        ]
    },

    # !TODO IF YOU SET LENGTH LOWER THAN 4, IT WILL ERROR
    '5 hours box combine': {
        'length': 8, 
        'beats': [
            b(1, name='5 hours box combine color 1', length=4),
            b(5, name='5 hours box combine color 2', length=4),
        ]
    },

    '5 hours pinwheel grid': {
        'length': 4, 
        # 'autogen': 'complex grid',
        'beats': [
            *make_transforms(
                1, 
                beat_lengths=[
                    .2, 
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                ],
                object=get_rectangle_numpy(2, 20, color=(30, 30, 0)),
                poses=[[(8, 4), None]],
                rotations=[
                    (0, 3.14 / 4),
                    None,
                    (None, 2 * 3.14 / 4),
                    None,
                    (None, 3 * 3.14 / 4),
                    None,
                    (None, 4 * 3.14 / 4),
                    None,
                ],
            ),
            *make_transforms(
                1, 
                beat_lengths=[
                    .2, 
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                ],
                object=get_rectangle_numpy(2, 20, color=(0, 30, 30)),
                poses=[[(-8, 4), None]],
                rotations=[
                    (0, -3.14 / 4),
                    None,
                    (None, 2 * -3.14 / 4),
                    None,
                    (None, 3 * -3.14 / 4),
                    None,
                    (None, 4 * -3.14 / 4),
                    None,
                ],
            ),
            *make_transforms(
                1, 
                beat_lengths=[
                    .2, 
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                ],
                object=get_rectangle_numpy(2, 20, color=(30, 0, 30)),
                poses=[[(-8, -4), None]],
                rotations=[
                    (0, 3.14 / 4),
                    None,
                    (None, 2 * 3.14 / 4),
                    None,
                    (None, 3 * 3.14 / 4),
                    None,
                    (None, 4 * 3.14 / 4),
                    None,
                ],
            ),
            *make_transforms(
                1, 
                beat_lengths=[
                    .2, 
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                    .2,
                    .8,
                ],
                object=get_rectangle_numpy(2, 20, color=(30, 30, 30)),
                poses=[[(8, -4), None]],
                rotations=[
                    (0, -3.14 / 4),
                    None,
                    (None, 2 * -3.14 / 4),
                    None,
                    (None, 3 * -3.14 / 4),
                    None,
                    (None, 4 * -3.14 / 4),
                    None,
                ],
            ),
            # grid_f(3, function=lambda x: 0, clear=False, length=2),
        ]
    },

    '5 hours box combine ': {
        'length': 64,
        'beats': [
            # grid_f(1, function=clear_grid, length=0.01),
            grid_f(1, function=spawn_row_then_move, y=0, clear=True, bounce=True, color=blue_c, vector=(0, 1), length=64),
            grid_f(1, function=spawn_col_then_move, x=0, bounce=True, color=red_c, vector=(1, 0), length=64),
        ]
    },

    '5 hours rotate circle 1': {
        'length': 32,
        'beats': [
            grid_f(1, function=lambda x: 0, clear=False, length=32),
            *get_random_rotate_circles(num=16, beat_length=2, colors=soft_colors, circles_angles=[-6.28, 6.28]),
        ]
    },

    '5 hours rotate circle 2': {
        'length': 32,
        'beats': [
            # grid_f(1, function=lambda x: 0, clear=False, length=32),
            *get_random_rotate_circles(num=16, beat_length=2, colors=hard_colors, circles_angles=[-6.28, 6.28]),
        ]
    },

    "Deorro - Five Hours (Static Video) [LE7ELS]": {
        "bpm": 128,
        "song_path": "songs/Deorro - Five Hours (Static Video) [LE7ELS].ogg",
        "delay_lights": 0.37665,
        "skip_song": 0.0,
        "beats": [ 
            # grid_f(1, filename='nyan.webp', rotate_90=True, length=100),
            grid_f(1, filename='ricardo.gif', length=100),
            # b(1, name='five hours eggplant wrap', length=79),
            b(1, name='5 hours grid intro', length=113),
            b(113, name='5 hours grid chorus', length=64),
            b(177, name='5 hours box combine', length=64),
            b(241, name='5 hours pinwheel grid', length=64),
            b(305, name='5 hours grid chorus', length=64),
            grid_f(369, function=clear_grid, length=.01),
            b(369, name='5 hours rotate circle 1', length=32),
            b(391, name='5 hours rotate circle 2', length=64),
        ]
    }
}



            # grid_f(
            #     1,
            #     function=our_transform,
            #     object=grid_helpers.get_2d_arr_from_text('😋'),
            #     name='oy',
            #     start_pos=(-10, 0),
            #     end_pos=(10, 0),
            #     start_rot = 0,
            #     end_rot = 6.24,
            #     length=1,
            # ),
            # grid_f(
            #     2,
            #     function=our_transform,
            #     object='oy',
            #     end_pos=(-10, 0),
            #     end_rot = 0,
            #     length=1,
            # ),



    # 'five hours eggplant wrap': {
    #     'length': 160,
    #     'beats': [
    #         grid_f(1, text='🍆', font_size=9, length=.01),
    #         # grid_f(1, filename='nyan.webp', grid_rotate=True, length=16),
    #         grid_f(1, function=move_grid, wrap=True, vector=(0, -1), beat_divide=3, length=64),        
    #     ]
    # },


            # grid_f(
            #     1,
            #     function=our_transform,
            #     object=get_rectangle_numpy(1, 1, color=(100, 0, 0)),
            #     name='oy',
            #     start_pos=(15, 0),
            #     end_scale=(1, 21),
            #     length=1,
            # ),
            # grid_f(
            #     2,
            #     function=our_transform,
            #     object='oy',
            #     end_scale=(45, 21),
            #     length=1,
            # ),
            # grid_f(
            #     3,
            #     function=our_transform,
            #     object='oy',
            #     end_scale=(1, 21),
            #     length=1,
            # ),
            # grid_f(
            #     4,
            #     function=our_transform,
            #     object='oy',
            #     end_scale=(1, 1),
            #     length=1,
            # ),