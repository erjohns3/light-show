effects = {
    "Ghosts melody": {
        "length": 32,
        "beats": [
            [1, "Strobe", 0.6, .5, .5],
            [2, "Strobe", 0.6, .5, .5],
            [3, "Strobe", 0.6, .5, .5],
            [4, "Strobe", 0.6, .5, .5],
            [9, "Strobe", 0.6, .5, .5],
            [10, "Strobe", 0.6, .5, .5],
            [15.5, "Strobe", 0.3, .5, .5],
            [16.5, "Strobe", 0.3, .5, .5],
            [17, "Strobe", 0.6, .5, .5],
            [18, "Strobe", 0.6, .5, .5],
            [19, "Strobe", 0.6, .5, .5],
            [25, "Strobe", 0.6, .5, .5],
            [31, "Strobe", 0.6, .5, .5],
            [32, "Strobe", 0.6, .5, .5],
        ],
    },
    "Ghosts bassline": {
        "length": 2,
        "beats": [
            [1, "Purple bottom", 1, 0.42, .2],
            [2, "Green bottom", 1, 0.42, .2],
        ],
    },
    "Ghosts UV": {
        "length": 1,
        "beats": [
            [1, "UV", .6, 0.6, .2],
        ],
    },
    "Ghosts rainbow":{
        "length": 2,
        "beats": [
            [1, [40, 0, 0, 0, 0, 0, 0], 0.7],
            [1.7, [40, 0, 0, 0, 0, 0, 0], 0.3, 1, 0],
            [1.7, [0, 30, 20, 0, 0, 0, 0], 0.3, 0, 1],
            [2, [0, 30, 20, 0, 0, 0, 0], 0.7],
            [2.7, [0, 30, 20, 0, 0, 0, 0], 0.3, 1, 0], 
            [2.7, [40, 0, 0, 0, 0, 0, 0], 0.3, 0, 1],
        ],
    },
    "Ghosts riser":{
        "length": 4,
        "beats": [
            [1, "Pink bottom", 2, .15, .3],
            [3, "Pink bottom", 2, .3, .15],
        ],
    },
    "Ghosts blue fade":{
        "length": 4,
        "beats": [
            [1, "Blue top", 2, .08, .15],
            [3, "Blue top", 2, .15, .08],
        ],
    },
    "Ghosts UV fade":{
        "length": 16,
        "beats": [
            [1, "UV", 8, .1, .4],
            [9, "UV", 8, .4, .1],
        ],
    },
    # "Ghosts ay strobe":{
    #     "length": 0.4,
    #     "beats": [
    #         "1": [[[20, 50, 0, 0, 0, 0, 0], 0.07],
    #         "1.2": [[[0, 0, 0, 0, 0, 0, 100], 0.07],
    #     }
    # },
    "Rainbow bad": {
        "length": 2,
        "beats": [
            [1, [40, 0, 0, 0, 0, 0, 0], 0.7],
            [1.7, [40, 0, 0, 0, 0, 0, 0], 0.3, 1, 0], 
            [1.7, [0, 30, 20, 0, 0, 0, 0], 0.3, 0, 1],
            [2, [0, 30, 20, 0, 0, 0, 0], 0.7],
            [2.7, [0, 30, 20, 0, 0, 0, 0], 0.3, 1, 0], 
            [2.7, [40, 0, 0, 0, 0, 0, 0], 0.3, 0, 1],
        ],
    },
    "Ghosts breakdown":{
        "length": 32,
        "beats": [
            [1, "UV Strobe", 4, .4, .4],
            [5, "Rainbow bad", 4], 
            [5, "Ghosts bassline", 4],
            [9, "UV Strobe", 6, .4, .4],
            [15, "Ghosts bassline", 2],
            [17, "UV Strobe", 4, .4, .4],
            [21, "Rainbow bad", 4], 
            [21, "Ghosts bassline", 4],
            [25, "UV Strobe", 6, .4, .4],
            [31.85, "Firebrick bottom", .5],
        ],
    },

    "ghosts show": {
        "beats": [
            [17, "Ghosts melody", 96], 
            [17, "Ghosts bassline", 96], 
            [17, "Ghosts blue fade", 96], 
            [17, "Ghosts UV fade", 96],
            [81, "Ghosts UV", 32],
            [113, "Rainbow bad", 32],
            [145, "Ghosts breakdown", 32],
            [177, "Ghosts melody", 64], 
            [177, "Ghosts bassline", 64], 
            [177, "UV", 32, .4, .4],
            [209, "Ghosts UV", 32],
            [241, "wandering", 32],
            [273, "Ghosts breakdown", 32],
            [305, "Ghosts breakdown", 32], 
            [305, "Ghosts bassline", 64, 0.3, 0.3],
            [337, "UV", 32],
            [369, "Ghosts bassline", 32],
        ],
        "delay_lights": 0,
        "skip_song": 4.2,
        "bpm": 128,
        "song_path": "songs/deadmau5 feat. Rob Swire - Ghosts N Stuff.ogg",
        "profiles": ["Shows"],
    },
}