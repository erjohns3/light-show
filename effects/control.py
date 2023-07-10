from effects.compiler import *

effects = {

    "control UV clap": {
        "length": 2,
        "autogen": "UV",
        "beats": [
            [2, "UV", 1, 1, 0],
        ],
    },

    "control UV offbeat": {
        "length": 1,
        "beats": [
            [1.5, "UV", 1, 1, 0],
        ],
    },

    "control strobe front": {
        "length": .2,
        "beats": [
            [1, "White front", .07],
        ],
    },
    "control strobe back": {
        "length": .2,
        "beats": [
            [1, "White back", .07],
        ],
    },
    "control ghostly": {
        "length": 16,
        "beats": [
            [1, "control strobe back", 3, .1, .2],
            [4, "control strobe back", 3, .2, .1],
            [7, "control strobe front", 3, .1, .2],
            [10, "control strobe front", 3, .2, .1],
        ],
    },

    "control cycle bottom": {
        "length": 32,
        "beats": [
            [1, "Red bottom", 8],
            [1, "Blue bottom", 8, .2, 1],
            [9, "Red bottom", 8, 1, .1],
            [9, "Blue bottom", 8],
            [17, "Red bottom", 8, .1, 1],
            [17, "Blue bottom", 8],
            [25, "Red bottom", 8,],
            [25, "Blue bottom", 8, 1, .2],
        ],
    },

    "control pulse rb": {
        "length": 1,
        "beats": [
            [1, "Red bottom", 1, 1, 0],
            [1, "Blue bottom", 1, 1, 0],
        ],
    },

    "control pulse top": {
        "length": 4,
        "beats": [
            [1, "Purple top", .5, 1, 0, 0, 0],
            [2, "Pink top", .5, 1, 0],
            [3, "Blue top", .5, 1, 0],
            [4, "Red top", .5, 1, 0, 0, -40/360],
        ],
    },

    "control cycle bottom pulse": {
        "length": 32,
        "beats": [
            [1, "control cycle bottom", 32, .3],
            [1, "control pulse rb", 8, .1, .4],
            [9, "control pulse rb", 8, .4, .1],
            [17, "control pulse rb", 8, .1, .4],
            [25, "control pulse rb", 8, .4, .1],
        ],
    },

    "control cycle bottom waves": {
        "length": 32,
        "beats": [
            [1, "control cycle bottom", 32, .3],
            [1, "Red bottom", 4, .4, 0],
            [1, "Blue bottom", 4, .4, 0],
            [9, "Red bottom", 4, .4, 0],
            [9, "Blue bottom", 4, .4, 0],
            [17, "Red bottom", 4, .4, 0],
            [17, "Blue bottom", 4, .4, 0],
            [22, "Blue bottom", 2, .4, 0],
            [22, "Red bottom", 2, .4, 0],
            [25, "Blue bottom", 2, .4, 0],
            [25, "Red bottom", 2, .4, 0],
        ]
    },

    "control cycle bottom waves high": {
        "length": 32,
        "beats": [
            [1, "control cycle bottom", 32, .5],
            [1, "Red bottom", 4, .4, 0],
            [1, "Blue bottom", 4, .4, 0],
            [9, "Red bottom", 4, .4, 0],
            [9, "Blue bottom", 4, .4, 0],
            [17, "Red bottom", 4, .4, 0],
            [17, "Blue bottom", 4, .4, 0],
            [22, "Blue bottom", 2, .4, 0],
            [22, "Red bottom", 2, .4, 0],
            [25, "Blue bottom", 2, .4, 0],
            [25, "Red bottom", 2, .4, 0],
        ]
    },

    "control UV clap full": {
        "length": 16,
        "beats": [
            [1, "control UV clap", 16],
            [15.5, "UV", .4, 1, 0],
        ],
    },

    "control blat top": {
        "length": 8,
        "beats": [
            [1, "White top", 4, .6, .2],
            [5, "White top", .2, .2],
            [5, "control subtract green triplet top",4],
        ],
    },

    "control blat red top": {
        "length": 8,
        "beats": [
            [1, "Red top", 4, .6, .2],
            [5, "Red top", .2, .2],
            [5, "control subtract all triplet top",4],
        ],
    },

    "control top step fade": {
        "length": 4,
        "beats": [
            [1, "Red top", 1, 1, .5],
            [2, "Red top", 3, .5, .05],
            [2, "Red top", 1, .2, 0],
            [3, "Red top", 1, .2, 0],
            [4, "Red top", 1, .1, 0],
        ],
    },

    "control subtract 20 top": {
        "length": .1,
        "beats": [
            [1, [-20, -20, -20, 0, 0, 0, 0], 1, 1, .5],
        ],
    },

    "control subtract 20 bottom": {
        "length": .1,
        "beats": [
            [1, [0, 0, 0, -20, -20, -20, 0], 1, 1, .5],
        ],
    },

    "control subtract 20 top green": {
        "length": .1,
        "beats": [
            [1, [0, -20, 0, 0, 0, 0, 0], 1, 1, .5],
        ],
    },

    "control subtract 20 bottom green": {
        "length": .1,
        "beats": [
            [1, [0, 0, 0, 0, -20, 0, 0], 1],
        ],
    },

    "control subtract 20 top blue": {
        "length": .1,
        "beats": [
            [1, [0, 0, -20, 0, 0, 0, 0], 1],
        ],
    },

    "control subtract 20 top red": {
        "length": .1,
        "beats": [
            [1, [-20, 0, 0, 0, 0, 0, 0], 1],
        ],
    },

    "control subtract 20 bottom blue": {
        "length": .1,
        "beats": [
            [1, [0, 0, 0, 0, 0, -20, 0], 1],
        ],
    },

    "control subtract 20 bottom red": {
        "length": .1,
        "beats": [
            [1, [0, 0, 0, -20, 0, 0, 0], 1],
        ],
    },

    "control subtract green triplet top": {
        "length": 1,
        "beats": [
            [1, "control subtract 20 top green", .33, 1, 0],
            [1.33, "control subtract 20 top green", .33, 1, 0],
            [1.66, "control subtract 20 top green", .33, 1, 0]
        ],
    },

    "control subtract green triplet bottom": {
        "length": 1,
        "beats": [
            [1, "control subtract 20 bottom green", .33, 1, 0],
            [1.33, "control subtract 20 bottom green", .33, 1, 0],
            [1.66, "control subtract 20 bottom green", .33, 1, 0]
        ],
    },

    "control subtract all triplet top": {
        "length": 1,
        "beats": [
            [1, "control subtract 20 top", .33, 1, 0],
            [1.33, "control subtract 20 top", .33, 1, 0],
            [1.66, "control subtract 20 top", .33, 1, 0],
        ],
    },

    "control bottom ripple fast": {
        "length": .5,
        "beats": [
            [1, "Purple bottom", .5, 1],
            [1,  "control subtract 20 bottom", .25, 0, 1],
            [1,  "control subtract 20 bottom", .25, 1, 0],
        ],
    },

    "control bottom purple pulse": {
        "length": 1,
        "beats": [
            [1, "Purple bottom", .5, 1, 0],
            [1.5, "Purple bottom", .5, 0, 1],
        ],
    },

    "control top purple pulse": {
        "length": 1,
        "beats": [
            [1, "Purple top", .5, 1, 0],
            [1.5, "Purple top", .5, 0, 1],
        ],
    },

    "control bottom purple pulse color change": {
        "length": 2,
        "beats": [
            [1, "control bottom purple pulse", 2],
            [1,  "control subtract 20 bottom red", .5, 0, 2],
            [1.5,  "control subtract 20 bottom red", .5, 2, 0],
            [2,  "control subtract 20 bottom blue", .5, 0, 2],
            [2.5,  "control subtract 20 bottom blue", .5, 2, 0],
        ],
    },

    "control top purple pulse color change": {
        "length": 2,
        "beats": [
            [1, "control top purple pulse", 2],
            [1,  "control subtract 20 top red", .5, 0, 2],
            [1.5,  "control subtract 20 top red", .5, 2, 0],
            [2,  "control subtract 20 top blue", .5, 0, 2],
            [2.5,  "control subtract 20 top blue", .5, 2, 0],
        ],
    },

    "control bottom ripple triplet": {
        "length": 1,
        "beats": [
            [1, "Purple bottom", 1, 1],
            [1,  "control subtract 20 bottom red", .33, 2,0],
            [1.33,  "control subtract 20 bottom red", .33, 2, 0],
            [1.66,  "control subtract 20 bottom red", .33, 2, 0],
        ],
    },

    "control top flicker fade": {
        "length": 4,
        "beats": [
            [1, "Red top", 4, 1, 0],
            [2,  "control subtract 20 top"],
            [2.5,  "control subtract 20 top"],
            [2.7,  "control subtract 20 top"],
            [3,  "control subtract 20 top"],
        ],
    },

    "control back let the": {
        "length": 4,
        "beats": [
            [4, "Red back", .5, 1, 0, 0, 0],
            [4.5, "Red back", .5, 1, 0, 0, 0],
        ],
    },

    "control front let the": {
        "length": 4,
        "beats": [
            [4, "Red front", .5, 1, 0, 0, 0],
            [4.5, "Red front", .5, 1, 0, 0, 0],
        ],
    },

    "control top let the full": {
        "length": 16,
        "beats": [
            [1, "control back let the", 4, 1, 1, 0, -40/360],
            [5, "control front let the", 4, 1, 1, 0, -60/360],
            [9, "control back let the", 4, 1, 1, 0, -80/360],
        ],
    },

    "control top flash": {
        "length": 4,
        "beats": [
            [1, "White top", .5, 1, .2],
            [1.5, "White top", .5, .2, 0],
        ],
    },

    "control bottom rainbow": {
        "length": 4,
        "beats": [
            [1, "Red top", 4, 1, 0],
            [2,  "control subtract 20 top"],
            [2.5,  "control subtract 20 top"],
            [2.7,  "control subtract 20 top"],
            [3,  "control subtract 20 top"],
        ],
    },

    "control intro no bass": {
        "length": 64,
        "beats": [
            [1, "control top step fade", 4, 1, 1, 0, 267/360],
            [9, "control top step fade", 4, 1, 1, 0, 267/360],
            [17, "control top step fade", 4, 1, 1, 0, 285/360],
            [25, "control top step fade", 4, 1, 1, 0, 285/360],
            [30, "control top flicker fade", 3, 1, 1, 0, 300/360],
            [33, "control top step fade", 4, 1, 1, 0, 267/360],
            [41, "control top step fade", 4, 1, 1, 0, 267/360],
            [49, "control top step fade", 4, 1, 1, 0, 285/360],
            [57, "control top step fade", 4, 1, 1, 0, 285/360],
        ],
    },

    "Emmit Fenn  Control": {
        "bpm": 120,
        "song_path": "songs/Emmit Fenn - Control.ogg",
        "delay_lights": 0.055,
        "skip_song": 0.0,
        "beats": [
            [1, "control intro no bass", 128],
            [65, "control UV clap full", 64, .5],
            [65, "control cycle bottom pulse", 64, 1, 1, 0, -.05],
            [97, "control blat top", 8],
            [126, "control top flicker fade", 3, 1, 1, 0, 300/360],
            [129, "control UV offbeat", 4, .8, .2],
            [137, "control bottom ripple triplet", 8, 1, 0],
            [145, "control bottom purple pulse color change",8, .8],
            [153, "control bottom purple pulse color change",13.5, .8, .8, 0, -20/300],
            
            [169, "control bottom purple pulse color change",16, .8],
            [169, "control ghostly", 32],
            [185, "control bottom purple pulse color change",15.5, .8, .8, 0, -20/300],
            [201, "control top let the full", 64],
            [217, "control top flash", 4],
            [233, "control top flash", 4],
            [233, "control UV clap full", 24,.5],

            [249, "control top flash", 4],
            [265, "control top flash", 4],
            
            [209, "control cycle bottom waves", 53],
            [259, "UV Strobe", 2, .1, .8],
            
            [269, "control UV clap full", 64],
            [269, "control blat red top", 8],
            [269, "control bottom ripple triplet", 8, 1, 0],

            [277, "control cycle bottom waves high", 56],
            [277, "control pulse top", 24],
            [301, "control blat top", 8],
            [301, "control pulse top", 32, .6],
            [333, "control UV offbeat", 4, .8, .2],
        ]
    }
}