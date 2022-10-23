from effects.compiler import beat
# [beat, effect, length, start intensity, end intensity, beat skip, hue[-1, 1], sat, brightness]

effects = {

    # blues from -.17 - 0

    # 1 intro
    # 33 im blue
    # 65 im blue with bass
    # 97 drop
    # (109 singing slightly)
    # 129 verse
    # 193 im blue
    # 225 more im blue

    # 276? restart after slowdown

    "im blue pulse top": {
        "length": 1,
        "beats": [
            [1, "Blue top", 1, 1, 0], 
        ],
    },

    "im blue chop end top": {
        "length": .5,
        "beats": [
            [1.4, "Sidechain top b", .1], 
            [1.4, "Sidechain top g", .1], 
        ],
    },

    "im blue pulses": {
        "length": 1,
        "beats": [
            [1, "Blue top", 1, 1, 0], 
        ],
    },

    "im blue smooth top": {
        "length": 8,
        "beats": [
            [1, "Blue top", 8, 1, 1],
            [1, "Green top", 4, 0, 1],
            [5, "Green top", 4, 1, 0]
        ],
    },

    "im blue smooth front": {
        "length": 8,
        "beats": [
            [1, "Blue front", 8, 1, 1],
            [1, "Green front", 4, 0, 1],
            [5, "Green front", 4, 1, 0]
        ],
    },

    "im blue smooth back": {
        "length": 8,
        "beats": [
            [1, "Blue back", 8, 1, 1],
            [1, "Green back", 4, 0, 1],
            [5, "Green back", 4, 1, 0]
        ],
    },

    "im blue change on beat front": {
        "length": 8,
        "beats": [
            [1, "Blue front", 1, 1, 0, 0, 0],
            [2, "Blue front", 1, 1, 0, 0, -.0425],
            [3, "Blue front", 1, 1, 0, 0, -.084],
            [4, "Blue front", 1, 1, 0, 0, -.1275],
            [5, "Blue front", 1, 1, 0, 0, -.17],
            [6, "Blue front", 1, 1, 0, 0, -.1275],
            [7, "Blue front", 1, 1, 0, 0, -.084],
            [8, "Blue front", 1, 1, 0, 0, -.0425],
        ],
    },

    "im blue change on beat back": {
        "length": 8,
        "beats": [
            [1, "Blue back", 1, 1, 0, 0, 0],
            [2, "Blue back", 1, 1, 0, 0, -.0425],
            [3, "Blue back", 1, 1, 0, 0, -.084],
            [4, "Blue back", 1, 1, 0, 0, -.1275],
            [5, "Blue back", 1, 1, 0, 0, -.17],
            [6, "Blue back", 1, 1, 0, 0, -.1275],
            [7, "Blue back", 1, 1, 0, 0, -.084],
            [8, "Blue back", 1, 1, 0, 0, -.0425],
        ],
    },

    "im blue change on beat front back": {
        "length": 8,
        "beats": [
            [1, "im blue change on beat front", 8, 1, 1, 0],
            [1, "im blue change on beat back", 8, 1, 1, 4.5],
        ],
    },

    "im blue white accel bottom": {
        "length": 4,
        "beats": [
            [1, "White bottom", 1, 0, .1],
            [2, "White bottom", 1, .2, .4],
            [3, "White bottom", 1, .4, 1],
        ],
    },

    "im blue bass pulses bottom": {
        "length": 16,
        "beats": [
            #[1, "Blue bottom", 16, .3, .3],
            [1, "Blue bottom", 1, 1, 0],
            [3, "Blue bottom", 1, 1, 0],
            [4.5, "Blue bottom", 4.5, 1, 0],
            [11, "Blue bottom", 1, 1, 0],
            [12.5, "Blue bottom", 4.5, 1, 0],
        ],
    },

    "im blue bass pulses bottom 2": {
        "length": 8,
        "beats": [
            [1, "Blue bottom", 3, 1, .2],
            [4, "Blue bottom", 5, 1, 0],
        ],
    },

    "im blue blue strobe top": {
        "length": .2,
        "beats": [
            [1, "Blue top", 0.07]
        ],
    },

    "im blue green strobe top": {
        "length": .2,
        "beats": [
            [1, "Green top", 0.07]
        ],
    },

    "im blue everything": {
        "length": .5,
        "beats": [
            [1, "Blue top", .5],
            [1, "Blue bottom", .5],
            [1, "Sidechain top r", .5, 1, 1],
            [1, "Sidechain top g", .5, 1, 1],
            [1, "Sidechain bottom r", .5, 1, 1],
            [1, "Sidechain bottom g", .5, 1, 1],
        ],
    },

    "im blue strobe top": {
        "length": 16,
        "beats": [
            [1, "Blue top", 16],
            [1, "im blue green strobe top", 16],
        ],
    },

    "im blue drop": {
        "length": 16,
        "beats": [
            [1, "im blue bass pulses bottom 2", 16, 1, 1],
            [1, "im blue strobe top", 12, 1, .2],
            [13, "Blue top", 4, .6, 0],
        ],
    },

    "im blue drop 2": {
        "length": 16,
        "beats": [
            [1, "im blue bass pulses bottom 2", 16, 1, 1],
            [1, "Blue top", 12, 1],
            [1, "im blue chop end top", 12],

            [1, "Green top", 1, .57],
            [1.5, "Green top", 1, 0],
            [2, "Green top", 1, .29],
            [2.5, "Green top", 1, .57],
            [3, "Green top", 1, .71],
            [3.5, "Green top", 1, .14],
            [4, "Green top", 1, .43],
            [4.5, "Green top", 1, .57],
            [5, "Green top", 1, .57],
            [5.5, "Green top", 1, .29],
            [6, "Green top", 1, .57],
            [6.5, "Green top", 1, .86],
            [7, "Green top", 1, 1],
            [7.5, "Green top", 1, .29],
            [8, "Green top", 1, .86],
            [8.5, "Green top", 1, .71],
            [9, "Green top", 1, .57],
            [9.5, "Green top", 1, 0],
            [10, "Green top", 1, .29],
            [10.5, "Green top", 1, .57],
            [11, "Green top", 1, .71],
            [11.5, "Green top", 1, .14],
            [12, "Green top", 1, .43],
            [12.5, "Green top", 1, .57],

            [13, "Blue top", 4, .6, 0],
        ],
    },

    "im blue verse": {
        "length": 100,
        "beats": [
            [1, "im blue smooth front", 100],
            [1, "im blue smooth back", 100, 1, 1, 4],
            [13, "im blue everything", 1],
            [24.5, "im blue everything", 1],
            [33, "im blue everything", 1],
            [37, "im blue everything", 1],
            [41, "im blue everything", 1],
            [46.5, "im blue everything", 1],
        ],
    },

    "blue show": {
        "bpm": 135,
        "song_path": "songs/Eiffel 65  Blue Flume Remix  Official Visualiser.ogg",
        "delay_lights": 0.0228,
        "skip_song": 0.0,
        "beats": [
            # blue tinkling
            [1, "im blue smooth top", 31],
            [29, "im blue white accel bottom", 4],
            # im blue
            [33, "im blue change on beat front back", 64],
            # im blue with bass
            [65, "im blue bass pulses bottom", 32],
            [97, "im blue drop 2", 32],
            [129, "im blue verse", 64],
            [193, "im blue drop", 32],
        ]
    }
}