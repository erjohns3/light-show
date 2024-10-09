from effects.compiler import *

effects = {
    "Moe Shop - Notice (w\u29f8 TORIENA)": {
        "bpm": 125,
        "song_path": "songs/Moe Shop - Notice (w\u29f8 TORIENA).ogg",
        "delay_lights": 0.45539999999999997,
        "skip_song": 0.0,
        "beats": [
            *make_twinkle(start_beat=7.75, length=1, color=GColor.pink, twinkle_length=.15, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
            *make_twinkle(start_beat=7.75, length=1, color=GColor.green, twinkle_length=.15, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
            b(33, 'RBBB 1 bar', length=128)
        ]
    }
}