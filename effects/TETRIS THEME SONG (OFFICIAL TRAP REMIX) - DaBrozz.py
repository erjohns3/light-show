import pygame

from effects.compiler import *
from scripts import tetris_grid
import joystick_and_keyboard_helpers


def start_new_tetris_game(grid_info):
    tetris_grid.start_new_game()


def tetris(grid_info):
    if getattr(grid_info, 'beat_divide', None) is None:
        grid_info.beat_divide = 1

    if grid_info.curr_sub_beat == grid_info.start_sub_beat:
        joystick_and_keyboard_helpers.clear_events()
        
    if tetris_grid.game_state is None:
        tetris_grid.start_new_game()

    for normalized_event in joystick_and_keyboard_helpers.inputs_since_last_called():
        if normalized_event == 'y':
            tetris_grid.start_new_game()
        elif normalized_event == 'left':
            tetris_grid.move_left()
        elif normalized_event == 'right':
            tetris_grid.move_right()
        elif normalized_event == 'x':
            tetris_grid.rotate_left()
        elif normalized_event == 'b':
            tetris_grid.rotate_right()
        elif normalized_event == 'down':
            tetris_grid.move_down()
        elif normalized_event == 'a':
            tetris_grid.hard_drop()

    if grid_info.curr_sub_beat % grid_info.beat_divide == 0:
        tetris_grid.advance_game_state()
    
    tetris_grid.fill_grid_with_game_state()



effects = {
    "tetris drop": {
        "length": 1,
        "beats": [
            b(1, name='Red top', length=.50),
            grid_f(1.50, function=tetris, beat_divide=12, grid_skip_top_fill=True, length=.50),
        ]
    },
    "TETRIS THEME SONG (OFFICIAL TRAP REMIX) - DaBrozz": {
        "bpm": 143,
        "song_path": "songs/TETRIS THEME SONG (OFFICIAL TRAP REMIX) - DaBrozz.ogg",
        "delay_lights": 0,
        "skip_song": 0.0,
        "beats": [
            grid_f(1, function=start_new_tetris_game, length=0.01),

            grid_f(1, function=tetris, beat_divide=12, grid_skip_top_fill=True, length=129),
            grid_f(128, text='OY', font_size=8, grid_skip_top_fill=True, length=1),
            b(129, name='tetris drop', length=64),
            grid_f(193, function=tetris, grid_skip_top_fill=True, beat_divide=12, length=129),
        ]
    }
}