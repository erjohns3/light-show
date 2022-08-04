import random
import os
import subprocess
import pathlib
import platform



def is_windows():
    plt = platform.system()
    if plt == "Windows":
        return True
    return False

def is_linux():
    plt = platform.system()
    if plt == "Linux":
        return True
    return False

def is_macos():
    plt = platform.system()
    if plt == "Darwin":
        return True
    return False

if is_windows():
    ray_directory = pathlib.Path('Y:/')
elif is_linux(): # actually only works on andrews computer lol
    ray_directory = pathlib.Path('/mnt/ray_network_share')
else:
    print('ray_directory does not exist')

python_file_directory = pathlib.Path(__file__).parent


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# go up a line: '\033[A'
# up a line and begining: '\033[F'


def random_letters(num_chars: int) -> str:
    letters = [chr(ord('a') + a) for a in range(26)]
    return ''.join(random.sample(letters, num_chars))


def get_all_paths_in_directory(directory, only_files=False, exclude_names=None):
    paths = []
    for filename in os.listdir(directory):
        if exclude_names is not None and filename in exclude_names:
            continue
        filepath = pathlib.Path(directory).joinpath(filename)
        if not only_files or os.path.isfile(filepath):
            paths.append((filename, filepath))
    return paths

def is_linux_root():
    return is_linux() and os.geteuid() == 0

def run_command_blocking(full_command_arr, debug=False, print_std_out=False):
    for index in range(len(full_command_arr)):
        cmd = full_command_arr[index]
        if type(cmd) != str:
            print(f'{bcolors.WARNING}WARNING: the parameter "cmd" was not a str, casting and continuing{bcolors.ENDC}')
            full_command_arr[index] = str(full_command_arr[index])

    if is_windows():
        if full_command_arr[0] in ['ffmpeg', 'ffplay', 'ffprobe']:
            full_command_arr[0] += '.exe'

    full_call = full_command_arr[0] + ' ' + ' '.join(map(lambda x: f'"{x}"', full_command_arr[1:]))
    process = subprocess.Popen(full_command_arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if debug:
        print(f'Finished execution, return code was {process.returncode}')

    return_string_start = f'SUCCESS Executed: {bcolors.OKGREEN}'
    if process.returncode:
        return_string_start = f'FAILURE Executed: {bcolors.FAIL}'
        print(f'stdout: {stdout.decode("utf-8")}\nstderr: {stderr.decode("utf-8")}')

    if debug or process.returncode:
        print(f'{return_string_start}{full_call}{bcolors.ENDC}')

    if print_std_out and not process.returncode:
        print(f'stdout: {stdout.decode("utf-8")}')
    return process.returncode, stdout, stderr

def run_command_async(full_command_arr, debug=False):
    for index in range(len(full_command_arr)):
        cmd = full_command_arr[index]
        if type(cmd) != str:
            print(f'{bcolors.WARNING}WARNING: the parameter "cmd" was not a str, casting and continuing{bcolors.ENDC}')
            full_command_arr[index] = str(full_command_arr[index])

    if is_windows():
        if full_command_arr[0] in ['ffmpeg', 'ffplay']:
            full_command_arr[0] += '.exe'

    full_call = full_command_arr[0] + ' ' + ' '.join(map(lambda x: f'"{x}"', full_command_arr[1:]))
    process = subprocess.Popen(full_command_arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if debug:
        print(f'started process with "{full_call}"')
    return process


# -ss '120534ms'
def seconds_to_fmmpeg_ms_string(seconds):
    return str(int(seconds * 1000)) + 'ms'

# 63 -> '00:06:03'
def seconds_to_hmsm_string(seconds) -> str:
    seconds = float(seconds)
    milliseconds = seconds % 1
    seconds = int(seconds)
    minutes = seconds // 60
    hours = str(minutes // 60).zfill(2)
    minutes = str(minutes % 60).zfill(2)
    seconds = str(seconds % 60).zfill(2)
    milliseconds = str(milliseconds)[1:4].ljust(4, '0')

    agged = f'{hours}:{minutes}:{seconds}{milliseconds}'
    return agged


# argument stuff
    # global args
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--testing', action='store_true', default=False,
    #                help='To run without rasberry pi support')
    # args = parser.parse_args()
