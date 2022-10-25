import os
import argparse
import traceback
import json
import shutil

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
    ssh.connect(hostname=doorbell_ip,
                port = 22,
                username='pi')

    print(f'{bcolors.OKBLUE}Moving from "{local_filepath}", to remote "{doorbell_ip}:{remote_filepath}"{bcolors.ENDC}')
    scp = SCPClient(ssh.get_transport())

    if is_windows():
        remote_filepath = str(remote_filepath).replace('\\\\', '/').replace('\\', '/')
    scp.put(str(local_filepath), remote_filepath)
    scp.close()


def download_youtube_url(url=None, dest_path=None, max_length_seconds=None, codec='vorbis'):
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
            'preferredcodec': codec,
        }],
        'noplaylist': True,
    }
    import yt_dlp

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if max_length_seconds is not None:
                info_dict_no_dl = ydl.extract_info(url, download=False)
                vid_duration_seconds = info_dict_no_dl['duration']
                print(f'Duration of video is {vid_duration_seconds} seconds, max is {max_length_seconds} seconds')
                if vid_duration_seconds > max_length_seconds:
                    print_yellow(f'Video is too long, returning')
                    return None

            print_green(f'started downloading {url}')
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
        
        shutil.move(downloaded_filepath, no_special_chars_filepath)
        return no_special_chars_filepath

    return downloaded_filepath


def get_info_from_youtube_playlist(url, write_files=True):
    print(f'URL: {url}')
    curl = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
    out = curl.stdout.read().decode("utf-8")
    start = out.find("var ytInitialData = ") + 20
    end = out.find(";</script>", start)
    videos = []
    print(f'start: {start}, end {end}')
    if start >= 0 and end >= 0:
        if write_files:
            with open(get_temp_dir().joinpath('playlist_full.html'), 'w', encoding="utf-8") as f:
                f.write(out)
            with open(get_temp_dir().joinpath('playlist_parse.html'), 'w', encoding="utf-8") as f:
                f.write(out[start:end])
        
        list1 = []
        try:
            dict = json.loads(out[start:end])
            list1 = dict['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']
        except Exception as e:
            print_red(traceback.format_exc())
            print(f'loading json failed', flush=True)
        
        # old
        for item1 in list1:
            try:
                list2 = item1['itemSectionRenderer']['contents']
                for item2 in list2:
                    try:
                        if 'playlistVideoListRenderer' not in item2 and 'continuationItemRenderer' in item2:
                            print('continuation item --- item3: ', item3)
                            continue

                        
                        list3 = item2['playlistVideoListRenderer']['contents']
                        for item3 in list3:
                            title_obj = item3['playlistVideoRenderer']['title']
                            title = title_obj['runs'][0]['text']
                            if len(title_obj['runs']) > 1:
                                print_blue(f'Why is runs greater than 1 for {title}?')

                            navigation_obj = item3['playlistVideoRenderer']['navigationEndpoint']
                            watch_endpoint_obj = navigation_obj['watchEndpoint']
                            video_id = watch_endpoint_obj['videoId']
                            video_url = f'https://www.youtube.com/watch?v={video_id}'

                            contributor_list = item3['playlistVideoRenderer']['contributorName']['runs']
                            
                            contributor_name = ''
                            for contributor_obj in contributor_list:
                                if 'Added by ' == contributor_obj['text']:
                                    continue
                                contributor_name = contributor_obj['text']

                            videos.append((title, video_url, contributor_name))
                    except Exception as e:
                        print_red(f'parsing 4 failed last time it was item3, printing below: {traceback.format_exc()}')
                        print(item3)
            except Exception as e:
                print_red(f'parsing 3 failed: {traceback.format_exc()}')
    else:
        print('--- WARNING: JSON NOT FOUND ---')

    print(f'There were {len(videos)} vidoes on the initial curl')
    if len(videos) >= 100:
        import requests
        print_blue('Querying continuation URL because there are over 100 videos...')
        time.sleep(3)

        # currently this is the INNER_TUBE_API_KEY and its hardcoded i think https://github.com/0xced/XCDYouTubeKit/pull/545
        url = 'https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false'
        # params = {
        #     'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
        #     'prettyPrint': False,
        # }

        body = {
            "client": {
                "clientName": "WEB",
                "clientVersion": "2.20221024.01.00"
            },
            "continuation": "4qmFsgJhEiRWTFBMOGdKZ2wwRHdjaEI2SW1vQjYwZkR2a3FMY2dyc1lDaC0aFENBRjZCbEJVT2tOSFVRJTNEJTNEmgIiUEw4Z0pnbDBEd2NoQjZJbW9CNjBmRHZrcUxjZ3JzWUNoLQ%3D%3D"
        }

        response = requests.post(url, json=json.dumps(body))
        # response = requests.post(url, params=params, json=body)
        print(f'response status code: {response.status_code}')
        print(f'default headers: {response.request.headers}')


        if write_files:
            with open(get_temp_dir().joinpath('playlist_full_cont_1.html'), 'w', encoding="utf-8") as f:
                f.write(response.text)
            # with open(get_temp_dir().joinpath('playlist_parse_cont_1.html'), 'w', encoding="utf-8") as f:
            #     f.write(out[start:end])

    exit()
    return videos


# working postman

# full URL: https://www.youtube.com/youtubei/v1/browse?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8&prettyPrint=false


# url: https://www.youtube.com/youtubei/v1/browse

# key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8
# prettyPrint=false


# body
# {
#     "context": {
#         "client": {
#             "clientName": "WEB",
#             "clientVersion": "2.20221024.01.00"
#         }
#     },
#     "continuation": "4qmFsgJhEiRWTFBMOGdKZ2wwRHdjaEI2SW1vQjYwZkR2a3FMY2dyc1lDaC0aFENBRjZCbEJVT2tOSFVRJTNEJTNEmgIiUEw4Z0pnbDBEd2NoQjZJbW9CNjBmRHZrcUxjZ3JzWUNoLQ%3D%3D"
# }



# python requests default headers
# {
#     'User-Agent': 'python-requests/2.26.0', 
#     'Accept-Encoding': 'gzip, deflate, br', 
#     'Accept': '*/*', 
#     'Connection': 'keep-alive', 
#     'Content-Length': '234', 
#     'Content-Type': 'application/json'
# }



# full dump

# {
#     "context":{
#     "client":{
#     "hl":"en","gl":"US","remoteHost":"73.143.173.76","deviceMake":"","deviceModel":"","visitorData":"CgtRVGpVSGpxelBPSSjY3dyaBg%3D%3D","userAgent":"Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0,gzip(gfe)","clientName":"WEB","clientVersion":"2.20221024.01.00","osName":"X11","osVersion":"","originalUrl":"https://www.youtube.com/playlist?list=PL8gJgl0DwchB6ImoB60fDvkqLcgrsYCh-","screenPixelDensity":2,"platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{
#     "appInstallData":"CNjd3JoGENSDrgUQmcauBRDpjf4SELKI_hIQvrauBRDiua4FEOrKrgUQgon-EhCo1K4FELiLrgUQ6dWuBRDbyq4FENmP_hIQmM2uBRDYvq0FEJH4_BI%3D"},"screenDensityFloat":1.5,"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"America/New_York","browserName":"Firefox","browserVersion":"106.0","acceptHeader":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8","deviceExperimentId":"CgtqRDB1UGRBaEtxMBDY3dyaBg%3D%3D","screenWidthPoints":847,"screenHeightPoints":503,"utcOffsetMinutes":-240,"mainAppWebInfo":{
#     "graftUrl":"https://www.youtube.com/playlist?list=PL8gJgl0DwchB6ImoB60fDvkqLcgrsYCh-","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":false}},"user":{
#     "lockedSafetyMode":false},"request":{
#     "useSsl":true,"internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{
#     "clickTrackingParams":"CDgQ7zsYACITCPOC1PSQ-voCFQPHPwQdV_AA6A=="},"adSignalsInfo":{
#     "params":[{
#     "key":"dt","value":"1666658009145"},{
#     "key":"flash","value":"0"},{
#     "key":"frm","value":"0"},{
#     "key":"u_tz","value":"-240"},{
#     "key":"u_his","value":"1"},{
#     "key":"u_h","value":"960"},{
#     "key":"u_w","value":"1707"},{
#     "key":"u_ah","value":"960"},{
#     "key":"u_aw","value":"1707"},{
#     "key":"u_cd","value":"24"},{
#     "key":"bc","value":"31"},{
#     "key":"bih","value":"503"},{
#     "key":"biw","value":"847"},{
#     "key":"brdim","value":"0,16,0,16,1707,0,847,937,847,503"},{
#     "key":"vis","value":"1"},{
#     "key":"wgl","value":"true"},{
#     "key":"ca_type","value":"image"}]}},"continuation":"4qmFsgJhEiRWTFBMOGdKZ2wwRHdjaEI2SW1vQjYwZkR2a3FMY2dyc1lDaC0aFENBRjZCbEJVT2tOSFVRJTNEJTNEmgIiUEw4Z0pnbDBEd2NoQjZJbW9CNjBmRHZrcUxjZ3JzWUNoLQ%3D%3D"}



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('url', type=str)
    parser.add_argument('--show', dest='gen_show', default=None, action='store_true')
    parser.add_argument('--max_seconds', dest='max_seconds', default=None, type=float)
    args = parser.parse_args()

    downloaded_filepath = download_youtube_url(url=args.url, dest_path=python_file_directory.joinpath('songs'), max_length_seconds=args.max_seconds)
    if downloaded_filepath is None:
        exit()

    if args.gen_show:
        import generate_show
        print_blue('Generating show file for the downloaded file')
        relative_downloaded_filepath = downloaded_filepath.relative_to(python_file_directory)
        output_filepath = python_file_directory.joinpath('effects').joinpath(downloaded_filepath.stem + '.py')
        _song_length, bpm_guess, delay, _boundary_beats = generate_show.get_src_bpm_offset(downloaded_filepath, use_boundaries=False)
        generate_show.write_effect_to_file_pretty(
            output_filepath, 
            {
                downloaded_filepath.stem + ' show': {
                    'bpm': bpm_guess,
                    'song_path': str(relative_downloaded_filepath),
                    'delay_lights': delay,
                    'skip_song': 0.0,
                    'beats': [],
                }
            },
            write_compiler=True,
        )

    remote_folder = pathlib.Path('/home/pi/light-show/songs')
    print('Starting scp to doorbell')
    scp_to_doorbell(local_filepath=downloaded_filepath, remote_folder=remote_folder)



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