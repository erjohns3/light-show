import json
import os
import sys

import yt_dlp

from helpers import *


def scp_to_doorbell(local_filepath, remote_folder):
    # looks like most people use https://www.fabfile.org/ for the higher level library
    import paramiko
    from scp import SCPClient
    
    remote_filepath = remote_folder.joinpath(local_filepath.name)

    # doorbell_ip = 'doorbell'
    doorbell_ip = '192.168.86.58'

    ssh = paramiko.client.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=doorbell_ip, # doorbell IP
                port = 22,
                username='pi')

    print(f'{bcolors.OKBLUE}Moving from "{local_filepath}", to remote "{doorbell_ip}:{remote_filepath}"{bcolors.ENDC}')
    scp = SCPClient(ssh.get_transport())
    scp.put(local_filepath, remote_filepath)
    scp.close()


def download_youtube_url_to_ogg(url=None, dest_path=None):
    if url is None:
        url = input('Enter the URL you want to download:\n')

    inject_path_prefix = dest_path or ''
    ydl_opts = {
        'format': 'vorbis/bestaudio/best',
        'outtmpl': f'{str(inject_path_prefix) + os.path.sep}%(title)s.%(ext)s',
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_filename = info_dict['title'] + '.ogg'

    downloaded_filepath = inject_path_prefix.joinpath(downloaded_filename)

    # this sucks for some reason
    no_special = ''.join(char for char in downloaded_filename if char.isalnum() or char == ' ' or char == '.')
    if downloaded_filename != no_special:
        print('we might be crashing rn')
        no_special_chars_filepath = inject_path_prefix.joinpath(no_special)
        os.rename(downloaded_filepath, no_special_chars_filepath)
        return no_special_chars_filepath

    return downloaded_filepath


if __name__ == '__main__':
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    downloaded_filepath = download_youtube_url_to_ogg(url=url, dest_path=python_file_directory.joinpath('songs'))
    remote_folder = pathlib.Path('/home/pi/light-show/songs')
    print('Starting scp to doorbell')
    scp_to_doorbell(local_filepath=downloaded_filepath, remote_folder=remote_folder)