from effects.compiler import *
effects = {
    "RBBB 1 bar": {
        "length": 4,
        "beats": [
            [1, [100, 0, 0, 0, 0, 0, 0], 0.25],
            [2, [0, 0, 100, 0, 0, 0, 0], 0.25],
            [3, [0, 0, 100, 0, 0, 0, 0], 0.25],
            [4, [0, 0, 100, 0, 0, 0, 0], 0.25],
        ],
    },

    "RBBB 1 bar bottom": {
        "length": 4,
        "beats": [
            [1, [0, 0, 0, 100, 0, 0, 0], 0.25],
            [2, [0, 0, 0, 0, 0, 100, 0], 0.25],
            [3, [0, 0, 0, 0, 0, 100, 0], 0.25],
            [4, [0, 0, 0, 0, 0, 100, 0], 0.25],
        ],
    },

    'Red bottom green laser flash': {
        'length': 1,
        'profiles': [f'All lasers'],
        'beats': [
            b(1, name='Red bottom', length=.5),    
            b(1.5, name='green laser', length=.5),    
        ],
    },

    # flashes
    "White flash": {
        "length": 1,
        "beats": [
            [1, [100, 100, 100, 100, 100, 100, 0], 0.3, 0.1, 0],
        ],
    },

    "Pulse": {
        "length": 1,
        "beats": [
            [1, [100, 100, 100, 0, 0, 0, 0], 0.9, 1, 0],
        ],
    },
    "UV pulse": {
        "length": 1,
        "autogen": True,
        "trigger": "add",
        "loop": False,
        "profiles": ["Andrew"],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 100], 1, 1, 0, 0],
        ]
    },
    "UV pulse slow": {
        "length": 2,
        "autogen": True,
        "trigger": "add",
        "loop": False,
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 100], 1, 1, 0, 0],
        ]
    },
}




for amt in range(1, 101):
    if amt < 7 or amt % 5 == 0:
        effects[f'Laser motor {amt}'] = {
            'length': 1,
            'profiles': [f'All lasers'],
            'beats': [
                [1, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, amt], 1],
                
                
                # b(1, name='laser motor', laser_motor=amt, length=1),
            ],
        }