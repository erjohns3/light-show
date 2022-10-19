import generate_show
from helpers import *
import server
import youtube_helpers

if __name__ == '__main__':
    rekordbox_song_directory = ray_directory.joinpath('music_creation', 'downloaded_songs')
    effect_output_directory = python_file_directory.joinpath('effects').joinpath('rekordbox_effects')

    server.update_config_and_lut_from_disk()
    channel_lut = server.get_channel_lut()
    effects_config = server.get_effects_config()

    for filename, filepath in get_all_paths(rekordbox_song_directory, only_files=True, recursive=True):
        if filepath.suffix in ['.py', '.exe']:
            continue
        new_show, local_filepath = generate_show.generate_show(filepath, channel_lut, effects_config, overwrite=True, simple=False, debug=True, include_song_path=False, output_directory=effect_output_directory, random_color=False)
        remote_folder = pathlib.Path('/home/pi/light-show/effects/rekordbox_effects')
        print_blue(f'Show created, scping from "{local_filepath}" to folder "{remote_folder}"')

        youtube_helpers.scp_to_doorbell(local_filepath, remote_folder)
