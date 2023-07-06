

# adding to queue 
            # if len(song_queue) < 2:
            #     song_queue.append([name, get_queue_salt(), uuid])
            # else:
            #     for index, (queue_effect_name, uuid) in enumerate(song_queue):                
            #         if index == 0:
            #             continue
            #         print(f'checking if {queue_effect_name} was downloaded\n' * 8)
            #         if queue_effect_name not in songs_downloaded_this_process:
            #             print(f'inserting into {index + 1}\n' * 8)
            #             song_queue.insert(index + 1, [name, get_queue_salt(), uuid])
            #             break
            # songs_downloaded_this_process.add(name)



        # def gen_show_and_add_to_config(filepath, mode):
        #     new_effect, _output_filepath = generate_show.generate_show(filepath, overwrite=True, mode=mode)
        #     effect_name = list(new_effect.keys())[0]
        #     effects_config[effect_name] = new_effect[effect_name]
        #     # set_effect_defaults(effects_config[effect_name])
        #     add_dependancies(new_effect)
        #     return effect_name



# # only works to 10 decimal places
# def round_to(n, precision):
#     correction = 0.5 if n >= 0 else -0.5
#     return round(int( n/precision+correction ) * precision, 10)


# new_effects_made = set()
# def make_new_effect(effects_config, effect_name, hue_shift=0, sat_shift=0, bright_shift=0):
#     hue_shift = round_to(hue_shift, 0.05)
#     sat_shift = round_to(sat_shift, 0.05)
#     bright_shift = round_to(bright_shift, 0.01)
    
#     new_effect_name = effect_name + f' hue {hue_shift} sat {sat_shift} bright {bright_shift}'.replace('.', '_dot_')
#     if new_effect_name in new_effects_made:
#         return new_effect_name
#     new_effects_made.add(new_effect_name)

#     output_directory = pathlib.Path(__file__).parent.joinpath('effects', 'generated_effects')
#     if not os.path.exists(output_directory):
#         print(f'making directory {output_directory}')
#         os.mkdir(output_directory)

#     output_filepath = output_directory.joinpath(new_effect_name + '.py')

#     effects_config[new_effect_name] = {
#         'beats': [
#             [1, effect_name, effects_config[effect_name]['length']],
#         ],
#         'hue_shift': hue_shift,
#         'sat_shift': sat_shift,
#         'bright_shift': bright_shift,
#     }


#     # effects_config[new_effect_name] = deepcopy(effects_config[effect_name])
#     # effects_config[new_effect_name]['hue_shift'] = 90
#     # del effects_config[new_effect_name]['autogen']
#     # del effects_config[new_effect_name]['cache_dirty']
#     write_effect_to_file_pretty(output_filepath, {new_effect_name: effects_config[new_effect_name]})
#     return new_effect_name






# old shit to look thru effects:

# counting number of times effect is used
# effect_usages = {}
# for effect_name, effect in effect_files_json.items():
#     for beats in effect['beats']:
#         if type(beats[1]) == str:
#             if beats[1] not in effect_usages:
#                 effect_usages[beats[1]] = 0
#             effect_usages[beats[1]] += 1

# filtering to only ones in between 4 and 16
# effects_config_4_16 = dict(filter(lambda x: 4 <= x[1]['length'] <= 16, effects_config.items()))
# effect_usages_4_16 = dict(filter(lambda x: x[0] in effects_config_labeled, effect_usages.items()))


# making probability distribution
# effect_probabilities = {}
# total = sum(effect_usages_4_16.values())
# for effect_name, times_used in effect_usages_4_16.items():
#     effect_probabilities[effect_name] = times_used / total

# print('frequency of potential effects used')
# for times_used, effect_name in sorted([(x, y) for y, x in effect_usages_4_16.items()]):
#     print(f'times_used: {times_used}, {effect_name}')






# if rip_out_char is not None:
#     shows_json_str = shows_json_str.replace(rip_out_char, '')
# def eliminate(string, matches):
#     found = set()
#     for match in matches:
#         if match in found:
#             continue
#         found.add(match)
#         string = string.replace(match, '')
#     return string




# import colorsys
# from scipy.stats import circmean
# avg_hue_cache = {}
# def get_avg_hue(channel_lut, effect_name):
#     if effect_name in avg_hue_cache:
#         return avg_hue_cache[effect_name]
#     all_hues = []
#     for compiled_channel in channel_lut[effect_name]['beats']:
#         for i in range(3):
#             rd, gr, bl = compiled_channel[i * 3:(i * 3) + 3]
#             hue, sat, bright = colorsys.rgb_to_hsv(max(0, rd / 100.), max(0, bl / 100.), max(0, gr / 100.))
#             all_hues.append(hue)
#     avg_hue_cache[effect_name] = circmean(all_hues, low=0, high=1)
#     # print(all_hues, avg_hue_cache[effect_name])
#     # exit()
#     return avg_hue_cache[effect_name]






                # executor.map(partial(gen_show_worker, mode=args.autogen_mode), all_song_paths)


    # if any(disco_color_rgb):
    #     disco_chars = [' '] * 14 
    #     for rgb_index in range(3):
    #         if disco_color_rgb[rgb_index]:
    #             curr_disco_positions = [
    #                 int(disco_pos) + rgb_index,
    #                 int(disco_pos) + 5 + rgb_index,
    #                 int(disco_pos) + 10 + rgb_index,
    #             ]
    #             for index in range(len(curr_disco_positions)):
    #                 curr_disco_positions[index] = curr_disco_positions[index] % 14
    #                 disco_chars[curr_disco_positions[index]] = 'o'
    #                 disco_styles[curr_disco_positions[index]][rgb_index] = disco_color_rgb[rgb_index]


        # if args.autogen == 'all':
        #     import tqdm
        #     from functools import partial
        #     from concurrent.futures import ThreadPoolExecutor, as_completed, wait

        #     autogen_song_directory = 'songs'
        #     print_yellow(f'AUTOGENERATING ALL SHOWS IN DIRECTORY {autogen_song_directory}')
        #     # for _name, song_path in get_all_paths(autogen_song_directory, only_files=True):

        #     all_song_paths = list(map(lambda x: x[1], get_all_paths(autogen_song_directory, only_files=True)))
        #     progress_bar = tqdm.tqdm(total=len(all_song_paths))
        #     with ThreadPoolExecutor() as executor:
        #         futures = [executor.submit(gen_show_worker, song_path, mode=args.autogen_mode) for song_path in all_song_paths]


        #         # 18 in flight light shows: {'Nice For What', 'Jon Hopkins  Breathe This Air feat Purity Ring Official Video', 'Jsan x Pandrezz  Insomnia', 'Coldplay  Paradise Official Audio', 'UH OH TOWN Original Aka Stinky Lavender Town', 'DRAM  Broccoli feat Lil Yachty Official Music Video', 'Hypnocurrency', 'Daft Punk  Get Lucky Evan Duffy Improvisation', 'Tailwind', 'Møme  Aloha Official Music Video ft Merryn Jeann', 'Kenny Price - The Shortest Song In The World', 'Toby Keith  Red Solo Cup Unedited Version', 'Short Song', 's_Drake  Massive Official Audio', 'Halogen  U Got That', 'hooked', 'Littles kids playing recorders', 'Caravan Palace  Star Scat'}
        #         # 10 in flight light shows: {'porter robinson  a breath superbloom edit', 'Short Song', 'Jon Hopkins  Breathe This Air feat Purity Ring Official Video', 'Coldplay  Paradise Official Audio', 'Juvenile  Back That Thang Up ft Mannie Fresh Lil Wayne', 'Kenny Price - The Shortest Song In The World', 'Littles kids playing recorders', 's_Drake  Massive Official Audio', 'Daft Punk  Something About Us Official Video', 'YuGiOh  Season 1 Theme Song'}
                
        #         # wait(futures)
        #         # print('donzo')
        #         # exit()
        #         try:
        #             for future in as_completed(futures):
        #                 print_bold(f'{len(in_flight)} in flight light shows: {in_flight}', flush=True)
        #                 progress_bar.update(1)

        #                 # os.system(f'kill -9 {os.getpid()}')
        #         except:
        #             print_red(traceback.format_exc(), flush=True)
        #             os.system(f'kill -9 {os.getpid()}')

        #         # executor.map(partial(gen_show_worker, mode=args.autogen_mode), all_song_paths)

        #     progress_bar.close()
        #     print_green(f'FINISHED AUTOGENERATING ALL ({len(all_song_paths)}) SHOWS IN DIRECTORY {autogen_song_directory} in {time.time() - time_start} seconds')
        #     exit()


