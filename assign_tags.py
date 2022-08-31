import music_tag

from helpers import * 

# can do the same thing with tags['artist'] too

def assign_tag(filepath, tags, tag_name):
    if not tags[tag_name]:
        print_red(f'NOT SET {tag_name} - {filepath.name}')
        new_tag = input().strip()
        if new_tag:
            tags[tag_name] = new_tag
            print_green(f'{tag_name} - {tags[tag_name]}: "{filepath.name}"')
            tags.save()
        else:
            print('Entered nothing, skipping file')
    else:
        print_green(f'{tag_name} - {tags[tag_name]}: "{filepath.name}"')


def assign_title_tag_if_not_exist(filepath):
    if filepath.suffix in ['.mp3', '.ogg', '.wav']:
        tags = music_tag.load_file(filepath)
        assign_tag(filepath, tags, 'title')
        assign_tag(filepath, tags, 'artist')

for name, path in get_all_paths('songs', only_files=True):
    assign_title_tag_if_not_exist(path)
