from effects.compiler import b, grid_f

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


    "Attack repeater": {
        "length": 8,
        "beats": [
            [1, [20, 0, 20, 0, 0, 0, 0], 0.55, 0.5, 0],
            [2, [0, 0, 0, 0, 30, 5, 0], 0.55, 0.5, 0],
            [3, [20, 0, 20, 0, 0, 0, 0], 0.55, 0.5, 0],
            [4, [0, 0, 0, 0, 30, 5, 0], 0.55, 0.5, 0],
            [5, [20, 0, 20, 0, 0, 0, 0], 0.3, 0.5, 0],
            [5.5, [0, 0, 0, 0, 30, 0, 5], 0.3, 1, 0],
            [6, [0, 0, 0, 0, 0, 0, 70], 0.3, 1, 0],
            [6.5, [0, 0, 0, 0, 0, 0, 70], 0.3, 1, 0],
            [7, [0, 0, 0, 0, 0, 0, 70], 1.2, 1, 0]
        ],
    },
    # "attack show": {
    #     "beats": [
    #         [1, "Green fade", 1],
    #         [3, "Yellow fade", 1],
    #         [5, "Green fade", 1],
    #         [7, "Yellow fade", 1],
    #         [9, "Green fade", 1],
    #         [11, "Yellow fade", 1],
    #         [13, "Green fade", 1],
    #         [15, "Triplets top", 2],
    #         [17, "White flash", 1], 
    #         [17, "Attack repeater", 8],
    #         [25, "Attack repeater", 24],
    #     ],
    #     "delay_lights": 0.0,
    #     "skip_song": 0.35,
    #     "bpm": 144,
    #     "song_path": "songs/attack_season_4_op.ogg",
    #     "profiles": ["Shows"],
    # },
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
    "Luigi Hats": {
        "length": 0.5,
        "beats": [
            [1, [0, 0, 0, 0, 0, 4, 0], 0.5, 1, 0.4],
        ],
    },
    "Luigi Yellow Top": {
        "length": 1,
        "beats": [
            [1, [20, 20, 0, 0, 0, 0, 0], 1],
        ],
    },
    "Luigi Cyan Bottom": {
        "length": 1,
        "beats": [
            [1, [0, 0, 0, 20, 0, 20, 0], 1],
        ],
    },
    "Luigi Whoo": {
        "length": 1,
        "beats": [
            [1, [0, 5, 0, 10, 0, 10, 5], 0.5, 0, 1],
            [1.5, [0, 5, 0, 10, 0, 10, 5], 0.35, 1, 0],
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