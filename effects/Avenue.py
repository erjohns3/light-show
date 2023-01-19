effects = {

    "avenue pulse red": {
        "length": 1,
        "beats": [
            [1, "Red bottom", .5, 0, 1],
            [1.5, "Red bottom", .5, 1, 0],
        ],
    },

    "avenue pulse colors": {
        "length": 8,
        "beats": [
            [1, "avenue pulse red", 1, 1, 1, 0, 0],
            [2, "avenue pulse red", 1, 1, 1, 0, .125],
            [3, "avenue pulse red", 1, 1, 1, 0, .25],
            [4, "avenue pulse red", 1, 1, 1, 0, .375],
            [5, "avenue pulse red", 1, 1, 1, 0, .5],
            [6, "avenue pulse red", 1, 1, 1, 0, .625],
            [7, "avenue pulse red", 1, 1, 1, 0, .75],
            [8, "avenue pulse red", 1, 1, 1, 0, .875],
        ],
    },

    "Avenue": {
        "bpm": 128,
        "song_path": "songs/Avenue.ogg",
        "delay_lights": 0.09605,
        "skip_song": 0.0,
        "not_done": True,
        "beats": [
            [1, "avenue pulse colors", 50],
        ]
    }
}