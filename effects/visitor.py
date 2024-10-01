from effects.compiler import *

print('file in question')
effects = {
    "Mad Zach - The Visitor": {
        "beats": [
            [1, "White", 176, 0.5, 0],
            [1, "White Strobe", 176, 0, 1],
            [177, "RGB Flash", 912],
        ],
        "delay_lights": 0,
        "skip_song": 0,
        "bpm": 170,
        "song_path": "songs/Mad Zach - The Visitor.ogg",
        "profiles": ["Shows"]
    },
    "White": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[100, 100, 100], bottom_rgb=[100, 100, 100], length=1),
        ],
    },
    "White Strobe": {
        "length": 1.5,
        "beats": [
            b(1, back_rgb=[100, 100, 100], length=0.04),
            b(1.17, bottom_rgb=[100, 100, 100], length=0.04),
            b(1.33, front_rgb=[100, 100, 100], length=0.04),
            b(1.5, bottom_rgb=[100, 100, 100], length=0.04),
            b(1.67, front_rgb=[100, 100, 100], length=0.04),
            b(1.83, back_rgb=[100, 100, 100], length=0.04),
            b(2, front_rgb=[100, 100, 100], length=0.04),
            b(2.17, back_rgb=[100, 100, 100], length=0.04),
            b(2.33, bottom_rgb=[100, 100, 100], length=0.04),
        ],
    },
    "RGB Flash": {
        "length": 1.5,
        "autogen": "flash",
        "beats": [
            b(1, back_rgb=[100, 0, 0], length=0.04),
            b(1.17, bottom_rgb=[0, 100, 0], length=0.04),
            b(1.33, front_rgb=[0, 0, 100], length=0.04),
            b(1.5, bottom_rgb=[100, 0, 0], length=0.04),
            b(1.67, front_rgb=[0, 100, 0], length=0.04),
            b(1.83, back_rgb=[0, 0, 100], length=0.04),
            b(2, front_rgb=[100, 0, 0], length=0.04),
            b(2.17, back_rgb=[0, 100, 0], length=0.04),
            b(2.33, bottom_rgb=[0, 0, 100], length=0.04),
        ],
    }
}
