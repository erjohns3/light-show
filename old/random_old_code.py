

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