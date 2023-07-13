from effects.compiler import *

effects = {

    "specto veldt": {
        "length": 4,
        "beats": [
            grid_f(1, function=grid_visualizer, color=(255, 0, 0), song_path='songs/deadmau5 feat. Chris James - The Veldt.ogg', length=1),
            grid_f(2, function=grid_visualizer, color=(0, 255, 0), song_path='songs/deadmau5 feat. Chris James - The Veldt.ogg', flip=True, length=1),
            grid_f(3, function=grid_visualizer, color=(0, 0, 255), song_path='songs/deadmau5 feat. Chris James - The Veldt.ogg', length=1),
            grid_f(4, function=grid_visualizer, color=(255, 0, 255), song_path='songs/deadmau5 feat. Chris James - The Veldt.ogg', flip=True, length=1),
        ],
    },

    "deadmau5 feat. Chrisasdasd James - The Veldt": {
        "bpm": 128,
        "song_path": "songs/deadmau5 feat. Chris James - The Veldt.ogg",
        "delay_lights": 0.048100000000000004,
        "skip_song": 0.0,
        "beats": [
            # b(1, name='specto veldt', length=1000),
            grid_f(1, function=grid_visualizer, color=(255, 0, 0), song_path='songs/deadmau5 feat. Chris James - The Veldt.ogg', length=1000),
        ]
    }
}