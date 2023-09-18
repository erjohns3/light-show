import pathlib
import shutil

import script_helpers
script_helpers.make_directory_above_importable()

from helpers import *
import sound_video_helpers

this_file_folder = pathlib.Path(__file__).parent.resolve()


# !TODO DO THIS I THINK PROBABLY WAY FASTER:
# import demucs.separate
# demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", "track with space.mp3"])

def separate_stem(audio_path, stem, desintation_folder=get_temp_dir()):
    avail_stems = ['vocals', 'drums', 'bass', 'other']
    if stem not in avail_stems:
        print_red(f'invalid separation stem "{stem}", need to choose from {avail_stems}')
        exit()

    wanted_output_stem_path = desintation_folder.joinpath(f'STEM_{stem.upper()}_{audio_path.stem}.mp3')
    wanted_output_no_stem_path = desintation_folder.joinpath(f'STEM_NO_{stem.upper()}_{audio_path.stem}.mp3')

    if wanted_output_stem_path.exists() and wanted_output_no_stem_path.exists():
        print_yellow(f'Skipping "{audio_path}" because it already has stems')
        return wanted_output_stem_path, wanted_output_no_stem_path

    separation_model = 'htdemucs_ft'
    expected_demucs_output_stem = get_temp_dir().joinpath(separation_model, audio_path.stem, f'{stem}.mp3')
    expected_demucs_output_no_stem = get_temp_dir().joinpath(separation_model, audio_path.stem, f'no_{stem}.mp3')
    if not expected_demucs_output_stem.exists():
        ret_code, stdout, stderr = run_command_blocking([
            'demucs',
            '-n', separation_model,
            audio_path,
            '--two-stems', stem,
            '-o', get_temp_dir(),
            '--mp3',
        ], stdout_pipe=None, stderr_pipe=None, debug=False)
        if ret_code:
            print_red(f'error running demucs, you probably need to install it with "pip install demucs": {stderr}')
            exit()
    
    if not expected_demucs_output_stem.exists() or not expected_demucs_output_no_stem.exists():
        return None, print_red(f'expected separated output "{expected_demucs_output_stem}" or "{expected_demucs_output_no_stem}" doesnt exist')

    shutil.move(expected_demucs_output_stem, wanted_output_stem_path)
    shutil.move(expected_demucs_output_no_stem, wanted_output_no_stem_path)
    return wanted_output_stem_path, wanted_output_no_stem_path



wanted_stems = ['vocals']

music_folder_name = 'StreamerGames'
music_folder = get_ray_directory().joinpath('music_creation', 'downloaded_songs', music_folder_name)
stem_destination_folder = make_if_not_exist(music_folder.parent.joinpath(f'{music_folder_name}_STEMS'))

audio_paths = list(get_all_paths(music_folder, allowed_extensions=['.mp3', '.wav', '.ogg']))
actual_paths_to_use = []
for _, audio_path in audio_paths:
    length = sound_video_helpers.get_length(audio_path)
    if length > 60 * 5:
        print_yellow(f'Skipping "{audio_path}" because its longer than 5 minutes')
        continue
    actual_paths_to_use.append(audio_path)

input(print_red(f'Going to convert {len(actual_paths_to_use)} songs (skipped {len(audio_paths) - len(actual_paths_to_use)}) to stems: {wanted_stems}, press enter to continue'))

for audio_path in actual_paths_to_use:
    for stem_type in wanted_stems:
        stem_path, no_stem_path = separate_stem(audio_path, stem_type, desintation_folder=stem_destination_folder)
        print_green(f'{green("Created stems")}:\n    stem: {stem_path}\n    no_stem: {no_stem_path}')
