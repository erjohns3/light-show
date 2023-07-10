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
}
effects = {
    '5 hours intro': {
        'length': 79,
        'beats': [
            grid_f(1, function=lambda x: None, grid_skip_top_fill=True, length=79),
            grid_f(1, function=move_grid, vector=(0, 1), length=6),
            grid_f(1, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(4, function=spawn_row, color=colors['pink'], length=0.01),
            grid_f(6.75, function=spawn_row, color=colors['green'], length=0.01),
            grid_f(7, function=move_grid, vector=(0, 2), length=73),
            grid_f(9.5, function=spawn_row, color=colors['blue'], length=0.01),
            grid_f(12, function=spawn_row, color=colors['white'], length=0.01),
            grid_f(14.5, function=spawn_row, color=colors['white'], length=0.01),
        ]
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
            b(1, name='5 hours intro', length=79),
            b(79, name='RBBB 1 bar', length=30, bright_shift=-.8),
            b(113, name='5 hours main chorus', length=64),
        ]
    }
}