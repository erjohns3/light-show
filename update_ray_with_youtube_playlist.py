import json
import time
import argparse
import sys

import youtube_helpers
from helpers import *
import generate_rekordbox_effects


if __name__ == '__main__':
    downloaded_songs_directory = ray_directory.joinpath('music_creation').joinpath('downloaded_songs')
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
                print(f'Sleeping for {10} seconds before downloading again to prevent throttling...')
                time.sleep(10)
            already_downloaded = True

            cleaned_contributor_name = ''.join(filter(lambda x: x.isascii(), contributor_name)).replace(' ', '_')

            dest_path = downloaded_songs_directory
            if contributor_name:
                dest_path = downloaded_songs_directory.joinpath(cleaned_contributor_name)
                if not os.path.exists(dest_path):
                    print(f'Creating {dest_path} because it doesnt exist')
                    os.mkdir(dest_path)

            filepath = youtube_helpers.download_youtube_url(url=url, dest_path=dest_path, codec='mp3')
            generate_rekordbox_effects.generate_rekordbox_effect(filepath)
            urls_downloaded[url] = str(filepath)
            
            print(f'{green("DOWNLOADED")}: author: {yellow(contributor_name)}, title: {blue(title)}, video url: {url} to {filepath}')

            with open(urls_downloaded_filepath, 'w') as f:
                file_str = json.dumps(urls_downloaded, indent=4, sort_keys=True)
                f.writelines([file_str])

        if not already_downloaded:
            print('nothing downloaded')

        seconds_to_sleep = random.randint(59, 60)
        print(f'Sleeping for 1 minutes ({seconds_to_sleep} seconds)...')
        time.sleep(seconds_to_sleep)
