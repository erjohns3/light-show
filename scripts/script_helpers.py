import sys
import pathlib

def make_directory_above_importable():
    path_above_file = pathlib.Path(__file__).parent.joinpath('..').resolve()
    sys.path.insert(0, str(path_above_file))