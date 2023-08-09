import os
import argparse
import time
import random
import signal
import sys
import pathlib

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
import script_helpers
script_helpers.make_directory_above_importable()

from helpers import *
import grid_helpers
import joystick_and_keyboard_helpers


PONG_X_OFFSET = 0
PONG_Y_OFFSET = 0

GRID_BLOCK_SIZE = 1
PONG_WIDTH = 20
PONG_HEIGHT = 32

PLAYER_WIDTH = 3

class PongGameState:
    def __init__(self):
        self.player_1 = [PONG_WIDTH // 2, PONG_HEIGHT - 1]
        self.player_2 = [PONG_WIDTH // 2, 0]
        self.ball = [PONG_WIDTH // 2, PONG_HEIGHT // 2]
        self.ball_direction = random.choice([[-1, -1], [1, -1], [-1, 1], [1, 1]])

    def __repr__(self):
        return f'PongGameState({self.player_1=}, {self.player_2=}, {self.ball=}, {self.ball_direction})'


block_colors = {
    'player': [100, 100, 100],
    'empty': [0, 0, 1],
    'ball': [0, 100, 0],
    'out_of_bounds': [0, 0, 0],
}
def fill_grid_with_game_state():
    for g_x, g_y in grid_helpers.coords():
        x = (g_x // 2) - PONG_X_OFFSET
        y = (g_y // 2) + PONG_Y_OFFSET
        if grid_helpers.visible_coord((g_x, g_y)):
            if x < 0 or x >= PONG_WIDTH or y < 0 or y >= PONG_HEIGHT:
                grid_helpers.grid[g_x][g_y] = block_colors['out_of_bounds']
            elif x == game_state.ball[0] and y == game_state.ball[1]:
                grid_helpers.grid[g_x][g_y] = block_colors['ball']
            elif y == game_state.player_1[1] and x in [game_state.player_1[0] + z for z in range(PLAYER_WIDTH)]:
                grid_helpers.grid[g_x][g_y] = block_colors['player']            
            elif y == game_state.player_2[1] and x in [game_state.player_2[0] + z for z in range(PLAYER_WIDTH)]:
                grid_helpers.grid[g_x][g_y] = block_colors['player']


def in_bounds(pos):
    x, y = pos
    if x < 0 or x >= PONG_WIDTH or y < 0 or y >= PONG_HEIGHT:
        return False
    return True


def is_avail(game_state, pos):
    x, y = pos
    if in_bounds(pos) and game_state.board[x][y] == None:
        return True
    return False


def add_points(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


game_state = None
def start_new_game():
    global game_state
    game_state = PongGameState()



directions = {
    'left': [-1, 0],
    'right': [1, 0],
    'up': [0, -1],
    'down': [0, 1],
}
def move_player_1_left():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_point = add_points(game_state.player_1, directions['left'])
    if new_point[0] < 0:
        return
    game_state.player_1 = new_point


def move_player_2_left():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_point = add_points(game_state.player_1, directions['left'])
    if new_point[0] < 0:
        return
    game_state.player_2 = new_point


def move_player_1_right():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_point = add_points(game_state.player_1, directions['right'])
    if new_point[0] + PLAYER_WIDTH > PONG_WIDTH:
        return
    game_state.player_1 = new_point


def move_player_2_right():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_point = add_points(game_state.player_1, directions['right'])
    if new_point[0] + PLAYER_WIDTH > PONG_WIDTH:
        return
    game_state.player_2 = new_point


def advance_game_state():
    if game_state is None:
        print_red(f'game_state is none, returning')
        return
    new_ball_point = add_points(game_state.ball, game_state.ball_direction)
    if not in_bounds(new_ball_point):
        return start_new_game()
    if new_ball_point[1] == game_state.player_1[1] and new_ball_point[0] in [game_state.player_1[0] + z for z in range(PLAYER_WIDTH)]:
        game_state.ball_direction[1] *= -1
        new_ball_point[1] += game_state.ball_direction[1] * 2

    if new_ball_point[1] == game_state.player_2[1] and new_ball_point[0] in [game_state.player_2[0] + z for z in range(PLAYER_WIDTH)]:
        game_state.ball_direction[1] *= -1
        new_ball_point[1] += game_state.ball_direction[1] * 2

    if new_ball_point[0] == 0 or new_ball_point[0] == PONG_WIDTH - 1:
        game_state.ball_direction[0] *= -1
        new_ball_point[0] += game_state.ball_direction[0] * 2

    game_state.ball = new_ball_point


states_per_second = 4
def play_game_main():
    global states_per_second, game_state
    fps = 60
    last_state_time = 0
    frame = 0

    game_state = PongGameState()
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
            if normalized_input == 'left':
                move_player_1_left()
            if normalized_input == 'right':
                move_player_1_right()

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