from effects.compiler import b
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

    "im blue pulse bottom": {
        "length": 1,
        "beats": [
            [1, "Blue bottom", .5, 1], 
            [1.5, "Blue bottom", .5, 0, 0], 
        ],
    },

    "im blue chop end top": {
        "length": .5,
        "beats": [
            [1.3, "Sidechain top b", .4], 
            [1.3, "Sidechain top g", .4], 
        ],
    },

    "im blue pulses": {
        "length": 1,
        "beats": [
            [1, "Blue top", 1, 1, 0], 
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

    "im blue smooth fast front": {
        "length": 4,
        "beats": [
            [1, "Blue front", 4, 1, 1],
            [1, "Green front", 2, 0, 1],
            [3, "Green front", 2, 1, 0]
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

    "im blue smooth fast back": {
        "length": 4,
        "beats": [
            [1, "Blue back", 4, 1, 1],
            [1, "Green back", 2, 0, 1],
            [3, "Green back", 2, 1, 0]
        ],
    },

    "im blue change on beat front": {
        "length": 8,
        "beats": [
            [1, "Blue front", 1, 1, 1, 0, 0],
            [2, "Blue front", 1, 1, 1, 0, -.0425],
            [3, "Blue front", 1, 1, 1, 0, -.084],
            [4, "Blue front", 1, 1, 1, 0, -.1275],
            [5, "Blue front", 1, 1, 1, 0, -.17],
            [6, "Blue front", 1, 1, 1, 0, -.1275],
            [7, "Blue front", 1, 1, 1, 0, -.084],
            [8, "Blue front", 1, 1, 1, 0, -.0425],
        ],
    },

    "im blue change on beat flash front": {
        "length": 8,
        "beats": [
            [1, "Blue front", .6, 1, 1, 0, 0],
            [2, "Blue front", .6, 1, 1, 0, -.0425],
            [3, "Blue front", .6, 1, 1, 0, -.084],
            [4, "Blue front", .6, 1, 1, 0, -.1275],
            [5, "Blue front", .6, 1, 1, 0, -.17],
            [6, "Blue front", .6, 1, 1, 0, -.1275],
            [7, "Blue front", .6, 1, 1, 0, -.084],
            [8, "Blue front", .6, 1, 1, 0, -.0425],
        ],
    },

    "im blue change on beat back": {
        "length": 8,
        "beats": [
            [1, "Blue back", 1, 1, 1, 0, 0],
            [2, "Blue back", 1, 1, 1, 0, -.0425],
            [3, "Blue back", 1, 1, 1, 0, -.084],
            [4, "Blue back", 1, 1, 1, 0, -.1275],
            [5, "Blue back", 1, 1, 1, 0, -.17],
            [6, "Blue back", 1, 1, 1, 0, -.1275],
            [7, "Blue back", 1, 1, 1, 0, -.084],
            [8, "Blue back", 1, 1, 1, 0, -.0425],
        ],
    },

    "im blue change on beat flash back": {
        "length": 8,
        "beats": [
            [1, "Blue back", .6, 1, 1, 0, 0],
            [2, "Blue back", .6, 1, 1, 0, -.0425],
            [3, "Blue back", .6, 1, 1, 0, -.084],
            [4, "Blue back", .6, 1, 1, 0, -.1275],
            [5, "Blue back", .6, 1, 1, 0, -.17],
            [6, "Blue back", .6, 1, 1, 0, -.1275],
            [7, "Blue back", .6, 1, 1, 0, -.084],
            [8, "Blue back", .6, 1, 1, 0, -.0425],
        ],
    },

    "im blue change on beat front back": {
        "length": 32,
        "beats": [
            [1, "im blue change on beat front", 28, 1, 1, 0],
            [1, "im blue change on beat back", 28, 1, 1, 4.5],
            [29, "Blue top", 4, 1, 0],
        ],
    },

    "im blue change on beat flash front back": {
        "length": 32,
        "beats": [
            [1, "im blue change on beat flash front", 28, 1, 1, 0],
            [1, "im blue change on beat flash back", 28, 1, 1, 4.5],
            [29, "Blue top", 4, 1, 0],
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

    "im blue white accel front": {
        "length": 4,
        "beats": [
            [1, "White front", 1, 0, .1],
            [2, "White front", 1, .2, .4],
            [3, "White front", 1, .4, 1],
        ],
    },

    "im blue white accel back": {
        "length": 4,
        "beats": [
            [1, "White back", 1, 0, .1],
            [2, "White back", 1, .2, .4],
            [3, "White back", 1, .4, 1],
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

    "im blue bass pulses bottom 3": {
        "length": 32,
        "beats": [
            [1, "Blue bottom", 3, 1, .2],
            [4, "Blue bottom", .5, 1, .2],
            [4.5, "Blue bottom", 4.5, 1, 0],
            [9, "Blue bottom", .5, 1, .2],
            [9.5, "Blue bottom", 2.5, 1, .2],
            [12, "Blue bottom", .5, 1, .2],
            [12.5, "Blue bottom", 4.5, 1, 0],
            [17, "Blue bottom", 3, 1, .2],
            [20, "Blue bottom", .5, 1, .2],
            [20.5, "Blue bottom", 4.5, 1, 0],
            [25, "Blue bottom", .5, 1, .2],
            [25.5, "Blue bottom", 2.5, 1, .2],
            [28, "Blue bottom", 5, 1, 0],
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
            [1, "Blue top", .5, 1, 0],
            [1, "Blue bottom", .5, 1, 0],
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
            [1, "im blue green strobe top", 16, 1, .5],
        ],
    },

    "im blue strobe pulse top": {
        "length": 1,
        "beats": [
            [1, "im blue strobe top", .5],
        ],
    },

    "im blue UV clap": {
        "length": 4,
        "beats": [
            [3, "UV", 1, 1, 0],
        ],
    },

    "im blue drop": {
        "autogen": "downbeat mixed",
        "intensity": "high",
        "length": 16,
        "beats": [
            [1, "im blue bass pulses bottom 2", 16, 1, 1],
            [1, "im blue strobe pulse top", 12, .6],
            [13, "Blue top", 4, .6, 0],
        ],
    },

    "im blue drop 2": {
        "length": 16,
        "beats": [
            
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

    "im blue drop 3": {
        "length": 16,
        "beats": [
            
            [1, "Blue top", 4, 1],
            [9, "Blue top", 4, 1],
            [1, "im blue chop end top", 4],
            [9, "im blue chop end top", 4],

            [1, "Green top", 1, .57],
            [1.5, "Green top", 1, 0],
            [2, "Green top", 1, .29],
            [2.5, "Green top", 1, .57],
            [3, "Green top", 1, .71],
            [3.5, "Green top", 1, .14],
            [4, "Green top", 1, .43],
            [4.5, "Green top", 1, .57],
            [5, "Blue top", 4, .6, 0],
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

    "im blue drop extras": {
        "length": 32,
        "beats": [
            # bass
            [1, "Blue bottom", 3, 1, .2],
            [4, "Blue bottom", .5, 1, .2],
            [4.5, "Blue bottom", 4.5, 1, 0],
            [9, "Blue bottom", .5, 1, .2],
            [9.5, "Blue bottom", 2.5, 1, .2],
            [12, "Blue bottom", .5, 1, .2],
            [12.5, "Blue bottom", 4.5, 1, 0],
            [17, "Blue bottom", 3, 1, .2],
            [20, "Blue bottom", .5, 1, .2],
            [20.5, "Blue bottom", 4.5, 1, 0],
            [25, "Blue bottom", .5, 1, .2],
            [25.5, "Blue bottom", 2.5, 1, .2],
            [28, "Blue bottom", 5, 1, 0],

            [5.5, "UV", .5, 0, 1],
            [6.5, "UV", .5],
            [7.4, "UV", .2],

            [13, "UV", .2],
            [13.75, "UV", .2],
            [14, "UV", .2],
            [14.25, "UV", .2],
            [14.5, "UV", .2],
            [15, "UV", .2],
            [16, "UV", .2],

            [22, "UV", .2],
            [22.75, "UV", .2],
            [23, "UV", .2],
            [23.25, "UV", .2],
            [23.5, "UV", .2],
            [24, "UV", .2],
        ],
    },

    "im blue slowed": {
        "length": 12,
        "beats": [
            
            # [1, "White top", 2, 0, 1],
            # [1, "White bottom", 2, 0, 1],
            # [3, "Blue top", 12],
            # [3, "Blue bottom", 12],
            # [3, "Red top", 4, 1, 0],
            # [3, "Red bottom", 4, 1, 0],
            # [3, "Green top", 4],
            # [3, "Green bottom", 4],
            # [7, "Green top", 4, 1, 0],
            # [7, "Green bottom", 4, 1, 0],
            

            [1, "Red top", 3, 0, 1],
            [1, "Red bottom", 3, 0, 1],
            [4, "Red top", 3, 1, 0],
            [4, "Red bottom", 3, 1, 0],
            [4, "Green top", 3, 0, 1],
            [4, "Green bottom", 3, 0, 1],
            [7, "Green top", 3, 1, 0],
            [7, "Green bottom", 3, 1, 0],
            [7, "Blue top", 4, 0, 1],
            [7, "Blue bottom", 4, 0, 1],
            [10.2, "Sidechain top b", .3],
            [10.5, "Sidechain bottom b", .1],
            [10.7, "Sidechain bottom b", .4],
            [11, "Sidechain top b", .4],
            [11.6, "Sidechain top b", .1],
            [11.8, "Sidechain top b", .1],
        ],
    },

    "im blue strobe slow": {
        "length": 1,
        "beats": [
            [1, "Blue top", .2],
            [1.5, "Blue bottom", .2],
        ],
    },

    "im blue strobe fast": {
        "length": .5,
        "beats": [
            [1, "Blue top", .1],
            [1.25, "Blue bottom", .1],
        ],
    },

    "im blue strobe chaos": {
        "length": 12,
        "beats": [
            [1, "im blue strobe bottom", 12],
            [1, "im blue strobe front", 12],
            [1, "im blue strobe back", 12],
        ],
    },

    "im blue strobe bottom": {
        "length": .4,
        "beats": [
            [1, "Blue bottom", .07],
        ],
    },

    "im blue strobe front": {
        "length": .3,
        "beats": [
            [1, "Blue front", .07],
        ],
    },

    "im blue strobe back": {
        "length": .2,
        "beats": [
            [1, "Blue back", .07],
        ],
    },

    "im blue verse": {
        "length": 100,
        "beats": [
            [1, "im blue UV clap", 100],
            #[1, "im blue smooth front", 100],
            #[1, "im blue smooth back", 100, 1, 1, 4],

            #[1, "im blue white accel bottom", 100, 1, 1, 2],
            #[1, "im blue white accel back", 100, 1, 1, 0],
            #[1, "im blue white accel front", 100, 1, 1, 3],

            # Flash blue whenever he says blue
            [13, "im blue everything", 1],
            [24.5, "im blue everything", 1],
            [33, "Blue top", 1, 1, 0],
            [37, "Blue top", 1, 1, 0],
            [41, "Blue top", 1, 1, 0],
            [46.5, "Blue top", 1, 1, 0],

            [33, "Blue bottom", 2, 1, 0],
            [35, "Blue bottom", 1.5, 1, 0],
            [36.5, "Blue bottom", 2, 1, 0],
            [43, "Blue bottom", 1.5, 1, 0],
            [44.5, "Blue bottom", 2, 1, 0],
            [49, "Blue bottom", 2, 1, 0],
            [51, "Blue bottom", 1.5, 1, 0],
            [52.5, "Blue bottom", 2, 1, 0],
            [57, "Blue bottom", 2, 1, 0],
            [59, "Blue bottom", 1.5, 1, 0],
            [60.5, "Blue bottom", 2, 1, 0],
        ],
    },

    "blue show": {
        "bpm": 135,
        "song_path": "songs/Eiffel 65  Blue Flume Remix  Official Visualiser.ogg",
        "delay_lights": 0.0228,
        "skip_song": 0.0,
        "beats": [
            # blue tinkling
            #[1, "im blue smooth top", 31],
            [1, "im blue smooth fast front", 31, .2],
            [1, "im blue smooth fast back", 31, .2],
            [29, "im blue white accel bottom", 4],
            # im blue
            [33, "im blue pulse bottom", 32, .7],
            #[33, "im blue change on beat front back", 32, .5],
            
            # im blue with bass
            [65, "im blue change on beat flash front back", 32, .5],
            [65, "im blue bass pulses bottom", 32],
            [97, "im blue drop 2", 32, .7],
            [97, "im blue bass pulses bottom 2", 32],
            [129, "im blue verse", 64],
            [193, "im blue drop", 32],
            [225, "im blue drop 3", 32],
            [225, "im blue drop extras", 32],
            [265, "im blue slowed", 11, .5, 1],
            [276, "im blue drop", 32],
            [308, "im blue strobe chaos", 24],
            [332, "im blue strobe fast", 4],
            [336, "im blue strobe slow", 4],


            [340, "im blue UV clap", 28],
            [340, "im blue bass pulses bottom 3", 28],
            #[340, "im blue smooth fast front", 28],
            #[340, "im blue smooth fast back", 28],
            #[368, "Blue top", 8, 1, 0],
            [368, "Blue bottom", 8, 1, 0],
        ]
    }
}