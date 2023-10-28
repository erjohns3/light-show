import sys
import signal
import argparse
import time

from helpers import *
import grid_helpers
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


def send_rekordbox_effects_to_doorbell():
    start_time = time.time()
    print_cyan('send_rekordbox_effects_to_doorbell: taring all effects...')
    process = run_command_async([
        'tar',
        'czf',
        '-',
        'effects/rekordbox_effects',
    ])

    print_cyan('redirecting output to ssh...')
    
    # run_command_blocking([
    #     'ps -ef | grep ssh-agent'
    # ])

    # !TODO this asks for a password, but it shouldnt, idk how to fix, on windows it works
    id_rsa_path = pathlib.Path.home().joinpath('.ssh', 'id_rsa')
    ret_code, stdout, stderr = run_command_blocking([
        'ssh',
        '-i',
        str(id_rsa_path),
        # '-T'
        'pi@192.168.86.55',
        'cd light-show && tar xvzf -',
    ], stdin=process.stdout)
    print(f'Result was {ret_code}. Finished sending rekordbox effects to doorbell in {time.time() - start_time} seconds')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser(description='Generate rekordbox effects')
    parser.add_argument('--skip_generation', dest='generate_shows', action='store_false', default=True, help='Skip generation of effects')
    parser.add_argument('--winamp', dest='winamp', default=None, action='store_true')
    args = parser.parse_args()

    if is_andrews_main_computer() and args.winamp == None:
        args.winamp = True

    if args.winamp == None:
        args.winamp = False

    if args.winamp:
        if not grid_helpers.try_load_winamp():
            print_red(f'Failed to load winamp, exiting')
            exit()

    # if is_andrews_main_computer():
    #     print_yellow('On andrews computer so using local song path')
    #     rekordbox_song_directory = pathlib.Path(__file__).resolve().parent.joinpath('songs')
    # else:

    rekordbox_song_directory = get_ray_directory().joinpath('music_creation', 'downloaded_songs')
    rekordbox_shows_output_directory = pathlib.Path(__file__).parent.joinpath('effects').joinpath('rekordbox_effects')

    if args.generate_shows:
        autogen.generate_all_songs_in_directory(rekordbox_song_directory, output_directory=rekordbox_shows_output_directory, include_song_path=True)

    if is_doorbell():
        print_yellow('Skipping SCP to doorbell because on doorbell')
        exit() 

    # if is_andrews_main_computer():
    #     print_yellow('Skipping SCP to doorbell because on andrews main computer')
    #     exit() 

    send_rekordbox_effects_to_doorbell()

    


