import os
import pathlib
import subprocess

try:
    profile
except NameError:
    profile = lambda x: x

helper_file_folder = pathlib.Path(__file__).parent.resolve()

def is_windows():
    import platform
    return platform.system() == "Windows"


def is_linux():
    import platform
    return platform.system() == "Linux"


def is_macos():
    import platform
    return platform.system() == "Darwin"

def get_datetime_str():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def unix_to_human_readable(unix_time):
    import datetime
    return datetime.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')

def is_image_path(path):
    return path.endswith('.jpg') or path.endswith('.png') or path.endswith('.webp')

def get_hostname():
    import socket
    return socket.gethostname()

def is_marias_computer():
    return get_hostname() in ['DESKTOP-IKO6828']


def is_ray():
    return get_hostname() in ['ray']


def is_erics_laptop():
    return get_hostname() in ['Eric-Laptop']


def is_andrews_main_computer():
    return get_hostname() in ['zetai']


def is_andrews_laptop():
    return get_hostname() in ['DESKTOP-754BOFE']


def is_doorbell():
    return get_hostname() in ['doorbell']


def is_screensaver_running():
    if not is_ray():
        print_yellow('is_screensaver_running() was called, but on a computer that isnt ray, returning False')
        return False

    import psutil
    for process in psutil.process_iter():
        try:
            if 'python.exe' in process.name():
                args = process.cmdline()
                if len(args) > 1:
                    if args[1].endswith('screensaver.py'):
                        if len(args) > 2 and args[2].lower() == '/s':
                            return True
        except psutil.NoSuchProcess:
            pass
    return False


ray_is_active_andrew = False
def get_ray_directory():
    global ray_is_active_andrew
    if is_ray() or is_erics_laptop():
        return pathlib.Path('T:/')
    elif is_andrews_main_computer() or is_andrews_laptop():
        mount_path = pathlib.Path('/mnt/ray_network_share')
        if ray_is_active_andrew:
            return mount_path
        _, stdout, _ = run_command_blocking([
            'ls',
            str(mount_path),
        ])
        if stdout:
            return mount_path
        else:
            print_red('Cannot find any files in {mount_path}, you probably need to run "sudo mount -t cifs -o vers=3.0,username=${USER},password=${PASSWORD},uid=$(id -u),gid=$(id -g) //192.168.86.210/T /mnt/ray_network_share/"')
            exit()
    else:
        print_red('doesnt know how contact ray_directory')

nas_is_active_andrew = False
def get_nas_directory():
    global nas_is_active_andrew
    if is_andrews_main_computer() or is_andrews_laptop():
        mount_path = pathlib.Path('/mnt/nas')
        if nas_is_active_andrew:
            return mount_path
        _, stdout, _ = run_command_blocking([
            'ls',
            str(mount_path),
        ])
        if stdout:
            return mount_path
        else:
            print_red('Cannot find any files in {mount_path}, you probably need to run "sudo mount -t cifs -o username=crammem,password=#Cumbr1dge,uid=$(id -u),gid=$(id -g) //192.168.86.75/Raymond /mnt/nas/"')
            exit()
    else:
        print_red('doesnt know how contact nas_directory')


def get_stack_trace() -> str:
    import traceback
    return traceback.format_exc()


def print_stacktrace() -> None:
    print_red(get_stack_trace())


video_extensions = set(map(lambda x: x.lower(), ['.WEBM', '.MPG', '.MP2', '.MPEG', '.MPE', '.MPV', '.OGG', '.MP4', '.M4P', '.M4V', '.AVI', '.WMV', '.MOV', '.QT', '.FLV', '.SWF', '.AVCHD', '.mkv']))


doorbell_ip = '192.168.86.55'
ssh_connection = None
def maybe_open_ssh_connection_doorbell():
    global ssh_connection
    import paramiko

    if ssh_connection is not None and ssh_connection.get_transport() and ssh_connection.get_transport().is_active:
        return ssh_connection
    
    print_cyan('opening ssh_connection to doorbell')
    ssh_connection = paramiko.client.SSHClient()
    ssh_connection.load_system_host_keys()
    ssh_connection.connect(hostname=doorbell_ip,
                port = 22,
                username='pi')


# looks like most people use https://www.fabfile.org/ for the higher level library
scp_connection = None
def maybe_open_scp_connection_doorbell():
    global scp_connection
    from scp import SCPClient

    if scp_connection is not None and scp_connection.transport and scp_connection.transport.is_active:
        return scp_connection

    print_cyan('opening scp_connection to doorbell')    
    maybe_open_ssh_connection_doorbell()
    scp_connection = SCPClient(ssh_connection.get_transport())


def close_connections_to_doorbell():
    if scp_connection is not None and scp_connection.transport and scp_connection.transport.is_active:
        print_cyan('closing ssh_connection')
        scp_connection.close()
        return
    
    if ssh_connection is not None and ssh_connection.get_transport() and ssh_connection.get_transport().is_active:
        print_cyan('closing ssh_connection')
        ssh_connection.close()


def run_command_on_doorbell_via_ssh(command, keep_open=False):
    print_yellow('andrew: trying this new extra scp step on error (assuming rekord_box folder doesnt exist)')

    maybe_open_ssh_connection_doorbell()
    _stdin, _stdout, _stderr = ssh_connection.exec_command(command)
    if not keep_open:
        close_connections_to_doorbell()
    return _stdin, _stdout, _stderr


def scp_to_doorbell(local_filepath, remote_folder, keep_open=False):
    remote_filepath = remote_folder.joinpath(local_filepath.name)

    if is_windows():
        remote_filepath = str(remote_filepath).replace('\\\\', '/').replace('\\', '/')

    print(f'{bcolors.OKBLUE}Moving from "{local_filepath}", to remote "{doorbell_ip}:{remote_filepath}"{bcolors.ENDC}')
    maybe_open_scp_connection_doorbell()
    scp_connection.put(str(local_filepath), remote_filepath)

    if not keep_open:
        close_connections_to_doorbell()


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


color_tracker = 0
avail_colors = [(yellow, 'yellow'), (green, 'green'), (cyan, 'cyan'), (blue, 'blue'), (red, 'red')]
def next_color(s, skip=None):
    global color_tracker
    while True:
        color_tracker = (color_tracker + 1) % len(avail_colors)
        if skip is None or avail_colors[color_tracker][1] not in skip:
            break
    return avail_colors[color_tracker][0](s)

# I think this is called "true color" which is 24 bit color
# @profile
def rgb_ansi(text, rgb_tuple):
    rgb_style = f'38;2;{rgb_tuple[0]};{rgb_tuple[1]};{rgb_tuple[2]}'
    return f'\033[{rgb_style}m{text}\033[0m'



def disable_color():
    global bcolors
    bcolors.HEADER = ''
    bcolors.OKBLUE = ''
    bcolors.OKCYAN = ''
    bcolors.OKGREEN = ''
    bcolors.WARNING = ''
    bcolors.FAIL = ''
    bcolors.ENDC = ''
    bcolors.BOLD = ''
    bcolors.UNDERLINE = ''


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


def get_no_duplicate_spaces(s):
    import re
    return re.sub(r"\s+", " ", s)


def random_letters(num_chars: int) -> str:
    import random
    letters = [chr(ord('a') + a) for a in range(26)]
    return ''.join(random.sample(letters, num_chars))

def get_all_paths(directory, only_files=False, exclude_names=None, recursive=False, allowed_extensions=None, quiet=False):
    directory = pathlib.Path(directory)

    if not directory.exists():
        if not quiet:
            print(f'{directory} does not exist, returning [] for paths')
        return

    exclude_names = set(exclude_names or [])

    for entry in directory.iterdir():
        if entry.name in exclude_names:
            continue
        
        if entry.is_file():
            if allowed_extensions and entry.suffix not in allowed_extensions:
                continue
            yield entry.name, entry
        elif entry.is_dir() and recursive:
            yield from get_all_paths(entry, only_files, exclude_names, recursive, allowed_extensions, quiet)
        elif not only_files:
            yield entry.name, entry


def start_http_server_blocking(port, filepath_to_serve):
    import http.server
    import socketserver

    Handler = http.server.SimpleHTTPRequestHandler
    os.chdir(filepath_to_serve)
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print_blue(f'serving simple http server at {port} at path {filepath_to_serve}, can hit with http://localhost:{port}')
        httpd.serve_forever()


def start_http_server_async(port, filepath_to_serve):
    import threading
    threading.Thread(target=start_http_server_blocking, args=(port, filepath_to_serve,)).start()


def is_python_32_bit():
    import sys
    return sys.maxsize > 2**32

def start_video_in_mpv_async(video_path, volume=70):
    print(f'start_video_in_mpv: starting "{video_path}"')
    run_command_async([
        'mpv', 
        str(video_path), 
        '--no-resume-playback',
        '--sid=no',
        '--title=mpv_vtuber_window',
        '--x11-name=mpv_vtuber_window',
        f'--volume={volume}',
    ], debug=True)

def is_linux_root():
    return is_linux() and os.geteuid() == 0

def run_command_blocking(full_command_arr, timeout=None, debug=False, stdin_pipe=None, stdout_pipe=subprocess.PIPE, stderr_pipe=subprocess.PIPE, timing=False):
    import time 
    start_time = time.time()
    for index in range(len(full_command_arr)):
        cmd = full_command_arr[index]
        if type(cmd) != str:
            if not isinstance(cmd, pathlib.Path):
                print_yellow(f'WARNING: the parameter "cmd" was not a str, casting and continuing')
            full_command_arr[index] = str(full_command_arr[index])

    if is_windows():
        if full_command_arr[0] in ['ffmpeg', 'ffplay', 'ffprobe']:
            full_command_arr[0] += '.exe'

    full_call = full_command_arr[0] + ' ' + ' '.join(map(lambda x: f'"{x}"', full_command_arr[1:]))
    if debug:
        print(f'going to run "{full_call}"')
    
    # env = os.environ.copy() # env['SSH_AUTH_SOCK'] = os.
    process = subprocess.Popen(full_command_arr, stdout=stdout_pipe, stderr=stderr_pipe, stdin=stdin_pipe)
    stdout, stderr = process.communicate(timeout=timeout)

    if debug:
        print(f'Finished execution, return code was {process.returncode}')

    if stdout is not None:
        stdout = stdout.decode("utf-8")
    if stderr is not None:
        stderr = stderr.decode("utf-8")

    if debug:
        if process.returncode:
            print_red(f'FAILURE executing "{full_call}"')
            if stdout:
                print('stdout', stdout)
            if stderr:
                print_red('stderr', stderr)
        else:
            print_green(f'SUCCESS executing "{full_call}"')
            if stdout:
                print('stdout', stdout)
            if stderr:
                print_red('stderr', stderr)
        
    if timing:
        print_blue(f'Took {time.time() - start_time:.2f} seconds, command was "{full_call}"')
    return process.returncode, stdout, stderr


def make_if_not_exist(output_dir, quiet=False):
    output_dir = pathlib.Path(output_dir)
    if not output_dir.exists():
        if not quiet:
            print_yellow(f'Creating {output_dir} since it didn\'t exist')
        os.mkdir(output_dir)
    return output_dir


def get_temp_dir():
    return make_if_not_exist(pathlib.Path(__file__).parent.joinpath('temp'))

def get_sub_temp_dir(name=None):
    if name is None:
        name = random_letters(15)
    return make_if_not_exist(get_temp_dir().joinpath(name))

def get_temp_file(name=None):
    if name is None:
        name = random_letters(15)
    return get_temp_dir().joinpath(name)


def run_command_async(full_command_arr, debug=False, stdin=None):
    import subprocess

    for index in range(len(full_command_arr)):
        cmd = full_command_arr[index]
        if type(cmd) != str:
            print_yellow(f'the parameter "cmd" was not a str, casting and continuing')
            full_command_arr[index] = str(full_command_arr[index])

    if is_windows():
        if full_command_arr[0] in ['ffmpeg', 'ffplay']:
            full_command_arr[0] += '.exe'

    full_call = full_command_arr[0] + ' ' + ' '.join(map(lambda x: f'"{x}"', full_command_arr[1:]))
    process = subprocess.Popen(full_command_arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=stdin)
    
    if debug:
        print(f'started process with "{full_call}"')
    return process


def executable_running(executable_name):
    import psutil
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == executable_name:
            return True
    return False


def kill_process_by_name(executable_name):
    import psutil
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == executable_name:
            try:
                proc.kill()
            except psutil.AccessDenied:
                print_red(f'Access denied for {executable_name=}')
            except psutil.NoSuchProcess:
                pass


# -ss '120534ms'
def seconds_to_fmmpeg_ms_string(seconds):
    if seconds < 0:
        print_red(f'WARNING: seconds_to_fmmpeg_ms_string was called with {seconds=}, returning 0')
        return '0ms'
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

def hmsm_string_to_seconds(string):
    parts = string.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_parts = parts[2].split(".")
    seconds = int(seconds_parts[0])
    milliseconds = int(seconds_parts[1])
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 100


def play_file_mpv(video_path, volume=None, subtitles=False, run_async=False):
    cmd = [
        'mpv', 
        video_path, 
        '--no-resume-playback',
        '--no-pause',
        '--load-scripts=no',
    ]
    if not subtitles:
        cmd.append('--sid=no')
    if volume is not None:
        cmd.append(f'--volume={volume}')
    if run_async:
        return run_command_async(cmd)
    else:
        run_command_blocking(cmd, stdout_pipe=None, stderr_pipe=None)



def kill_self(seconds=0):
    import time
    if seconds:
        print(f'Sleeping for {seconds} before killing self')
        time.sleep(seconds)
    if is_windows():
        kill_string = f'taskkill /PID {os.getpid()} /f'
    else:
        kill_string = f'kill -9 {os.getpid()}'
    for i in range(10):
        print(f'{i}: running to kill: "{kill_string}"')
        os.system(kill_string)
    print_red('THIS SHOULD BE UNREACHABLE')



def path_is_local(path):
    if is_ray():
        if path.resolve().parts[0] in ['C:\\', 'T:\\']:
            return True
    elif is_linux():
        if ''.join(path.resolve().parts[0:2]) != '/mnt':
            return True
    elif is_windows():
        if not is_andrews_laptop():
            print(f'path_is_local called, assuming that only the C:\\ drive is local. update this code if you dont want it to print every time')
        if path.resolve().parts[0] == 'C:\\':
            return True
    return False

# Going over network is quite slow with processing, copy things locally to speed things up on successive runs.
def copy_file_locally(file_path, output_directory=get_temp_dir()):
    import shutil
    if path_is_local(file_path):
        return file_path

    dest_path = output_directory.joinpath(file_path.name)
    if not dest_path.exists() and file_path.exists():
        print_yellow(f'WARNING: Copying {file_path.name} locally. This is for speedup because networking is slow. Copying {file_path} to {dest_path}')
        shutil.copy(file_path, dest_path)
        print_green('Finished copying file')
    return dest_path


def dump_text_to_file(text, output_directory=get_temp_dir()):
    filepath = output_directory.joinpath(random_letters(15) + '.txt')
    filepath.write_text(text)
    return filepath


# import sys
# import pathlib
# sys.path.insert(0, str(pathlib.Path(__file__).parent.joinpath('..').resolve()))


# go up a line: '\033[A'
# up a line and begining: '\033[F'


# disabling std out
# if is_windows():
#     null_std_out = open('nul', 'w')
# elif is_linux() or is_macos():
#     null_std_out = open('/dev/null', 'w')

