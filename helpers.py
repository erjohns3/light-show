import os
import pathlib


def is_windows():
    import platform
    plt = platform.system()
    if plt == "Windows":
        return True
    return False


def is_linux():
    import platform
    plt = platform.system()
    if plt == "Linux":
        return True
    return False


def is_macos():
    import platform
    plt = platform.system()
    if plt == "Darwin":
        return True
    return False


def is_marias_computer():
    import socket
    return socket.gethostname() in ['DESKTOP-IKO6828']


def is_ray():
    import socket
    return socket.gethostname() in ['ray']


def is_erics_laptop():
    import socket
    return socket.gethostname() in ['LAPTOP-ERIC']


def is_andrews_main_computer():
    import socket
    return socket.gethostname() in ['zetai']


def is_andrews_laptop():
    import socket
    return socket.gethostname() in ['DESKTOP-754BOFE']


def get_ray_directory():
    if is_windows():
        return pathlib.Path('Y:/')
    elif is_andrews_main_computer():
        return pathlib.Path('/mnt/ray_network_share')
    else:
        print_red('doesnt know how contact ray_directory')


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


def yellow(s):
    return f'{bcolors.WARNING}{s}{bcolors.ENDC}'

def green(s):
    return f'{bcolors.OKGREEN}{s}{bcolors.ENDC}'

def cyan(s):
    return f'{bcolors.OKCYAN}{s}{bcolors.ENDC}'

def bold(s):
    return f'{bcolors.BOLD}{s}{bcolors.ENDC}'

def blue(s):
    return f'{bcolors.OKBLUE}{s}{bcolors.ENDC}'

def red(s):
    return f'{bcolors.FAIL}{s}{bcolors.ENDC}'



def print_yellow(*args, **kwargs):
    args = map(str, args)
    print(yellow(' '.join(args)), **kwargs)

def print_green(*args, **kwargs):
    args = map(str, args)
    print(green(' '.join(args)), **kwargs)

def print_cyan(*args, **kwargs):
    args = map(str, args)
    print(cyan(' '.join(args)), **kwargs)

def print_bold(*args, **kwargs):
    args = map(str, args)
    print(bold(' '.join(args)), **kwargs)

def print_blue(*args, **kwargs):
    args = map(str, args)
    print(blue(' '.join(args)), **kwargs)

def print_red(*args, **kwargs):
    args = map(str, args)
    print(red(' '.join(args)), **kwargs)


def get_clean_filesystem_string(s):
    return ''.join(char for char in s if char.isalnum() or char in ' -_.()[],')

def get_no_duplicate_spaces(s):
    import re
    return re.sub(r"\s+", " ", s)


def random_letters(num_chars: int) -> str:
    import random
    letters = [chr(ord('a') + a) for a in range(26)]
    return ''.join(random.sample(letters, num_chars))


def get_all_paths(directory, only_files=False, exclude_names=None, recursive=False):
    if not isinstance(directory, pathlib.Path):
        directory = pathlib.Path(directory)
    if not directory.exists():
        print_yellow(f'{directory} does not exist, returning [] for paths')
        return []
    paths = []
    directory = pathlib.Path(directory)
    for filename in os.listdir(directory):
        if exclude_names is not None and filename in exclude_names:
            continue
        filepath = pathlib.Path(directory).joinpath(filename)
        
        if filepath.is_file() or not only_files:
            paths.append((filename, filepath))
        if filepath.is_dir() and recursive:
            paths += get_all_paths(filepath, only_files=only_files, exclude_names=exclude_names, recursive=recursive)
    return paths

def is_linux_root():
    return is_linux() and os.geteuid() == 0

def run_command_blocking(full_command_arr, timeout=None, debug=False, print_std_out=False):
    import subprocess
    for index in range(len(full_command_arr)):
        cmd = full_command_arr[index]
        if type(cmd) != str:
            print_yellow(f'WARNING: the parameter "cmd" was not a str, casting and continuing')
            full_command_arr[index] = str(full_command_arr[index])

    if is_windows():
        if full_command_arr[0] in ['ffmpeg', 'ffplay', 'ffprobe']:
            full_command_arr[0] += '.exe'

    process = subprocess.Popen(full_command_arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(timeout=timeout)

    if debug:
        print(f'Finished execution, return code was {process.returncode}')

    return_string_start = f'SUCCESS Executed: {bcolors.OKGREEN}'
    if process.returncode:
        return_string_start = f'FAILURE Executed: {bcolors.FAIL}'
        print(f'stdout: {stdout.decode("utf-8")}\nstderr: {stderr.decode("utf-8")}')

    if debug or process.returncode:
        full_call = full_command_arr[0] + ' ' + ' '.join(map(lambda x: f'"{x}"', full_command_arr[1:]))
        print(f'{return_string_start}{full_call}{bcolors.ENDC}')

    if print_std_out and not process.returncode:
        print(f'stdout: {stdout.decode("utf-8")}')
    return process.returncode, stdout.decode("utf-8"), stderr.decode("utf-8")


def make_if_not_exist(output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir


def get_temp_dir():
    return make_if_not_exist(pathlib.Path(__file__).parent.joinpath('temp'))


def run_command_async(full_command_arr, debug=False):
    import subprocess

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






# make directory above importable
# import sys
# import pathlib

# def make_directory_above_importable():
#     path_above_file = pathlib.Path(__file__).parent.joinpath('..').resolve()
#     sys.path.insert(0, str(path_above_file))


# go up a line: '\033[A'
# up a line and begining: '\033[F'


# disabling std out
# if is_windows():
#     null_std_out = open('nul', 'w')
# elif is_linux() or is_macos():
#     null_std_out = open('/dev/null', 'w')
