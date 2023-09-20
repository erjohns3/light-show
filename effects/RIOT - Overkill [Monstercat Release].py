from effects.compiler import *

effects = {
    "over - Red quarters": {
        'length': 0.5,
        'beats': [b(1, name='Red top', length=.25)]
    },
    "over - Blue quarters": {
        'length': 0.5,
        'beats': [b(1, name='Blue top', length=.25)]
    },
    "over - Green quarters": {
        'length': 0.5,
        'beats': [b(1, name='Green top', length=.25)]
    },

    "over - Blue bottom eighths": {
        'length': 0.25,
        'beats': [b(1, name='Blue bottom', length=.125)]
    },

    "over - drum eighths": {
        'length': 8,
        'beats': [
            b(1, name='over - Blue bottom eighths', length=.75),
            b(2.5, name='over - Blue bottom eighths', length=.75),
        ]
    },

    "RIOT - Overkill [Monstercat Release]": {
        "bpm": 174,
        "song_path": "songs/RIOT - Overkill [Monstercat Release].ogg",
        "delay_lights": -0.3435,
        "skip_song": 0.0,
        "beats": [
            b(16, name='over - Red quarters', length=64),
            b(80, name='over - Blue quarters', length=64),
            b(144, name='over - Green quarters', length=64),

            b(176, name='over - drum eighths', length=32),

            b(208, name='over - Red quarters', length=32),

            b(240, name='over - Blue quarters', length=32),


            b(240, name='over - Blue quarters', length=28),

            # women: "kill them all"
            b(268, name='Green top', length=4),
            
            # breakdown before drop
            b(272, name='over - Blue quarters', length=28),
            
            # man: "kill them all"
            b(300, name='Green top', length=4),

            # drop
            b(304, name='over - Blue quarters', length=32),

            # b(238.79, name='Red top', length=1),
            # b(270.75, name='Blue top', length=1),
            # b(294.75, name='Green top', length=1),
            # b(298.88, name='Red top', length=1),
            # b(300.38, name='Blue top', length=1),
            # b(301.75, name='Green top', length=1),
            # b(322.79, name='Red top', length=1),
            # b(325.75, name='Blue top', length=1),
        ]
    }
}