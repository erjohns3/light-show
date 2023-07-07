import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import argparse
import time
import random
import signal
import sys

import keyboard

import script_helpers
script_helpers.make_directory_above_importable()

from helpers import *
import grid_helpers

grid = grid_helpers.get_grid()
GRID_WIDTH = grid_helpers.get_grid_width()
GRID_HEIGHT = grid_helpers.get_grid_height()

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



def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    grid_helpers.grid_reset_and_write()
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)




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
        return f'TGameState({self.p_name}, {self.p_anchor}, {self.p_rotation})'


block_colors = {
    'active_piece': [0, 100, 0],
    'dead_square': [0, 5, 0],
    'flash': [100, 100, 100],
    'empty': [.8, 0, 0],
    'out_of_bounds': [0, 0, 0],
}
def fill_grid_and_render(game_state):
    active_poses = set()
    if game_state.p_name is not None:
        active_poses = set(get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor))

    for g_x, g_y in grid_helpers.grid_coords():
        x = (g_x // 2) - TETRIS_X_OFFSET
        y = (g_y // 2) + TETRIS_Y_OFFSET
        if grid_helpers.grid_in_bounds((g_x, g_y)):
            if x < 0 or x >= TETRIS_WIDTH or y < 0 or y >= TETRIS_HEIGHT:
                grid[g_x][g_y] = block_colors['out_of_bounds']
            elif (x, y) in active_poses:
                grid[g_x][g_y] = block_colors['active_piece']
            elif game_state.board[x][y] is not None:
                grid[g_x][g_y] = block_colors['dead_square']
            else:
                grid[g_x][g_y] = block_colors['empty']
    grid_helpers.render_grid(terminal=args.local)


def try_get_gamepad_controller():
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        controller = pygame.joystick.Joystick(0)
        controller.init()
        return controller
    return None


def get_joystick_direction(controller):
    x_axis = controller.get_axis(0)
    y_axis = controller.get_axis(1)
    threshold = 0.5
    if x_axis < -threshold:
        if args.local:
            return 'left'
        else:
            return 'right'
    elif x_axis > threshold:
        if args.local:
            return 'right'
        else:
            return 'left'
    elif y_axis < -threshold:
        return 'up'
    elif y_axis > threshold:
        return 'down'
    return None


last_key_pressed = None
def on_key_event(event):
    global last_key_pressed
    last_key_pressed = event.name
    # print(f"Key {event.name} was {'pressed' if event.event_type == keyboard.KEY_DOWN else 'released'}")

keyboard_mappings = {
    'esc': 'quit',
    'enter': 'enter',
    'a': 'left',
    'd': 'right',
    'w': 'up',
    's': 'down',
    'left': 'left',
    'right': 'right',
    'up': 'up',
    'down': 'down',
    'q': 'fps_down',
    'e': 'fps_up',
}
joy_button_mapping = {
    3: 'quit',
    0: 'enter',
    1: 'fps_up',
    2: 'fps_down',
    11: 'right',
    12: 'left',
    13: 'up',
    14: 'down',
}
def read_input(controller):
    if controller is None:
        global last_key_pressed
        if last_key_pressed in keyboard_mappings:
            temp = last_key_pressed
            last_key_pressed = None
            return keyboard_mappings[temp]
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in joy_button_mapping:
                    return joy_button_mapping[event.button]
        
        pygame.event.pump()
        joystick_direction = get_joystick_direction(controller)
        return joystick_direction


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


def clear_y(game_state, y):
    for x2 in range(TETRIS_WIDTH):
        game_state.board[x2][y] = None
    for x2 in range(TETRIS_WIDTH):
        for y2 in range(y, 0, -1):
            game_state.board[x2][y2] = game_state.board[x2][y2 - 1]
    for x2 in range(TETRIS_WIDTH):
        game_state.board[x2][0] = None


def tetris_game_for_grid():
    pass


directions = {
    'left': [-1, 0],
    'right': [1, 0],
    'up': [0, -1],
    'down': [0, 1],
}
states_per_second = 4
def play_game(serial_communicator, controller):
    global states_per_second
    fps = 60
    last_state_time = 0
    frame = 0

    game_state = TetrisGameState()
    while True:
        start_loop = time.time()
        input_read = read_input(controller)
        graphics_changed = False

        if input_read == 'quit':
            if not args.local:
                grid_helpers.grid_reset_and_write()
            pygame.quit()
            exit(1)
        elif input_read == 'enter':
            print_yellow('Resetting game')
            return
        elif input_read == 'fps_up':
            print('fps_up', states_per_second)
            states_per_second += 0.5
        elif input_read == 'fps_down':
            states_per_second -= 0.5
        if game_state.p_name is not None and input_read in ['left', 'right', 'up', 'down']:
            if input_read in ['left', 'right']:
                new_p_anchor = add_points(game_state.p_anchor, directions[input_read])
                if is_anchor_safe(game_state, new_p_anchor):
                    game_state.p_anchor = new_p_anchor
                    graphics_changed = True
            elif input_read == 'up':
                game_state.p_rotation = game_state.p_rotation - 1
                if game_state.p_rotation < 0:
                    game_state.p_rotation = 3
                graphics_changed = True
            elif input_read == 'down':
                new_p_anchor = add_points(game_state.p_anchor, directions['down'])
                if is_anchor_safe(game_state, new_p_anchor):
                    game_state.p_anchor = new_p_anchor
                    graphics_changed = True

        if (time.time() - last_state_time) > 1 / states_per_second:
            # print_cyan(f'State frame {frame}')
            if game_state.p_name is None:
                game_state.p_name = random.choice(list(pieces.keys()))
                game_state.p_anchor = [(TETRIS_WIDTH // 2) - 2, 0]
                game_state.p_rotation = 0
                for pos in get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor):
                    if not is_avail(game_state, pos):
                        print('pos', pos, 'not avail')
                        fill_grid_and_render(game_state)
                        print_red('Game over!')
                        return
            else:
                new_p_anchor = add_points(game_state.p_anchor, directions['down'])
                if is_anchor_safe(game_state, new_p_anchor):
                    game_state.p_anchor = new_p_anchor
                    graphics_changed = True
                else:
                    for pos in get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor):
                        game_state.board[pos[0]][pos[1]] = 1
                    game_state.p_name = None
                    game_state.p_anchor = None
                    game_state.p_rotation = None

                    for y in range(TETRIS_HEIGHT):
                        clear = True
                        for x in range(TETRIS_WIDTH):
                            if game_state.board[x][y] is None:
                                clear = False
                                break
                        if clear:
                            clear_y(game_state, y)
                    graphics_changed = True

            if graphics_changed:
                fill_grid_and_render(game_state)
            if frame == 1:
                exit()
            last_state_time = time.time()

        to_wait = 1 / fps - (time.time() - start_loop)
        if to_wait > 0:
            time.sleep(to_wait)
        frame += 1


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--keyboard', action='store_true')
    argparse.add_argument('--local', action='store_true')
    args = argparse.parse_args()

    serial_communicator = None
    if args.local:
        # !TODO find alternative that works for linux
        keyboard.on_press(on_key_event)
        keyboard.on_release(on_key_event)

        # !TODO long term I really should just be rendering to terminal whats visible on grid
        block_colors = {
            'active_piece': [0, 100, 0],
            'dead_square': [0, 80, 0],
            'flash': [100, 100, 100],
            'empty': [30, 0, 0],
            'out_of_bounds': [0, 0, 0],
        }
    else:
        disable_color()
        serial_communicator = grid_helpers.get_grid_serial()

    controller = try_get_gamepad_controller()
    if controller is None:
        print_red('No controller found, using keyboard')
    if args.keyboard:
        controller = None

    while True:
        play_game(serial_communicator, controller)