# building just python, then running
    # rm winamp_visual.cpython-311-x86_64-linux-gnu.so; python build_projectm.py build --build-lib=. && python test_winamp_visual.py

# building c++ library, python library, and running
    # rm projectm/CMakeCache.txt; rm projectm/src/libprojectM/CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Release projectm/CMakeLists.txt -Bprojectm/ -Sprojectm/ && cmake --build projectm/ -- -j4 && rm winamp_visual.cpython-311-x86_64-linux-gnu.so; python build_projectm.py build --build-lib=. && python test_winamp_visual.py

# must be on 311..., not b311


# FOR RASPERRY PI:
    # RUNNING ONLY:
        # MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 LD_LIBRARY_PATH=src/libprojectM:/home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/:/usr/lib/aarch64-linux-gnu python test_winamp_visual.py
    # PARTIAL BUILD:
        # rm winamp_visual.cpython-39-aarch64-linux-gnu.so; python build_projectm.py build --build-lib=. && LD_LIBRARY_PATH=src/libprojectM:/home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/:/usr/lib/aarch64-linux-gnu && MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 LD_LIBRARY_PATH=src/libprojectM:/home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/:/usr/lib/aarch64-linux-gnu python test_winamp_visual.py
    # FULL BUILD:
        # rm CMakeCache.txt; cmake -DCMAKE_BUILD_TYPE=Release && cmake --build . -- -j4 && rm winamp_visual.cpython-39-aarch64-linux-gnu.so; python build_projectm.py build --build-lib=. && LD_LIBRARY_PATH=src/libprojectM:/home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/:/usr/lib/aarch64-linux-gnu && MESA_GL_VERSION_OVERRIDE=3.3 MESA_GLSL_VERSION_OVERRIDE=330 LD_LIBRARY_PATH=src/libprojectM:/home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/:/usr/lib/aarch64-linux-gnu python test_winamp_visual.py



import sys
import time
import pathlib
import random
import collections
import ctypes

import numpy as np


this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
sys.path.insert(0, str(this_file_directory.parent))
from helpers import *


project_m_build_dir = this_file_directory.joinpath('projectm', 'src', 'libprojectM')
wanted_so = project_m_build_dir.joinpath('libprojectM-4.so.4').resolve()
ctypes.cdll.LoadLibrary(str(wanted_so))

import winamp_visual
winamp_visual.setup_winamp()


preset_history = collections.deque([])
preset_index = -1
def last_preset():
    global preset_index
    if preset_index <= 0:
        return
    preset_index -= 1
    preset_path = preset_history[preset_index]
    print(f'Preset index is at {preset_index}/{len(preset_history) - 1} now')
    load_preset(preset_path)


def next_preset():
    global preset_index
    if preset_index >= len(preset_history) - 1:
        return
    preset_index += 1
    preset_path = preset_history[preset_index]
    print(f'Preset index is at {preset_index}/{len(preset_history) - 1} now')
    load_preset(preset_path)


presets_directory = this_file_directory.joinpath('projectm', 'presets')
presets_drawing_liquid_directory = presets_directory.joinpath('presets-cream-of-the-crop', 'Drawing', 'Liquid')
presets_dancer_glowsticks_directory = presets_directory.joinpath('presets-cream-of-the-crop', 'Dancer', 'Glowsticks Mirror')

all_presets = list(get_all_paths(presets_directory, recursive=True, only_files=True, allowed_extensions=['.milk']))
print_green(f'{len(all_presets):,} milk visualizer presets to choose from')

def load_preset(preset_path):
    better_print = preset_path.relative_to(presets_directory)
    better_print = better_print.relative_to(better_print.parts[0])
    print_blue(f'Python: loading preset {better_print}')
    winamp_visual.load_preset(str(preset_path))


print_green(f'{len(all_presets):,} milk visualizer presets to choose from')
def random_preset():
    global preset_index
    preset_path = random.choice(all_presets)[1]

    preset_history.append(preset_path)
    preset_index = len(preset_history) - 1
    print(f'Python: randomly loading preset, preset index at {preset_index}/{len(preset_history) - 1} now')

    load_preset(preset_path)

def increase_beat_sensitivity():
    winamp_visual.set_beat_sensitivity(winamp_visual.get_beat_sensitivity() + .01)
    print(f'beat sensitivity: {winamp_visual.get_beat_sensitivity()}')

def decrease_beat_sensitivity():
    winamp_visual.set_beat_sensitivity(winamp_visual.get_beat_sensitivity() - .01)
    print(f'beat sensitivity: {winamp_visual.get_beat_sensitivity()}')


def get_beat_sensitivity():
    return winamp_visual.get_beat_sensitivity()


def compute_frame():
    winamp_visual.render_frame()


def load_into_numpy_array(np_arr):
    winamp_visual.load_into_numpy_array(np_arr)


def print_to_terminal_higher_level():
    winamp_visual.print_to_terminal_higher_level()
