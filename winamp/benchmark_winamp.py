import sys
import pathlib

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
sys.path.insert(0, str(this_file_directory.parent))
from helpers import *
import winamp_wrapper


# python_file = this_file_directory.joinpath('load_all_presets.py')
python_file = this_file_directory.joinpath('load_all_presets.py')


perf_file = get_temp_dir().joinpath('perf.data')
print(f'Outputting to {perf_file}')
retcode, stdout, stderr = run_command_blocking([
    'perf', 'record',
    '--call-graph', 'dwarf',
    '-o', perf_file,
    sys.executable,
    str(python_file),
])

if retcode != 0:
    print_red(f'perf record failed, {retcode=}, {stdout=}, {stderr=}')
    exit()

retcode, _stdout, stderr = run_command_blocking([
    'perf', 'report',
    '-i', perf_file,
    # '--stdio',
    # '--no-children',
    # '--no-demangle',
    # '--show-nr-samples',
    # '--show-total-period',
], stdout_pipe=None)