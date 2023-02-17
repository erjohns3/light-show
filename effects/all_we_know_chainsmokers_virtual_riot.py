from effects.compiler import b

# python light_server.py --local --keyboard --show "g_The Chainsmokers - All We Know ft. Phoebe Ryan" --delay .189
effects = {
    "chain green laser and sidechain all else": {
        'length': 1,
        "beats": [
            b(1, name='green laser', length=1),
            b(1, name='Sidechain all but laser', length=1),
        ]
    },


    "chain sing stepping 1": {
        'length': 8,
        "beats": [
            b(1, name='Red top', length=1.5, hue_shift=.05, intensity=(1, 0)),
            b(2, name='Red top', length=1.5, hue_shift=.05, intensity=(1, 0)),
            b(3, name='Red top', length=1.5, hue_shift=.05, intensity=(1, 0)),
            b(4, name='Red top', length=1.5, hue_shift=.07, intensity=(1, 0)),
            b(5, name='Red top', length=1.5, hue_shift=.13, intensity=(1, 0)),
            b(6, name='Red top', length=1.5, hue_shift=.10, intensity=(1, 0)),
            b(7, name='Red top', length=1.5, hue_shift=.07, intensity=(1, 0)),
        ]
    },

    "chain sing stepping 2": {
        'length': 8,
        "beats": [
            b(1, name='Red top', length=1.5, hue_shift=.05, intensity=(1, 0)),
            b(2, name='Red top', length=1.5, hue_shift=.05, intensity=(1, 0)),
            b(3, name='Red top', length=1.5, hue_shift=.08, intensity=(1, 0)),
            b(4, name='Red top', length=1.5, hue_shift=.12, intensity=(1, 0)),
            b(5, name='Red top', length=1.5, hue_shift=.08, intensity=(1, 0)),
            b(6, name='Red top', length=1.5, hue_shift=.12, intensity=(1, 0)),
            b(7, name='Red top', length=1.5, hue_shift=.12, intensity=(1, 0)),
            b(7.2, name='Red top', length=1.1, hue_shift=.2, intensity=(0, 1)),
            b(8, name='Red top', length=2, hue_shift=.2, intensity=(1, 0)),
        ]
    },

    "chain singing": {
        'length': 68,
        "beats": [
            b(2, name='chain sing stepping 1', length=8, hue_shift=0),
            b(9, name='Red top', length=2.2, hue_shift=.05, intensity=(1, 0)),
            b(11, name='chain sing stepping 2', length=8, hue_shift=.2),
            b(19, name='chain sing stepping 1', length=8, hue_shift=.4),
            b(27, name='chain sing stepping 2', length=8, hue_shift=.49),
            b(35, name='chain sing stepping 1', length=8, hue_shift=.62),
            b(43, name='chain sing stepping 2', length=8, hue_shift=.71),
            b(50, name='chain sing stepping 1', length=7, hue_shift=.62),
            b(56, name='Red top', length=4.2, hue_shift=.7, intensity=(1, .4)),
            b(58, name='Red top', length=4, hue_shift=.8, intensity=(0, .3)),
            b(59, name='Red top', length=4.5, hue_shift=.9, intensity=(0, .3)),
            b(60, name='Red top', length=3, hue_shift=.9, intensity=(0, .3)),
        ]
    },


    "chain chorus 16 bar sidechain": {
        'length': 16,
        "beats": [
            b(3, name='chain green laser and sidechain all else', length=.4),
            b(11.5, name='chain green laser and sidechain all else', length=.3),
            b(16.6, name='chain green laser and sidechain all else', length=.2),
        ]
    },
    "chain chorus": {
        'length': 64,
        "beats": [
            b(1, name='laser motor', length=32),
            b(1, name='chain chorus 16 bar sidechain', length=16),
            b(19.5, name='chain green laser and sidechain all else', length=.1),
            # b(23.7, name='chain green laser and sidechain all else', length=.15),
            b(26, name='chain green laser and sidechain all else', length=.4),
            # b(33, name='chain chorus 16 bar sidechain', length=16),


            # ending beats
            b(62, name='Red disco', length=.05),
            b(62.5, name='Green disco', length=.05),
            b(63, name='Blue disco', length=.05),
            b(63.5, name='Red disco', length=.05),
            b(64, name='Green disco', length=.05),
            b(64.5, name='Red disco', length=.05),
        ]
    },



    "chain sidechain laser stuff": {
        'length': 1,
        "beats": [
            b(1.12, name='Sidechain motor', length=.5),
            b(1.25, name='Sidechain laser', length=.75),
        ]
    },
    "chain laser": {
        'length': 16,
        "beats": [
            b(1, name='chain sidechain laser stuff', length=16),
            b(1, name='green laser', length=16),
        ]
    },

    "chain laser 2 beat": {
        'length': 2,
        "beats": [
            b(1, name='chain sidechain laser stuff', length=2),
            b(1, name='green laser', length=1),
        ]
    },

    "chain disco strobe through": {
        'length': 8,
        "beats": [
            b(2, name='Green disco', length=.3),
            b(2.5, name='Red disco', length=.3),

            b(4, name='Green disco', length=.3),
            b(4.5, name='Blue disco', length=.3),

            b(6, name='Green disco', length=.3),
            b(6.5, name='Blue disco', length=.3),
            b(6.5, name='Red disco', length=.3),


            b(8, name='Red disco', length=.05),
            b(8.1, name='Green disco', length=.05),
            b(8.2, name='Blue disco', length=.05),
            b(8.3, name='Red disco', length=.05),
            b(8.4, name='Green disco', length=.05),
            b(8.5, name='Red disco', length=.05),
            b(8.6, name='Red disco', length=.05),

            # b(1, name='disco strobe', length=2),
            # b(1, name='green laser', length=1),
        ]
    },

    "The Chainsmokers - All We Know ft. Phoebe Ryan (Virtual Riot Remix)": {
        "bpm": 175,
        "song_path": "songs/The Chainsmokers - All We Know ft. Phoebe Ryan (Virtual Riot Remix).ogg",
        "delay_lights": 0.017595,
        "skip_song": 0.0,
        "beats": [
            b(5, name='z_rainbow good top pulse 1', length=64),
            b(69, name='z_rainbow good top pulse 2', length=64),
            # b(132, name='laser motor', length=65),
            # b(133, name='chain laser', length=64),
            # b(196, name='laser motor', length=33),
            # b(197, name='chain laser', length=32),
            b(228, name='laser motor', length=17),
            b(229, name='chain laser', length=16),

            b(244, name='laser motor', length=9),
            b(245, name='chain laser 2 beat', length=8),
            b(245, name='chain disco strobe through', length=8),
            
            
            b(261, name='chain chorus', length=64),

            b(321, name='chain singing', length=68),
            b(325, name='chain chorus', length=64),
        ]
    },
}