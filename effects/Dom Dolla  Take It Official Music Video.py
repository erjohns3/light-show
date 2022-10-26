from effects.compiler import b

effects = {
    "dom sidechain motor halfs": {
        'length': 1,
        "beats": [
            b(1, name='Sidechain motor', length=.5),
        ]
    },
    "dom chorus": {
        'length': 16,
        "beats": [
            b(1, name='RBBB 1 bar', length=16),
            b(1, name='laser motor', length=16),
            b(1, name='dom sidechain motor halfs', length=16),
            b(1, name='green laser', length=8.5),
            # b(13, name='dom sidechain motor halfs', length=2),
            b(13, name='green laser', length=1),
            # b(16, name='green laser', length=12),        
        ]
    },
    "Dom Dolla  Take It Official Music Video show": {
        "bpm": 123,
        "song_path": "songs/Dom Dolla  Take It Official Music Video.ogg",
        "delay_lights": 0.15150000000000002,
        "skip_song": 0.0,
        "beats": [
            b(16, name='green laser motor', length=32),
            b(16, name='porter flubs phrase', length=16, hue_shift=.2),
            b(33, name='green laser', length=32),
            b(33, name='porter flubs phrase', length=16, hue_shift=.6),
            b(49, name='porter flubs phrase', length=16, hue_shift=.8),
            b(80, name='dom chorus', length=64),
            # b(80, name='laser motor', length=32),
            # b(80, name='dom sidechain motor halfs', length=10),
            # b(80, name='green laser', length=12),
            # b(92, name='dom sidechain motor halfs', length=2),
            # b(96, name='green laser', length=12),
        ]
    }
}