import os
import sys
import pathlib
from tinytag import TinyTag

song_dir = pathlib.Path('songs')

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