from effects.compiler import *

effects = {
    "cnam top colors": {
        "length": 2,
        "beats": [
            [1, "Green top", 1, 0.2, 0.2],
            [1.5, "Cyan top", 1, 0.2, 0.2],
            [2, "Blue top", 1, 0.2, 0.2],
            [2.5, "Red top", 1, 0.2, 0.2],            
        ],
    },
    "cnam bass hits": {
        "length": 8,
        "beats": [
            [1, "Firebrick bottom", .8, 1, 0.1], 
            [1, "Sidechain top rbg", .8, 1, 0.1],
        ],
    },
    "cnam faster bass hits": {
        "length": 2,
        "beats": [
            [1, "Firebrick bottom", .8, 1, 0.1], 
            [1, "Sidechain top rbg", .8, 1, 0.1],
        ],
    },
    "cnam drop": {
        "beats": [
            [1, "cnam top colors", 96], 
            [1, "cnam bass hits", 32],
            [1, "cnam faster bass hits", 64],
        ],
    },
    "cnam show": {
        "beats": [
            [1, "wandering", 64, 0, 1],
            [65, "wandering", 128],
            [193, "cnam drop", 96],
        ],
        "delay_lights": .22,
        "not_done": True,
        "skip_song": 0,
        "bpm": 120,
        "song_path": "songs/Porter Robinson x Illenium x Said the Sky Mix by C-Nam.ogg",
        "profiles": ["Shows"],
    },
}