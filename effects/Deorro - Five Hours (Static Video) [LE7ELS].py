from effects.compiler import b

import grid_helpers


grid = grid_helpers.get_grid()
def move_grid(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1
    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        grid_helpers.grid_move(grid_info.vector)


def spawn_row(grid_info):
    for x in range(grid_helpers.GRID_WIDTH):
        grid[x][0] = grid_info.color



colors = {
    'white': (100, 0, 100),
    'pink': (100, 0, 100),
    'green': (0, 100, 0),
    'red': (100, 0, 0),
    'blue': (0, 0, 100),
}
effects = {
    '5 hours intro': {
        'length': 79,
        'beats': [
            b(1, grid_function=spawn_row, color=colors['white'], length=0.01),
            b(1, grid_function=move_grid, vector=(0, 1), grid_skip_top_fill=True, length=6),
            b(4, grid_function=spawn_row, color=colors['white'], length=0.01),
            b(6.75, grid_function=spawn_row, color=colors['white'], length=0.01),
            b(7, grid_function=move_grid, vector=(0, 2), grid_skip_top_fill=True, length=73),
            b(9.5, grid_function=spawn_row, color=colors['white'], length=0.01),
            b(12, grid_function=spawn_row, color=colors['white'], length=0.01),
            b(14.5, grid_function=spawn_row, color=colors['white'], length=0.01),
        ]
    },


    '5 hours main chorus': {
        'length': 64,
        'beats': [
            b(1.5, grid_function=spawn_row, color=colors['pink'], length=0.01),
            b(1, grid_function=move_grid, vector=(0, 3), grid_skip_top_fill=True, length=64),
            b(2.5, grid_function=spawn_row, color=colors['pink'], length=0.01),
            b(3.5, grid_function=spawn_row, color=colors['blue'], length=0.01),
            b(4.5, grid_function=spawn_row, color=colors['green'], length=0.01),
        ]
    },


    'wipe sad': {
        'length': 8,
        'beats': [
            b(1, grid_text='DIE', font_size=14, length=.01),
            # b(1, grid_filename='dog.jpg', length=.01),
            b(1, grid_function=move_grid, vector=(0, -1), grid_skip_top_fill=True, beat_divide=6, length=64),        
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