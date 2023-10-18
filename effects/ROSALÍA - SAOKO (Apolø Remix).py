from effects.compiler import *

def get_circle_pulse_beats(start_beat=1, start_color=GColor.white, end_color=GColor.red):
    arr = []
    total = 16
    for i in range(total):
        before_color = interpolate_vectors_float(start_color, end_color, i / total)
        after_color = interpolate_vectors_float(start_color, end_color, (i+1) / total)
        arr.append(grid_f(
            start_beat + (i * .15),
            function=our_transform,
            object=get_centered_circle_numpy_nofill(radius=i+1),
            start_color=before_color,
            end_color=after_color,
            length=1,
        ))
    return arr

def squares_up(info):
    if getattr(info, 'filled_to', None) is None:
        info.filled_to = 0
        info.last_color = [random.randint(0, 30), random.randint(0, 30), random.randint(0, 150)]
    
    coords_length = grid_helpers.total_coords
    percent_done = info.curr_sub_beat / info.length
    fill_to = int(percent_done * coords_length)
    for index, (x, y) in enumerate(grid_helpers.coords_y_first()):
        if info.filled_to <= index <= fill_to:
            grid_helpers.grid[x][y] = white
            grid_helpers.grid[x][y] = info.last_color

            chosen_index = random.randint(0, 2)
            if random.randint(0, 1) == 0:
                info.last_color[chosen_index] = max(info.last_color[chosen_index] - 15, 0)
            else:
                info.last_color[chosen_index] = min(info.last_color[chosen_index] + 15, 254)
    info.filled_to = fill_to

def get_wub_bounce(beats, colors, speed=1, end_point=112, start_colors_at_beat=None):
    components = []
    counter = 0
    y_index = 0
    spawn_points = [0, 31]
    vectors = [(0, speed), (0, -speed)]

    for index, beat in enumerate(beats):
        next_beat = beats[index + 1] if index + 1 < len(beats) else end_point
        color = GColor.white
        if type(colors[0]) in [int, float]:
            color = colors
        elif start_colors_at_beat is None or beat > start_colors_at_beat:
            color = colors[counter % len(colors)]
            counter += 1
        y_index = 1 - y_index
        components.append(grid_f(beat, function=spawn_row, clear=True, y=spawn_points[y_index], color=color, length=0.05))    

        components.append(grid_f(beat, function=move_until_y_occupy, y=spawn_points[1-y_index], vector=vectors[y_index], length=next_beat - beat))
    return components

verse_colors = [GColor.red, GColor.orange, GColor.yellow] * 14



effects = {
    "saoko verse" : {
        'length': 42,
        'beats': [
            grid_f(1, function=lambda x: x, clear=False, length=42),
            *get_wub_bounce(list(range(1, 42)), verse_colors, end_point=42, start_colors_at_beat=1),
        ],
    },
    "saoko bass" : {
        "length": 4,
        "beats": [
            b(1, name='Red bottom', length=1.5, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),
            b(2.75, name='Orange bottom', length=0.75, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),
            b(3.75, name='Yellow bottom', length=0.75, hue_shift=.85, sat_shift=-.25, intensity=(1,0)),        
        ],
    },
    "sidechain motor halfs": {
        'length': 1,
        "beats": [
            b(1.15, name='Sidechain motor', length=.85),
        ]
    },
     "chorus laser": {
        'length': 16,
        'autogen': 'laser long',
        "beats": [
            b(1, name='laser motor', length=16),
            b(1, name='dom sidechain motor halfs', length=16),
            b(1, name='red laser', length=16),
        ]
    },
    "circle pulse": {
        "length": 4,
        "beats": [
            *get_circle_pulse_beats(start_beat=1, start_color=GColor.red, end_color=GColor.yellow),
        ],
    },
    "ROSALÍA - SAOKO (Apolø Remix)": {
        "bpm": 118,
        "song_path": "songs/ROSALÍA - SAOKO (Apolø Remix).ogg",
        "delay_lights": 0.0,
        "skip_song": 0.0,
        "beats": [
            # start
            grid_f(5, filename='thunder.gif', rotate_90=False, length=44),
            b(5, name='saoko bass', length=42),
            # 17 chica que dices
            b(17, name='Orange top', length=4),
            #saoko papi
            b(21, name='Yellow top', length=4),
            b(29, name='Red top', length=4),
            # chica que dices
            b(32, name='Orange top', length=4),
            b(37, name='Yellow top', length=4),
            # Verse
            b(49, name='saoko verse', length=32),
            # transformo
            b(81, name='chorus laser', length=32),
            b(81, name='circle pulse', length=32),
            # quiet moment
            b(113, name='saoko bass', length=42),
            grid_f(113, filename='fire.gif', rotate_90=False, length=44),
            b(120, name='Strobe bottom', length=9),
            # go go go go 
            b(129, name='UV pulse', length=15),
            # quiet moment
            b(145, name='Orange top', length=15),
            # que algo
            b(161, name='Yellow top', length=4),
            # bump
            b(176, name='saoko verse', length=64),
            # 
            b(193, name='Orange top', length=8),
            # bump
            b(209, name='Yellow top', length=8),
            #
            b(225, name='Red top', length=8),
            #end
            b(241, name='Orange top', length=8),
        ]
    }
}