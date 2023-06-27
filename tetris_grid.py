import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ["SDL_VIDEODRIVER"] = "dummy"
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
GRID_COL_LENGTH = 30

grid = [None] * GRID_ROW_LENGTH
for x in range(GRID_ROW_LENGTH):
    grid[x] = [None] * GRID_COL_LENGTH
    for y in range(GRID_COL_LENGTH):
        grid[x][y] = [0, 0, 0]
init_grid = copy.deepcopy(grid)
grid_msg = [0] * (GRID_COL_LENGTH * GRID_ROW_LENGTH * 3)

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
class GameState:
    def __init__(self):
        self.p_name = None
        self.p_anchor = None
        self.p_rotation = None
        self.board = [[None for y in range(GRID_COL_LENGTH)] for x in range(GRID_ROW_LENGTH)]

    def __repr__(self):
        return f'GameState({self.p_name}, {self.p_anchor}, {self.p_rotation})'


item_colors = {
    'active_piece': [0, 100, 0],
    'dead_square': [0, 0, 100],
    'flash': [100, 100, 100],
    'empty': [.8, 0, 0],
}

item_colors_keyboard = {
    'active_piece': blue('▓'),
    'dead_square': red('▓'),
    'flash': green('▓'),
    'empty': '○',
}
character = '○'
def render(serial_communicator, game_state):
    active_poses = set()
    if game_state.p_name is not None:
        active_poses = set(get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor))
    if serial_communicator:
        for x in range(GRID_ROW_LENGTH):
            for y in range(GRID_COL_LENGTH):
                index = grid_index[x][y] * 3
                if index >= 0:
                    if (x, y) in active_poses:
                        grid[x][y] = item_colors['active_piece']
                    elif game_state.board[x][y] is not None:
                        grid[x][y] = item_colors['dead_square']
                    else:
                        grid[x][y] = item_colors['empty']

        grid_out =  serial_communicator.out_waiting
        grid_in = serial_communicator.in_waiting

        if grid_out == 0 and grid_in > 0:
            pack_grid_into_message()
            serial_communicator.read(grid_in)
            serial_communicator.write(bytes(grid_msg))
    else:    
        for y in range(GRID_COL_LENGTH):
            row = []
            for x in range(GRID_ROW_LENGTH):
                index = grid_index[x][y] * 3
                if index >= 0:
                    if (x, y) in active_poses:
                        row.append(item_colors_keyboard['active_piece'])
                    elif game_state.board[x][y] is not None:
                        row.append(item_colors_keyboard['dead_square'])
                    else:
                        row.append(item_colors_keyboard['empty'])
            print(''.join(row))


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


last_key_pressed = None
def on_key_event(event):
    global last_key_pressed
    last_key_pressed = event.name
    # print(f"Key {event.name} was {'pressed' if event.event_type == keyboard.KEY_DOWN else 'released'}")
keyboard.on_press(on_key_event)
keyboard.on_release(on_key_event)

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


def in_bounds(pos):
    x, y = pos
    if x < 0 or x >= GRID_ROW_LENGTH or y < 0 or y >= GRID_COL_LENGTH:
        return False
    index = grid_index[x][y]
    if index < 0:
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


directions = {
    'left': [-1, 0],
    'right': [1, 0],
    'up': [0, -1],
    'down': [0, 1],
}
states_per_second = 4
def play_game(serial_communicator, controller):
    global states_per_second
    fps = 40
    last_state_time = 0
    frame = 0

    game_state = GameState()
    while True:
        start_loop = time.time()
        input_read = read_input(controller)
        graphics_changed = False

        if input_read == 'quit':
            if not args.local:
                reset_grid()
                pack_grid_into_message()
                serial_communicator.write(bytes(grid_msg))
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
                game_state.p_rotation = (game_state.p_rotation + 1) % 4
                graphics_changed = True
            elif input_read == 'down':
                new_p_anchor = add_points(game_state.p_anchor, directions['down'])
                if is_anchor_safe(game_state, new_p_anchor):
                    game_state.p_anchor = new_p_anchor
                    graphics_changed = True

        if (time.time() - last_state_time) > 1 / states_per_second:
            print_cyan(f'State frame {frame}')
            if game_state.p_name is None:
                game_state.p_name = random.choice(list(pieces.keys()))
                game_state.p_anchor = [GRID_ROW_LENGTH // 2, 0]
                game_state.p_rotation = 0
                for pos in get_board_points(game_state.p_name, game_state.p_rotation, game_state.p_anchor):
                    if not is_avail(game_state, pos):
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
                    graphics_changed = True

                    # check for full rows
                    print('would check for full rows now')
                    for row in range(GRID_COL_LENGTH):
                        pass
                        # if None not in game_state.board[row]:
                        #     for col in range(GRID_ROW_LENGTH):
                        #         game_state.board[row][col] = None
                        #     for row2 in range(row, 0, -1):
                        #         game_state.board[row2] = game_state.board[row2 - 1]
                        #     game_state.board[0] = [None] * GRID_ROW_LENGTH

            if graphics_changed:
                render(serial_communicator, game_state)
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
    if not args.local:
        disable_color()
        serial_communicator = get_serial_communicator()

    controller = init_controller()
    if controller is None:
        print_red("No controller found, using keyboard")
    if args.keyboard:
        controller = None

    # while True:
    play_game(serial_communicator, controller)