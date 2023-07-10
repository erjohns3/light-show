from effects.compiler import b, grid_f

import grid_helpers

def move_grid(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1
    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        grid_helpers.grid_move(grid_info.vector)


def spawn_row(grid_info):
    for x in range(grid_helpers.GRID_WIDTH):
        grid_helpers.grid[x][0] = grid_info.color



colors = {
    'white': (100, 100, 100),
    'pink': (100, 0, 100),
    'green': (0, 100, 0),
    'red': (100, 0, 0),
    'blue': (0, 0, 100),
    'note_1': (100, 0, 100),
    'note_2': (0, 0, 100),
    'note_3': (100, 0, 0),
    'note_4': (0, 100, 0),
    'note_5': (0, 100, 100),
}

effects = {
    '5 hours intro tapped': {
        'length': 113,
        'beats': [
            grid_f(1, function=lambda x: None, grid_skip_top_fill=True, length=113),
            grid_f(1, function=move_grid, vector=(0, 1), length=8.5),
            grid_f(9.5, function=move_grid, vector=(0, 1), length=29),
            grid_f(38.5, function=move_grid, vector=(0, 1), length=11.5),
            grid_f(50, function=move_grid, vector=(0, 1), length=63),

            grid_f(1, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(3.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(6.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(9.54, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(12.12, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(14.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(16.92, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(19.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(21.12, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(23.25, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(25.33, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(27.12, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(28.96, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(30.67, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(32.33, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(33.92, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(35.46, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(37.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(38.42, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(39.83, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(41.12, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(42.42, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(43.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(45.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(46.33, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(47.46, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(48.67, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(49.75, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(50.88, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(51.96, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(52.96, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(54.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(55.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(56.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(57.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(57.96, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(58.88, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(59.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(60.71, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(61.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(62.42, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(63.29, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(64.12, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(64.92, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(65.75, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(66.54, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(67.29, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(68.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(68.83, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(69.54, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(70.29, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(71.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(71.71, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(72.38, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(73.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(73.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(74.46, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(75.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(75.71, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(76.33, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(76.96, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(77.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(78.21, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(78.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(79.42, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(80.0, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(80.62, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(81.21, function=spawn_row, color=colors['note_2'], length=0.01),
            grid_f(81.67, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(82.29, function=spawn_row, color=colors['note_3'], length=0.01),
            grid_f(82.88, function=spawn_row, color=colors['note_4'], length=0.01),
            grid_f(83.46, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(84.04, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(84.58, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(85.12, function=spawn_row, color=colors['note_2'], length=0.01),
            grid_f(85.62, function=spawn_row, color=colors['note_1'], length=0.01),
            grid_f(86.17, function=spawn_row, color=colors['note_3'], length=0.01),
            grid_f(86.75, function=spawn_row, color=colors['note_4'], length=0.01),
            grid_f(87.33, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(87.88, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(88.42, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(89.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(89.5, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(90.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(90.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(91.17, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(91.67, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(92.25, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(92.79, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(93.33, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(93.83, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(94.38, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(94.88, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(95.38, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(95.92, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(96.38, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(96.92, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(97.46, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(98.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(98.5, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(99.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(99.5, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(100.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(100.5, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(100.96, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(101.5, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(102.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(102.5, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(103.0, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(103.54, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(104.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(104.54, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(105.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(105.54, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(106.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(106.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(107.04, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(107.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(108.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(108.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(109.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(109.58, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(110.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(110.62, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(111.08, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(111.62, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(112.08, function=spawn_row, color=colors['white'], length=0.01),
            
        ],
    },

    '5 hours main chorus': {
        'length': 64,
        'beats': [
            grid_f(1.5, function=spawn_row, color=colors['pink'], length=0.01),
            grid_f(1, function=move_grid, vector=(0, 3), grid_skip_top_fill=True, length=64),
            grid_f(2.5, function=spawn_row, color=colors['pink'], length=0.01),
            grid_f(3.5, function=spawn_row, color=colors['blue'], length=0.01),
            grid_f(4.5, function=spawn_row, color=colors['green'], length=0.01),
        ]
    },


    'wipe sad': {
        'length': 16,
        'beats': [
            grid_f(1, text='😭', font_size=13, length=.01),
            # grid_f(1, filename='nyan.webp', grid_rotate=True, length=16),
            grid_f(1, function=move_grid, vector=(0, -1), grid_skip_top_fill=True, beat_divide=12, length=64),        
        ]
    },


    "Deorro - Five Hours (Static Video) [LE7ELS]": {
        "bpm": 128,
        "song_path": "songs/Deorro - Five Hours (Static Video) [LE7ELS].ogg",
        "delay_lights": 0.37665,
        "skip_song": 0.0,
        "beats": [ 
            # b(1, name='wipe sad', length=79),
            b(1, name='5 hours intro tapped', length=113),
            # b(79, name='RBBB 1 bar', length=30, bright_shift=-.8),
            b(113, name='5 hours main chorus', length=64),
        ]
    }
}