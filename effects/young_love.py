from effects.compiler import *

effects = {
    "love kicks": {
        "length": 1,
        "beats": [
            [1, "Green bottom", 0.25, 1, 0],
            [1, "UV", 0.25, 1, 0],
        ],
    },
    "Superhumanoids - Too Young For Love": {
        "beats": [
            [1, "rainbow good slow top", 32],
            [33, "love kicks", 128],
        ],
        "not_done": True,
        "delay_lights": .08,
        "skip_song": 0,
        "bpm": 138,
        "song_path": "songs/Superhumanoids - Too Young For Love.ogg",
        "profiles": ["Shows"],
    },
}
