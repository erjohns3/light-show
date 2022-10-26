from effects.compiler import b

effects = {
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

    "control intro no bass": {
        "length": 64,
        "beats": [
            [1, "control top step fade", 16, 1, 1, 0, 267/360],
            [17, "control top step fade", 16, 1, 1, 0, 267/360],
            [30, "control top step fade", 2, 1, 1, 0, 300/360],
        ],
    },

    "control show": {
        "bpm": 120,
        "song_path": "songs/Emmit Fenn  Control.ogg",
        "delay_lights": 0.055,
        "skip_song": 0.0,
        "beats": [
            [1, "control intro no bass", 100],
        ]
    }
}