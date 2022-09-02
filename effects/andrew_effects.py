effects = {
    "A - Nothing": {
        "length": 1,
        "trigger": "hold",
        "profiles": ['Andrew'],
        "beats": [
            [1, [-10000, -10000, -10000, -10000, -10000, -10000, -10000], 1],
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
}