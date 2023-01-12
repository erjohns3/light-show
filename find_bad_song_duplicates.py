from helpers import *



for name, path in get_all_paths(only_files=True, recursive=True, allowed_filepaths=['.wav', '.ogg']):
    print(blue(name), path)