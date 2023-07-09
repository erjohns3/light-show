from effects.compiler import b

import grid_helpers


grid = grid_helpers.get_grid()
def move_grid(grid_info):
    if grid_info.curr_sub_beat % 1 == 0:
        grid_helpers.grid_move(grid_info.vector)


def spawn_row(grid_info):
    for x in range(grid_helpers.GRID_WIDTH):
        grid[x][0] = grid_info.color

colors = {
    'white': (100, 100, 100),
    'pink': (100, 0, 100),
}

effects = {
    '5 hours intro': {
        'length': 79,
        'beats': [
            b(1, grid_function=move_grid, vector=(0, 3), grid_skip_top_fill=True, length=79),
            b(1, grid_function=spawn_row, color=colors['white'], length=0.01),
            b(2, grid_function=spawn_row, color=colors['pink'], length=0.01),
        ]
    },



    "Deorro - Five Hours (Static Video) [LE7ELS]": {
        "bpm": 128,
        "song_path": "songs/Deorro - Five Hours (Static Video) [LE7ELS].ogg",
        "delay_lights": 0.37665,
        "skip_song": 0.0,
        "beats": [ 
            b(1, name='5 hours intro', length=79),
            b(79, name='RBBB 1 bar', length=1000),
            b(113, name='RBBB 1 bar', length=1000),
        ]
    }
}