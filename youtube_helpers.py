import json
import os
import sys

import yt_dlp

from helpers import *


def scp_to_doorbell(local_filepath, remote_folder):
    # looks like most people use https://www.fabfile.org/ for the higher level library
    import paramiko
    from scp import SCPClient
    
    remote_filepath = remote_folder.joinpath(local_filepath.name)

    # doorbell_ip = 'doorbell'
    doorbell_ip = '192.168.86.58'

    ssh = paramiko.client.SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=doorbell_ip, # doorbell IP
                port = 22,
                username='pi')

    print(f'{bcolors.OKBLUE}Moving from "{local_filepath}", to remote "{doorbell_ip}:{remote_filepath}"{bcolors.ENDC}')
    scp = SCPClient(ssh.get_transport())
    scp.put(local_filepath, remote_filepath)
    scp.close()


def download_youtube_url_to_ogg(url=None, dest_path=None, max_length_seconds=None):
    if url is None:
        url = input('Enter the URL you want to download:\n')

    inject_path_prefix = dest_path or ''
    
    # all ydl opts: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
    ydl_opts = {
        'format': 'vorbis/bestaudio/best',
        'outtmpl': f'{str(inject_path_prefix) + os.path.sep}%(title)s.%(ext)s',
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'vorbis',
        }],
        'noplaylist': True,
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if max_length_seconds is not None:
                info_dict_no_dl = ydl.extract_info(url, download=False)
                vid_duration_seconds = info_dict_no_dl['duration']
                print(f'Duration of video is {vid_duration_seconds} seconds, max is {max_length_seconds} seconds')
                if vid_duration_seconds > max_length_seconds:
                    print_yellow(f'Video is too long, returning')
                    return None

            info_dict = ydl.extract_info(url, download=True)
            download_infos = info_dict['requested_downloads']
            if not download_infos:
                raise Exception('The youtube video didnt download, download_infos is empty')
            if len(download_infos) > 1:
                raise Exception('Multiple youtube videos were downloaded, this shouldnt be possible')
            info = download_infos[0]
            downloaded_filepath = pathlib.Path(info['filepath'])
    except Exception as e:
        print(f'Couldnt download url {url} due to {e}')
        return None

    # this sucks for some reason
    no_special_name = ''.join(char for char in downloaded_filepath.stem if char.isalnum() or char == ' ')
    if downloaded_filepath.name != no_special_name + downloaded_filepath.suffix:
        if not no_special_name:
            no_special_name = random_letters(5)
            print(f'Somehow {downloaded_filepath} has stripped down to nothing, making up {no_special_name} to assign')
        no_special_name += downloaded_filepath.suffix
        no_special_chars_filepath = downloaded_filepath.parent.joinpath(no_special_name)
        os.rename(downloaded_filepath, no_special_chars_filepath)
        return no_special_chars_filepath

    return downloaded_filepath


if __name__ == '__main__':
    url = None
    if len(sys.argv) > 1:
        url = sys.argv[1]
    max_length_seconds = None
    if len(sys.argv) > 2:
        max_length_seconds = float(sys.argv[2])
    downloaded_filepath = download_youtube_url_to_ogg(url=url, dest_path=python_file_directory.joinpath('songs'), max_length_seconds=max_length_seconds)
    if downloaded_filepath is None:
        exit()

    # remote_folder = pathlib.Path('/home/pi/light-show/songs')
    # print('Starting scp to doorbell')
    # scp_to_doorbell(local_filepath=downloaded_filepath, remote_folder=remote_folder)



# KEY: id
# KEY: title
# KEY: formats
# KEY: thumbnails
# KEY: thumbnail
# KEY: description
# KEY: uploader
# KEY: uploader_id
# KEY: uploader_url
# KEY: channel_id
# KEY: channel_url
# KEY: duration
# KEY: view_count
# KEY: average_rating
# KEY: age_limit
# KEY: webpage_url
# KEY: categories
# KEY: tags
# KEY: playable_in_embed
# KEY: is_live
# KEY: was_live
# KEY: live_status
# KEY: release_timestamp
# KEY: automatic_captions
# ['af', 'ak', 'sq', 'am', 'ar', 'hy', 'as', 'ay', 'az', 'bn', 'eu', 'be', 'bho', 'bs', 'bg', 'my', 'ca', 'ceb', 'zh-Hans', 'zh-Hant', 'co', 'hr', 'cs', 'da', 'dv', 'nl', 'en-orig', 'en', 'eo', 'et', 'ee', 'fil', 'fi', 'fr', 'gl', 'lg', 'ka', 'de', 'el', 'gn', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jv', 'kn', 'kk', 'km', 'rw', 'ko', 'kri', 'ku', 'ky', 'lo', 'la', 'lv', 'ln', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'ne', 'nso', 'no', 'ny', 'or', 'om', 'ps', 'fa', 'pl', 'pt', 'pa', 'qu', 'ro', 'ru', 'sm', 'sa', 'gd', 'sr', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'st', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'ti', 'ts', 'tr', 'tk', 'uk', 'und', 'ur', 'ug', 'uz', 'vi', 'cy', 'fy', 'xh', 'yi', 'yo', 'zu']
# KEY: subtitles
# []
# KEY: comment_count
# KEY: chapters
# KEY: like_count
# KEY: channel
# KEY: channel_follower_count
# KEY: upload_date
# KEY: availability
# KEY: original_url
# KEY: webpage_url_basename
# KEY: webpage_url_domain
# KEY: extractor
# KEY: extractor_key
# KEY: playlist
# KEY: playlist_index
# KEY: display_id
# KEY: fulltitle
# KEY: duration_string
# KEY: requested_subtitles
# KEY: _has_drm
# KEY: requested_downloads
# KEY: asr
# KEY: filesize
# KEY: format_id
# KEY: format_note
# KEY: source_preference
# KEY: fps
# KEY: height
# KEY: quality
# KEY: has_drm
# KEY: tbr
# KEY: url
# KEY: width
# KEY: language
# KEY: language_preference
# KEY: preference
# KEY: ext
# KEY: vcodec
# KEY: acodec
# KEY: dynamic_range
# KEY: abr
# KEY: downloader_options
# ['http_chunk_size']
# KEY: container
# KEY: protocol
# KEY: audio_ext
# KEY: video_ext
# KEY: format
# KEY: resolution
# KEY: http_headers

# 'downloader_option""" s': {'http_chunk_size': 10485760}, 
# 'container': 'webm_dash', 'protocol': 'https', 'audio_ext': 'webm', 'video_ext': 'none', 'format': '251 - audio only (medium)', 'resolution': 'audio only', 

# 'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-us,en;q=0.5', 'Sec-Fetch-Mode': 'navigate'}, 

# 'epoch': 1661879371, '_filename': '/home/andrew/programming/python/light-show/songs/[regex_01] Learn about four regex special characters - . _ $ ^.webm', '__postprocessors': [], '__real_download': True, '__finaldir': '/home/andrew/programming/python/light-show/songs', 'filepath': '/home/andrew/programming/python/light-show/songs/[regex_01] Learn about four regex special characters - . _ $ ^.ogg', '__write_download_archive': True}], 'asr': 48000, 'filesize': 4460455, 'format_id': '251', 'format_note': 'medium', 'source_preference': -1, 'fps': None, 'height': None, 'quality': 3, 'has_drm': False, 'tbr': 105.087, 'url': 'https://rr3---sn-jvhj5nu-cvnk.googlevideo.com/videoplayback?expire=1661900970&ei=SkQOY_-iG4yF8wTDhqj4CQ&ip=73.143.173.76&id=o-AMNz4tVSAYpGqgmidOx5T6DxHaMMWPiGjcw2_MCcLYTM&itag=251&source=youtube&requiressl=yes&mh=Uv&mm=31%2C29&mn=sn-jvhj5nu-cvnk%2Csn-ab5l6ndy&ms=au%2Crdu&mv=m&mvi=3&pl=23&initcwndbps=1725000&vprv=1&mime=audio%2Fwebm&gir=yes&clen=4460455&otfp=1&dur=339.561&lmt=1607751812560202&mt=1661878888&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&rbqsm=fr&txp=6211222&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cotfp%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAJn4_gb-NfbM5yKv-4hGcuncUWGISIWhoyI78R_3VbL9AiBm974caezi5KPomgDq0zuG4zVrVNeX3SNbVNhLNyR5-A%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIhAKge_gFyTbNCL3UUzipdpSU4zxG7D2RmgreJqVaAQET1AiAYHxj7UZzGFasUnTQgAFEKI6k37O9FYSsXVv7BGgvcaA%3D%3D', 'width': None, 'language': '', 'language_preference': -1, 'preference': None, 'ext': 'webm', 'vcodec': 'none', 'acodec': 'opus', 'dynamic_range': None, 'abr': 105.087, 'downloader_options': {'http_chunk_size': 10485760}, 'container': 'webm_dash', 'protocol': 'https', 'audio_ext': 'webm', 'video_ext': 'none', 'format': '251 - audio only (medium)', 'resolution': 'audio only', 'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-us,e """n;q=0.5', 'Sec-Fetch-Mode': 'navigate'}}