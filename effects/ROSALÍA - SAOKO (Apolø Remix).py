from effects.compiler import *

effects = {
    "saoko verse" : {
        "length": 4,
        "beats": [
            b(1, name='UV pulse', length=4),
        ],
    },
    "saoko bass" : {
        "length": 4,
        "beats": [
            b(1, name='Red bottom', length=1.5, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),
            b(2.75, name='Purple bottom', length=0.75, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),
            b(3.75, name='Red bottom', length=0.75, hue_shift=.85, sat_shift=-.25, intensity=(1,0)),        
        ],
    },
    "ROSALÍA - SAOKO (Apolø Remix)": {
        "bpm": 118,
        "song_path": "songs/ROSALÍA - SAOKO (Apolø Remix).ogg",
        "delay_lights": 0.0,
        "skip_song": 0.0,
        "beats": [
            # start
            b(5, name='saoko bass', length=42),
            # 17 chica que dices
            b(17, name='Orange top', length=4),
            #saoko papi
            b(21, name='Yellow top', length=4),
            b(29, name='Red top', length=4),
            # chica que dices
            b(32, name='Orange top', length=4),
            b(37, name='Yellow top', length=4),
            # Verse
            b(49, name='saoko verse', length=42),
            # transformo
            b(81, name='red laser', length=32),
            # quiet moment
            b(113, name='saoko bass', length=42),
            # go go go go 
            b(129, name='UV pulse', length=15),
            # quiet moment
            b(145, name='Orange top', length=15),
            # que algo
            b(161, name='Yellow top', length=4),
            # bump
            b(176, name='saoko verse', length=8),
            # 
            b(193, name='Orange top', length=8),
            # bump
            b(209, name='Yellow top', length=8),
            #
            b(225, name='Red top', length=8),
            #end
            b(241, name='Orange top', length=8),
        ]
    }
}