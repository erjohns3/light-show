import pygame

from effects.compiler import *
from scripts import tetris_grid
import joystick_and_keyboard_helpers

def tetris(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1

    if grid_info.curr_sub_beat == grid_info.start_sub_beat:
        joystick_and_keyboard_helpers.clear_events()
        
    if tetris_grid.game_state is None:
        tetris_grid.start_new_game()

    for normalized_event in joystick_and_keyboard_helpers.inputs_since_last_called():
        if normalized_event == 'x':
            tetris_grid.start_new_game()
        elif normalized_event == 'left':
            tetris_grid.move_left()
        elif normalized_event == 'right':
            tetris_grid.move_right()
        elif normalized_event == 'b':
            tetris_grid.rotate()
        elif normalized_event == 'down':
            tetris_grid.move_down()
        elif normalized_event == 'a':
            tetris_grid.hard_drop()

    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        tetris_grid.advance_game_state()
    
    tetris_grid.fill_grid_with_game_state()



effects = {
    "tetris_flash": {
        "length": 1,
        "beats": [
            b(1, name='Red top', length=.25),
            grid_f(1.25, function=tetris, beat_divide=12, grid_skip_top_fill=True, length=.75),
        ]
    },
    "TETRIS THEME SONG (OFFICIAL TRAP REMIX) - DaBrozz": {
        "bpm": 143,
        "song_path": "songs/TETRIS THEME SONG (OFFICIAL TRAP REMIX) - DaBrozz.ogg",
        "delay_lights": 0.02155,
        "skip_song": 0.0,
        "beats": [
            grid_f(1, function=tetris, beat_divide=12, length=130),
            b(130, name='tetris_flash', length=1000),
        ]
    }
}