from effects.compiler import *

effects = {
    "8films effect": {
        "length": 24,
        "beats": [
            b(1, name='Pink top', length=4),
            b(5, name='Blue top', length=4),
            b(9, name='Seafoam top', length=4),
            b(13, name='Purple top', length=4),
            b(17, name='Yellow top', length=4),
            b(21, name='Orange top', length=4),
        ],
    },
    "8films": {
        "bpm": 130,
        "song_path": "songs/8films.ogg",
        "delay_lights": 0.3666384615384616,
        "skip_song": 0.0,
        "beats": [
            b(5, name='8films effect', length=1000),
        ]
    }
}