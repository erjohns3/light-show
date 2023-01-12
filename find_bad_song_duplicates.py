from thefuzz import fuzz, process

from helpers import *


def is_similar(item1, item2):
    return fuzz.ratio(item1, item2) > 90

def fuzzy_find_get_one(search, collection):
    return process.extractOne(search, collection)[0]


allowed_filepaths = set(['.mp3', '.wav', '.ogg'])
ray_songs_folder = get_ray_directory().joinpath('music_creation').joinpath('downloaded_songs')
songs_folder = pathlib.Path(__file__).resolve().parent.joinpath('songs')
print(f'Scanning {ray_songs_folder} and {songs_folder} for duplicates...')
for name2, path2 in get_all_paths(ray_songs_folder, only_files=True, recursive=True, allowed_filepaths=allowed_filepaths):
    # print('scanning', path2, name2)
    for name1, path1 in get_all_paths(songs_folder, only_files=True, recursive=True, allowed_filepaths=allowed_filepaths):
        if path1.stem != path2.stem and is_similar(path1.stem, path2.stem):
            print(f'TOO SIMILAR:\n    {blue(path1.stem)} - {path1}\n    {yellow(path2.stem)} - {path2}')
print_green('Done')