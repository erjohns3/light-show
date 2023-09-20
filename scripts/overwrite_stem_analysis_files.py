import sys
import pathlib

import sqlite3

this_file_directory = pathlib.Path(__file__).parent.absolute()
sys.path.append(str(this_file_directory.parent))

from helpers import *


# T:\programming\random\sqlcipher\bld\sqlite3.exe C:\Users\Ray\AppData\Roaming\Pioneer\rekordbox\master.db "PRAGMA key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497';" ".clone decrypted.db" ".exit"
retcode, stdout, stderr = run_command_blocking([
    'T:\programming\random\sqlcipher\bld\sqlite3.exe',
    'C:\Users\Ray\AppData\Roaming\Pioneer\rekordbox\master.db',
    '"PRAGMA key = \'402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497\';"',
    '".clone decrypted.db"',
    '".exit"',
])

if retcode != 0:
    print_red(f'error decrypting: {retcode=} {stdout=} {stderr=}')
    sys.exit(1)



unencrypted_db_path = this_file_directory.joinpath('decrypted.db')
roaming_folder = pathlib.Path(os.getenv('APPDATA'))
before_pioneer = roaming_folder.joinpath('Pioneer', 'rekordbox', 'share')

try:
    conn = sqlite3.connect(unencrypted_db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT FolderPath, BPM, AnalysisDataPath FROM djmdContent')
    rows = cursor.fetchall()

    song_to_analysis = {}
    for song_path, bpm, ending_analysis_path in rows:
        if ending_analysis_path:
            ending_analysis_path = ending_analysis_path[1:]
            analysis_path = before_pioneer.joinpath(ending_analysis_path)
            if not analysis_path.exists():
                print_red(f'DOESNT EXIST SKIPPING: {analysis_path=}')
                continue
            song_to_analysis[pathlib.Path(song_path).resolve()] = analysis_path
except sqlite3.Error as e:
    print_red('SQLite error:', e)
finally:
    conn.close()

folder_to_stems_and_music = {}
rekordbox_songs_folder = get_ray_directory().joinpath('music_creation', 'downloaded_songs')
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


for folder, (all_stem_paths, real_music_folder) in folder_to_stems_and_music.items():
    print(f'{folder=}')
    for _, stem_path in all_stem_paths:
        real_title = stem_path.name.replace('STEM_NO_VOCALS_', '').replace('STEM_VOCALS_', '')        

        real_path = real_music_folder.joinpath(real_title)
        if not real_path.exists():
            print_yellow(f'{real_path=} does not exist')
            continue
        if stem_path not in song_to_analysis:
            print_red(f'{stem_path=} not in song_to_analysis')
            continue
        if real_path not in song_to_analysis:
            print_red(f'{real_path=} not in song_to_analysis')
            continue
        copy_from = song_to_analysis[real_path]
        copy_to = song_to_analysis[stem_path]
        print_green(f'copying {stem_path} to {real_path} - {copy_from=} to {copy_to=}')
        import shutil
        shutil.copy(copy_from, copy_to)

# from pysqlcipher3 import dbapi2 as sqlite
# db_path = 'master.db'
# key = '402fd482c38817c35ffa8ffb8c7d93143b749e7d315df7a81732a1ff43608497'
# conn = sqlite.connect(db_path)
# conn.execute(f'PRAGMA key = '{key}'')
# conn.execute('PRAGMA cipher_compatibility = 4')
