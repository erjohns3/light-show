from effects.compiler import *
import grid_helpers

def bar_down(grid_info):
    if getattr(grid_info, 'y', None) is None or grid_info.curr_sub_beat == 0:
        grid_info.y = 0

    if grid_info.y > grid_helpers.GRID_HEIGHT - 1:
        return

    for x in grid_info.x_range:
        grid_helpers.grid[x][grid_info.y] = grid_info.color

    speed = int(1 / getattr(grid_info, 'speed', 1))
    if grid_info.curr_sub_beat % speed == 0:
        grid_info.y += 1


def spawn_half_fallers(start_beat, total_beats, start_color, end_color, intensity=1):
    building = []
    half_x = grid_helpers.GRID_WIDTH // 2
    for beat in range(start_beat, start_beat + total_beats + 1):
        percent_done = (beat - start_beat) / total_beats
        curr_color = interpolate_vectors_float(start_color, end_color, percent_done)
        curr_color = scale_vector(curr_color, intensity)
        building += [
            grid_f(beat, function=bar_down, length=8, x_range=range(half_x), color=curr_color),
            grid_f(beat + .5, function=bar_down, length=8, x_range=range(half_x, grid_helpers.GRID_WIDTH), color=curr_color),
        ]
    return building


def get_growing_circle_freeze_after(start_beat, start_scale, end_scale, freeze_after, length, color):
    return [
        grid_f(
            start_beat,
            function=our_transform,
            object=get_centered_circle_numpy(radius=10),
            start_color=color,
            start_scale=start_scale,
            end_scale=end_scale,
            length=freeze_after,
        ),
        grid_f(
            start_beat + freeze_after,
            function=our_transform,
            object=get_centered_circle_numpy(radius=10),
            start_color=color,
            start_scale=end_scale,
            length=length - freeze_after,
        ),
    ]


def get_wub(start_beat):
    return [
        *get_growing_circle_freeze_after(start_beat, (.01, .01), (.5, .5), 3, 4, color=GColor.blue),
        *get_growing_circle_freeze_after(start_beat + 4, (.01, .01), (1, 1), 3, 4, color=GColor.green),
        *get_growing_circle_freeze_after(start_beat + 8, (.25, .25), (1.5, 1.5), 3, 8, color=GColor.red),
    ]


def spawn_line(start_beat, pos, color, length):
    def ok(info):
        x, y = pos
        for i in range(length):
            final_y = (y + i) % grid_helpers.GRID_HEIGHT
            grid_helpers.grid[x][final_y] = color
    return grid_f(start_beat, function=ok, length=.04)


def get_marchers(start_beat, length):
    return [
        grid_f(start_beat, function=lambda x: x, clear=False, length=length),
        spawn_line(start_beat, (-7, 12), color=GColor.blue, length=5),
        spawn_line(start_beat, (-3, 5), color=GColor.red, length=5),
        spawn_line(start_beat, (1, 8), color=GColor.blue, length=5),
        spawn_line(start_beat, (5, -3), color=GColor.red, length=5),
        spawn_line(start_beat, (9, -10), color=GColor.blue, length=5),
    ]

def make_marchers_and_move(start_beat, vector=(0, 1), move_length=.25, length=1):
    arr = get_marchers(start_beat, length)
    for o in range(length):
        curr_beat = start_beat + o
        arr.append(grid_f(curr_beat, function=move_grid, vector=vector, wrap=True, length=move_length))
    return arr

def just_move_marchers(start_beat, skip_beat, vector=(0, 1), move_length=.25, length=1):
    arr = []
    for o in range(0, length, skip_beat):
        curr_beat = start_beat + o
        arr.append(grid_f(curr_beat, function=move_grid, vector=vector, wrap=True, length=move_length))
        arr.append(grid_f(curr_beat + 1.5, function=move_grid, vector=vector, wrap=True, length=move_length))
    return arr


def just_move_marchers_on_beat(start_beat, vector=(0, 1), move_length=.25, length=1):
    arr = []
    for o in range(0, length):
        curr_beat = start_beat + o
        arr.append(grid_f(curr_beat, function=move_grid, vector=vector, wrap=True, length=move_length))
    return arr


effects = {
    "over - Overkill chant bottom": {
        'length': 8,
        'beats': [
            b(3, name='Blue bottom', length=.4, intensity=.3),
            b(4, name='Blue bottom', length=.4, intensity=.3),
            b(5, name='Orange bottom', length=1, intensity=.6),
            b(6, name='Orange bottom', length=2, intensity=(.6, 0)),
        ]
    },

    "over - Red halfs": {'length': 1, 'beats': [b(1, name='Red bottom', length=.5)]},
    "over - Blue halfs": {'length': 1, 'beats': [b(1, name='Blue bottom', length=.5)]},
    "over - Green halfs": {'length': 1, 'beats': [b(1, name='Green bottom', length=.5)]},
    "over - sidechain grid halfs": {'length': 1, 'beats': [b(1, name='sidechain grid', length=.5)]},


    "over - Red quarters": {'length': 0.5, 'beats': [b(1, name='Red bottom', length=.25)]},
    "over - Blue quarters": {'length': 0.5, 'beats': [b(1, name='Blue bottom', length=.25)]},
    "over - Green quarters": {'length': 0.5, 'beats': [b(1, name='Green bottom', length=.25)]},
    "over - sidechain grid quarters": {'length': .5, 'beats': [b(1, name='sidechain grid', length=.25)]},

    "over - Red bottom eighths": {
        'length': 0.25,
        'beats': [
            b(1, name='Red bottom', length=.125),
            grid_f(1, function=sidechain_grid, length=.125, intensity=0),
        ],
    },

    "sidechain grid": {
        'length': 1,
        'beats': [
            grid_f(1, function=sidechain_grid, length=1, intensity=0),
        ],
    },


    "over - drum eighths": {
        'length': 8,
        'beats': [
            b(1, name='over - Red bottom eighths', length=.75),
            b(2.5, name='over - Red bottom eighths', length=.75),
        ]
    },

    "over - strobe flash": {
        'length': 2,
        'beats': [
            b(1, name='laser motor', length=2),
            b(1, name='Red disco', length=.25),
            # b(1.5, name='green laser', length=.25),
            b(1.5, name='Green disco', length=.25),
            b(2, name='Blue disco', length=.25),
            # b(2.5, name='green laser', length=.25),
            b(2.5, name='Green disco', length=.25),
        ]
    },

    

    "RIOT - Overkill [Monstercat Release]": {
        "bpm": 174,
        "song_path": "songs/RIOT - Overkill [Monstercat Release].ogg",
        "delay_lights": -0.3435,
        "skip_song": 0.0,
        "beats": [
            # b(16, name='over - Red quarters', length=64),
            *spawn_half_fallers(16, 64, start_color=GColor.blue, end_color=GColor.purple, intensity=.3),
            *spawn_half_fallers(80, 64, start_color=GColor.orange, end_color=GColor.pink, intensity=1),
            
            b(80, name='over - Overkill chant bottom', length=128),

            *spawn_half_fallers(144, 64, start_color=GColor.orange, end_color=GColor.pink, intensity=1),
            # *spawn_half_fallers(144, 64, start_color=GColor.green, end_color=GColor.red, intensity=1),

            b(176, name='over - drum eighths', length=32),

            b(192, name='Red disco', length=16),
            
            
            # *make_twinkle(start_beat=208, length=64, color=GColor.blue, twinkle_length=1, num_twinkles=40, twinkle_lower_wait=1, twinkle_upper_wait=4),


            # b(208, name='over - Red quarters', length=32),

            grid_f(240, function=lambda x: x, clear=False, length=60),
            *make_marchers_and_move(240, vector=(0, 2), move_length=.25, length=28),

            grid_f(268, text='kill', font_size=8, length=.04),

            grid_f(269.5, text='kill', subtract=True, font_size=8, length=.04),
            grid_f(269.5, text='them', font_size=8, length=.04),
            
            grid_f(271, text='them', subtract=True, font_size=8, length=.04),
            grid_f(271, text='all', font_size=8, length=.04),
            
            grid_f(272, text='all', subtract=True, font_size=8, length=.04),

            *just_move_marchers(272, skip_beat=4, vector=(0, -2), move_length=.4, length=16),
            *just_move_marchers(288, skip_beat=4, vector=(0, -3), move_length=.4, length=8),
            *just_move_marchers_on_beat(296, vector=(0, -6), move_length=.6, length=4),

            # # breakdown before drop
            # b(272, name='over - Blue quarters', length=28),
            
            # # man: "kill them all"
            grid_f(300, text='kill', font_size=8, color=GColor.red, length=1),
            grid_f(301.5, text='them', font_size=8, color=GColor.red, length=1),
            grid_f(303, text='all', font_size=8, color=GColor.red, length=1.5),
            # b(300, name='Green top', length=4),

            # # drop
            # b(304, name='over - Blue quarters', length=32),

            *get_wub(307),

            b(318, name='over - sidechain grid quarters', length=1.5),
            b(319.5, name='over - sidechain grid halfs', length=3),
            
            grid_f(325, text='bussin', font_size=5, color=GColor.green, length=1.5),

            b(327, name='over - strobe flash', length=12),
            grid_f(339, text='bop', font_size=5, color=GColor.green, length=.75),
            
            b(339, name='laser motor', length=3),
            # what
            b(340, name='green laser', length=2),
            
            b(349, name='over - strobe flash', length=5),

            b(354, name='Red bottom', length=1, intensity=(1, 0)),
            b(355, name='Blue bottom', length=1, intensity=(1, 0)),

            grid_f(357, text='bop', font_size=5, color=GColor.green, length=.25),
            grid_f(357.5, text='bop', font_size=5, color=GColor.green, length=.25),
            grid_f(358, text='bop', font_size=5, color=GColor.green, length=.5),


            # b(238.79, name='Red top', length=1),
            # b(270.75, name='Blue top', length=1),
            # b(294.75, name='Green top', length=1),
            # b(298.88, name='Red top', length=1),
            # b(300.38, name='Blue top', length=1),
            # b(301.75, name='Green top', length=1),
            # b(322.79, name='Red top', length=1),
            # b(325.75, name='Blue top', length=1),
        ]
    }
}