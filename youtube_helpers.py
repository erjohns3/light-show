import json
import yt_dlp
import os

from helpers import *


def download_video(dest_path=None):
    if dest_path:
        os.chdir(dest_path)

    url = input('Enter the URL you want to download:\n')
    url = 'https://www.youtube.com/watch?v=AqAkKOIuCUo'

    inject_path_prefix = ''
    if dest_path:        
        inject_path_prefix = str(dest_path) + os.path.sep

    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'outtmpl': f'{inject_path_prefix}%(title)s.%(ext)s',
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([url])

if __name__ == '__main__':
    download_video(dest_path=python_file_directory.joinpath('songs'))
