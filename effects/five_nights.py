effects = {
    "five nights pulse white": {
        "length": 1,
        "beats": [
            [1, "White bottom", .5, 0, 1],
            [1.5, "White bottom", .5, 1, 0],
        ],
    },

    "five nights pulse red": {
        "length": 4,
        "beats": [
            [1, "Red bottom",1, 1,1],
            [2, "Red bottom",1 , .6, .6],
            [3, "Red bottom",1 , .3, .3],
            [4, "Red bottom",1 , 0,0]
        ],
    },

    "torreador": {
        "length": 8,
        "beats": [
            [1, "Cyan top", 1, 1, 1],
            [2, "Pink top", .75, 1, 1],
            [2.75, "Yellow top", .25, 1, 1],
            [3, "Cyan top", 1, 1, 1],
            [4, "Pink top", 1, 1, 1],
            [5, "Yellow top", .75, 1, 1],
            [5.75, "Cyan top", .25, 1, 1],
            [6, "Pink top", .75, 1, 1],
            [6.75, "Yellow top", .25, 1, 1],
            [7, "Cyan top", 1, 1, 0]
        ],
    },

    # bass: 1 2.5 3 (rest) 5 (stocatto) 6.5 7 8 8.5 
    "five nights bass 1": {
        "length": 8,
        "beats": [
            [1, "Green bottom", 1.5, 1, .2],
            [2.5, "Green bottom", .2],
            [3, "Red bottom", 1, 1, 0],
            [5, "Green bottom", 1.5, 1, .2],
            [6.5, "Green bottom", .1],
            [7, "Red bottom", .5],
            [8, "Red bottom", .2],
            [8.5, "Red bottom", .2],
        ],
    },

    "five nights melody 1 intro": {
        "length": 8,
        "beats": [
            [1, "five nights pulse white", 1, .2],
            [2, "five nights pulse white", 1, .3],
            [3, "five nights pulse white", 1, .4],
            [4, "five nights pulse white", 1, .5],
            [5, "five nights pulse white", 1, .6],
            [6, "five nights pulse white", 1, .7],
            [7, "five nights pulse white", 1, .8],
            [8, "five nights pulse white", 1, .9],
        ],
    },

    "five nights green red top": {
        "length": 2,
        "beats": [
            [1, "Green front", 0.5, 0, 1],
            [1.5, "Green front", 0.5, 1, 0],
            [2, "Red back", .5, 0, 1],
            [2.5, "Red back", .5, 1, 0],
        ],
    },

    "five nights red green top": {
        "length": 2,
        "beats": [
            [1, "Red front", 0.5, 0, 1],
            [1.5, "Red front", 0.5, 1, 0],
            [2, "Green back", .5, 0, 1],
            [2.5, "Green back", .5, 1, 0],
        ],
    },

    "five nights red circle": {
        "length": 1.5,
        "beats": [
            [1, "Red back", 0.5],
            [1.5, "Red front", 0.5],
            [2, "Red bottom", .5],
        ],
    },

    "five nights red circle 2": {
        "length": 1.5,
        "beats": [
            [1, "Red front", 0.5],
            [1.5, "Red back", 0.5],
            [2, "Red bottom", .5],
        ],
    },

    "five nights green circle": {
        "length": 1.5,
        "beats": [
            [1, "Green back", 0.5],
            [1.5, "Green front", 0.5],
            [2, "Green bottom", .5],
        ],
    },

    "five nights green circle 2": {
        "length": 1.5,
        "beats": [
            [1, "Green front", 0.5],
            [1.5, "Green back", 0.5],
            [2, "Green bottom", .5],
        ],
    },

    "five nights chorus": {
        "length": 50,
        "beats": [
            [1, "five nights green red top", 7],
            [9, "five nights red green top", 7],
            [17, "five nights red circle", 8],
            [25, "five nights green circle 2", 8],
            [33, "five nights red circle 2", 8],
            [41, "five nights green circle", 8],
        ],
    },

    "five_nights_show": {
        "bpm": 103,
        "song_path": "songs\\The Living Tombstone  Five Nights at Freddys Song LYRICS.ogg",
        "delay_lights": 0.14900000000000002,
        "skip_song": 0.0,
        "beats": [
            # quiet intro
            [1,"five nights melody 1 intro", 16],
            [1, "torreador", 49, .1, .5],
            # Getting louder
            [17, "five nights pulse red", 32],
            # Build up to chorus
            [49, "five nights bass 1", 31],
            [49, "UV Strobe", 16],
            # half way through chorus
            [65, "UV pulse", 15],
            # (one beat dark)
            # Chorus
            [81, "five nights chorus", 50]
        ]
    }
}