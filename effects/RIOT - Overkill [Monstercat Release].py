from effects.compiler import *
import grid_helpers

def bar_down(grid_info):
    if getattr(grid_info, 'y', None) is None or grid_info.curr_sub_beat == 0:
        grid_info.y = grid_helpers.GRID_HEIGHT - 1

    if grid_info.y < 0:
        return

    for x in grid_info.x_range:
        grid_helpers.grid[x][grid_info.y] = grid_info.color

    speed = int(1 / getattr(grid_info, 'speed', 1))
    if grid_info.curr_sub_beat % speed == 0:
        grid_info.y -= 1


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


def get_growing_circle_freeze_after(name, start_beat, start_scale, end_scale, freeze_after, length, color):
    return [
        grid_f(
            start_beat,
            function=our_transform,
            object=name,
            start_color=color,
            start_scale=start_scale,
            end_scale=end_scale,
            length=freeze_after,
        ),
        grid_f(
            start_beat + freeze_after,
            function=our_transform,
            object=name,
            length=length - freeze_after,
        ),
    ]


def get_wub(start_beat):
    random_name = random_letters(7)
    return [
        grid_f(
            start_beat,
            function=our_transform,
            object=get_centered_circle_numpy(radius=10),
            name=random_name,
            start_scale = (.01, .01),
            length=.04,
        ),
        *get_growing_circle_freeze_after(random_name, start_beat, (.01, .01), (.5, .5), 3, 4, color=GColor.blue),
        *get_growing_circle_freeze_after(random_name, start_beat + 4, (.01, .01), (1, 1), 3, 4, color=GColor.green),
        *get_growing_circle_freeze_after(random_name, start_beat + 8, (.25, .25), (1.5, 1.5), 3, 4, color=GColor.red),
    ]


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

    "over - Red quarters": {'length': 0.5, 'beats': [b(1, name='Red top', length=.25)]},
    "over - Blue quarters": {'length': 0.5, 'beats': [b(1, name='Blue top', length=.25)]},
    "over - Green quarters": {'length': 0.5, 'beats': [b(1, name='Green top', length=.25)]},

    "over - Red bottom eighths": {
        'length': 0.25,
        'beats': [
            b(1, name='Red bottom', length=.125),
            grid_f(1, function=sidechain_grid, length=.125, intensity=0),
        ],
    },

    "over - drum eighths": {
        'length': 8,
        'beats': [
            b(1, name='over - Red bottom eighths', length=.75),
            b(2.5, name='over - Red bottom eighths', length=.75),
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


            # b(208, name='over - Red quarters', length=32),

            # b(240, name='over - Blue quarters', length=32),


            # b(240, name='over - Blue quarters', length=28),

            # # women: "kill them all"
            grid_f(268, text='kill', font_size=8, length=1),
            grid_f(269.5, text='them', font_size=8, length=1),
            grid_f(271, text='all', font_size=8, length=1),
            # b(268, name='Green top', length=4),
            
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


            grid_f(325, text='bussin', font_size=5, color=GColor.green, length=1.5),



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