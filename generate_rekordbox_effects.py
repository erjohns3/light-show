import sys
import signal


from helpers import *
import autogen


# !TODO replace this with just the youtube_helpers
# def ssh_to_doorbell_make_if_not_exist(local_effect_path):
#     remote_folder = pathlib.Path('/home/pi/light-show/effects/rekordbox_effects')
#     try:
#         scp_to_doorbell(local_effect_path, remote_folder, keep_open=True)
#     except:
#         print_yellow('andrew: trying this new extra scp step on error (assuming rekord_box folder doesnt exist)')
#         _stdin, _stdout, _stderr = run_command_on_doorbell_via_ssh('mkdir /home/pi/light-show/effects/rekordbox_effects', keep_open=True)
#         scp_to_doorbell(local_effect_path, remote_folder)



def signal_handler(sig, frame):
    print('SIG Handler: ' + str(sig), flush=True)
    if 'multiprocessing' in sys.modules:
        import multiprocessing
        active_children = multiprocessing.active_children()        
        if active_children:
            print_yellow(f'Module multiprocessing was imported! Killing active_children processes, PIDS: {[x.pid for x in active_children]}')
            for child in active_children:
                print_yellow(f'killing {child.pid}')
                child.kill()
    sys.exit()



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # if is_andrews_main_computer():
    #     print_yellow('On andrews computer so using local song path')
    #     rekordbox_song_directory = pathlib.Path(__file__).resolve().parent.joinpath('songs')
    # else:

    rekordbox_song_directory = get_ray_directory().joinpath('music_creation', 'downloaded_songs')
    rekordbox_shows_output_directory = pathlib.Path(__file__).parent.joinpath('effects').joinpath('rekordbox_effects')

    autogen.generate_all_songs_in_directory(rekordbox_song_directory, output_directory=rekordbox_shows_output_directory, include_song_path=False)

    if is_linux() and not is_andrews_main_computer():
        print_yellow('Skipping SCP to doorbell because on doorbell')
        exit() 

    # if is_andrews_main_computer():
    #     print_yellow('Skipping SCP to doorbell because on andrews main computer')
    #     exit() 

    print_cyan('scping all effects to doorbell...')
    run_command_blocking([
        'tar',
        'czf',
        '-',
        'effects/autogen_shows',
    ])
    
    # redirect to
    run_command_blocking([
        'ssh', 
        '-T', 
        'pi@192.168.86.55',
        '"cd light-show && tar xvzf -"',
    ])
    
    # for effect_name, effect_path in get_all_paths(rekordbox_shows_output_directory, only_files=True, allowed_extensions=['.py']):
    #     ssh_to_doorbell_make_if_not_exist(effect_path)
    
    # close_connections_to_doorbell()


# import light_server
# light_server.load_effects_config_from_disk()
# channel_lut = light_server.get_channel_lut()


# def generate_rekordbox_effect(filepath):
#     _, _, local_filepath = autogen.generate_show(filepath, overwrite=True, mode=None, include_song_path=False, output_directory=effect_output_directory, random_color=False)

#     if is_andrews_main_computer():
#         print_yellow('Skipping SCP to doorbell because on andrews main computer')
#         return

#     print_blue(f'Show created, scping from "{local_filepath}" to folder "{remote_folder}"')
#     remote_folder = pathlib.Path('/home/pi/light-show/effects/rekordbox_effects')

#     try:
#         youtube_helpers.scp_to_doorbell(local_filepath, remote_folder)
#     except:
#         # !TODO catch the right exception here (file not found)
#         print_yellow('andrew: trying this new extra scp step on error (assuming rekord_box folder doesnt exist)')
    
#         ssh = paramiko.client.SSHClient()
#         ssh.load_system_host_keys()
#         ssh.connect(hostname=youtube_helpers.doorbell_ip,
#                     port = 22,
#                     username='pi')
#         stdin, stdout, stderr = ssh.exec_command('mkdir /home/pi/light-show/effects/rekordbox_effects')
#         youtube_helpers.scp_to_doorbell(local_filepath, remote_folder)


# for filename, filepath in get_all_paths(rekordbox_song_directory, only_files=True, recursive=True):
#     if filepath.suffix in ['.py', '.exe', '.html']:
#         continue
#     if filename.startswith('.'):
#         continue
#     generate_rekordbox_effect(filepath)