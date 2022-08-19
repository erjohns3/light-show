effects = {
    "Triplets bottom": {
        "length": 1,
        "beats": [
            [1, [0, 0, 0, 10, 40, 0, 0], 0.33],
            [1.33, [0, 0, 0, 0, 10, 40, 0], 0.33],
            [1.66, [0, 0, 0, 40, 0, 10, 0], 0.33],
        ],
    },
    "Triplets top": {
        "length": 1,
        "beats": [
            [1, [10, 40, 10, 0, 0, 0, 0], 0.33, 0.3, 0.2],
            [1.33, [0, 10, 40, 0, 0, 0, 0], 0.33, 0.3, 0.2],
            [1.66, [40, 0, 10, 0, 0, 0, 0], 0.33, 0.3, 0.2],
        ],
    },
    "Yellow fade": {
        "length": 1,
        "beats": [
            [1, [0, 0, 0, 30, 30, 0, 0], 1, 1, 0],
        ],
    },
    "Green fade": {
        "length": 2,
        "beats": [
            [2, [0, 0, 0, 0, 25, 0, 0], 0.55, 1, 0.5],
        ],
    },
    "shelter bottom sidechain": {
        "length": 1,
        "beats": [
            [1, [0, 0, 0, -100, -100, -100, 0], 0.1, 0, 1],
            [1.1, [0, 0, 0, -100, -100, -100, 0], 0.3, 1, 0],
        ],
    },
    "top blue kick": {
        "length": 1,
        "beats": [
            [1, [0, 0, 255, 0, 0, 0, 0], 0.1, 0, 0.08],
            [1.1, [0, 0, 255, 0, 0, 0, 0], 1, 0.08, 0.04],
        ],
    },
    "Yellow Top to Bottom hang": {
        "length": 4,
        "beats": [
            [1, [114, 60, 5, 0, 25, 0, 0], .2, 0, .5],
            [1.2, [114, 60, 5, 0, 25, 0, 0], 1.1, .5, 0],
            [1.3, [0, 0, 0, 114, 60, 5, 0], 1.3, 0, .6],
            [2.6, [0, 0, 0, 114, 60, 5, 0], 38, .6, .6],
        ],
    },
    "muddy yellow ay": {
        "length": 1,
        "beats": [
            [1, [114, 60, 5, 0, 0, 0, 0], 1, 0.4, 0],
        ],
    },
    "Blue fade bottom": {
        "length": 16,
        "beats": [
            [1, [0, 0, 0, 0, 255, 0, 0], 8, 0, 0.1],
            [9, [0, 0, 0, 0, 255, 0, 0], 4, 0.1, 0.13],
            [13, [0, 0, 0, 0, 255, 0, 0], 4, 0.13, 0.2],
        ],
    },
    "Rainbow smooth": {
        "length": 4,
        "beats": [
            [1, [100, 0, 0, 0, 0, 0, 0], 0.5, 0, 0.1],
            [1.5, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.1, 0.1],
            [2, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.1, 0.2],
            [2.5, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.2, 0.2],
            [3, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.3, 0.4],
            [3.5, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.3, 0.3],
            [4, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.4, 0.5],
            [4.5, [100, 0, 0, 0, 0, 0, 0], 0.5, 0.3, 0.3]
        ],
    },
    "Chorus bottom": {
        "length": 3,
        "beats": [
            [1, "Cyan bottom", 1, 0.08, 0.08],
            [2, "Yellow bottom", 1, 0.08, 0.08],
            [3, "Pink bottom", 1, 0.08, 0.08],
        ],
    },
    "Shelter sub Chorus": {
        "length": 16,
        "beats": [
            [1, "shelter bottom sidechain", 12], 
            [1, "muddy yellow ay", 1], 
            [1, "Chorus bottom", 3],
            [2, "top blue kick", 2],
            [5, "muddy yellow ay", 1], 
            [5, "Chorus bottom", 3],
            [6, "top blue kick", 2],
            [9, "muddy yellow ay", 1], 
            [9, "Chorus bottom", 3],
            [10, "top blue kick", 2],
            [13, "Triplets bottom", 4],
        ],
    },
    "Shelter Chorus": {
        "length": 32,
        "beats": [
            [1, "Shelter sub Chorus", 32],
        ],
    },
    "Long way forward": {
        "length": 16,
        "beats": [
            [1.25, [0, 255, 0, 0, 0, 0, 0], 1, 0.08, 0.08],
            [1.75, [0, 0, 255, 0, 0, 0, 0], 1, 0.08, 0.08],
            [2, [0, 255, 0, 0, 0, 0, 0], 1, 0.08, 0.08],
            [3, [0, 0, 255, 0, 0, 0, 0], 2, 0.08, 0.08],
            [5, [0, 255, 0, 0, 0, 0, 0], 3, 0.08, 0.08],
        ],
    },
    "shelter rising uh uh uh uh": {
        "length": 4,
        "beats": [
            [1, "Cyan top", 1, 0.1, 0.1],
            [2, "Cyan top", 1, 0.15, 0.15],
            [3, "Cyan top", 1, 0.2, 0.2],
            [4, "Cyan top", 1, 0.25, 0.25],
        ],
    },
    "shelter green bottom": {
        "length": 1,
        "beats": [
            [1, "Green bottom", 1, 0.1, 0.1],
        ],
    },
    "shelter tambos": {
        "length": 2,
        "beats": [
            [2, "Indigo bottom", .3, 0.3, 0.1],
        ],
    },
    "rainbow good top": {
        "length": 8,
        "beats": [
            [1, "Green top", 3.7, .2, 0],
            [1, "Red top", 2.66, 0, .2],
            [3.66, "Red top", 3.7, 0.2, 0],
            [3.66, "Blue top", 2.66, 0, .2],
            [6.32, "Blue top", 3.7, 0.2, 0],
            [6.32, "Green top", 2.66, 0, 0.2],
        ],
    },
    "rainbow good slow top": {
        "length": 16,
        "beats": [
            [1, "Green top", 7.3, .2, 0],
            [1, "Red top", 5.3, 0, .2],
            [6.3, "Red top", 7.3, 0.2, 0],
            [6.3, "Blue top", 5.3, 0, .2],
            [11.6, "Blue top", 7.3, 0.2, 0],
            [11.6, "Green top", 5.4, 0, 0.2],
        ],
    },
    "shelter drum build": {
        "length": 3,
        "beats": [
            [2, "Green top", .05],
            [2.1, "Green top", .05],
            [2.2, "Green top", .08],
            # [2.25, "Green top", .05],
            [2.45, "Green top", .05],
            [2.7, "Green top", .05],
            [2.95, "Green top", .05],
            [3.22, "Green top", .05],
        ],
    },
    "shelter show": {
        "beats": [
            [1, "muddy yellow ay", 1], 
            [5, "muddy yellow ay", 1],
            [9, "muddy yellow ay", 1],
            [13, "shelter rising uh uh uh uh", 4],
            [17, "shelter tambos", 12],
            [17, "muddy yellow ay", 1],
            [21, "muddy yellow ay", 1],
            [25, "muddy yellow ay", 1],
            [29, "UV", 4], 
            [29, "shelter rising uh uh uh uh", 4],
            [33, "Shelter Chorus", 32],
            [61, "Triplets bottom", 4],
            [73, "Pulse", 8, 0.2, 0.2],
            [81, "Yellow fade", 1],
            [82, "Pulse", 15, 0.2, 0.2],
            [97, "rainbow good top", 24],
            [97, "Green fade", 16],
            [113, "shelter tambos", 8],
            [121, "UV", 6],
            [126, "shelter drum build", 3],
            [129, "Shelter Chorus", 64],
            [161, "UV pulse slow", 32],
            [193, "rainbow good top", 56],
            [225, "Green fade", 24],
            [249, "UV pulse slow", 6],
            [257, "Pulse", 12, 0.2, 0.2],
            [257, "shelter tambos", 28],
            [269, "shelter rising uh uh uh uh", 4],
            [273, "Pulse", 12, 0.2, 0.2],
            [285, "UV Strobe", 1.7, .1, 1],
            [286.7, "UV Strobe", 2.3, 1, 0],
            [289, "Shelter Chorus", 32],
            [321, "Long way forward", 24],
        ],
        "delay_lights": 0.1,
        "skip_song": 0.21,
        "bpm": 100,
        "song_path": "songs/shelter.ogg",
        "profiles": ["Shows"],
    },
}
