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
    "Musician Lyrical Oo": {
        "length": 2,
        "beats": [
            [1, [0, 100, 0, 0, 0, 0, 0], 0.5, 1, 0.2],
            [2, [0, 80, 100, 0, 0, 0, 0], 0.5, 1, 0.2],
        ],
    },
    "musician sidechain": {
        "length": 1,
        "beats": [
            [1, "Sidechain top rbg", .3, .5, 0],
        ],
    },
    "musician loop": {
        "length": 16,
        "beats": [
            [1, "Rainbow bad", 12],
            [13, "Musician Lyrical Oo", 4],
        ],
    },
    "musician show": {
        "beats": [
            [1, "musician loop", 400],
        ],
        "delay_lights": 0.0,
        "skip_song": 6.15,
        "bpm": 120,
        "song_path": "songs/Porter Robinson - Musician (Official Music Video).ogg",
        "profiles": ["Shows"],
    },
}