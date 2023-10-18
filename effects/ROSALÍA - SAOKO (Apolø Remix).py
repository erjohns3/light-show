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
            b(3.75, name='Yellow bottom', length=0.75, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),        
        ],
    },
     "S chorus laser": {
        'length': 16,
        'autogen': 'laser long',
        "beats": [
            b(1, name='laser motor', length=16),
            b(1, name='dom sidechain motor halfs', length=16),
            b(1, name='red laser', length=16),
        ]
    },
    "S circle pulse": {
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
            b(5, name='saoko bass', length=42),
            # 17 chica que dices
            grid_f(17, filename='thunder.gif', rotate_90=True, length=28),
            # 21 saoko papi
            # 32 chica que dices
            # transition
            b(45, name='S circle pulse', length=4),
            # 49 Verse
            b(49, name='saoko verse', length=32),
            # 81 transformo
            b(81, name='S chorus laser', length=28),
            b(81, name='saoko bass', length=32),
            # transition
            b(109, name='S circle pulse', length=4),
            b(109, name='Strobe bottom', length=4),
            # 113 quiet moment
            b(113, name='saoko bass', length=48),
            grid_f(113, filename='fire.gif', rotate_90=True, length=48),
            # quiet moment
            # que algo
            b(160, name='S circle pulse', length=4),
            b(164, name="Strobe bottom", length=12, sat_shift=.2, intensity=(0, 1)),
            b(172, name='S circle pulse', length=4),
            # bump
            b(176, name='saoko verse', length=64),
            b(176, name='S chorus laser', length=64),
        ]
    }
}