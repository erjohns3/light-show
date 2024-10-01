from effects.compiler import *

grid_f_mask_return = grid_f(
    1, 
    function=grid_winamp_mask,
    preset='202-wave.milk',
    priority=10000,
    length=1,
)
effects = {
    "A - Nothing": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=-1000, red_laser=-1000, laser_motor=-1000, disco_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - Mask winamp": {
        "length": 1,
        "trigger": "toggle",
        "profiles": ['Andrew'],
        "beats": [
            grid_f_mask_return,
        ],
    },
    "A - random winamp": {
        "length": 1,
        "trigger": "hold", # TODO MAKE A NEW TYPE TAP THAT ONLY RUNS 1 FRAME
        "profiles": ['Andrew'],
        "beats": [
            grid_f(
                1, 
                function=randomize_preset_on_object,
                bobby_jones=grid_f_mask_return[1],
                length=1,
            ),
        ],
    },
    "A - laser only rotate green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=100, red_laser=-1000, laser_motor=100, disco_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - laser only green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=100, red_laser=-1000, laser_motor=-1000, disco_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - laser only rotate red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=-1000, red_laser=100, laser_motor=100, disco_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - laser red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, red_laser=100, length=1),
        ],
    },
    "A - laser motor": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, laser_motor=100, length=1),
        ],
    },
    "A - only Flash Top": {
        "length": 0.2,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, top_rgb=[100, 100, 100], length=0.07),
            b(1, bottom_rgb=[-10000, -10000, -10000], length=2),
            b(1.07, top_rgb=[-10000, -10000, -10000], bottom_rgb=[-10000, -10000, -10000], length=2),
        ],
    },
    "A - only Flash Bottom": {
        "length": 0.2,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            b(1, bottom_rgb=[100, 100, 100], length=0.07),
            b(1, top_rgb=[-10000, -10000, -10000], length=2),
            b(1.07, top_rgb=[-10000, -10000, -10000], bottom_rgb=[-10000, -10000, -10000], length=2),
        ],
    },
    "A - only UV": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=100, length=1),
        ],
    },
    "A - only Red top": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[2000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - only Green top": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, 2000, -1000], bottom_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - only Blue top": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, 2000], bottom_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "A - only Red bottom": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[2000, -1000, -1000], length=1),
        ],
    },
    "A - only Green bottom": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, 2000, -1000], length=1),
        ],
    },
    "A - only Blue bottom": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, 2000], length=1),
        ],
    },
    "A - only disco red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=-1000, red_laser=-1000, laser_motor=-1000, disco_rgb=[100, 0, 0], length=1),
        ],
    },
    "A - only disco green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=-1000, red_laser=-1000, laser_motor=-1000, disco_rgb=[0, 100, 0], length=1),
        ],
    },
    "A - only disco blue": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=-1000, red_laser=-1000, laser_motor=-1000, disco_rgb=[0, 0, 100], length=1),
        ],
    },
    "A - disco red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, disco_rgb=[100, 0, 0], length=1),
        ],
    },
    "A - disco green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, disco_rgb=[0, 100, 0], length=1),
        ],
    },
    "A - disco blue": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            b(1, disco_rgb=[0, 0, 100], length=1),
        ],
    },
}
