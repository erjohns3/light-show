from thefuzz import fuzz, process

from helpers import *


def is_similar(item1, item2):
    return fuzz.ratio(item1, item2) > 30

def fuzzy_find_get_one(search, collection):
    return process.extractOne(search, collection)[0]


allowed_filepaths = set(['.wav', '.ogg'])
ray_songs_folder = get_ray_directory().joinpath('music_creation').joinpath('downloaded_songs')
songs_folder = pathlib.Path(__file__).resolve().parent.joinpath('songs')
print(f'Scanning {ray_songs_folder} and {songs_folder} for duplicates...')
for name2, path2 in get_all_paths(ray_songs_folder, only_files=True, recursive=True, allowed_filepaths=allowed_filepaths):
    print(name2)
    for name1, path1 in get_all_paths(songs_folder, only_files=True, recursive=True, allowed_filepaths=allowed_filepaths):
        print(name1)
        if is_similar(name1, name2):
            print('TOO SIMILAR:', blue(path1), yellow(path2))