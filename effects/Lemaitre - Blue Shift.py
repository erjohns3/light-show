from effects.compiler import *


effects = {
    "Rain": {"profiles": ['Fun Grid'], "loop": True, "beats": make_rain()},
    "Rain fast": {"profiles": ['Fun Grid'], "loop": True, "beats": make_rain(speed=.6)},
    "Rain fast lots": {"profiles": ['Fun Grid'], "loop": True, "beats": make_rain(speed=.6, num_rains=40)},
    
    "Move Left": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_x, length=1, by=1)]},
    "Move Right": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_x, length=1, by=-1)]},
    "Move Up": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_y, length=1, by=1)]},
    "Move Down": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_y, length=1, by=-1)]},


    "Move Left Wrap": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_x_wrap, length=1, by=1)]},
    "Move Right Wrap": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_x_wrap, length=1, by=-1)]},
    "Move Up Wrap": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_y_wrap, length=1, by=1)]},
    "Move Down Wrap": {"profiles": ['Fun Grid'], "trigger": "hold", "loop": True, "beats": [grid_f(1, function=move_y_wrap, length=1, by=-1)]},


    "twinkle white": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.white)},
    "twinkle blue": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.blue)},
    "twinkle green": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.green)},
    "twinkle red": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.red)},
    "twinkle purple": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.purple)},
    "twinkle yellow": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.yellow)},
    "twinkle cyan": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.cyan)},
    "twinkle orange": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.orange)},
    "twinkle pink": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.pink)},
    "twinkle light_blue": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.light_blue)},
    "twinkle light_green": {"profiles": ['Fun Grid'], "loop": True, "beats": make_twinkle(color=GColor.light_green)},

    
    "trail ball fast": {
        "profiles": ['Emma'],
        "trigger": "toggle",
        "loop": True,
        'beats': [
            grid_f(1, function=trail_ball_fade, length=64, speed=1),
        ],
    },
    "trail ball mid": {
        "profiles": ['Emma'],
        "trigger": "toggle",
        "loop": True,
        'beats': [
            grid_f(1, function=trail_ball_fade, length=64, speed=.5),
        ],
    },
    "trail ball slow": {
        "profiles": ['Emma'],
        "trigger": "toggle",
        "loop": True,
        'beats': [
            grid_f(1, function=trail_ball_fade, length=64, speed=.25),
        ],
    },
    "fire ball fade": {
        "profiles": ['Emma'],
        "trigger": "hold",
        'beats': [
            grid_f(1, function=fire_ball_fade, length=8, speed=1),
        ],
    },
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