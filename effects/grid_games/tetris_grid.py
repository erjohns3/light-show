import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import argparse
import time
import random
import signal
import sys
import pathlib


this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
sys.path.insert(0, str(this_file_directory.parent))

from helpers import *
import grid_helpers
import joystick_and_keyboard_helpers

# TETRIS_X_OFFSET = 3
# TETRIS_Y_OFFSET = 1

# GRID_BLOCK_SIZE = 1
# TETRIS_WIDTH = 10
# TETRIS_HEIGHT = 20


TETRIS_X_OFFSET = 0
TETRIS_Y_OFFSET = 0

GRID_BLOCK_SIZE = 2
TETRIS_WIDTH = 10
TETRIS_HEIGHT = 15



# https://static.wikia.nocookie.net/tetrisconcept/images/3/3d/SRS-pieces.png/revision/latest?cb=20060626173148
pieces = {
    'line': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    'square': [
        [(1, 0), (1, 1), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (2, 0), (2, 1)],       
    ],
    'T': [
        [(0, 1), (1, 1), (2, 1), (1, 0)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 1)],
    ],
    'L': [
        [(0, 1), (1, 1), (2, 1), (2, 0)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 0)],
    ],
    'J': [
        [(0, 1), (1, 1), (2, 1), (0, 0)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (0, 2)],
    ],
    'S': [
        [(0, 1), (1, 1), (1, 0), (2, 0)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 2), (1, 2), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 2), (1, 2), (1, 1), (2, 1)],
        [(0, 1), (0, 2), (1, 1), (1, 0)],
    ],
}
class TetrisGameState:
    def __init__(self):
        self.p_name = None
        self.p_anchor = None
        self.p_rotation = None
        self.board = [[None for y in range(TETRIS_HEIGHT)] for x in range(TETRIS_WIDTH)]

    def __repr__(self):
        return f'TetrisGameState({self.p_name}, {self.p_anchor}, {self.p_rotation})'


block_colors = {
    'active_piece': [0, 100, 0],
    'dead_square': [0, 50, 0],
    'flash': [100, 100, 100],
    'empty': [0, 0, 10],
    'out_of_bounds': [0, 0, 0],
}
def fill_grid_with_game_state():
    active_poses = set()
    if game_state.p_name is not None:
        active_poses = set(get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor))

    for g_x, g_y in grid_helpers.coords():
        x = (g_x // 2) - TETRIS_X_OFFSET
        y = (g_y // 2) + TETRIS_Y_OFFSET
        if grid_helpers.visible_coord((g_x, g_y)):
            if x < 0 or x >= TETRIS_WIDTH or y < 0 or y >= TETRIS_HEIGHT:
                grid_helpers.grid[g_x][g_y] = block_colors['out_of_bounds']
            elif (x, y) in active_poses:
                grid_helpers.grid[g_x][g_y] = block_colors['active_piece']
            elif game_state.board[x][y] is not None:
                grid_helpers.grid[g_x][g_y] = block_colors['dead_square']
            else:
                grid_helpers.grid[g_x][g_y] = block_colors['empty']


def in_bounds(pos):
    x, y = pos
    if x < 0 or x >= TETRIS_WIDTH or y < 0 or y >= TETRIS_HEIGHT:
        return False
    return True


def is_avail(game_state, pos):
    x, y = pos
    if in_bounds(pos) and game_state.board[x][y] == None:
        return True
    return False


def add_points(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def get_board_points(p_name, p_rotation, p_anchor):
    for pos in pieces[p_name][p_rotation]:
        yield add_points(p_anchor, pos)


def is_anchor_safe(game_state, p_anchor):
    for pos in get_board_points(game_state.p_name, game_state.p_rotation, p_anchor):
        if not is_avail(game_state, pos):
            return False
    return True


def clear_y(y):
    for x2 in range(TETRIS_WIDTH):
        game_state.board[x2][y] = None
    for x2 in range(TETRIS_WIDTH):
        for y2 in range(y, 0, -1):
            game_state.board[x2][y2] = game_state.board[x2][y2 - 1]
    for x2 in range(TETRIS_WIDTH):
        game_state.board[x2][0] = None


game_state = None
def start_new_game():
    global game_state
    game_state = TetrisGameState()
    spawn_new_piece()


directions = {
    'left': [-1, 0],
    'right': [1, 0],
    'up': [0, -1],
    'down': [0, 1],
}
def move_left():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_anchor = add_points(game_state.p_anchor, directions['left'])
    if is_anchor_safe(game_state, new_anchor):
        game_state.p_anchor = new_anchor
    
def move_right():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_anchor = add_points(game_state.p_anchor, directions['right'])
    if is_anchor_safe(game_state, new_anchor):
        game_state.p_anchor = new_anchor

def move_down():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_anchor = add_points(game_state.p_anchor, directions['down'])
    if is_anchor_safe(game_state, new_anchor):
        game_state.p_anchor = new_anchor
        return True
    else:
        for pos in get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor):
            x, y = pos
            game_state.board[x][y] = game_state.p_name

        for y in range(TETRIS_HEIGHT):
            if all(game_state.board[x][y] is not None for x in range(TETRIS_WIDTH)):
                clear_y(y)
        if not spawn_new_piece():
            start_new_game()
        return False


def rotate_left():
    temp = game_state.p_rotation - 1
    if temp < 0:
        temp = 3
    rotate(temp)


def rotate_right():
    rotate((game_state.p_rotation + 1) % 4)


def try_safe_anchor(piece_name, anchor, rotation_index):
    for (x, y) in get_board_points(piece_name, rotation_index, anchor):
        if x < 0:
            return add_points(anchor, directions['right'])
        elif x >= TETRIS_WIDTH:
            return add_points(anchor, directions['left'])
        elif y >= TETRIS_HEIGHT:
            return add_points(anchor, directions['up'])
        elif game_state.board[x][y] is not None:
            return add_points(anchor, directions['up'])


def rotate(rotation_index):
    if game_state is None:
        print_red(f'game_state is none, returning')
        return

    new_anchor = game_state.p_anchor
    while True:
        potential_new_anchor = try_safe_anchor(game_state.p_name, new_anchor, rotation_index)
        if potential_new_anchor is None:
            break
        new_anchor = potential_new_anchor

    game_state.p_anchor = new_anchor
    game_state.p_rotation = rotation_index


def spawn_new_piece():
    game_state.p_name = random.choice(list(pieces.keys()))
    game_state.p_anchor = [(TETRIS_WIDTH // 2) - 2, 0]
    game_state.p_rotation = 0
    for pos in get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor):
        if not is_avail(game_state, pos):
            print_red('Game over!')
            return False
    return True


def hard_drop():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    while move_down():
        pass


def advance_game_state():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    move_down()


states_per_second = 4
def play_game_main():
    global states_per_second, game_state
    fps = 60
    last_state_time = 0
    frame = 0

    game_state = TetrisGameState()
    spawn_new_piece()
    start_loop = time.time()
    while True:
        for normalized_input in joystick_and_keyboard_helpers.inputs_since_last_called():
            if normalized_input == 'quit':
                if not args.local:
                    grid_helpers.reset()
                    grid_helpers.render()
                pygame.quit()
                exit(1)
            elif normalized_input == 'y':
                print_yellow('Resetting game')
                return
            elif normalized_input == 'back':
                states_per_second = max(.001, states_per_second - 0.5)
            elif normalized_input == 'start':
                states_per_second += 0.5
            elif normalized_input == 'a':
                hard_drop()
            elif normalized_input == 'x':
                rotate_left()
            elif normalized_input == 'b':
                rotate_right()
            if normalized_input == 'left':
                move_left()
            if normalized_input == 'right':
                move_right()
            elif normalized_input == 'down':
                move_down()

        if (time.time() - last_state_time) > 1 / states_per_second:
            advance_game_state()
            fill_grid_with_game_state()
            grid_helpers.render(terminal=args.local)
            last_state_time = time.time()

        to_wait = 1 / fps - (time.time() - start_loop)
        if to_wait > 0:
            time.sleep(to_wait)
        frame += 1


if __name__ == "__main__":
    def signal_handler(sig, frame):
        print('SIG Handler in tetris_grid.py: ' + str(sig), flush=True)
        if not args.local:
            grid_helpers.reset()
            grid_helpers.render()
        sys.exit()

    argparse = argparse.ArgumentParser()
    argparse.add_argument('--keyboard', action='store_true')
    argparse.add_argument('--local', action='store_true')
    argparse.add_argument('--rotate', dest='rotate_terminal', action='store_true')
    args = argparse.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while True:
        play_game_main()