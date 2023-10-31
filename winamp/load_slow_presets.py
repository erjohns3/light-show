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
    print_red(f'winamp_wrapper.try_load_audio_device() failed')
    exit()

easy_preset_name = '210-wave-smooth-80'
slow_presets = [
    'Flexi + geiss - botnet nz+ let us out fractal spiders2 pure opulenth pony.milk',
]

runs = {}
num_times = 300
start_time = time.time()
for index in tqdm(range(num_times)):
    t1 = time.time()
    winamp_wrapper.load_preset(easy_preset_name, timing=False, quiet=True)
    winamp_wrapper.compute_frame()
    for preset_name in slow_presets:
        winamp_wrapper.load_preset(preset_name, timing=False, quiet=True)
        winamp_wrapper.compute_frame()
    runs[index] = time.time() - t1

print_blue(f'First run took {runs[0]:.2f} seconds')
print_blue(f'Last run took {runs[num_times-1]:.2f} seconds')

time_taken = time.time() - start_time
print_green(f'TOTAL load_slow_presets.py took {time_taken:.2f} seconds over {num_times} runs. {num_times/time_taken:.3f} per loading all')

