from effects.compiler import b, grid_f


effects = {
    "everything bottom glow": {
        "length": 1,
        "beats": [
            [1, "Pink bottom", 1],
        ],
    },
    "everything melody glow top": {
        "length": 8,
        "beats": [
            [1, "Pink top", 3.5],
            [4.5, "Green top", 2],
            [6.5, "Cyan top", 2.5],
        ],
    },
    "everything melody glow bottom": {
        "length": 8,
        "beats": [
            [1, "Pink bottom", 3.5],
            [4.5, "Green bottom", 2],
            [6.5, "Cyan bottom", 2.5],
        ],
    },
    "everything melody 2 glow top": {
        "length": 10,
        "beats": [
            [1, "Pink top", 3.5],
            [4.5, "Green top", 2],
            [6.5, "Cyan top", 2.5],
            [9, "Yellow top", 2],
        ],
    },
    "everything melody 2 glow bottom": {
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
        "autogen": "downbeat bottom",
        "intensity": "high",
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
            [1, "Sidechain top g", 1, 0, 0],
            [1, "Sidechain top b", 1, 1, 1],

            [2, "Sidechain top r", 1, .6, .6],
            [2, "Sidechain top g", 1, .2, .2],
            [2, "Sidechain top b", 1, 1, 1],
            
            [3, "Sidechain top r", 1, .4, .4],
            [3, "Sidechain top g", 1, .4, .4],
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
            [8, "Sidechain top g", 1, .3, .3],
            [8, "Sidechain top b", 1, .7, .7],
        ],
    },
    "everything UV waver": {
        "length": 1.5,
        "beats": [
            [1, "UV", .5, 1, 0],
            [1.25, "UV", .25, 0, 1],
            [2, "UV", .4, .2, .8],
        ],
    },
    "Radiohead - Everything in Its Right Place (Sam Goku Edit)": {
        "beats": [
            [1, "rainbow good slow top", 120, 0, .35],
            [1, "everything bottom glow", 120, .25, .25],
            [1, "everything kick", 31],
            [33, "everything kick", 24],
            [65, "everything kick line", 56],
            [121, "everything melody glow bottom", 8, .5, .7],
            [121, "UV", 8],
            [129, "everything melody glow bottom", 72, .7, .7],
            # [129, "rainbow good slow top", 60, .35, .35],
            # [129, "everything kick top RGB", 64, 1, 1],
            [129, "everything melody glow top", 60, .4, .4],
            [129, "everything kick line 2", 60],
            [189, "UV", 4],
            [193, "everything melody 2 glow top", 16, .4, .05],
            [193, "everything kick 2", 16, 1, 0],
            [193, "everything melody 2 glow bottom", 40, .5, .2],
            [193, "everything UV waver", 8, .1, 1],
            [201, "everything UV waver", 16],
            [217, "everything UV waver", 8, 1, .4],

            # why is this wrong
            # [233, "everything melody 2 glow bottom", 32, .2, .2],

            # [209, "everything kick 2", 16, 1, 0],


# snap to hooked ending
# BPM: 128, Sub: 10559, Beat: 440.96, Pygame
# pos: 206.23, Seconds: 206.24, 102% lights


# played whole way through hooked ending
# BPM: 128, Sub: 10547, Beat: 440.46, Pygame s:
# pos: 205.98, Seconds: 206.0, 102% lightss





# snap to shelter
# -skip 280 Beat: 323.6, Pygame pos: 193.9,
# Seconds: 193.6, 94% lights


# dkew?
# BPM: 50.0, Beat: 320.0, Pygame pos: 19.3,
# 383.4, Seconds: 382.8, 93% ligh





# snap to 
#  ▆▆▆▆▆▆▆▆▆▆▆▆▆▆
# BPM: 120, Beat: 402.1, Pygame pos: 200.6,
# Seconds: 200.6, 90% lights


# skew 3 min play
# BPM: 120, Beat: 448.9, Pygame pos: 223.9,
# Seconds: 223.9, 100% lights

            [305, "everything kick line", 16, 0, 1],
            [321, "everything kick line 2", 128],
            [321, "everything melody glow bottom", 128, .7, .7],
            [321, "everything melody glow top", 128, .4, .4],

        ],
        "delay_lights": .02,
        "skip_song": 0,
        "bpm": 120,
        "song_path": "songs/Radiohead - Everything in Its Right Place (Sam Goku Edit).ogg",
        "profiles": ["Shows"],
    },
}