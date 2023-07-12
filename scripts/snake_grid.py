import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
import argparse
import time
import random
import collections

import keyboard

import script_helpers
script_helpers.make_directory_above_importable()

import grid_helpers
from helpers import *


class SnakeGameState:
    def __init__(self):
        self.player_head_pos = (grid_helpers.get_grid_width() // 2, grid_helpers.get_grid_height() // 2)
        self.player_body_poses = collections.deque()
        self.food_pos = random_pos()
        self.frame = 0
        self.direction = 'left'


item_colors = {
    'player': [100, 100, 100],
    'empty': [.8, 0, 0],
    'food': [0, 100, 0],
}
item_styles = {}
for item, color in item_colors.items():
    color_scaled = [round(c * 2.55) for c in color]
    item_styles[item] = f'rgb({color_scaled[0]},{color_scaled[1]},{color_scaled[2]})'

def render(game_state):
    for g_x, g_y in grid_helpers.coords():
        if grid_helpers.visible_coord((g_x, g_y)):
            if (g_x, g_y) == game_state.player_head_pos or (g_x, g_y) in game_state.player_body_poses:
                grid_helpers.grid[g_x][g_y] = item_colors['player']
            elif (g_x, g_y) == game_state.food_pos:
                grid_helpers.grid[g_x][g_y] = item_colors['food']
            else:
                grid_helpers.grid[g_x][g_y] = item_colors['empty']
    grid_helpers.render(terminal=args.local)


def init_controller():
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


keyboard_mappings = {
    'esc': 'quit',
    'enter': 'enter',
    'a': 'left',
    'd': 'right',
    'w': 'up',
    's': 'down',
    'q': 'fps_down',
    'e': 'fps_up',
}
def read_input(controller):
    if controller is None:
        if keyboard.is_pressed('q'):
            return 'quit'
        for key in keyboard_mappings:
            if keyboard.is_pressed(key):
                return keyboard_mappings[key]
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.JOYBUTTONDOWN:
                button_index = event.button
                if button_index == 3: 
                    return 'quit'
                if button_index == 0: # a button
                    return 'enter'
                if button_index == 1: # b button
                    return 'fps_up'
                if button_index == 2: # x button
                    return 'fps_down'
        pygame.event.pump()
        joystick_direction = get_joystick_direction(controller)
        return joystick_direction



def legal(game_state, pos):
    if grid_helpers.visible_coord(pos) and pos not in game_state.player_body_poses:
        return True
    return False


def random_pos():
    while True:
        x = random.randint(0, grid_helpers.get_grid_width() - 1)
        y = random.randint(0, grid_helpers.get_grid_height() - 1)
        if grid_helpers.visible_coord((x, y)):
            return (x, y)


directions = {
    'left': [-1, 0],
    'right': [1, 0],
    'up': [0, -1],
    'down': [0, 1],
}
allowed_turn = {
    'left': ['up', 'down'],
    'right': ['up', 'down'],
    'up': ['left', 'right'],
    'down': ['left', 'right'],
}
states_per_second = 4
pending_action = None
to_blank = None
def play_game(controller):
    global states_per_second, pending_action, to_blank
    fps = 60
    last_state_time = 0
    frame = 0

    game_state = SnakeGameState()
    while True:
        start_loop = time.time()
        input_read = read_input(controller)

        if input_read == 'quit':
            if not args.local:
                grid_helpers.reset()
                grid_helpers.render()
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
        if input_read in ['left', 'right', 'up', 'down']:
            pending_action = input_read

        if (time.time() - last_state_time) > 1 / states_per_second:
            print_cyan(f'State frame {frame}')
            if pending_action in ['left', 'right', 'up', 'down'] and pending_action in allowed_turn[game_state.direction]:
                print(f'updated direction to {pending_action}')
                game_state.direction = pending_action
            print(pending_action, allowed_turn[game_state.direction])

            last_head_pos = game_state.player_head_pos
            last_body_pos = (game_state.player_body_poses and game_state.player_body_poses[-1]) or game_state.player_head_pos
            d = directions[game_state.direction]
            new_player_pos = (game_state.player_head_pos[0] + d[0], game_state.player_head_pos[1] + d[1])
            if not legal(game_state, new_player_pos):
                print_red('player lost, resetting game')
                return

            game_state.player_head_pos = new_player_pos
            print_green(f'Player moved to {new_player_pos}')

            if game_state.player_body_poses:
                to_blank = game_state.player_body_poses.pop()
                game_state.player_body_poses.appendleft(last_head_pos)

            if game_state.player_head_pos == game_state.food_pos:
                game_state.player_body_poses.append(last_body_pos)
                print_green(f'Player ate food at {game_state.food_pos}')
                game_state.food_pos = random_pos()

            render(game_state)
            last_state_time = time.time()
            pending_action = None

        to_wait = 1 / fps - (time.time() - start_loop)
        if to_wait > 0:
            time.sleep(to_wait)
        frame += 1


if __name__ == "__main__":
    argparse = argparse.ArgumentParser()
    argparse.add_argument('--keyboard', action='store_true')
    argparse.add_argument('--local', action='store_true')
    args = argparse.parse_args()

    if not args.local:
        disable_color()

    controller = init_controller()
    if controller is None:
        print_red("No controller found, using keyboard")
    if args.keyboard:
        controller = None

    while True:
        play_game(controller)