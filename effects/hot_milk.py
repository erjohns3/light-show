from effects.compiler import beat

effects = {
    "Snails House  Hot Milk show": {
        "bpm": 150,
        "song_path": "songs/Snails House  Hot Milk.ogg",
        "delay_lights": 0.02055,
        "skip_song": 0.0,
        "beats": [
            beat(1, name='porter flubs phrase', length=64, hue_shift=.7, intensity=(1, 0)),
        ]
    }
}