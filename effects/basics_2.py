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
    }
}