import sys
import pathlib

from thefuzz import fuzz, process

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory.parent))

from helpers import *


def is_similar(item1, item2):
    return fuzz.ratio(item1, item2) > 80

def fuzzy_find_get_one(search, collection):
    return process.extractOne(search, collection)[0]


allowed_extensions = set(['.mp3', '.wav', '.ogg'])
ray_songs_folder = get_ray_directory().joinpath('music_creation').joinpath('downloaded_songs')
songs_folder = pathlib.Path(__file__).resolve().parent.joinpath('songs')
print(f'Scanning {ray_songs_folder} and {songs_folder} for duplicates...')
for name2, path2 in get_all_paths(ray_songs_folder, recursive=True, allowed_extensions=allowed_extensions, only_files=True):
    for name1, path1 in get_all_paths(songs_folder, recursive=True, allowed_extensions=allowed_extensions, only_files=True):
        if path1.stem != path2.stem and is_similar(path1.stem, path2.stem):
            print(f'TOO SIMILAR:\n    {blue(path1.stem)} - {path1}\n    {yellow(path2.stem)} - {path2}')
print_green('Done')