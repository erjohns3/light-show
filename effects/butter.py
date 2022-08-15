effects = {
    # 1 string and weird metal 
    # 33 synth adds in
    # 65 kick adds in, synth starts trending up
    # 97 fast kick at
    # 121 right before drop
    # 129 drop
    # 193 break




    "butter melody 1 down":{
        "length": 8,
        "beats":{
            "1": [["Red top", .2], ],
            "1.75": [["Red top", .2]],
            "2.50": [["Red top", .2]],
            "3.25": [["Red top", .2]],
            "4": [["Red top", .2]],
            "4.75": [["Red top", .2], ["Green top", 4, 0, 1]],
            "4.95": [["Sidechain top bg", .55], ["Sidechain top r", 3, 0, 1]],
            "5.5": [["Red top", .2]],
            "5.7": [["Sidechain top bg", .55]],
            "6.25": [["Red top", .2]],
            "6.45": [["Sidechain top bg", .55]],
            "7": [["Red top", .2]],
            "7.2": [["Sidechain top bg", 1.8]],
        }
    },

    "butter melody 1 up":{
        "length": 8,
        "beats":{
            "1": [["Red top", .2], ],
            "1.75": [["Red top", .2]],
            "2.50": [["Red top", .2]],
            "3.25": [["Red top", .2]],
            "4": [["Red top", .2]],
            "4.75": [["Red top", .2], ["Blue top", 4, 0, 1]],
            "4.95": [["Sidechain top bg", .55]],
            "5.5": [["Red top", .2]],
            "5.7": [["Sidechain top bg", .55]],
            "6.25": [["Red top", .2]],
            "6.45": [["Sidechain top bg", .55]],
            "7": [["Red top", .2]],
            "7.2": [["Sidechain top bg", 1.8]],
        }
    },

    "butter melody 2":{
        "length": 8,
        "beats":{
            "1.75": [["Red top", .1]],
            "2": [["Red top", .2]],
            "2.5": [["Red top", .1]],
            "2.75": [["Red top", .2]],
            "3.25": [["Red top", .1]],
            "3.5": [["Red top", .2]],
            "4.25": [["Red top", .2]],
            "4.75": [["Red top", .1]],
            "5": [["Red top", .2]],
            "5.5": [["Red top", .1]],
            "5.75": [["Red top", .2]],
            "6.25": [["Red top", .1]],
            "6.5": [["Red top", .2]],
            "7": [["Red top", .1]],
            "7.25": [["Red top", .1]],
            "7.5": [["Red top", .1]],
            "7.75": [["Red top", .1]],
            "8": [["Red top", .1]],
        }
    },

    "butter melody 3":{
        "length": 8,
        "beats":{
            "1.75": [["Red top", .1]],
            "2": [["Red top", .2]],
            "2.5": [["Red top", .1]],
            "2.75": [["Red top", .2]],
            "3.25": [["Red top", .1]],
            "3.5": [["Red top", .2]],
            "4.25": [["Red top", .2]],
            "4.75": [["Red top", .1]],
            "5": [["Red top", 1.9, 1, 0], ["Green top", 1.9, 0, .3], ["Blue top", 1.9, 0, .7]],
        }
    },

    "butter melody 4":{
        "length": 8,
        "beats":{
            "1.75": [["Red top", .1]],
            "2": [["Red top", .2]],
            "2.5": [["Red top", .1]],
            "2.75": [["Red top", .2]],
            "3.25": [["Red top", .1]],
            "3.5": [["Red top", .2]],
            "4.25": [["Red top", .2]],
            "4.75": [["Red top", .1]],
            "5": [["Red top", .2]],
            "5.5": [["Red top", .1]],
            "5.75": [["Red top", .2]],
            "6.25": [["Red top", .1]],
            "6.5": [["Red top", .2]],
            "7": [["Red top", .1]],
            "7.25": [["Red top", .1]],
        }
    },

    "butter melody":{
        "length": 64,
        "beats":{
            "1": [["butter melody 1 down", 8]],
            "9": [["butter melody 2", 8]],
            "17": [["butter melody 1 up", 8]],
            "25": [["butter melody 3", 8]],
            "33": [["butter melody 1 down", 8]],
            "41": [["butter melody 4", 8]],
            "49": [["butter melody 1 up", 8]],
            "57": [["butter melody 3", 4]],
            "61": [["butter melody 3", 2, 1, 0, 4]],
        }
    },
    "Some color bottom":{
        "length": 1,
        "beats":{
            "1": [[[0, 0, 0, 20, 0, 40, 0], 1]]
        }
    },
    "butter kicks":{
        "length": 2,
        "beats":{
            "1": ["Green bottom", 0.1, 0.6, 0.17],
            "1.1": ["Green bottom", 3, 0.17, 0.17],
            "2": [["Sidechain bottom g", 0.5, 1, 0], ["Some color bottom", 0.3, 1, .7]],

        }
    },
    "butter bassline":{
        "length": 32,
        "beats":{
            "1": ["butter kicks", 15],
            "17": ["butter kicks", 12],
            "29": ["butter kicks", 2, 1, 0],
        }
    },
    "butter ho":{
        "length": 32,
        "beats":{
            "16.5": ["UV", .3]
        }
    },
    "butter chorus":{
        "length": 64,
        "beats":{
            "1": [["butter melody", 64], ["butter bassline", 64], ["butter ho", 64]],
        }
    },
    "Testing":{
        "length": 64,
        "beats":{
            "1": ["Blue bottom", 64, 1, 1],
        }
    },
    "butter show":{
        "beats":{
            "1": [["Nothing", 32]],
            "33": [["wandering", 32]],
            "65": [["RBBB 1 bar", 32]],
            "97": [["Ghosts bassline", 24]],
            "121": [["wandering", 4]],
            "125": [["UV", 4]],
            "129": [["butter chorus", 64]],
            "193": [["UV Pulse", 64]],
            "257": [["RBBB 1 bar", 64]], # buildup
            "321": [["butter chorus", 64]],
        },
        "delay_lights": .14,
        "skip_song": 0,
        "bpm": 112,
        "song_path": "songs/Not Butter.ogg",
        "profiles": ["Shows"],
    },
}