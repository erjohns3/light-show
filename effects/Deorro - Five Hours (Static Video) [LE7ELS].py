from effects.compiler import b

import grid_helpers


grid = grid_helpers.get_grid()
def tech_move_up(grid_info):
    if grid_info.curr_sub_beat % 1 == 0:
        grid_helpers.grid_move([0, 3])


def tech_spawn_white_row(grid_info):
    print('SHOULD SPAWN\n' * 800)
    for x in range(grid_helpers.GRID_WIDTH):
        grid[x][0] = (100, 100, 100)
    exit()

effects = {
    '5 hours intro': {
        'length': 79,
        'beats': [
            b(1, grid_function=tech_spawn_white_row, length=0.1),
            b(1, grid_function=tech_move_up, grid_skip_top_fill=True, length=79),
            b(2, grid_function=tech_spawn_white_row, length=0.1),
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