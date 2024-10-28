from effects.compiler import *

effects = {
    "Repeat": {
        "length": 16,
        "beats": [
            *make_twinkle(start_beat=7.75, length=1.25, color=GColor.pink, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
            *make_twinkle(start_beat=7.75, length=1.25, color=GColor.green, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),

            b(7.75, 'Sidechain top', length=1.25),
            b(7.75, 'Sidechain bottom', length=1.25),

            b(1, 'RBBB 1 bar', length=16),
        ]
    },

    "Moe Shop - Notice (w\u29f8 TORIENA)": {
        "bpm": 125,
        "song_path": "songs/Moe Shop - Notice (w\u29f8 TORIENA).ogg",
        "delay_lights": 0.45539999999999997,
        "skip_song": 0.0,
        "beats": [
            *make_twinkle(start_beat=7.75, length=1.25, color=GColor.pink, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
            *make_twinkle(start_beat=7.75, length=1.25, color=GColor.green, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),


            
            b(33, 'Repeat', length=128)
        ]
    }
}