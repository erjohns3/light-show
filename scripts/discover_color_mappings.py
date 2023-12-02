# sudo -E python discover_color_mappings.py

import pathlib
import sys
import signal
import json

# import keyboard
from sshkeyboard import listen_keyboard

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory.parent))

import grid_helpers
from effects.compiler import GridInfo
from helpers import *



def signal_handler(sig, frame):
    print('SIG Handler inside discover_color_mappings.py: ' + str(sig), flush=True)
    grid_helpers.reset()
    grid_helpers.render()
    sys.exit()


def on_press(key):
    # print(f'{key=} pressed')
    key_name = key

    if key_name in keyboard_dict:
        keyboard_dict[key_name]()
    else:
        print(f'key {key_name} not in keyboard_dict')

def on_release(key):
    pass
    # print(f'key {key} released')


rgb_index_to_letter = {
    0: 'red',
    1: 'green',
    2: 'blue',
}
letter_to_rgb_index = {v: k for k, v in rgb_index_to_letter.items()}
def load_output_mappings(filepath):
    global real_color, term_color

    try:
        with open(filepath) as f:
            initial_mapping_read = json.load(f)
    except:
        print_stacktrace()
        print_red(f'warning load_output_mappings() failed to load {filepath}, stack trace above, initing to nothing')
        initial_mapping_read = {}
        real_color = (100, 0, 0)
        term_color = (10, 0, 0)  
  
    output_mappings = {}
    for letter, sub_map_arr in initial_mapping_read.items():
        rgb_index = letter_to_rgb_index[letter]
        
        for sub_map in sub_map_arr:
            real = sub_map['real_color']
            term = sub_map['term_color']
            make_real = [0, 0, 0] 
            make_term = [0, 0, 0]
            make_real[rgb_index] = real
            make_term[rgb_index] = term
            output_mappings[tuple(make_real)] = tuple(make_term)
    return output_mappings


def write_output_mappings(filepath):
    to_dump = {}

    for real_color, term_color in output_mappings.items():
        for rgb_index, value in enumerate(real_color):
            if value:
                break
        if rgb_index_to_letter[rgb_index] not in to_dump:
            to_dump[rgb_index_to_letter[rgb_index]] = []
        to_dump[rgb_index_to_letter[rgb_index]].append({
            'real_color': real_color[rgb_index],
            'term_color': term_color[rgb_index],
        })

    with open(filepath, 'w') as file:
        final_str = json.dumps(to_dump, indent=4)
        file.writelines([final_str])
    print(f'wrote output mappings to {filepath}')



real_color = (100, 0, 0)
term_color = (10, 0, 0)

character = '▆'
def lock_into_output_mapping():
    output_mappings[real_color] = term_color
    print(f'mapped {real_color} to {term_color} ({rgb_ansi(character, term_color)})')

    for rgb_index, value in enumerate(real_color):
        if value:
            break
    {
        0: make_red,
        1: make_green,
        2: make_blue,
    }[rgb_index]()


def make_grid_darker(n = 1):
    global real_color, term_color
    real_color = list(real_color)
    for index, value in enumerate(real_color):
        if value:
            real_color[index] = max(1, value - n)
    real_color = tuple(real_color)
    reprint_terminal()
    term_color = find_right_below(real_color)
    reprint_real_grid()


def make_grid_lighter(n = 1):
    global real_color, term_color
    real_color = list(real_color)
    for index, value in enumerate(real_color):
        if value:
            real_color[index] = min(100, value + n)
    real_color = tuple(real_color)
    term_color = find_right_below(real_color)
    reprint_terminal()
    reprint_real_grid()


def make_terminal_darker(n = 1):
    global term_color
    term_color = list(term_color)
    for index, value in enumerate(term_color):
        if value:
            term_color[index] = max(1, value - n)
    term_color = tuple(term_color)
    reprint_terminal()


def make_terminal_lighter(n = 1):
    global term_color
    term_color = list(term_color)
    for index, value in enumerate(term_color):
        if value:
            term_color[index] = min(100, value + n)
    term_color = tuple(term_color)
    reprint_terminal()

def find_first_missing(rgb):
    for rgb_index, value in enumerate(rgb):
        if value:
            break
    for i in range(1, 100):
        new = list(rgb)
        new[rgb_index] = i
        if tuple(new) not in output_mappings:
            return tuple(new)

def find_right_below(rgb):
    for rgb_index, value in enumerate(rgb):
        if value:
            break
    for i in range(1, 100):
        new = list(rgb)
        new[rgb_index] = i
        if tuple(new) in output_mappings:
            return output_mappings[tuple(new)]
    thing = [0, 0, 0]
    thing[rgb_index] = 1
    return tuple(thing)

def make_red():
    global real_color, term_color
    real_color = find_first_missing((1, 0, 0))
    term_color = find_right_below(real_color)
    print(f'make_red called, starting with {real_color=}, {term_color=}')
    reprint_terminal_and_real_grid()

def make_green():
    global real_color, term_color
    real_color = find_first_missing((0, 1, 0))
    term_color = find_right_below(real_color)
    print(f'make_green called, starting with {real_color=}, {term_color=}')
    reprint_terminal_and_real_grid()

def make_blue():
    global real_color, term_color
    real_color = find_first_missing((0, 0, 1))
    term_color = find_right_below(real_color)
    print(f'make_blue called, starting with {real_color=}, {term_color=}')
    reprint_terminal_and_real_grid()


saved_real_color = None
blast_rgb = (255, 255, 255)
blast = False
def blast_toggle():
    global real_color, saved_real_color, blast
    blast = not blast
    print(f'{blast=}')
    if blast:
        saved_real_color = real_color
        real_color = blast_rgb
    else:
        real_color = saved_real_color
    reprint_real_grid()

output_mapping_filepath = 'output_mappings_anderew.json'


output_mappings = load_output_mappings(output_mapping_filepath)

def reprint_terminal():
    print(term_color)
    grid_helpers.fill(term_color)

    for (x, y) in grid_helpers.coords():
        rgb = list(map(int, grid_helpers.grid[x][y]))
        if rgb:
            print(rgb, rgb_ansi(character, rgb))
            break
    # grid_helpers.render_grid(terminal=True, reset_terminal=False)
    print(f'Terminal color is {term_color}')
    

def reprint_real_grid():        
    grid_helpers.reset()
    
    for x, y in [
        [2, 1]
    ]:
        for rgb_index, value in enumerate(real_color):
            grid_helpers.grid[x][y][rgb_index] = value

    grid_helpers.render()    
    print(f'Real color is {real_color}')


def reprint_terminal_and_real_grid():
    reprint_terminal()    
    reprint_real_grid()


keyboard_dict = {
    'p': lambda: write_output_mappings(output_mapping_filepath),
    'space': lock_into_output_mapping,
    'left': make_terminal_darker,
    'right': make_terminal_lighter,
    'q': lambda: make_grid_darker(8),
    'e': lambda: make_grid_lighter(8),
    'a': make_grid_darker,
    'd': make_grid_lighter,
    'm': blast_toggle,
    'w': reprint_real_grid,
    'down': lambda: make_terminal_darker(8),
    'up': lambda: make_terminal_lighter(8),
    'r': make_red,
    'g': make_green,
    'b': make_blue,
}

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
listen_keyboard(
    on_press=on_press,
    on_release=on_release,
)


