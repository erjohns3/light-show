effects = {
    "everything bottom glow": {
        "length": 1,
        "beats": [
            [1, "Pink bottom", 1],
        ],
    },
    "everything melody glow": {
        "length": 8,
        "beats": [
            [1, "Pink bottom", 3.5],
            [4.5, "Green bottom", 2],
            [6.5, "Cyan bottom", 2.5],
        ],
    },
    "everything melody 2 glow": {
        "length": 10,
        "beats": [
            [1, "Pink bottom", 3.5],
            [4.5, "Green bottom", 2],
            [6.5, "Cyan bottom", 2.5],
            [9, "Yellow bottom", 2],
        ],
    },
    "everything kick": {
        "length": 1,
        "beats": [
            [1, "White bottom", 0.15, 0.2, 0.05],
        ],
    },
    "everything kick 2": {
        "length": 1,
        "beats": [
            [1, "White top", 0.15, 0.2, 0.05],
            [1, "White bottom", 0.15, 0.2, 0.05],
        ],
    },
    "everything kick line 2": {
        "length": 4,
        "beats": [
            [1, "everything kick 2", 1],
            [2, "everything kick 2", 1],
            [3, "everything kick 2", 1],
            [3.5, "everything kick 2", 1],
            [4, "everything kick 2", 1],
        ],
    },
    "everything kick line": {
        "length": 4,
        "beats": [
            [1, "everything kick", 1],
            [2, "everything kick", 1],
            [3, "everything kick", 1],
            [3.5, "everything kick", 1],
            [4, "everything kick", 1],
        ],
    },
    "everything kick top RGB": {
        "length": 8,
        "beats": [
            [1, "White top", 8],

            #  1: full green

            [1, "Sidechain top r", 1, 1, 1],
            [1, "Sidechain top g", 1, .2, .2],
            [1, "Sidechain top b", 1, 1, 1],

            [2, "Sidechain top r", 1, .6, .6],
            [2, "Sidechain top g", 1, .5, .5],
            [2, "Sidechain top b", 1, 1, 1],
            
            [3, "Sidechain top r", 1, .4, .4],
            [3, "Sidechain top g", 1, .85, .85],
            [3, "Sidechain top b", 1, 1, 1],
                        
            # 3.66: full red

            [4, "Sidechain top r", 1, .4, .4],
            [4, "Sidechain top g", 1, 1, 1],
            [4, "Sidechain top b", 1, .8, .8],
                        
            [5, "Sidechain top r", 1, .7, .7],
            [5, "Sidechain top g", 1, 1, 1],
            [5, "Sidechain top b", 1, .4, .4],
                        
            [6, "Sidechain top r", 1, .9, .9],
            [6, "Sidechain top g", 1, 1, 1],
            [6, "Sidechain top b", 1, .1, .1],

            # 6.33: full blue

            [7, "Sidechain top r", 1, 1, 1],
            [7, "Sidechain top g", 1, .85, .85],
            [7, "Sidechain top b", 1, .3, .3],
                        
            [8, "Sidechain top r", 1, 1, 1],
            [8, "Sidechain top g", 1, .4, .4],
            [8, "Sidechain top b", 1, .7, .7],
        ],
    },
    "everything show": {
        "beats": [
            [1, "rainbow good slow top", 120, 0, .35],
            [1, "everything bottom glow", 120, .25, .25],
            [1, "everything kick", 31],
            [33, "everything kick", 24],
            [65, "everything kick line", 56],
            [121, "everything melody glow", 72, .25, .5],
            [121, "UV", 8],
            # [129, "rainbow good slow top", 60, .35, .35],
            [129, "everything kick top RGB", 64, .4, .4],
            [129, "everything kick line 2", 64],
            [189, "UV", 4],
            [193, "rainbow good slow top", 64, .35, 0],
            [193, "everything kick 2", 16],
            [193, "everything melody 2 glow", 48, .5, .5],
            [209, "everything kick 2", 160, 1, 0],
        ],
        "delay_lights": .02,
        "skip_song": 0,
        "bpm": 120,
        "song_path": "songs/Radiohead - Everything in Its Right Place (Sam Goku Edit).ogg",
        "profiles": ["Shows"],
    },
}