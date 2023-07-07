import os
import sys
import pathlib
from tinytag import TinyTag


this_file_directory = pathlib.Path(__file__).parent.resolve()
directory_above_this_file = this_file_directory.parent.resolve()
song_dir = directory_above_this_file.joinpath('songs')

if len(sys.argv) == 2:
    filename = sys.argv[1]
    filepath = pathlib.Path(song_dir.joinpath(filename))
    if filepath.suffix in ['.mp3', '.ogg', '.wav']:
        tag = TinyTag.get(filepath)
        title = input("Enter Title: ")
        setattr(tag, 'title', title)
        artist = input("Enter Artist: ")
        setattr(tag, 'artist', artist)

else:
    for filename in os.listdir(song_dir):
        filepath = pathlib.Path(song_dir.joinpath(filename))
        if filepath.suffix in ['.mp3', '.ogg', '.wav']:
            tag = TinyTag.get(filepath)
            print('')
            print(filename)
            save = False
            title = tag.title
            if title is None:
                title = input("Enter Title: ")
                save = True

            artist = tag.artist
            if artist is None:
                artist = input("Enter Artist: ")
                save = True
    
            if save:
                print('saving...')
                os.system(f'ffmpeg -i "{filepath}" -metadata title="{title}" -metadata artist="{artist}" -c:a copy tmp.ogg')
                os.system(f'mv tmp.ogg "{filepath}"')





# andrews file
# import music_tag

# from helpers import * 

# # can do the same thing with tags['artist'] too

# def assign_tag(filepath, tags, tag_name):
#     if not tags[tag_name]:
#         print_red(f'NOT SET {tag_name} - {filepath.name}')
#         new_tag = input().strip()
#         if new_tag:
#             tags[tag_name] = new_tag
#             print_green(f'{tag_name} - {tags[tag_name]}: "{filepath.name}"')
#             tags.save()
#         else:
#             print('Entered nothing, skipping file')
#     else:
#         print_green(f'{tag_name} - {tags[tag_name]}: "{filepath.name}"')


# def assign_title_tag_if_not_exist(filepath):
#     if filepath.suffix in ['.mp3', '.ogg', '.wav']:
#         tags = music_tag.load_file(filepath)
#         assign_tag(filepath, tags, 'title')
#         assign_tag(filepath, tags, 'artist')

# for name, path in get_all_paths('songs', only_files=True):
#     assign_title_tag_if_not_exist(path)
