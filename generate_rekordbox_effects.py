from helpers import *
import youtube_helpers
import generate_show


# import light_server
# light_server.load_effects_config_from_disk()
# channel_lut = light_server.get_channel_lut()
effects_config = generate_show.get_top_level_effect_config()

def generate_rekordbox_effect(filepath):
    import paramiko
    from scp import SCPClient

    effect_output_directory = pathlib.Path(__file__).parent.joinpath('effects').joinpath('rekordbox_effects')

    new_show, local_filepath = generate_show.generate_show(filepath, None, effects_config, overwrite=True, mode=None, include_song_path=False, output_directory=effect_output_directory, random_color=False)
    remote_folder = pathlib.Path('/home/pi/light-show/effects/rekordbox_effects')
    print_blue(f'Show created, scping from "{local_filepath}" to folder "{remote_folder}"')

    
    try:
        youtube_helpers.scp_to_doorbell(local_filepath, remote_folder)
    except:
        # !TODO catch teh right exception here (file not found)
        print_yellow('andrew: trying this new extra scp step on error (assuming rekord_box folder doesnt exist)')
    
        ssh = paramiko.client.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(hostname=youtube_helpers.doorbell_ip,
                    port = 22,
                    username='pi')

        youtube_helpers.scp_to_doorbell(local_filepath, remote_folder)


if __name__ == '__main__':
    rekordbox_song_directory = get_ray_directory().joinpath('music_creation', 'downloaded_songs')
    for filename, filepath in get_all_paths(rekordbox_song_directory, only_files=True, recursive=True):
        if filepath.suffix in ['.py', '.exe', '.html']:
            continue
        if filename.startswith('.'):
            continue
        generate_rekordbox_effect(filepath)