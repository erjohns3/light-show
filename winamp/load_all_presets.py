import sys
import time
import pathlib
import time
from tqdm import tqdm

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
sys.path.insert(0, str(this_file_directory.parent))
from helpers import *
import winamp_wrapper


if not winamp_wrapper.try_load_winamp_cxx_module():
    print_red(f'winamp_wrapper.try_load_winamp_cxx_module() failed')
    exit()

if not winamp_wrapper.try_load_audio_device():
    print_red(f'winamp_wrapper.try_load_winamp_cxx_module() failed')
    exit()


time_per_preset = {}
start_time = time.time()
for index, (_, path) in enumerate(tqdm(winamp_wrapper.all_presets)):
    t1 = time.time()
    winamp_wrapper.load_preset(path, quiet=True)
    time_per_preset[path] = time.time() - t1

for path, time in sorted(time_per_preset.items(), key=lambda item: item[1]):
    print(f'{time:.2f} seconds, {path}')
print_green(f'TOTAL load_all_presets.py took {time.time() - start_time:.2f} seconds')

