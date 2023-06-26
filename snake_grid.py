import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import argparse
import time
import copy
import random
import collections

import keyboard
import serial

from helpers import *

grid_index = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, -1, -1], 
    [63, 62, 61, 60, 59, 58, 57, 56, 55, 54, 53, 52, 51, 50, 49, 48, 46, 45, 44, 43, 42, 40, 39, 38, 37, 36, 35, 34, 33, 32, -1, -1], 
    [64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 85, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, -1], 
    [127, 126, 125, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100, 99, 98, 97, -1], 
    [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159], 
    [191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160], 
    [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223], 
    [255, 254, 253, 252, 251, 250, 249, 248, 247, 246, 245, 244, 243, 242, 241, 240, 239, 238, 237, 236, 235, 234, 233, 232, 231, 230, 229, 228, 227, 226, 225, 224], 
    [256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287], 
    [319, 318, 317, 316, 315, 314, 313, 312, 311, 310, 309, 308, 307, 306, 305, 304, 303, 302, 301, 300, 299, 298, 297, 296, 295, 294, 293, 292, 291, 290, 289, 288], 
    [320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351], 
    [383, 382, 381, 380, 379, 378, 377, 376, 375, 374, 373, 372, 371, 370, 369, 368, 367, 366, 365, 364, 363, 362, 361, 360, 359, 358, 357, 356, 355, 354, 353, 352], 
    [384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415], 
    [447, 446, 445, 444, 443, 442, 441, 440, 439, 438, 437, 436, 435, 434, 433, 432, 431, 430, 429, 428, 427, 426, 425, 424, 423, 422, 421, 420, 419, 418, 417, 416], 
    [448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479], 
    [511, 510, 509, 508, 507, 506, 505, 504, 503, 502, 501, 500, 499, 498, 497, 496, 495, 494, 493, 492, 491, 490, 489, 488, 487, 486, 485, 484, 483, 482, 481, 480], 
    [512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543], 
    [575, 574, 573, 572, 571, 570, 569, 568, 567, 566, 565, 564, 563, 562, 561, 560, 559, 558, 557, 556, 555, 554, 553, 552, 551, 550, 549, 548, 547, 546, 545, 544], 
    [576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607], 
    [639, 638, 637, 636, 635, 634, 633, 632, 631, 630, 629, 628, 627, 626, 625, 624, 623, 622, 621, 620, 619, 618, 617, 616, 615, 614, 613, 612, 611, 610, 609, 608]
]

GRID_ROW_LENGTH = 20
GRID_COL_LENGTH = 32

grid = [None] * GRID_ROW_LENGTH
for x in range(GRID_ROW_LENGTH):
    grid[x] = [None] * GRID_COL_LENGTH
    for y in range(GRID_COL_LENGTH):
        grid[x][y] = [0, 0, 0]
init_grid = copy.deepcopy(grid)
grid_msg = [0] * (GRID_COL_LENGTH * GRID_ROW_LENGTH * 3)


# fill grid with rgb values to 0-100
def pack_grid_into_message():
    for x in range(GRID_ROW_LENGTH):
        for y in range(GRID_COL_LENGTH):
            index = grid_index[x][y] * 3            
            if index >= 0:
                grid_msg[index] = round(grid[x][y][0] * 127 / 100) * 2
                grid_msg[index + 1] = round(grid[x][y][1] * 127 / 100) * 2
                grid_msg[index + 2] = round(grid[x][y][2] * 127 / 100) * 2


def reset_grid():
    for x in range(GRID_ROW_LENGTH):
        for y in range(GRID_COL_LENGTH):
            grid[x][y] = [0, 0, 0]


def get_serial_communicator():
    return serial.Serial(
        port='/dev/ttyS0',
        baudrate = 2000000,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0,
        write_timeout=0
    )


class GameState:
    def __init__(self):
        self.player_head_pos = (GRID_COL_LENGTH // 2, GRID_ROW_LENGTH // 2)
        self.player_body_poses = collections.deque()
        self.food_pos = random_pos()
        self.frame = 0
        self.direction = 'left'


104/255
71/255
14/255
item_colors = {
    'player': [100, 100, 100],
    'empty': [10, 10, 10],
    'food': [40.7, 100, 0],
}
item_styles = {}
for item, color in item_colors.items():
    color_scaled = [round(c * 2.55) for c in color]
    item_styles[item] = f'rgb({color_scaled[0]},{color_scaled[1]},{color_scaled[2]})'

console = None
character = '○'
def render(serial_communicator, game_state):
    if serial_communicator:
        reset_grid()
        grid_out =  serial_communicator.out_waiting
        grid_in = serial_communicator.in_waiting

        if grid_out == 0 and grid_in > 0:
            pack_grid_into_message()
            serial_communicator.read(grid_in)
            serial_communicator.write(bytes(grid_msg))
    else:
        global console
        if console is None:
            from rich.console import Console
            console = Console()
        for y in range(GRID_COL_LENGTH):
            for x in range(GRID_ROW_LENGTH):
                index = grid_index[x][y] * 3
                if index >= 0:
                    style = item_styles['empty']
                    if game_state.player_head_pos == (x, y):
                        style = item_styles['player']
                    elif (x, y) in game_state.player_body_poses:
                        style = item_styles['player']
                    elif game_state.food_pos == (x, y):
                        style = item_styles['food']
                    console.print(character, style=style, end='')
                else:
                    console.print(' ', end='')
            console.print()


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
        return 'left'
    elif x_axis > threshold:
        return 'right'
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

        pygame.event.pump()
        current_button_state = [controller.get_button(i) for i in range(controller.get_numbuttons())]
        joystick_direction = get_joystick_direction(controller)

        if current_button_state[0]: # a button
            return 'enter'
        if current_button_state[1]: # b button
            return 'fps_up'
        if current_button_state[2]: # x button
            return 'fps_down'
        return joystick_direction


def in_bounds(pos):
    x, y = pos
    if x < 0 or x >= GRID_ROW_LENGTH or y < 0 or y >= GRID_COL_LENGTH:
        return False
    index = grid_index[x][y]
    if index < 0:
        return False
    return True


def legal(game_state, pos):
    if in_bounds(pos) and pos not in game_state.player_body_poses:
        return True
    return False


def random_pos():
    while True:
        x = random.randint(0, GRID_ROW_LENGTH - 1)
        y = random.randint(0, GRID_COL_LENGTH - 1)
        if in_bounds((x, y)):
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
states_per_second = 1.2
def play_game(serial_communicator, controller):
    global states_per_second
    fps = 60
    last_state_time = 0
    frame = 0

    game_state = GameState()
    while True:
        start_loop = time.time()
        input_read = read_input(controller)

        if input_read == 'quit':
            pygame.quit()
            exit(1)
        elif input_read == 'enter':
            print_yellow('Resetting game')
            return
        elif input_read == 'fps_up':
            print('fps_up', states_per_second)
            states_per_second += 0.1
        elif input_read == 'fps_down':
            states_per_second -= 0.1
        
        if (time.time() - last_state_time) > 1 / states_per_second:
            print_cyan(f'State frame {frame}')
            if input_read in ['left', 'right', 'up', 'down'] and input_read in allowed_turn[game_state.direction]:
                print(f'updated direction to {input_read}')
                game_state.direction = input_read
            print(input_read, allowed_turn[game_state.direction])

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
                game_state.player_body_poses.pop()
                game_state.player_body_poses.appendleft(last_head_pos)

            if game_state.player_head_pos == game_state.food_pos:
                game_state.player_body_poses.append(last_body_pos)
                print_green(f'Player ate food at {game_state.food_pos}')
                game_state.food_pos = random_pos()

            render(serial_communicator, game_state)
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
    if not args.local:
        disable_color()
        serial_communicator = get_serial_communicator()

    controller = init_controller()
    if controller is None:
        print_red("No controller found, using keyboard")
    if args.keyboard:
        controller = None

    while True:
        play_game(serial_communicator, controller)