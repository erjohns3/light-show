import json
import time
import random

import autogen
import youtube_helpers
from helpers import *
import generate_rekordbox_effects
from copy import deepcopy


if __name__ == '__main__':
    downloaded_songs_directory = get_ray_directory().joinpath('music_creation').joinpath('downloaded_songs')
    urls_downloaded_filepath = get_temp_dir().joinpath('url_cache.json')

    try:
        with open(urls_downloaded_filepath, 'r') as f:
            urls_downloaded = json.loads(f.read())
    except:
        urls_downloaded = {}

    while True:
        already_downloaded = False
        funhouse_playlist_youtube_url = 'https://www.youtube.com/playlist?list=PL8gJgl0DwchB6ImoB60fDvkqLcgrsYCh-'    
        for title, url, contributor_name in youtube_helpers.get_info_from_youtube_playlist(funhouse_playlist_youtube_url):
            if url in urls_downloaded:
                continue
            
            if already_downloaded:
                sleep_time = 1
                print(f'Sleeping for {sleep_time} seconds before downloading again to prevent throttling...')
                time.sleep(sleep_time)
            already_downloaded = True

            cleaned_contributor_name = ''.join(filter(lambda x: x.isascii(), contributor_name)).replace(' ', '_')

            dest_path = downloaded_songs_directory
            if contributor_name:
                dest_path = downloaded_songs_directory.joinpath(cleaned_contributor_name)
                if not os.path.exists(dest_path):
                    print(f'Creating {dest_path} because it doesnt exist')
                    os.mkdir(dest_path)

            filepath = youtube_helpers.download_youtube_url(url=url, dest_path=dest_path, codec='mp3')
            print_green(f'Downloaded file to "{filepath}", {filepath.exists()=}')
            # generate_rekordbox_effects.generate_rekordbox_effect(filepath)
            src_bpm_offset_cache = autogen.get_src_bpm_offset(filepath, use_boundaries=True)
            rekordbox_effects_directory = pathlib.Path(__file__).parent.joinpath('effects').joinpath('rekordbox_effects')

            _, _, effect_filepath1 = autogen.generate_show(filepath, include_song_path=False, overwrite=True, mode=None, output_directory=rekordbox_effects_directory, src_bpm_offset_cache=deepcopy(src_bpm_offset_cache))
            _, _, effect_filepath2 = autogen.generate_show(filepath, include_song_path=False, overwrite=True, mode='lasers', output_directory=rekordbox_effects_directory, src_bpm_offset_cache=src_bpm_offset_cache)

            try:
                remote_folder = pathlib.Path('/home/pi/light-show/effects/autogen_shows')
                scp_to_doorbell(effect_filepath1, remote_folder)
                scp_to_doorbell(effect_filepath2, remote_folder)
                # generate_rekordbox_effects.ssh_to_doorbell(effect_filepath1)
                # generate_rekordbox_effects.ssh_to_doorbell(effect_filepath2)
            except Exception as e:
                print_stacktrace()
                print_yellow(f'Failed to ssh to doorbell, continuing...')

            urls_downloaded[url] = str(filepath)
            
            print(f'{green("DOWNLOADED")}: author: {yellow(contributor_name)}, title: {blue(title)}, video url: {url} to {filepath}')

            with open(urls_downloaded_filepath, 'w') as f:
                file_str = json.dumps(urls_downloaded, indent=4, sort_keys=True)
                f.writelines([file_str])

        if not already_downloaded:
            print('nothing downloaded')

        seconds_to_sleep = random.randint(59, 400)
        print(f'Sleeping for {seconds_to_sleep} seconds)...')
        time.sleep(seconds_to_sleep)
