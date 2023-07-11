from effects.compiler import *

import grid_helpers

# python light_server.py --local --show "five hours" --rotate --volume 70 --keyboard --skip_autogen --speed 1 --delay .189


wub_hits = [1, 3.79, 6.79, 9.54, 12.12, 14.58, 16.92, 19.08, 21.12, 23.25, 25.33, 27.12, 28.96, 30.67, 32.33, 33.92, 35.46, 37.04, 38.42, 39.83, 41.12, 42.42, 43.79, 45.0, 46.33, 47.46, 48.67, 49.75, 50.88, 51.96, 52.96, 54.04, 55.08, 56.08, 57.04, 57.96, 58.88, 59.79, 60.71, 61.58, 62.42, 63.29, 64.12, 64.92, 65.75, 66.54, 67.29, 68.04, 68.83, 69.54, 70.29, 71.04, 71.71, 72.38, 73.08, 73.79, 74.46, 75.04, 75.71, 76.33, 76.96, 77.58, 78.21, 78.79,              79.42, 80.0, 80.62, 81.21, 81.67, 82.29, 82.88, 83.46, 84.04, 84.58, 85.12, 85.62, 86.17, 86.75, 87.33, 87.88, 88.42, 89.0, 89.5, 90.08, 90.58, 91.17, 91.67, 92.25, 92.79, 93.33, 93.83, 94.38, 94.88, 95.38, 95.92, 96.38,              96.92, 97.46, 98.0, 98.5, 99.0, 99.5, 100.0, 100.5, 100.96, 101.5, 102.0, 102.5, 103.0, 103.54, 104.04, 104.54, 105.04, 105.54, 106.08, 106.58, 107.04, 107.58, 108.08, 108.58, 109.08, 109.58, 110.08, 110.62, 111.08, 111.62]


def squares_up(grid_info):
    grid_helpers

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

melody_colors = [
    note_1,
    note_1,
    note_1,
    note_2,
    note_1,
    note_3,
    note_1,
    note_4,
]

def get_wub_across():
    counter = 0
    for index, beat in enumerate(wub_hits):
        # yield grid_f(1, text=🍆, font_size=12, length=0.01)

        color = white
        if beat > 79:
            color = melody_colors[counter % len(melody_colors)]
            counter += 1
        yield grid_f(beat, function=spawn_row, y=0, color=color, length=0.01)


effects = {
    '5 hours intro': {
        'length': 113,
        'beats': [
            grid_f(1, function=lambda x: None, grid_skip_top_fill=True, length=113),
            grid_f(1, function=move_grid, vector=(0, 1), length=111),

            *get_wub_across(),
            # *get_wub_bounce(),

            grid_f(112, function=squares_up, length=2),
        ],
    },

    '5 hours main chorus': {
        'length': 64,
        'beats': [
            grid_f(1.5, function=spawn_row, y=0, color=pink, length=0.01),
            grid_f(1, function=move_grid, vector=(0, 3), grid_skip_top_fill=True, length=64),
            grid_f(2.5, function=spawn_row, y=0, color=pink, length=0.01),
            grid_f(3.5, function=spawn_row, y=0, color=blue, length=0.01),
            grid_f(4.5, function=spawn_row, y=0, color=green, length=0.01),
        ]
    },


    'five hours eggplant wrap': {
        'length': 160,
        'beats': [
            grid_f(1, text='🍆', font_size=9, length=.01),
            # grid_f(1, filename='nyan.webp', grid_rotate=True, length=16),
            grid_f(1, function=move_grid_wrap, vector=(0, -1), grid_skip_top_fill=True, beat_divide=3, length=64),        
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
            b(1, name='5 hours intro', length=113),
            # b(113, name='RBBB 1 bar', length=30, bright_shift=-.8),
            # b(113, name='5 hours main chorus', length=64),
        ]
    }
}



            # grid_f(1, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(3.79, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(6.79, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(9.54, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(12.12, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(14.58, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(16.92, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(19.08, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(21.12, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(23.25, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(25.33, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(27.12, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(28.96, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(30.67, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(32.33, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(33.92, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(35.46, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(37.04, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(38.42, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(39.83, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(41.12, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(42.42, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(43.79, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(45.0, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(46.33, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(47.46, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(48.67, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(49.75, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(50.88, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(51.96, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(52.96, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(54.04, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(55.08, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(56.08, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(57.04, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(57.96, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(58.88, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(59.79, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(60.71, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(61.58, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(62.42, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(63.29, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(64.12, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(64.92, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(65.75, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(66.54, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(67.29, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(68.04, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(68.83, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(69.54, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(70.29, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(71.04, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(71.71, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(72.38, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(73.08, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(73.79, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(74.46, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(75.04, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(75.71, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(76.33, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(76.96, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(77.58, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(78.21, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            # grid_f(78.79, function=spawn_row, font_size=9, y=0, color=white, length=0.01),
            
            # grid_f(79.42, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(80.0, function=spawn_row, font_size=9, y=0,  color=note_1, length=0.01),
            # grid_f(80.62, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(81.21, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(81.67, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(82.29, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(82.88, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(83.46, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),

            # grid_f(84.04, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(84.58, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(85.12, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(85.62, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(86.17, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(86.75, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(87.33, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(87.88, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),

            # grid_f(88.42, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(89.0, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(89.5, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(90.08, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(90.58, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(91.17, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(91.67, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(92.25, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),

            # grid_f(92.79, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(93.33, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(93.83, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(94.38, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(94.88, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(95.38, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(95.92, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(96.38, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),
            
            # grid_f(96.92, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(97.46, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(98.0, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(98.5, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(99.0, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(99.5, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(100.0, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(100.5, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),

            # grid_f(100.96, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(101.5, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(102.0, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(102.5, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(103.0, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(103.54, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(104.04, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(104.54, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),

            # grid_f(105.04, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(105.54, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(106.08, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(106.58, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(107.04, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(107.58, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
            # grid_f(108.08, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(108.58, function=spawn_row, font_size=9, y=0, color=note_4, length=0.01),

            # grid_f(109.08, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(109.58, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(110.08, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(110.62, function=spawn_row, font_size=9, y=0, color=note_2, length=0.01),
            # grid_f(111.08, function=spawn_row, font_size=9, y=0, color=note_1, length=0.01),
            # grid_f(111.62, function=spawn_row, font_size=9, y=0, color=note_3, length=0.01),
