effects = {
    # pulses and strobes
    "Strobe": {
        "length": 0.2,
        "beats": [
            [1, [100, 100, 100, 0, 0, 0, 0], 0.07],
        ],
    },
    "UV Strobe": {
        "length": 0.2,
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 100], 0.07],
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

    # Sidechain stuff
    "Nothing": {
        "length": 1,
        "beats": [
            [1, [-1000, -1000, -1000, -1000, -1000, -1000, -1000], 1],
        ],
    },
    "Sidechain top r": {
        "length": 1,
        "beats": [
            [1, [-1000, 0, 0, 0, 0, 0, 0], 1],
        ],
    },
    "Sidechain top g": {
        "length": 1,
        "beats": [
            [1, [0, -1000, 0, 0, 0, 0, 0], 1],
        ],
    },
    "Sidechain top b": {
        "length": 1,
        "beats": [
            [1, [0, 0, -1000, 0, 0, 0, 0], 1],
        ],
    },
    "Sidechain bottom b": {
        "length": 1,
        "beats": [
            [1, [0, 0, 0, 0, 0, -1000, 0], 1],
        ],
    },
    "Sidechain top bg": {
        "length": 1,
        "beats": [
            [1, [0, -1000, -1000, 0, 0, 0, 0], 1],
        ],
    },
    "Sidechain top rbg": {
        "length": 1,
        "beats": [
            [1, [-1000, -1000, -1000, 0, 0, 0, 0], 1],
        ],
    },
    "Sidechain bottom g": {
        "length": 1,
        "beats": [
            [1, [0, 0, 0, 0, -1000, 0, 0], 1],
        ],
    },

    # flashes
    "White flash": {
        "length": 1,
        "beats": [
            [1, [100, 100, 100, 100, 100, 100, 0], 0.3, 0.1, 0],
        ],
    },


    # timings
    "RBBB 1 bar": {
        "length": 4,
        "autogen": True,
        "beats": [
            [1, [100, 0, 0, 0, 0, 0, 0], 0.25],
            [2, [0, 0, 100, 0, 0, 0, 0], 0.25],
            [3, [0, 0, 100, 0, 0, 0, 0], 0.25],
            [4, [0, 0, 100, 0, 0, 0, 0], 0.25],
        ],
    },

    ##################################  colors
    "UV": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 0, 0, 0, 100], 1],
        ],
    },
    "White top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [100, 100, 100, 0, 0, 0, 0], 1],
        ],
    },
    "White bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 100, 100, 100, 0], 1],
        ],
    },
    "Red top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [100, 0, 0, 0, 0, 0, 0], 1],
        ],
    },
    "Red bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 100, 0, 0, 0], 1],
        ],
    },
    "Green top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 100, 0, 0, 0, 0, 0], 1],
        ],
    },
    "Green bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 0, 100, 0, 0], 1],
        ],
    },
    "Blue top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 100, 0, 0, 0, 0], 1],
        ],
    },
    "Blue bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 0, 0, 100, 0], 1],
        ],
    },
    "Orange top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [100, 40, 10, 0, 0, 0, 0], 1],
        ],
    },
    "Orange bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 100, 40, 10, 0], 1],
        ],
    },
    "Firebrick top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [178, 34, 34, 0, 0, 0, 0], 1],
        ],
    },
    "Firebrick bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 178, 34, 34, 0], 1],
        ],
    },
    "Cyan top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [10, 50, 100, 0, 0, 0, 0], 1],
        ],
    },
    "Cyan bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 10, 50, 100, 0], 1],
        ],
    },
    "Yellow top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [80, 100, 10, 0, 0, 0, 0], 1],
        ],
    },
    "Yellow bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 80, 100, 10, 0], 1],
        ],
    },
    "Pink top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [100, 10, 30, 0, 0, 0, 0], 1],
        ],
    },
    "Pink bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 100, 10, 30, 0], 1],
        ],
    },
    "Indigo top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [25, 0, 70, 0, 0, 0, 0], 1],
        ],
    },
    "Indigo bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 40, 0, 90, 0], 1],
        ],
    },
    "Purple bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 100, 0, 100, 0], 1],
        ],
    },
    "Rosy brown top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [70, 30, 30, 0, 0, 0, 0], 1],
        ],
    },
    "Rosy brown bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            [1, [0, 0, 0, 70, 30, 30, 0], 1],
        ],
    },
}