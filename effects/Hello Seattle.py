from effects.compiler import *

effects = {
    "Hello Seattle": {
        "bpm": 120,
        "song_path": "songs/Hello Seattle.ogg",
        "delay_lights": 0.23099999999999998,
        "skip_song": 0.0,
        "beats": [
            grid_f(1, filename='ricardo.gif', length=100),
            grid_f(101, function=winamp_grid, preset='202.milk', length=400),
            # grid_f(1, function=winamp_grid, preset='202.milk', length=400),
        ]
    }
}