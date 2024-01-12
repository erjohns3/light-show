# NOT COMPLETE OR TESTED

import pathlib
import sys

this_file_directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(this_file_directory.parent.absolute()))
from helpers import *


songs_dir = this_file_directory.parent.joinpath('songs')

scp_connection = maybe_open_scp_connection_doorbell()

remote_folder = pathlib.Path('/home/pi/light-show/songs')
for _, local_filepath in get_all_paths(songs_dir):
    if local_filepath.suffix != '.ogg':
        continue
    remote_filepath = remote_folder.joinpath(local_filepath.name)
    print_blue(f'Moving from "{local_filepath}", to remote "{doorbell_ip}:{remote_filepath}"')
    scp_connection.put(str(local_filepath), remote_filepath)
    break

close_connections_to_doorbell()

# scp_to_doorbell(local_filepath=downloaded_filepath, remote_folder=remote_folder)
