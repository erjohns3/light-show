from effects.compiler import b

effects = {
    "no sleep show": {
        "bpm": 125,
        "song_path": "songs\\io  No Sleep Official Lyric Video.ogg",
        "delay_lights": 0.25849999999999995,
        "skip_song": 0.0,
        "beats": [
            [4, 'Red top', 8, 1, 0],
            [4, 'Red disco', 160, 0, 1],
            [164, 'Red bottom pulse', 96],
            [164.5, 'Red disco pulse', 96],
            [260, 'Red top', 8, 1, 0],
            [260, 'Red disco', 140, 0, 1],
            [400, 'Red bottom pulse', 96],
            [400.5, 'Red disco pulse', 96],
        ]
    },

    "Red bottom pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            [1, [
                    0, 0, 0, 
                    0, 0, 0, 
                    100, 0, 0, 
                    0,
                    0, 0, 0,
                    0, 0, 0
                ], 1, 1, 0],
        ]
    },

    "Red disco": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            [1, [
                    0, 0, 0, 
                    0, 0, 0, 
                    0, 0, 0, 
                    0,
                    0, 0, 0,
                    100, 0, 0
                ], 1],
        ]
    },

    "Red disco pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            [1, 'Red disco', 1, 1, 0],
        ]
    },
}