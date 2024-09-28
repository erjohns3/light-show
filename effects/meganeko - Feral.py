from effects.compiler import *
from effects.overkill import * 

effects = {
    "test": {
        "length": 4,
        "beats": [
            b(1, name='Red top', length=.3),
            b(2, name='Blue top', length=.3),
            b(3, name='Blue top', length=.3),
            b(4, name='Blue top', length=.3),
        ],
    },


    "meganeko - Feral": {
        "bpm": 160,
        "song_path": "songs/meganeko - Feral.ogg",
        "delay_lights": .27,
        "skip_song": 0.0,
        "beats": [
            b(97, name='test', length=64),
            b(97+64, name='test', length=64, hue_shift=.4),
            # spawn_half_fallers(64, 1, start_color=GColor.orange, end_color=GColor.pink, intensity=1),
            # spawn_half_fallers(97, 1, start_color=GColor.orange, end_color=GColor.pink, intensity=1),

            # rest is at 240
        ]
    }
}