from effects.compiler import *

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
            b(1, top_rgb=[50, 100, 0], length=0.07),
            b(1.2, top_rgb=[0, 100, 50], length=0.07),
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
    
    "Musical idk color 1": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[100, 0, 0], length=1),
        ],
    },
    "Musical idk color 2": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[0, 80, 100], length=1),
        ],
    },
    "Musician Lyrical Oo": {
        "length": 2,
        "beats": [
            [1, "Musical idk color 1", .5, 1, 0.2],
            [2, "Musical idk color 2", .5, 1, 0.2],
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


    "Luigi Bass hits": {
        "length": 4,
        "beats": [
            [1, "Green bottom", .4, 1, 0],
            [1.75, "Green bottom", .4, 1, 0],
            [2.5, "Green bottom", .4, 1, 0],
            [3.35, "Green bottom", .4, 1, 0],
            [4.25, "Green bottom", .4, 1, 0],
        ],
    },
    "Luigi Bassline": {
        "length": 16,
        "beats": [
            [2, "Luigi Bass hits", 12],
        ],
    },
    "Luigi color for hats": {
        "length": 1,
        "beats": [
            b(1, uv=100, length=1),
        ],
    },
    "Luigi Hats": {
        "length": 0.5,
        "beats": [
            [1, "Luigi color for hats", 0.5, 1, 0.4],
        ],
    },
    "Luigi Yellow Top": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[20, 20, 0], length=1),
        ],
    },
    "Luigi Cyan Bottom": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[20, 0, 20], length=1),
        ],
    },
    "Luigi color for Whoo": {
        "length": 1,
        "beats": [
            b(1, uv=100, length=1),
        ],
    },
    "Luigi Whoo": {
        "length": 1,
        "beats": [
            [1, "Luigi color for Whoo", 0.5, 0, 1],
            [1.5, "Luigi color for Whoo", 0.35, 1, 0],
        ],
    },
    "luigi show": {
        "beats": [
            [1, "Luigi Bassline", 32],
            [13, "UV", 4], 
            [13, "Luigi Hats", 4],
            [29, "UV", 4], 
            [29, "Luigi Hats", 4],
            [33, "Luigi Cyan Bottom", 2],
            [35, "Luigi Yellow Top", 2],
            [37, "Luigi Cyan Bottom", 2],
            [39, "Luigi Yellow Top", 2],
            [41, "Luigi Cyan Bottom", 2],
            [43, "Luigi Yellow Top", 2],
            [45, "Luigi Cyan Bottom", 2],
            [47, "Luigi Yellow Top", 2],
            [51, "Luigi Cyan Bottom", 0.5],
            [51.5, "Luigi Yellow Top", 0.5],
            [52, "Luigi Cyan Bottom", 0.5],
            [52.5, "Luigi Yellow Top", 0.5],
            [53, "Luigi Cyan Bottom", 3],
            [57.5, "Luigi Whoo", 1],
            [59, "Luigi Bassline", 32],
            [71, "UV", 4], 
            [71, "Luigi Hats", 4],
            [83, "UV", 4], 
            [83, "Luigi Hats", 4],
        ],
        "delay_lights": 0.0,
        "skip_song": 1.74,
        "bpm": 90,
        "song_path": "songs/luigi.ogg",
        "profiles": ["Shows"],
    },

    "first love show": {
        "beats": [
            [1, "UV pulse", 32],
        ],
        "delay_lights": 5.75,
        "skip_song": 0.0,
        "bpm": 80,
        "song_path": "songs/神はサイコロを振らない × アユニ・D(BiSH⧸PEDRO) × n-buna from ヨルシカ「初恋」Studio Session Movie(Full Ver.).ogg",
        "profiles": ["Shows"],
        "not_done": True,
    },
}
