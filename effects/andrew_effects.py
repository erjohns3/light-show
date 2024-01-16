from effects.compiler import *

mask_grid_info = grid_f(
    1, 
    function=grid_winamp_mask,
    preset='202.milk',
    priority=10000,
    length=1,
)
effects = {
    "A - Nothing": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000], 1],
        ],
    },
    "A - Mask winamp": {
        "length": 1,
        "trigger": "toggle",
        "profiles": ['Andrew'],
        "beats": [
            mask_grid_info,
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
                bobby_jones=mask_grid_info,
                length=1,
            ),
        ],
    },
    "A - laser only rotate green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 100, -1000, 100, -1000, -1000, -1000], 1],
        ],
    },
    "A - laser only green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 100, -1000, -1000, -1000, -1000, -1000], 1],
        ],
    },
    "A - laser only rotate red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 100, 100, -1000, -1000, -1000], 1],
        ],
    },
    "A - laser red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0], 1],
        ],
    },
    "A - laser motor": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100], 1],
        ],
    },
    "A - only Flash Top": {
        "length": 0.2,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [100, 100, 100, 0, 0, 0, 0], 0.07],
            [1, [0, 0, 0, -10000, -10000, -10000, 0], 2],
            [1.07, [-10000, -10000, -10000, -10000, -10000, -10000, 0], 2],
        ],
    },
    "A - only Flash Bottom": {
        "length": 0.2,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [0, 0, 0, 100, 100, 100, 0], 0.07],
            [1, [-10000, -10000, -10000, 0, 0, 0, 0], 2],
            [1.07, [-10000, -10000, -10000, -10000, -10000, -10000, 0], 2],
        ],
    },
    "A - only UV": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, 100], 1],
        ],
    },
    "A - only Red top": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [2000, -1000, -1000, -1000, -1000, -1000, 0], 1],
        ],
    },
    "A - only Green top": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, 2000, -1000, -1000, -1000, -1000, 0], 1],
        ],
    },
    "A - only Blue top": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, 2000, -1000, -1000, -1000, 0], 1],
        ],
    },
    "A - only Red bottom": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, 2000, -1000, -1000, 0], 1],
        ],
    },
    "A - only Green bottom": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, 2000, -1000, 0], 1],
        ],
    },
    "A - only Blue bottom": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, 2000, 0], 1],
        ],
    },
    "A - only disco red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 100, 0, 0], 1],
        ],
    },
    "A - only disco green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 0, 100, 0], 1],
        ],
    },
    "A - only disco blue": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, 0, 0, 100], 1],
        ],
    },
    "A - disco red": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0], 1],
        ],
    },
    "A - disco green": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0], 1],
        ],
    },
    "A - disco blue": {
        "length": 1,
        "trigger": "hold",
        "profiles": ["Andrew"],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100], 1],
        ],
    },
}