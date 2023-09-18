import pathlib
import shutil

import script_helpers
script_helpers.make_directory_above_importable()

from helpers import *

this_file_folder = pathlib.Path(__file__).parent.resolve()


def separate_stem(audio_path, part):
    avail_stems = ['vocals', 'drums', 'bass', 'other']
    if part not in avail_stems:
        print_red(f'invalid separation stem "{part}", need to choose from {avail_stems}')
        exit()

    separation_model = 'htdemucs_ft'
    expected_output = this_file_folder.joinpath('separated', separation_model, audio_path.stem)

    if not expected_output.exists():
        print('Running separation algo...')
        ret_code, stdout, stderr = run_command_blocking([
            'demucs',
            '-n', separation_model,
            audio_path,
            '--mp3',
        ], stdout_pipe=None, stderr_pipe=None, debug=False)
        if ret_code:
            print_red(f'error running demucs, you probably need to install it with "pip install demucs": {stderr}')
            exit()
    
    full_path = expected_output.joinpath(f'{part}.mp3')
    if not full_path.exists():
        print_red(f'expected separated output "{full_path}" doesnt exist')
        exit()

    better_named_path = get_temp_dir().joinpath(f'{audio_path.stem}_{part}.mp3')
    if not better_named_path.exists():
        shutil.copy(full_path, better_named_path)
    return better_named_path



wanted_stems = ['vocals']

music_folder_name = 'Eric_Johnson'
music_to_stem = get_ray_directory().joinpath('music_creation', 'downloaded_songs', music_folder_name)

paths = list(get_all_paths(music_to_stem), allowed_extensions=['.mp3', '.wav', '.ogg'])
actual_paths_to_use = []
for _, path in paths:
    get_length
    if path.stem.endswith('_vocals'):
        continue
    actual_paths_to_use.append(path)


print_yellow(f'Going to convert {len(paths)} songs to ')