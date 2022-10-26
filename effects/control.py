from effects.compiler import b

effects = {

    "control UV clap": {
        "length": 2,
        "beats": [
            [2, "UV", 1, 1, 0],
        ],
    },

    "control cycle bottom": {
        "length": 32,
        "beats": [
            [1, "Red bottom", 8],
            [1, "Blue bottom", 8, .2, 1],
            [9, "Red bottom", 8, 1, .1],
            [9, "Blue bottom", 8],
            [17, "Red bottom", 8, .1, 1],
            [17, "Blue bottom", 8],
            [25, "Red bottom", 8,],
            [25, "Blue bottom", 8, 1, .2],
        ],
    },

    "control pulse rb": {
        "length": 1,
        "beats": [
            [1, "Red bottom", 1, 1, 0],
            [1, "Blue bottom", 1, 1, 0],
        ],
    },

    "control cycle bottom pulse": {
        "length": 32,
        "beats": [
            [1, "control cycle bottom", 32, .3],
            [1, "control pulse rb", 8, .1, .4],
            [9, "control pulse rb", 8, .4, .1],
            [17, "control pulse rb", 8, .1, .4],
            [25, "control pulse rb", 8, .4, .1],
        ],
    },

    "control UV clap full": {
        "length": 16,
        "beats": [
            [1, "control UV clap", 16],
            [15.5, "UV", .4, 1, 0],
        ],
    },

    "control top step fade": {
        "length": 4,
        "beats": [
            [1, "Red top", 1, 1, .5],
            [2, "Red top", 1, .3],
            [3, "Red top", 1, .15],
            [4, "Red top", 1, .05],
        ],
    },

    "control subtract 20": {
        "length": .1,
        "beats": [
            [1, [-20, -20, -20, 0, 0, 0, 0], 1, 1, .5],
        ],
    },

    "control top flicker fade": {
        "length": 4,
        "beats": [
            [1, "Red top", 4, 1, 0],
            [2,  "control subtract 20"],
            [2.5,  "control subtract 20"],
            [2.7,  "control subtract 20"],
            [3,  "control subtract 20"],
        ],
    },

    "control bottom rainbow": {
        "length": 4,
        "beats": [
            [1, "Red top", 4, 1, 0],
            [2,  "control subtract 20"],
            [2.5,  "control subtract 20"],
            [2.7,  "control subtract 20"],
            [3,  "control subtract 20"],
        ],
    },

    "control intro no bass": {
        "length": 64,
        "beats": [
            [1, "control top step fade", 4, 1, 1, 0, 267/360],
            [9, "control top step fade", 4, 1, 1, 0, 267/360],
            [17, "control top step fade", 4, 1, 1, 0, 285/360],
            [25, "control top step fade", 4, 1, 1, 0, 285/360],
            [30, "control top flicker fade", 3, 1, 1, 0, 300/360],
            [33, "control top step fade", 4, 1, 1, 0, 267/360],
            [41, "control top step fade", 4, 1, 1, 0, 267/360],
            [49, "control top step fade", 4, 1, 1, 0, 285/360],
            [57, "control top step fade", 4, 1, 1, 0, 285/360],
        ],
    },

    "control show": {
        "bpm": 120,
        "song_path": "songs/Emmit Fenn  Control.ogg",
        "delay_lights": 0.055,
        "skip_song": 0.0,
        "beats": [
            [1, "control intro no bass", 128],
            [65, "control UV clap full", 64],
            [65, "control cycle bottom pulse", 64, 1, 1, 0, -.05],
        ]
    }
}