import sys
import pathlib
import re
import shutil

this_file_directory = pathlib.Path(__file__).parent
sys.path.append(str(this_file_directory.parent))
from helpers import *
import youtube_download_helpers


effects_directory = this_file_directory.parent.joinpath('effects')




for _, filepath in get_all_paths(effects_directory):

    # if str(filepath).endswith('basics_old.py'):
    #     continue

    lines_to_write = {}
    if filepath.is_dir():
        continue
    
    with open (filepath, 'r') as file:
        data = file.read()
        
        # Regex pattern to capture the full match and the innermost arrays within "beats"
        pattern = r'(\[\s*(?:\d+(?:\.\d+)?|\.\d+)\s*,?\s*\[\s*(.*?)\s*\]\s*,?\s*(?:\d+(?:\.\d+)?|\.\d+)\s*\])'



        # this just checks if there's any remaining inner bracket combos
        good_check = r'\[.*?\[(.*?)\].*?\]'
        print_blue(filepath)
        if filepath.stem == 'compiler':
            continue
        for line in data.splitlines():
            brackets = []
            for char in line:
                if char == '#':
                    break
                if char == '[':
                    if brackets:
                        print(line)
                    brackets.append('[')
                elif char == ']':
                    if brackets and brackets[-1] == '[':
                        brackets.pop()
        continue


        # migration script below

        # Find all matches in the data along with their positions
        matches = re.finditer(pattern, data)

        for match in matches:
            full_match = match.group(1)
            innermost_array = match.group(2).strip()
            start_index = match.start(1)
            end_index = match.end(1)

            # Extract the line containing the match
            line_start = data.rfind('\n', 0, start_index) + 1
            line_end = data.find('\n', end_index)
            if line_end == -1:
                line_end = len(data)        
            line = data[line_start:line_end]

            line_index = data[:start_index].count('\n')

            # Highlight only the innermost array within the full match
            highlighted_innermost_array = blue(innermost_array)
            highlighted_full_match = full_match.replace(innermost_array, highlighted_innermost_array)
            highlighted_line = line.replace(full_match, highlighted_full_match)
            
            
            

            start_index_of_highlight = highlighted_line.find(highlighted_innermost_array)
            end_index_of_highlight = start_index_of_highlight + len(innermost_array)

            without = line[:start_index_of_highlight] + line[end_index_of_highlight:]

            # new = line[:start_index_of_highlight] + new_bit + line[end_index_of_highlight:]

            # print(without)
            def clean(s):
                return s.replace('[', '').replace(']', '').replace(' ', '').strip()
            beat_start, empty_arr, beat_length, *_ = without.split(',')
            beat_start = clean(beat_start)
            empty_arr = clean(empty_arr)
            beat_length = clean(beat_length)

            # print(f'{beat_start=}, {empty_arr=}, {beat_length=}')

            current_params = innermost_array.split(',')
            for i, param in enumerate(current_params):
                current_params[i] = clean(param)
            # print(current_params)

            if len(current_params) == 4:
                current_params[3:3] = current_params[0:3]
            if len(current_params) == 7:
                current_params[3:3] = current_params[0:3]
            # if len(current_params) == 10:
            #     current_params += [0,0,0]
            # if len(current_params) == 13:
            #     current_params += [0,0,0]


            # def b(start_beat=None, length=None, top_rgb=None, front_rgb=None, back_rgb=None, bottom_rgb=None, uv=None, green_laser=None, red_laser=None, laser_motor=None, disco_rgb=None):

            new_b = f'b({beat_start}'

            
            if current_params[0:3] == current_params[3:6] and any(list(map(int, current_params[0:3]))):
                new_b += f', top_rgb=[{", ".join(current_params[0:3])}]'

            elif any(list(map(int, current_params[0:3]))):
                new_b += f', back_rgb=[{", ".join(current_params[0:3])}]'
            
            elif any(list(map(int, current_params[3:6]))):
                new_b += f', front_rgb=[{", ".join(current_params[3:6])}]'

            if any(list(map(int, current_params[6:9]))):
                new_b += f', bottom_rgb=[{", ".join(current_params[6:9])}]'

            if len(current_params) > 9 and current_params[9] != '0':
                new_b += f', uv={current_params[9]}'

            if len(current_params) > 10 and current_params[10] != '0':
                new_b += f', green_laser={current_params[10]}'

            if len(current_params) > 11 and current_params[11] != '0':
                new_b += f', red_laser={current_params[11]}'

            if len(current_params) > 12 and current_params[12] != '0':
                new_b += f', laser_motor={current_params[12]}'


            if any(list(map(int, current_params[13:16]))):
                new_b += f', disco_rgb=[{", ".join(current_params[13:16])}]'

            new_b += f', length={beat_length})'

            leading_spaces = len(line) - len(line.lstrip())
            lines_to_write[line_index] = f'{leading_spaces * " "}{new_b},'
            print(highlighted_line)
            print(lines_to_write[line_index])


    if lines_to_write:
        new_name = filepath.stem + '_migrated.py'
        new_temp_filepath = get_temp_dir().joinpath(new_name)

        with open(new_temp_filepath, 'w') as write_file:
            with open(filepath, 'r') as read_file:
                data = read_file.read().splitlines()
                for index, line in enumerate(data):
                    if index in lines_to_write:
                        write_file.write(lines_to_write[index] + '\n')
                    else:
                        write_file.write(line + '\n')
        print(f'Compare old {blue(str(filepath))} and new {cyan(str(new_temp_filepath))} and type "y" to overwrite, anything else to continue')
        if input() == 'y':
            old_filepath = get_temp_dir().joinpath(filepath.stem + '_old.py')
            shutil.move(filepath, old_filepath)
            shutil.move(new_temp_filepath, filepath)
            print(f'Overwritten {filepath.stem} and moved the old file to {old_filepath}')
    else:
        print_yellow(f'No need to write to file: {filepath.stem}')