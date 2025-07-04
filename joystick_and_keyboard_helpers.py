import os
import threading

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

from helpers import *

if not is_doorbell():
    from pynput.keyboard import Listener, KeyCode





def clear_events():
    if not ensure_init():
        return
    pygame.event.clear()

pygame_keyboard_normalized = {
    pygame.K_ESCAPE: 'quit',
    pygame.K_RETURN: 'enter',
    pygame.K_a: 'left',
    pygame.K_d: 'right',
    pygame.K_w: 'up',
    pygame.K_s: 'down',
    pygame.K_LEFT: 'left',
    pygame.K_RIGHT: 'right',
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_i: 'y',
    pygame.K_j: 'x',
    pygame.K_l: 'b',
    pygame.K_COMMA: 'a',
}
joystick_normalized = {
    3: 'y',
    0: 'a',
    1: 'b',
    2: 'x',
    6: 'back',
    7: 'start',
    # 11: 'right',
    # 12: 'left',
    # 13: 'up',
    # 14: 'down',
}

joyhat_x_mapping = {
    -1: 'right' if is_doorbell() else 'left',
    1: 'left' if is_doorbell() else 'right',
}
# idk if this is used
def invert_left_right_joystick():
    global joystick_normalized
    new_joystick_normalized = {}
    for keycode, normed_value in joystick_normalized.items():
        if normed_value == 'left':
            new_joystick_normalized[keycode] = 'right'
        elif normed_value == 'right':
            new_joystick_normalized[keycode] = 'left'
        else:
            new_joystick_normalized[keycode] = normed_value
    joystick_normalized = new_joystick_normalized

inited_stuff = None
def ensure_init():
    global inited_stuff
    if inited_stuff is None:
        try:
            pygame.init()
            pygame.joystick.init()
            inited_stuff = True
            return True
        except:
            print_stacktrace()
            print_red('PYGAME COULDNT INITIALIZE JOYSTICKS RETURNING NONE')
            return None
    return True

has_inited = set()
def ensure_joystick_init():
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        if joystick not in has_inited:
            joystick.init()
            has_inited.add(joystick)


keyboard_dict = {}
def add_keyboard_events(keys_and_functions):
    for key, function in keys_and_functions.items():
        if key in keyboard_dict:
            print_red(f'WARNING: {key} already in keyboard_dict, overwriting\n' * 40)
        keyboard_dict[key] = function
if is_linux() and not is_doorbell():
    _return_code, stdout, _stderr = run_command_blocking([
        'xdotool',
        'getactivewindow',
    ])    
    if not stdout.strip():
        original_process_window_id = None
    else:
        original_process_window_id = int(stdout.strip())
# https://stackoverflow.com/questions/24072790/how-to-detect-key-presses how to check window name (not global)
def has_window_focus():
    if is_linux():
        return_code, stdout, _stderr = run_command_blocking([
            'xdotool',
            'getwindowfocus',
        ])
        if return_code != 0:
            return False
        other = int(stdout.strip())
        return original_process_window_id == other
    return True


def key_norm(key):
    if type(key) == KeyCode:
        return key.char
    else:
        return key.name


def listen_to_keyboard():
    def on_press(key):
        if not has_window_focus(): 
            return
        key_name = key_norm(key)
        if key_name in keyboard_dict:
            keyboard_dict[key_name]()
        else:
            all_events.append(key_name)

    def on_release(key):
        pass
        # if not has_window_focus(): 
        #     return
        # key = key_norm(key)
        # if key_name in keyboard_dict:
        #     if type(keyboard_dict[key_name]) == str:
        #         remove_effect_name(keyboard_dict[key_name])
    
    def keyboard_listener():
        with Listener(on_press=on_press, on_release=on_release) as listener: 
            listener.join()
    threading.Thread(target=keyboard_listener, args=[], daemon=True).start()


all_events = []
def inputs_since_last_called():
    if not ensure_init():
        return
    ensure_joystick_init()

    for event in pygame.event.get():
        if not is_doorbell():
            pass
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button in joystick_normalized:
                all_events.append(joystick_normalized[event.button])
        if event.type == pygame.JOYHATMOTION:
            x, y = event.value
            if x != 0:
                all_events.append(joyhat_x_mapping[x])
            if y == -1:
                all_events.append('down')
            elif y == 1:
                all_events.append('up')
    copy_of_all_events = all_events.copy()
    all_events.clear()
    return copy_of_all_events

    # active_joystick = get_active_joystick()
    # if active_joystick is None:
    #     print('No active joystick found, so wont be processing those events')
    # if active_joystick is None:
    #     print('No active joystick found, so wont be processing those events')


        # if active_joystick is not None:
            # elif event.type == pygame.JOYAXISMOTION:
            #     joystick_direction = get_joystick_direction(active_joystick)
            #     yield joystick_direction
        


# def get_joystick_direction(controller, invert_lr=False):
#     x_axis, y_axis = controller.get_axis(0), controller.get_axis(1)
#     threshold = 0.5
#     if x_axis < -threshold:
#         return 'left' if invert_lr else 'right'
#     elif x_axis > threshold:
#         return 'right' if invert_lr else 'left'
#     elif y_axis < -threshold:
#         return 'up'
#     elif y_axis > threshold:
#         return 'down'
    




# inited_stuff = None
# def get_active_joystick():
#     global inited_stuff
#     if inited_stuff is None:
#         try:
#             pygame.init()
#             pygame.joystick.init()
#             inited_stuff = True
#         except:
#             print_stacktrace()
#             print_red('PYGAME COULDNT INITIALIZE JOYSTICKS RETURNING NONE')
#             return None

#     for joystick in get_available_joysticks(): 
#         if not joystick.get_init():
#             joystick.init()
#         return joystick
