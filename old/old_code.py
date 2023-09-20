if args.print_beat and not args.local:
    print(f'Beat: {(beat_index // SUB_BEATS) + 1}, Seconds: {time_diff:.3f}')



def detailed_output_on_enter():
    while True:
        input()
        all_effect_names = []
        curr_beat = (beat_index / SUB_BEATS) + 1
        for effect in curr_effects:
            if has_song(effect[0]):
                all_effect_names += get_sub_effect_names(effect[0], curr_beat)
            else:
                all_effect_names.append(effect[0])
        print(f'beat: {curr_beat:2f}, current_effects playing: {all_effect_names}')

if args.enter:
    x = threading.Thread(target=detailed_output_on_enter).start()