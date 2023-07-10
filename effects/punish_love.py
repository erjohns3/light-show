from effects.compiler import b, grid_f

effects = {
    "punish laser": {
        'length': 4,
        "beats": [
            b(.5, name='laser motor', length=1),
            b(1, name='green laser', length=1),
        ]
    },
    "Delta Heavy  Punish My Love Official Video": {
        "bpm": 125,
        "song_path": "songs/Delta Heavy  Punish My Love Official Video.ogg",
        "delay_lights": 0.04,
        "skip_song": 0.0,
        "beats": [
            b(1, name='RBBB 1 bar', length=160),
            b(48, name='punish laser', length=32),
            b(161, name='dom chorus', length=64),
        ]
    }
}