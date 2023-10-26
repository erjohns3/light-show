# python build_c_module_for_python.py build --build-lib=.
    # puts so in current directory


# rm winamp_visual.cpython-311-x86_64-linux-gnu.so; python build_c_module_for_python.py build --build-lib=. && LD_LIBRARY_PATH=src/libprojectM python test_winamp_visual.py

# LD_LIBRARY_PATH=src/libprojectM ld winamp_visual.cpython-311-x86_64-linux-gnu.so

# LD_LIBRARY_PATH=src/libprojectM gdb python


# windows?
    # called by: python .\driver\build_c_module_for_python.py build --compiler=mingw32




from setuptools import setup, Extension
import sys
import pathlib

this_file_directory = pathlib.Path(__file__).parent.resolve()

sys.path.insert(0, str(this_file_directory))
from helpers import *

release_mode = 'release'
# if '--debug' in sys.argv:
#     del sys.argv[sys.argv.index('--debug')]
# if '--release' in sys.argv:
#     release_mode = 'release'
#     del sys.argv[sys.argv.index('--release')]

print_cyan(f'building with {release_mode=}, {this_file_directory=}')

src_folder = this_file_directory.joinpath('src')
src_libprojectM_folder = src_folder.joinpath('libprojectM')

# for copying but just using LD_LIBRARY_PATH for now
# for _, path in get_all_paths(src_libprojectM_folder):
#     if '.so' in path.name:
#     # if '.a' in path.name:
#         final_lib_path = this_file_directory.joinpath(path.name)
#         shutil.copy(path, final_lib_path)
#         extra_link_args.append(str(final_lib_path))

vendor_folder = this_file_directory.joinpath('vendor')
# glm_folder = vendor_folder.joinpath('glm')

extra_compile_args=['-std=c++14', '-g']
if release_mode == 'debug':
    extra_compile_args += ['-g']
# else:
#     extra_compile_args += ['-Ofast']

include_dir_api_1 = this_file_directory.joinpath('src', 'api', 'include')
include_dir_api_2 = this_file_directory.joinpath('src', 'playlist', 'api')
include_dir_api_3 = this_file_directory.joinpath('src', 'playlist', 'include')
include_dir_api_4 = this_file_directory.joinpath('src', 'api', 'include', 'projectM-4')

import numpy, os
numpy_lib_path = os.path.join(numpy.__path__[0], 'core', 'lib')
numpy_include_dir = numpy.get_include()



include_dirs = [
    str(src_folder),
    str(src_libprojectM_folder),
    str(vendor_folder), # for glm
    str(include_dir_api_1),
    str(include_dir_api_2),
    str(include_dir_api_3),
    str(include_dir_api_4),
    numpy_include_dir,
]

library_dirs = [
    str(src_libprojectM_folder),
    # str(numpy_lib_path),
]

if is_doorbell():
    custom_sdl_build = pathlib.Path('/home/pi/random/sdl_install/SDL-release-2.28.4/')
    
    include_dirs.append(str(custom_sdl_build))
    library_dirs.append(str(custom_sdl_build.joinpath('build', '.libs')))
    print_blue(f'IS DOORBELL ADDING CUSTOM DIRS: {library_dirs[-1]}, {include_dirs[-1]}')

    library_dirs.append(str(pathlib.Path('/usr/lib/aarch64-linux-gnu/libGLESv2.so')))
    include_dirs.append(str(pathlib.Path('/usr/include/GLES3/')))


sources = [
    str(this_file_directory.joinpath('winamp_visualmodule.cpp')),
    # str(numpy_lib_path),
]



# ProjectM::ProjectM() before
# zsh: floating point exception (core dumped)  LD_LIBRARY_PATH=src/libprojectM python test_winamp_visual.py

def get_python_config(flag):
    return subprocess.check_output(['python3-config', flag]).decode('utf-8').strip().split()

python_extra_compile_args = get_python_config('--cflags')
python_extra_link_args = get_python_config('--ldflags')

# extra_link_args = ['-rpath']
extra_link_args = []
the_module = Extension(
    'winamp_visual',
    sources=sources,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    # tries to do a .so (dynamic) build with this
    # needs numpy!!
    libraries = ['projectM-4', 'GLESv2', 'SDL2', 'SDL2main', 'dl', 'asound', 'pulse-simple', 'pulse', 'm', 'pthread', 'EGL'], # 'pthread' # glfw 

    # libraries = ['projectM-4', 'GLES', 'SDL2', 'SDL2main', 'dl', 'asound', 'pulse-simple', 'pulse', 'm', 'X11', 'Xext', 'Xcursor', 'Xinerama', 'Xi', 'Xrandr', 'Xss', 'Xxf86vm', 'rt', 'EGL', 'pthread'], # 'pthread' # glfw 
    extra_compile_args=extra_compile_args + python_extra_compile_args,
    extra_link_args=extra_link_args + python_extra_link_args,
)

setup(
    name = 'winamp_visual',
    version = '1.0',
    ext_modules = [the_module]
)
