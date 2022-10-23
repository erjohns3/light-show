from effects.compiler import beat

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
        "length": 64,
        "beats": [
            [1, "five nights static bottom", 16, .6, .6],
            [1, "five nights green red top", 7],
            [9, "five nights red green top", 7],
            [17, "five nights red circle", 8],
            [25, "five nights green circle 2", 16],
            [33, "five nights red circle 2", 8, 1],
            [41, "five nights static bottom", 8],
            [41, "five nights static top", 8],
            #  quarter notes after chorus
            [49, "rainbow good top", 16]
        ],
    },

     "five nights static bottom": {
        "length": 11,
        "beats": [
            [1, "White bottom", 11, 1, 1],
            [1.5, "Sidechain bottom rbg", .1 ],
            [2.1, "Sidechain bottom rbg", .1 ],
            [2.9, "Sidechain bottom rbg", .2 ],
            [3.2, "Sidechain bottom rbg", .1 ],
            [3.6, "Sidechain bottom rbg", .1 ],
            [4.1, "Sidechain bottom rbg", .1 ],
            [5.1, "Sidechain bottom rbg", .1],
            [5.5, "Sidechain bottom rbg", .2],
            [6, "Sidechain bottom rbg", .1],
            [6.2, "Sidechain bottom rbg", .1],
            [6.5, "Sidechain bottom rbg", .1],
            [7.3, "Sidechain bottom rbg", .1],
            [7.7, "Sidechain bottom rbg", .2],
            [8.1, "Sidechain bottom rbg", .1],
            [8.7, "Sidechain bottom rbg", .2],
            [8.97, "Sidechain bottom rbg", .1],
            [9.4, "Sidechain bottom rbg", .2],
            [9.9, "Sidechain bottom rbg", .1],
            [10.3, "Sidechain bottom rbg", .1],
            [10.7, "Sidechain bottom rbg", .1],
            [11.2, "Sidechain bottom rbg", .2],
            [11.8, "Sidechain bottom rbg", .1 ],
        ],
    },

    "five nights static top": {
        "length": 11,
        "beats": [
            [1, "White top", 11, 1, 1],
            [1.5, "Sidechain top rbg", .1 ],
            [2.1, "Sidechain top rbg", .1 ],
            [2.9, "Sidechain top rbg", .2 ],
            [3.2, "Sidechain top rbg", .1 ],
            [3.6, "Sidechain top rbg", .1 ],
            [4.1, "Sidechain top rbg", .1 ],
            [5.1, "Sidechain top rbg", .1],
            [5.5, "Sidechain top rbg", .2],
            [6, "Sidechain top rbg", .1],
            [6.2, "Sidechain top rbg", .1],
            [6.5, "Sidechain top rbg", .1],
            [7.3, "Sidechain top rbg", .1],
            [7.7, "Sidechain top rbg", .2],
            [8.1, "Sidechain top rbg", .1],
            [8.7, "Sidechain top rbg", .2],
            [8.97, "Sidechain top rbg", .1],
            [9.4, "Sidechain top rbg", .2],
            [9.9, "Sidechain top rbg", .1],
            [10.3, "Sidechain top rbg", .1],
            [10.7, "Sidechain top rbg", .1],
            [11.2, "Sidechain top rbg", .2],
            [11.8, "Sidechain top rbg", .1 ],
        ],
    },

    "five nights green red bottom": {
        "length": 2,
        "beats": [
            [1, "Red bottom", .9],
            [2, "Green bottom", .9],
        ],
    },

    "five_nights show": {
        "bpm": 103,
        "song_path": "songs/The Living Tombstone  Five Nights at Freddys Song LYRICS.ogg",
        "delay_lights": 0.13400000000000002,
        "skip_song": 0.0,
        "beats": [
            # quiet intro
            [1,"five nights melody 1 intro", 16, .4, .4],
            [1, "torreador", 16, .1, .5],
            # Verse
            [17, "torreador", 33, .8],
            [17, "five nights pulse red", 32],
            # Build up to chorus
            [49, "five nights bass 1", 31],
            [49, "UV Strobe", 16],
            # half way through chorus
            [65, "UV pulse", 15],
            # (one beat dark)
            # Chorus
            [81, "five nights chorus", 64],
            # Verse
            [145, "torreador", 33, .8],
            [145, "five nights pulse red", 32],
            # Build up to chorus
            [177, "five nights bass 1", 31],
            [177, "UV Strobe", 16],
            # half way through chorus
            [193, "UV pulse", 15],
             # (one beat dark)
            # Chorus
            [209, "five nights chorus", 40],
            [249, "five nights static top", 24, .5, .5, 3],
            [249, "five nights green red bottom", 22],
            # Scream thing at the end
            [273, "Red top", 16, 1, 1],
            [273, "Red bottom", 16, 1, 1],
            [273, "UV", 16, 1, 1],
        ]
    }
}

# [beat, effect, length, start intensity, end intensity, beat skip, hue[-1, 1], sat, brightness]