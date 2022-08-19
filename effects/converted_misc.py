# delete from misc.py when you convert any
effects = {
    "Cheesecake time": {
        "length": 8,
        "beats": [
            [7, "Yellow top", .5, 1, 0],
            [7.5, "Yellow top", .5, 1, 0],
        ],
    },
    "RB Strobe Top Bottom": {
        "length": 0.4,
        "beats": [
            [1, [50, 100, 0, 0, 0, 0, 0], 0.07],
            [1.2, [0, 100, 50, 0, 0, 0, 0], 0.07],
        ],
    },
    "cheesecake show": {
        "beats": [
            [1, "Cheesecake time", 64], 
            [1, "Rainbow bad", 64],
            [65, "Ghosts bassline", 14],
            [79, "RB Strobe Top Bottom", 2],
            [81, "Cheesecake time", 32], 
            [81, "Rainbow bad", 32],
        ],
        "delay_lights": 6.3,
        "skip_song": 0.0,
        "bpm": 97,
        "song_path": "songs/Cheesecake.ogg",
        "profiles": ["Shows"]
    },
}