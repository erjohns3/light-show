from effects.compiler import *

import grid_helpers

# python light_server.py --local --show "five hours" --rotate --volume 70 --keyboard --skip_autogen --speed 1 --delay .189


intro_beats = [1, 3.79, 6.79, 9.54, 12.12, 14.58, 16.92, 19.08, 21.12, 23.25, 25.33, 27.12, 28.96, 30.67, 32.33, 33.92, 35.46, 37.04, 38.42, 39.83, 41.12, 42.42, 43.79, 45.0, 46.33, 47.46, 48.67, 49.75, 50.88, 51.96, 52.96, 54.04, 55.08, 56.08, 57.04, 57.96, 58.88, 59.79, 60.71, 61.58, 62.42, 63.29, 64.12, 64.92, 65.75, 66.54, 67.29, 68.04, 68.83, 69.54, 70.29, 71.04, 71.71, 72.38, 73.08, 73.79, 74.46, 75.04, 75.71, 76.33, 76.96, 77.58, 78.21, 78.79,              79.42, 80.0, 80.62, 81.21, 81.67, 82.29, 82.88, 83.46, 84.04, 84.58, 85.12, 85.62, 86.17, 86.75, 87.33, 87.88, 88.42, 89.0, 89.5, 90.08, 90.58, 91.17, 91.67, 92.25, 92.79, 93.33, 93.83, 94.38, 94.88, 95.38, 95.92, 96.38,              96.92, 97.46, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 100.96, 101.5, 102.0, 102.5, 103.0, 103.54, 104.04, 104.54, 105.04, 105.54, 106.08, 106.58, 107.04, 107.58, 108.08, 108.58, 109.08, 109.58, 110.08, 110.62, 111.08, 111.62]



def squares_up(grid_info):
    length = grid_info.end_sub_beat - grid_info.start_sub_beat
    curr = grid_info.curr_sub_beat

    for x, y in grid_helpers.grid_coords():
        pass    



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

def get_wub_bounce(beats, colors, speed=1, end_point=112, length=None):
    components = [
        grid_f(1, function=lambda x: None, grid_skip_top_fill=True, length=length),
    ]
    print(f'creating grid_skip_top_fill at {1}, for {length=}')
    counter = 0
    y_index = 0
    spawn_points = [0, 31]
    vectors = [(0, speed), (0, -speed)]

    for index, beat in enumerate(beats):
        next_beat = beats[index + 1] if index + 1 < len(beats) else end_point
        color = colors[counter % len(colors)]
        counter += 1
        y_index = 1 - y_index
        print(f'creating at {beat}, for length {next_beat - beat}')
        components.append(grid_f(beat, function=spawn_row, clear=True, y=spawn_points[y_index], color=color, length=0.01))
        components.append(grid_f(beat, function=move_until_y_occupy, y=spawn_points[1-y_index], vector=vectors[y_index], length=next_beat - beat))
    return components



effects = {
    'five hours eggplant wrap': {
        'length': 160,
        'beats': [
            grid_f(1, text='🍆', font_size=9, length=.01),
            # grid_f(1, filename='nyan.webp', grid_rotate=True, length=16),
            grid_f(1, function=move_grid_wrap, vector=(0, -1), grid_skip_top_fill=True, beat_divide=3, length=64),        
        ]
    },

    '5 hours grid intro': {
        'length': 113,
        'beats': [
            # *get_wub_across(intro_beats, intro_melody_colors),
            *get_wub_bounce(intro_beats, intro_melody_colors, end_point=112, length=113),
            grid_f(112, function=squares_up, length=2),
        ],
    },

    '5 hours grid chorus': {
        'length': 4,
        'beats': [
            b(1, name='Red disco pulse', length=3),
            b(4, name='Red disco pulse', length=1),
            *get_wub_bounce(
                [x + .5 for x in range(1, 5)],
                colors=chorus_melody_colors, 
                speed=3,
                length=4,
                end_point=5,
            ),
        ]
    },

    "Deorro - Five Hours (Static Video) [LE7ELS]": {
        "bpm": 128,
        "song_path": "songs/Deorro - Five Hours (Static Video) [LE7ELS].ogg",
        "delay_lights": 0.37665,
        "skip_song": 0.0,
        "beats": [ 
            # grid_f(1, filename='nyan.webp', grid_skip_top_fill=True, rotate_90=True, length=100),
            # grid_f(1, filename='ricardo.gif', grid_skip_top_fill=True, length=100),
            # b(1, name='five hours eggplant wrap', length=79),
            b(1, name='5 hours grid intro', length=113),
            b(113, name='5 hours grid chorus', length=64),
        ]
    }
}
# exit()