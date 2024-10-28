from effects.compiler import *


effects = {
    "blue shift - circle pulse 1": {
        "profiles": ['Emma'],
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy(radius=10, color=GColor.blue, offset_y=-8),
                name='Ok 1',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (.01, .01),
                end_scale = (1, 1),
                length=1,
            ),
            grid_f(
                2,
                function=our_transform,
                object='Ok 1',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (1, 1),
                end_scale = (.01, .01),
                length=1,
            ),
        ],
    },
    "blue shift - circle pulse 2": {
        "profiles": ['Emma'],
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy(radius=10, color=GColor.green, offset_y=8),
                name='Ok 2',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (.01, .01),
                end_scale = (1, 1),
                length=1,
            ),
            grid_f(
                2,
                function=our_transform,
                object='Ok 2',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (1, 1),
                end_scale = (.01, .01),
                length=1,
            ),
        ],
    },
    "Lemaitre - Blue Shift": {
        "bpm": 118,
        "song_path": "songs/Lemaitre - Blue Shift.ogg",
        "delay_lights": 0.4043245762711864,
        "skip_song": 0.0,
        "beats": [
            # grid_f(1, function=trail_ball_fade, length=64, speed=1, clear=False),
            # b(1, name="blue shift - circle pulse 1", length=32, offset=1),
            *make_rain(length=108),
            # b(1, name="twinkle white", length=1),
            # b(3, name="twinkle blue", length=1),
            # b(5, name="twinkle white", length=1),
            # b(7, name="twinkle blue", length=1),
            # b(name="twinkle blue", length=32),
        ],
    }
}