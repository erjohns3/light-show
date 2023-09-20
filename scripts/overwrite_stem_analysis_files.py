import shutil
import sys
import pathlib

import sqlite3

this_file_directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(this_file_directory.parent))

from helpers import *

# !TODO assumes all real are mp3s (should we)


# for ray: T:\programming\random\sqlcipher\bld\sqlite3.exe C:\Users\Ray\AppData\Roaming\Pioneer\rekordbox\master.db "PRAGMA key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497';" ".clone decrypted.db" ".exit"
# for dj: T:\programming\random\sqlcipher\bld\sqlite3.exe C:\Users\dj\AppData\Roaming\Pioneer\rekordbox\master.db "PRAGMA key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497';" ".clone decrypted.db"

path_to_sqcipher_exe = get_ray_directory().joinpath('programming', 'random', 'sqlcipher', 'bld', 'sqlite3.exe')

roaming_folder = pathlib.Path(os.getenv('APPDATA'))
path_to_master_db = roaming_folder.joinpath('Pioneer', 'rekordbox', 'master.db')
if not path_to_master_db.exists():
    print_red(f'{path_to_master_db} doesnt exist, fix')
    exit()

# if not is_ray():
#     # path_to_master_db = FILL IN ME
#     print_red('LOOK AT THE CODE AND FILL IN THE PATH TO THE MASTER DB')
#     exit()

decrypted_db_output_path = this_file_directory.joinpath('decrypted.db').absolute().resolve()
if decrypted_db_output_path.exists():
    print_yellow('Deleting old unencrypted DB')
    decrypted_db_output_path.unlink()

retcode, stdout, stderr = run_command_blocking([
    path_to_sqcipher_exe,
    path_to_master_db,
    'PRAGMA key = \'402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497\'',
    f'.clone \'{str(decrypted_db_output_path)}\'',
    '.exit',
], debug=True)
if retcode != 0:
    print_red(f'error decrypting: {retcode=} {stdout=} {stderr=}')
    sys.exit(1)

if not decrypted_db_output_path.exists():
    print_red(f'Decrypting DB to {decrypted_db_output_path} didnt work')
    exit()

print_green(f'Decrypted DB to {decrypted_db_output_path}')
before_pioneer = roaming_folder.joinpath('Pioneer', 'rekordbox', 'share')

song_to_analysis = {}
try:
    conn = sqlite3.connect(decrypted_db_output_path)
    cursor = conn.cursor()

    cursor.execute('SELECT FolderPath, BPM, AnalysisDataPath FROM djmdContent')
    rows = cursor.fetchall()

    for song_path, bpm, ending_analysis_path in rows:
        if ending_analysis_path:
            ending_analysis_path = ending_analysis_path[1:]
            analysis_path = before_pioneer.joinpath(ending_analysis_path)
            if not analysis_path.exists():
                print_red(f'DOESNT EXIST SKIPPING: {analysis_path=}')
                continue
            song_to_analysis[pathlib.Path(song_path).absolute()] = analysis_path
except sqlite3.Error as e:
    print_red('SQLite error:', e)
finally:
    conn.close()

if not song_to_analysis:
    print_red('song_to_analysis is empty, look at this')
    exit()

# print_cyan('All songs and analysis paths:')
# for song, analysis_path in song_to_analysis.items():
#     print(f'Song: {song}, analysis: {analysis_path}')


folder_to_stems_and_music = {}
rekordbox_songs_folder = get_ray_directory().joinpath('music_creation', 'downloaded_songs')
print_cyan('looking thru all songs for stems and non stems {rekordbox_songs_folder}')
for _, path in get_all_paths(rekordbox_songs_folder):
    if not path.is_dir():
        continue
    if path.name.endswith('_STEMS'):
        print_green(f'found stems folder: {path}')
        stems = list(get_all_paths(path))
        real_music_name = path.name.replace('_STEMS', '')
        real_music_path = path.parent.joinpath(real_music_name)
        if not real_music_path.exists():
            print_red(f'{real_music_path=} does not exist')
            continue
        folder_to_stems_and_music[path] = (stems, real_music_path)


# for song_path, analysis_path in song_to_analysis.items():

success = []
no_stem_analysis = []
no_real_analysis = []
no_real_path = []
for folder, (all_stem_paths, real_music_folder) in folder_to_stems_and_music.items():
    print(f'{folder=}')
    for _, stem_path in all_stem_paths:
        real_title = stem_path.name.replace('STEM_NO_VOCALS_', '').replace('STEM_VOCALS_', '')        

        real_path = real_music_folder.joinpath(real_title)
        if not real_path.exists():
            print_yellow(f'{real_path=} does not exist')
            no_real_path.append(real_path)
            continue
        if stem_path not in song_to_analysis:
            print_red(f'{stem_path=} not in song_to_analysis')
            no_stem_analysis.append(stem_path)
            continue
        if real_path not in song_to_analysis:
            print_red(f'{real_path=} not in song_to_analysis')
            no_real_analysis.append(real_path)
            continue
        copy_from = song_to_analysis[real_path]
        copy_to = song_to_analysis[stem_path]
        print_green(f'copying {real_path} to {stem_path}')
        # shutil.copy(copy_from, copy_to)
        success.append(stem_path)

total_fail = len(no_stem_analysis) + len(no_real_path) + len(no_real_analysis)

print()
print_yellow(f'{no_real_path=}')
print_red(f'Failed on {total_fail}, {len(no_stem_analysis)=}, {len(no_real_path)=}, {len(no_real_analysis)=}')
print_green(f'Copied {len(success)} analysis files from real to stems')

# from pysqlcipher3 import dbapi2 as sqlite
# db_path = 'master.db'
# key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497'
# conn = sqlite.connect(db_path)
# conn.execute(f'PRAGMA key = '{key}'')
# conn.execute('PRAGMA cipher_compatibility = 4')
