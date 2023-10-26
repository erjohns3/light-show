import sys
import pathlib
import random

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory.parent))
from helpers import *




presets_directory = this_file_directory.parent.joinpath('winamp', 'projectm', 'presets')

seen = {}
for _, filepath in get_all_paths(presets_directory,recursive=True, only_files=True):
    if filepath.name not in seen:
        seen[filepath.name] = 0
    
    seen_times = seen[filepath.name]
    if seen_times != 0:
        print_red(f'{seen_times} OVERLAPS OF {filepath.name}')

    seen[filepath.name] += 1


the_names = list(seen.keys())
random.shuffle(the_names)
for index, name in enumerate(the_names):
    print(f'{str(index).rjust(3)}: {name}')
    if index > 50:
        break

