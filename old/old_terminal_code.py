            # getting duration thru the song
            # time_diff = time.time() - time_start
            # song_path = effects_config[effect_name]['song_path']
            # if 'song_path' in songs_config:
            #     f", {round(100 * (time_diff / songs_config[song_path]['duration']))}% song"

# Seconds: {round(time.time() - time_start, 2):.2f}\



    # # size_of_current_line = len(useful_info) - (terminal_size * (len(useful_info) // terminal_size))
    # size_of_current_line = len(useful_info) % (terminal_size + 1)
    # chars_until_end_of_line = terminal_size - size_of_current_line
    # # print(f'{size_of_current_line=}, {chars_until_end_of_line=}, {terminal_size=}')
    # useful_info += ' ' * chars_until_end_of_line
    # extra_lines_up = (len(useful_info) // (terminal_size + 1)) + 1
    # # if last_extra_lines is not None and last_extra_lines > extra_lines_up:
    # #     print(f'{" " * dead_space}\n' * (last_extra_lines - extra_lines_up))
    #     # print(f'last_extra_lines: {last_extra_lines}, extra_lines_up: {extra_lines_up}')
    #     # exit()




# terminal specific
if args.local:
    # straight pow(2, 16) to what i think it should be
    green_vals = {
        1: 1,
        .7: .6,
        .6: .4,
        .4: .2,
        .20: .13,
        0.1: .05,
        0: 0,    
    }
    red_vals = {
        1: 1,
        .7: .6,
        .6: .4,
        .4: .2,
        .20: .13,
        0.1: .05,
        0: 0,    
    }
    blue_vals = {
        1: 1,
        .7: .6,
        .6: .4,
        .4: .2,
        .20: .13,
        0.1: .05,
        0: 0,    
    }
    green_vals = {y:x for x, y in green_vals.items()}
    red_vals = {y:x for x, y in red_vals.items()}
    blue_vals = {y:x for x, y in blue_vals.items()}

    # floor to perceieved
    # green_vals = { 1: 1, .9: .95, .5: .70, .4: .60, .3: .45, .2: .30, .15: .25, .14: .2, .13: .18, .12: .15, .11: .1, .1: 0,  0: 0,  }
    # red_vals = { 1: 1,.9: .95,.5: .70,.4: .60,.3: .40,.25: .25,.2: .20,.14: .12,.13: .11,.12: 0, 0: 0, }
    # blue_vals = { 1: 1, .9: .90, .5: .65, .4: .50, .3: .35, .25: .28, .2: .2, .14: .15, .13: .13, .12: .11, .11: 0,  0: 0,  }

    max_num = pow(2, 16) - 1
    def get_interpolated_value(interpolation_dict, value):
        if value == 0:
            return 0
        if 255 <= value:
            return 255

        value /= 255
        pairs = sorted([(i, o) for i, o in interpolation_dict.items()])
        for index, (i1, o1) in enumerate(pairs):
            (i2, o2) = pairs[index + 1]
            if value <= pairs[index + 1][0]:
                difference_in_outputs = o2 - o1
                difference_in_inputs = i2 - i1
                difference_in_value = value - i1
                scaling = difference_in_value / difference_in_inputs
                # print(f'({i1=}, {i2=}), ({o1=}, {o2=}), {scaling=}, {difference_in_outputs=}, {difference_in_inputs=}, {difference_in_value=}')
                final_output = 255 * (o1 + (difference_in_outputs * scaling))
                # print(f'got {value}, returning: {final_output}')
                return int(final_output)

    terminal_lut = {'red': [0] * (255 + 1), 'green': [0] * (255 + 1), 'blue': [0] * (255 + 1)}
    for i in range(255 + 1):
        terminal_lut['red'][i] = get_interpolated_value(red_vals, i)
        terminal_lut['green'][i] = get_interpolated_value(green_vals, i)
        terminal_lut['blue'][i] = get_interpolated_value(blue_vals, i)
    purple = [153, 50, 204]
    terminal_size = os.get_terminal_size().columns


selected_song = all_candidates[0]
if len(all_candidates) > 1:
    non_autogen = list(filter(lambda x: not x.startswith('g_'), all_candidates))
    if len(non_autogen) != 1:
        raise Exception(f'{bcolors.FAIL}Too many candidates for show "{search}" {all_candidates}{bcolors.ENDC}')

    selected_song = non_autogen[0]

# if filter_song and effects_config[selected_song].get('song_not_avaliable', None):
#     print_yellow(f'Song isnt availiable for effect "{selected_song}", press enter to try downloading?')
#     input()
#     just_filename = pathlib.Path(effects_config[selected_song]['song_path']).stem
#     print(f'Searching with phrase "{just_filename}"')
#     youtube_search_result = youtube_helpers.youtube_search(just_filename)
#     if not youtube_search_result:
#         print('Couldnt find relevant video on youtube, exiting...')
#         exit()

#     url = youtube_search_result['webpage_url']
#     if youtube_helpers.download_youtube_url(url, dest_path='songs'):
#         print('downloaded video, continuing to try to recover')
#         effects_config[selected_song]['song_not_avaliable'] = False


# if search in collection:
#     return search
# search = name.lower()
# all_candidates = []

# lower_to_real = {x.lower():x for x in collection}
# for word in lower_to_real:
#     if search in word:
#         all_candidates.append(lower_to_real[word])
# if not all_candidates:
#     raise Exception(f'{bcolors.FAIL}No shows for "{search}" were found{bcolors.ENDC}')

# return all_candidates



# testing the youtube downloading
# the_thread = threading.Thread(target=download_song, args=('https://www.youtube.com/watch?v=tAhT6kFWkAo',))
# the_thread.start()



# print_yellow('Press ENTER to delete the autogen directory and retry')
# input()
# autogen_shows_dir = python_file_directory.joinpath('effects').joinpath('autogen_shows')
# # shutil.rmtree(autogen_shows_dir)
# # os.rmdir(autogen_shows_dir)
# update_config_and_lut_from_disk()


# old compile stuff

# numpy stuff
# final_channel += channels
# final_channel *= mult
# trying to optimize
# final_channel = list((x + y) * mult for x, y in zip(final_channel, channels))



# starter = time.time()
# block += time.time() - starter
# print(f'time spent in block: {block}')



# def fuzzy_find(name, valid_names, filter_words=None, filter_song=None):
#     if name in valid_names:
#         return name
#     name = name.lower()
#     all_candidates = []

#     if filter_song:
#         valid_names = list(filter(lambda x: 'song_path' in effects_config.get(x, []), valid_names))

#     if filter_words:
#         valid_names = list(filter(lambda x: any([y in x.lower() for y in filter_words]), valid_names))
#     valid_names = [x for x in valid_names if x[-5:] != '.webm']

#     lower_to_real = {x.lower():x for x in valid_names}
#     for show_name in lower_to_real:
#         if name in show_name:
#             all_candidates.append(lower_to_real[show_name])
#     if not all_candidates:
#         print(f'{bcolors.FAIL}No shows for "{name}" were found{bcolors.ENDC}')
#         exit()

#     selected_song = all_candidates[0]
#     if len(all_candidates) > 1:
#         # autogen = filter(lambda x: x.startswith('g_'), all_candidates)
#         non_autogen = list(filter(lambda x: not x.startswith('g_'), all_candidates))
#         if len(non_autogen) != 1:
#             print(f'{bcolors.FAIL}Too many candidates for show "{name}" {all_candidates}{bcolors.ENDC}')
#             exit()

#         selected_song = non_autogen[0]

#     if filter_song and effects_config[selected_song].get('song_not_avaliable', None):
#         print_yellow(f'Song isnt availiable for effect "{selected_song}", press enter to try downloading?')
#         input()
#         just_filename = pathlib.Path(effects_config[selected_song]['song_path']).stem
#         print(f'Searching with phrase "{just_filename}"')
#         youtube_search_result = youtube_helpers.youtube_search(just_filename)
#         if not youtube_search_result:
#             print('Couldnt find relevant video on youtube, exiting...')
#             exit()

#         url = youtube_search_result['webpage_url']
#         if youtube_helpers.download_youtube_url(url, dest_path='songs'):
#             print('downloaded video, continuing to try to recover')
#             effects_config[selected_song]['song_not_avaliable'] = False

#     return selected_song