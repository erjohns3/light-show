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
import pathlib
import random
import collections
import ctypes

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
sys.path.insert(0, str(this_file_directory.parent))
from helpers import *

if is_doorbell():
    os.environ['MESA_GL_VERSION_OVERRIDE'] = '3.3'
    os.environ['MESA_GLSL_VERSION_OVERRIDE'] = '330'
    os.environ['LD_LIBRARY_PATH'] = '/home/pi/random/sdl_install/SDL-release-2.28.4/build/.libs/'
    print_yellow(f'Assigning MESA_GL and MESA_GLSL overrides to get GLSL 3')
    print_yellow(f'note that in .zshrc the LD_LIBRARY_PATH is overriden to: ~/random/sdl_install/SDL-release-2.28.4/build/.libs/')


winamp_visual_loaded = False
def try_load_winamp_cxx_module():
    global winamp_visual_loaded
    project_m_build_dir = this_file_directory.joinpath('projectm', 'src', 'libprojectM')
    if not project_m_build_dir.exists():
        return print_red(f'project_m {project_m_build_dir} directory does not exist')

    if is_linux():
        wanted_so = project_m_build_dir.joinpath('libprojectM-4.so.4').resolve()
    elif is_macos():
        wanted_so = project_m_build_dir.joinpath('libprojectM-4.dylib').resolve()
    if not wanted_so.exists():
        return print_red(f'project_m c++ library: {wanted_so} does not exist')

    ctypes.cdll.LoadLibrary(str(wanted_so))

    import winamp_visual
    globals()[winamp_visual.__name__] = winamp_visual
    try:
        winamp_visual.setup_winamp()
    except:
        return print_red(f'winamp_visual.setup_winamp() failed, stacktrace: {get_stack_trace()}')

    print_green(f'winamp_visual.setup_winamp() succeeded')
    winamp_visual_loaded = True
    return True


def try_load_audio_device():
    audio_devices = get_audio_devices()
    for id, device_name in audio_devices.items():
        print(f'{id=}, {device_name=}')
    
    if len(audio_devices) == 0:
        return print_red('Init successful, but no audio devices found')
    
    loaded_id = -1
    if is_doorbell():
        loaded_id = init_audio_id(2)
        if loaded_id != -1:
            print_yellow(f'Loaded audio device id: {loaded_id}, this is hardcoded, fix')
    elif is_andrews_main_computer():
        for id, device_name in audio_devices.items():
            if 'Monitor of henry' in device_name:
                loaded_id = init_audio_id(id)
                if loaded_id != -1:
                    print_green(f'Loaded audio device id: {loaded_id}')
                break
        else:
            print_red('WARNING: ON ANDREWS COMPUTER BUT HENRY ISNT ON')
    elif is_macos():
        for id, device_name in audio_devices.items():
            if 'blackhole' in device_name.lower():
                loaded_id = init_audio_id(id)
                if loaded_id != -1:
                    print_green(f'Loaded audio device id: {loaded_id}')
                break
        else:
            print_red('WARNING: COULDNT FIND BLACKHOLE AUDIO DEVICE. MAKE SURE TO README.md')
    else:
        print_yellow(f'Trying to load default audio device (-1)')
        loaded_id = init_audio_id(-1) # !TODO i think this says to load the default
        if loaded_id != -1:
            print_green(f'Loaded audio device id: {loaded_id}')
    
    if loaded_id == -1:
        return print_red('Init successful, but couldnt load audio device id')
    return True


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

preset_name_to_filepath = {}
for _, filepath in all_presets:
    if filepath.name in preset_name_to_filepath:
        print_red(f'OVERLAPS IN WINAMP PRESET FILENAMES: {filepath.name}')
        exit()
    preset_name_to_filepath[filepath.stem] = filepath
    preset_name_to_filepath[filepath.name] = filepath
    # detect if not ascii:
    if not filepath.name.isascii():
        print_red(f'{filepath.name} ISNT ASCII')
        exit()

current_preset_path = None
def load_preset(preset_path_or_string, smooth_transition=False, timing=True, quiet=False):
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot load preset')
    
    start_time = time.time()
    preset_path_to_load = preset_path_or_string
    if isinstance(preset_path_or_string, str):
        preset_path_to_load = preset_name_to_filepath.get(preset_path_or_string, None)
        if preset_path_to_load is None:
            return print_red(f'preset name {preset_path_or_string} not found')

    global current_preset_path
    if current_preset_path == preset_path_to_load:
        return
    better_print = preset_path_to_load.relative_to(presets_directory)
    if 'cream' in better_print.parts[0]:
        better_print = better_print.relative_to(better_print.parts[0])
    if not quiet: print_blue(f'Python: loading preset {better_print}, real path: {preset_path_to_load}')
    current_preset_path = preset_path_to_load
    result = winamp_visual.load_preset(str(preset_path_to_load), smooth_transition)
    if timing:
        print(f'Python: loading preset took {time.time() - start_time:.3f} seconds')
    return result


def random_preset():
    global preset_index
    preset_path = random.choice(all_presets)[1]

    preset_history.append(preset_path)
    preset_index = len(preset_history) - 1
    print(f'Python: randomly loading preset, preset index at {preset_index}/{len(preset_history) - 1} now')

    load_preset(preset_path)

def increase_beat_sensitivity(amt=.01):
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot increase beat sensitivity')
    
    new_val = get_beat_sensitivity() + amt
    winamp_visual.set_beat_sensitivity(new_val)
    print(f'beat sensitivity: {get_beat_sensitivity()}')
    return new_val


def decrease_beat_sensitivity(amt=.01):
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot decrease beat sensitivity')
    new_val = get_beat_sensitivity() - amt
    winamp_visual.set_beat_sensitivity(new_val)
    print(f'beat sensitivity: {get_beat_sensitivity()}')
    return new_val


def get_beat_sensitivity():
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot get beat sensitivity')
    return winamp_visual.get_beat_sensitivity()


def compute_frame():
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot compute frame')
    winamp_visual.render_frame()


def load_into_numpy_array(np_arr):
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot load into numpy array')
    winamp_visual.load_into_numpy_array(np_arr)


def print_to_terminal_higher_level():
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot print to terminal')
    winamp_visual.print_to_terminal_higher_level()


def get_audio_devices():
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot print to terminal')
    return winamp_visual.get_audio_devices()


def init_audio_id(id):
    if not winamp_visual_loaded:
        return print_red(f'winamp_visual module not loaded, cannot print to terminal')
    return winamp_visual.init_audio_id(id)