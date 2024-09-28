import sys
import shutil
import pathlib

this_file_directory = pathlib.Path(__file__).parent
sys.path.append(str(this_file_directory.parent))
from helpers import *
import youtube_download_helpers


urls_to_read = this_file_directory.joinpath('input_download_mp3s_bulk.txt')
if not urls_to_read.exists():
    print_red(f'File not found: "{urls_to_read}". Exiting.')
    exit()

urls = []
with open(urls_to_read, 'r') as f:
    for line in f:
        if not line.strip():
            continue
        urls.append(line.strip())

if not urls:
    print_red('No URLs to download. Exiting.')
    exit()

def confirm():
    while True:
        response = input('Y/N: ').strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print_red('Invalid response. Please enter "Y" or "N".')


home_directory = pathlib.Path.home()
output_directory = home_directory.joinpath('music')
if not output_directory.exists():
    print_yellow(f'Create output directory? "{output_directory}"')
    if not confirm():
        print_red('Exiting.')
        exit()
    output_directory.mkdir()


for index, url in enumerate(urls):
    print_yellow(f'Downloading: "{url}"')
    output_path = youtube_download_helpers.download_youtube_url(url, dest_path = output_directory, codec='mp3')

    final_path = output_directory.joinpath(f'{index}_{output_path.name}')
    shutil.move(output_path, final_path)

    print_green(f'Downloaded song to "{final_path}"')