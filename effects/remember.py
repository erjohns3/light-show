from effects.compiler import *

effects = {
    "Thing": {
        "length": 1,
        "beats": [
            [1, 'Rosy brown bottom', .2, 1, 0],
        ],
    },

    "grid fill rbbb 4 bar": {
        'length': 4,
        'beats': [
            grid_f(1, function=fill_color, color=GColor.red, length=.25),
            grid_f(2, function=fill_color, color=GColor.blue, length=.25),
            grid_f(3, function=fill_color, color=GColor.blue, length=.25),
            grid_f(4, function=fill_color, color=GColor.blue, length=.25),
        ],
    },

    # 1 - 64: 
    "deadmau5 & Kaskade - I Remember (HQ)": {
        "not_done": False,
        "beats": [
            b(1, name='grid fill rbbb 4 bar', length=1640),
            b(1, name='RBBB 1 bar bottom', length=1640),


            # [1, "Red disco", 2000],
            # [1, "Blue disco", 2000],
            # [1, "Green disco", 2000],
            # [65, "wandering", 64],
            # [129, "Ghosts UV", 64],
            # [193, "Ghosts bassline", 64],
            # [257, "RBBB 1 bar", 64],
            # [394, "Blue top", 64],
        ],
        "delay_lights": .175,
        "skip_song": 0,
        "bpm": 128,
        "song_path": "songs/deadmau5 & Kaskade - I Remember (HQ).ogg",
        "profiles": ["Shows"],
    },
}