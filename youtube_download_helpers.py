import os
import argparse
import traceback
import json
from copy import deepcopy
import time
import subprocess
import shutil

from helpers import *


this_file_directory = pathlib.Path(__file__).parent.resolve()

ydl_search_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'download': False,
    # 'skip_download': True,
    # 'player_client': ['web'],
    # 'getid': True,
    'quiet': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


# API limiters
global last_youtube_searched_time
last_youtube_searched_time = None

minimum_youtube_api_wait_time_seconds = 1


# todo look into one of these, i the JS intepretor is being run in yt_download which is ridiculous: 
    # https://github.com/andrscyv/fast_youtube_search/blob/master/fast_youtube_search/search.py
    # https://github.com/alexmercerind/youtube-search-python
    # https://github.com/damonwonghv/youtube-search-api
def youtube_search_new(search_phrase, timing=False):
    time_start = time.time()
    num_requests = 1
    retcode, stdout, stderr = run_command_blocking([
        'yt-dlp',
        '--max-downloads', '1',
        '--flat-playlist',
        f'ytsearch{num_requests}:{search_phrase}',
        '--get-id',
        '--get-title',
        '--skip-download',
    ], stderr_pipe=subprocess.PIPE, stdout_pipe=subprocess.PIPE)
    if retcode:
        return print_red(f'Couldnt download "{search_phrase}" due to {get_stack_trace()}')
    _title, video_id = [line.strip() for line in stdout.splitlines() if line.strip()]
    if timing: print_blue(f'youtube_search_new took {time.time() - time_start} seconds')
    return f'https://www.youtube.com/watch?v={video_id}'


# variables to control search
results_to_consider = 1
def youtube_search(search_phrase, minimum_length_of_video_seconds=50, maximum_length_of_video_seconds=1000):
    # idk think about all this stuff
    global last_youtube_searched_time
    import yt_dlp
    if yt_dlp.version.__version__ < '2023.07.06':
        print(yt_dlp.version.__version__)
        raise Exception(f'Please run the command `pip install --upgrade yt-dlp`')

    if last_youtube_searched_time:
        time_to_wait = max(0, minimum_youtube_api_wait_time_seconds - (time.time() - last_youtube_searched_time))
        print(f'youtube_search: Sleeping {time_to_wait}')
        time.sleep(time_to_wait)

    curr_ydl_opts = deepcopy(ydl_search_opts)
    try:
        with yt_dlp.YoutubeDL(curr_ydl_opts) as ydl:
            # This line can throw a DownloadError, somehow split it up to consider the other results?
            to_search = f'ytsearch{results_to_consider}:{search_phrase}'
            print_blue(f'yt-dlp "{to_search}"')
            all_results = ydl.extract_info(to_search, download=False)
            for entry in all_results['entries']:
                if 'title' not in entry or 'webpage_url' not in entry:
                    print_red(f'Somehow title or webpage_url arent in this object {entry}')
                if 'duration' in entry and entry['duration'] >= minimum_length_of_video_seconds and entry['duration'] <= maximum_length_of_video_seconds:
                    tmp = get_temp_file()
                    with open(tmp, 'w') as f:
                        f.write(json.dumps(entry, indent=4))
                        print(f'Wrote search entry to {tmp}')
                    return entry
    except yt_dlp.DownloadError as e:
        # maybe i misread this, this can throw a DownloadError?
        print_red(f'Couldnt download "{search_phrase}" due to {get_stack_trace()}')

    last_youtube_searched_time = time.time()

# https://www.youtube.com/watch?v=2JpmVcJVfdQ
def download_youtube_url(url=None, dest_path=None, restrict_filenames=False, max_length_seconds=None, codec='vorbis', keep_video=False, cache_path=None):
    cache = {}
    if cache_path:
        cache_path = pathlib.Path(cache_path)
        if cache_path.exists():
            with open(cache_path, 'r') as f:
                cache = json.loads(f.read())
            if url in cache:
                print_green(f'Using cached url: {url}')
                return pathlib.Path(cache[url])

    if url is None:
        url = input('Enter the URL you want to download:\n')

    inject_path_prefix = dest_path or ''
    
    # all ydl opts: https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
    ydl_opts = {
        'format': f'{codec}/bestaudio/best',
        'outtmpl': f'{str(inject_path_prefix) + os.path.sep}%(title)s.%(ext)s',
        'restrictfilenames': restrict_filenames,
        'noplaylist': True,
        # See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': codec,
            'preferredquality': '0',
            # 'postprocessor_args': ['-ar', '48000'],
        }]
    }
#     ffmpeg
#  -i input.ogg -ar 48000 output.ogg

    if keep_video:
        ydl_opts['format'] = 'mp4/bestvideo/best' # !todo figure out if this is sacking video quality
        del ydl_opts['postprocessors']
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
        print_cyan(f'You probably need to run "pip install --upgrade yt_dlp"')
        return None

    if cache_path is not None:
        cache[url] = str(downloaded_filepath.absolute())
        with open(cache_path, 'w') as f:
            f.write(json.dumps(cache, indent=4))


    # changing to 48000hz in place
    # ffmpeg -i input.ogg -ar 48000 output.ogg

    extension = downloaded_filepath.suffix[1:]
    temp_output = get_temp_dir().joinpath(f'output.{extension}')
    print_green(f'Converting to 48000hz')
    retcode, stdout, stderr = run_command_blocking([
        'ffmpeg',
        '-i', str(downloaded_filepath),
        '-ar', '48000',
        str(temp_output),
    ])
    if retcode:
        print_red(f'Couldnt convert "{downloaded_filepath}" due to {stderr}')
        return None
    shutil.move(temp_output, downloaded_filepath)

    return downloaded_filepath


def process_playlist_video_renderers(playlist_video_renderers, videos):

    contributor_map = { 
        # generated by going to the playlist.  clicking on "by Eric Johnson and 13 others". 
        # inspecting that element and copying into claude, and gving this example and asking to extent
        'AIdro_kH8xRlSlTkyS2dguDj0fL91mWOqLPbnKX48gnnyNghkh11': 'Eric Johnson',
        'yti/ANjgQV-MqCnkF6jVQ_VNZ9LHD-D_KQ20w7JG-BRFGROF_b0': 'caschoener',
        'AIdro_nLOZiVoOnOY9sRG6PEfbeJQZgNEc94Ld_-R0YhapW-QHpFlNNHtQIwpPu8VJKX5wVYKg': 'Asmani Adhav',
        'AIdro_npcUR6XsdtEyWk5O0DUPbiBwaX_JeUikuODvjwubz_UpOPbxUG2HLiUrAGCHsdKbjT0g': 'HardQuestionsSimpleAnswers',
        'k__e7x5rKlrP1C0RaiL9vZYLSRE0rod2tPihCia7St4hqpl7yHenePAcqgdr2y-zSLcwCA-eoA': 'Incredible Memes',
        'AIdro_kpKZmzjrnNovcN37hiSQCEbrSCkLY8LEipYH8rJAg': 'lilwwl',
        'AIdro_m5V11sHxUxl0ogrSijXsvoMeBwHoRkO89CFz_ocI7-3o8': 'Lindsay C',
        'AIdro_najrNirkES91uW9O1x7uafNumbXLKuwgH-mLyamJqgfhwuBIDWRZGGBzH6fCNh-gOl0g': 'Maria Melchiorre',
        'AIdro_nXw5ZQhNzk1L8PIr9wX8fGIwH0-Jm_Jv5zf8Bc4OVJWlrv': 'Mary',
        'AIdro_l1MaAg8KPvcHZsg8Rsx18KEFurnzOyyt2sSAAuklPuc4U': 'Nico Tapiero',
        'AIdro_m4ocI3PZO6xxSVnWxJolEF60857FYrcJ78Dd_T2-VtoQo': 'Paul Farcasanu',
        'AIdro_kB0N2thlgiesfEOngboFyXozgcJ05SAWXuU1CDMs0': 'Robert Kerstens',
        'AIdro_mCWPvAqYUv-F0Vj0DZtyCDGDlIlAUtRinGRMwNYx4': 'StreamerGames',
        'AIdro_m7jFOr5WTivlEhGi5Aiukamm_IDgshihHjS7XoWXi2Tw': 'whyemma1'
    }        

    continuation_token = None
    for item3 in playlist_video_renderers:
        if 'playlistVideoListRenderer' not in item3 and 'continuationItemRenderer' in item3:
            ce = item3['continuationItemRenderer']['continuationEndpoint']; continuation_token = ce['commandExecutorCommand']['commands'][1]['continuationCommand']['token'] if 'commandExecutorCommand' in ce else ce['continuationCommand']['token']

            print_blue(f'continuation token: {continuation_token}')
            continue
            
        video_renderer = item3['playlistVideoRenderer']
        title = video_renderer['title']['runs'][0]['text']
        if len(video_renderer['title']['runs']) > 1:
            print_blue(f'Why is runs greater than 1 for {title}?')

        video_id = video_renderer['navigationEndpoint']['watchEndpoint']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        # Extract avatar URL from thumbnailOverlays
        try:
            avatar_url = video_renderer['thumbnailOverlays'][-1]['thumbnailOverlayAvatarStackViewModel']['avatarStack']['avatarStackViewModel']['avatars'][0]['avatarViewModel']['image']['sources'][1]['url']
            # Extract unique identifier from URL
            unique_id = avatar_url.split('/')[4].split('=')[0]
            
            # Look up in map, or use unique ID if not found
            contributor_name = contributor_map.get(unique_id, unique_id)
            if contributor_name == unique_id:
                # If not found in map, try to extract name from unique_id
                contributor_name = unique_id.split('_', 1)[1] if '_' in unique_id else unique_id
        except:
            contributor_name = 'unknown_err'

        videos.append((title, video_url, contributor_name))
    
    return continuation_token


def get_info_from_youtube_playlist(url, write_files=True):
    print(f'URL: {url}')
    curl = subprocess.Popen(['curl', url], stdout=subprocess.PIPE)
    out = curl.stdout.read().decode("utf-8")
    start = out.find("var ytInitialData = ") + 20
    end = out.find(";</script>", start)
    videos = []
    continuation_token = None
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
                        list3 = item2['playlistVideoListRenderer']['contents']
                        continuation_token = process_playlist_video_renderers(list3, videos)
                    except Exception as e:
                        print_red(f'parsing 4 failed last time it was list3, printing below: {traceback.format_exc()}')
                        # print(list3)
            except Exception as e:
                print_red(f'parsing 3 failed: {traceback.format_exc()}')
    else:
        print('--- WARNING: JSON NOT FOUND ---')

    print(f'{len(videos)} videos so far, there was a continuation_token, making another request for the next page in 1 seconds')
    continuation_index = 0
    while continuation_token:
        import requests
        time.sleep(1)
        print_blue(f'Querying continuation_token: {continuation_token}')

        url = 'https://www.youtube.com/youtubei/v1/browse'
        params = {
            # currently this is the INNER_TUBE_API_KEY and its hardcoded i think https://github.com/0xced/XCDYouTubeKit/pull/545
            'key': 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8',
            'prettyPrint': False,
        }
        body = {
            'context': {
                'client': {
                    'clientName': 'WEB',
                    'clientVersion': '2.20221024.01.00'
                }
            },
            'continuation': continuation_token
        }
        continuation_token = None
        response = requests.post(url, params=params, json=body)
        print(f'continuation request {continuation_index} status code: {response.status_code}')
        if response.status_code >= 500:
            print_red('500 status code, so returning no videos')
            return []
        if write_files:
            with open(get_temp_dir().joinpath(f'playlist_full_cont_{continuation_index}.json'), 'w', encoding="utf-8") as f:
                f.write(response.text)
        
        response_json = json.loads(response.text)
        recieved_action = response_json['onResponseReceivedActions'][0]
        continuation_items = recieved_action['appendContinuationItemsAction']
        playlist_video_renders = continuation_items['continuationItems']
        continuation_token = process_playlist_video_renderers(playlist_video_renders, videos)
        continuation_index += 1
    # print(f'{len(videos)} titles: ', ', '.join(map(lambda x: x[0], videos)))
    return videos





if __name__ == '__main__':
    print(this_file_directory.stem)
    default_for_this_dir = this_file_directory.stem == 'light-show'

    make_if_not_exist(pathlib.Path(__file__).resolve().parent.joinpath('songs'))
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument('url', type=str)
    parser.add_argument('--no_show', dest='gen_show', default=default_for_this_dir, action='store_false')
    parser.add_argument('--max_seconds', dest='max_seconds', default=None, type=float)
    parser.add_argument('--video', dest='keep_video', default=False, action='store_true')
    args = parser.parse_args()

    output_directory = pathlib.Path(__file__).parent.joinpath('songs')

    print(f'Downloading youtube video to {output_directory}')
    downloaded_filepath = download_youtube_url(url=args.url, dest_path=output_directory, max_length_seconds=args.max_seconds, keep_video=args.keep_video)
    if downloaded_filepath is None:
        print('Couldnt download video')
        exit()

    if args.gen_show:
        print_blue('Generating show file for the downloaded file')
        import autogen
        relative_downloaded_filepath = downloaded_filepath.relative_to(pathlib.Path(__file__).parent)
        output_filepath = pathlib.Path(__file__).parent.joinpath('effects').joinpath(downloaded_filepath.stem + '.py')
        _song_length, bpm_guess, delay, _boundary_beats, chunk_levels = autogen.get_src_bpm_offset(downloaded_filepath, use_boundaries=False)
        output_filepath = autogen.write_effect_to_file_pretty(
            output_filepath, 
            {
                downloaded_filepath.stem: {
                    'bpm': bpm_guess,
                    'song_path': str(relative_downloaded_filepath),
                    'delay_lights': delay,
                    'skip_song': 0.0,
                    'beats': [
                    ],
                }
            },
            write_compiler=True,
            # rip_out_char='"',
        )

    remote_folder = pathlib.Path('/home/pi/light-show/songs')
    print('Starting scp to doorbell')
    try:
        scp_to_doorbell(local_filepath=downloaded_filepath, remote_folder=remote_folder)
    except:
        print_stacktrace()
        print_yellow('The above error means the scp of the song failed scping to the doorbell, but the song was still downloaded to the local machine and the show was made. You will have to manually scp the song file over at some point')

    if args.gen_show:
        print_green(bold(f'\nStart editing your show here: "{output_filepath}"'))




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