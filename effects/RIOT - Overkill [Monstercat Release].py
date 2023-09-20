from effects.compiler import *

effects = {
    "Red quarters": {
        'length': 0.5,
        'beats': [
            b(1, name='Red top', length=.25),
        ]
    },

    "RIOT - Overkill [Monstercat Release]": {
        "bpm": 174,
        "song_path": "songs/RIOT - Overkill [Monstercat Release].ogg",
        "delay_lights": -0.2435,
        "skip_song": 0.0,
        "beats": [
            b(16, name='Red quarters', length=32),
            # b(78.92, name='Blue top', length=1),
            # b(111.04, name='Green top', length=1),
            # b(105.46, name='Red top', length=1),
            # b(144.58, name='Blue top', length=1),
            # b(143.96, name='Green top', length=1),
            # b(175.12, name='Red top', length=1),
            # b(183.12, name='Blue top', length=1),
            # b(190.79, name='Green top', length=1),
            # b(198.96, name='Red top', length=1),
            # b(206.92, name='Blue top', length=1),
            # b(231.29, name='Green top', length=1),
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