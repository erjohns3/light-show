from effects.compiler import b, grid_f

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
            b(3.5, name='chain green laser and sidechain all else', length=.4),
            b(11.5, name='chain green laser and sidechain all else', length=.3),
            b(16.7, name='chain green laser and sidechain all else', length=.2),
        ]
    },


    "chain chorus drums loop": {
        'length': 16,
        "beats": [
            b(1, name='Red bottom', length=1, intensity=(.6, 0)),
            b(3, name='UV', length=1, intensity=(1, 0)),
            b(4, name='Red bottom', length=1, intensity=(.6, 0)),
            b(6, name='Red bottom', length=1, intensity=(.6, 0)),
            b(7, name='UV', length=1, intensity=(1, 0)),
            b(1 + 8, name='Red bottom', length=1, intensity=(.6, 0)),
            b(2.5 + 8, name='Red bottom', length=1, intensity=(1, 0)),
            b(3 + 8, name='UV', length=1, intensity=(1, 0)),
            b(4 + 8, name='Red bottom', length=1, intensity=(.6, 0)),
            b(5.5 + 8, name='Red bottom', length=1, intensity=(1, 0)),
            b(6 + 8, name='Red bottom', length=1, intensity=(.6, 0)),
            b(7 + 8, name='UV', length=1, intensity=(1, 0)),

        ]
    },
    "chain chorus drums": {
        'length': 16,
        "beats": [
            b(1, name='chain chorus drums loop', length=16),
        ]
    },

    "chain chorus ending 2": {
        'length': 64,
        "beats": [
            b(61, name='Red disco', length=.12),
            b(61.5, name='Red disco', length=.12),
            b(62, name='Red disco', length=.12),
            b(62.5, name='Green disco', length=.12),
            b(63, name='Blue disco', length=.12),
            b(63.5, name='Red disco', length=.12),
            b(63.5, name='Blue disco', length=.12),
            b(64, name='Green disco', length=.12),
            b(64, name='Blue disco', length=.12),
            b(64.5, name='Red disco', length=.12),        
            b(64.5, name='Blue disco', length=.12),        
            b(64.5, name='Green disco', length=.12),        
        ],
    },
    "chain chorus sidechain and lasers": {
        'length': 64,
        "beats": [
            b(1, name='laser motor', length=64),
            b(1, name='chain chorus 16 bar sidechain', length=16),
            b(19.5, name='chain green laser and sidechain all else', length=.1),

            # triplets
            b(26, name='chain green laser and sidechain all else', length=.3),
            b(26.5, name='chain green laser and sidechain all else', length=.3),
            b(27, name='chain green laser and sidechain all else', length=.5),
            b(29, name='chain green laser and sidechain all else', length=.3),
            b(29.5, name='chain green laser and sidechain all else', length=.3),
            b(30, name='chain green laser and sidechain all else', length=.5),

            # next phrase
            b(33, name='chain chorus 16 bar sidechain', length=16),
            b(19.5 + 32, name='chain green laser and sidechain all else', length=.1),

            b(26 + 32, name='chain green laser and sidechain all else', length=.3),
            b(27 + 32, name='chain green laser and sidechain all else', length=.3),
        ]
    },

    "chain chorus": {
        'length': 128,
        "beats": [
            b(1, name='chain chorus sidechain and lasers', length=112),
            b(1, name='chain chorus drums', length=64, hue_shift=-.06),
            b(61, name='chain singing', length=68),
            b(65, name='chain chorus drums', length=64, hue_shift=.06),
            b(65, name='chain chorus ending 2', length=64),

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

    "Chain helper white top pulse": {
        "length": 8,
        "beats": [
            [3, "White top", .4, .6, 0],
            [7, "White top", .4, .6, 0],
        ],
    },

    "chain top pulse": {
        "length": 8,
        "autogen": "downbeat top",
        "intensity": "low",
        # "profiles": ["Andrew"],
        "beats": [
            [1, "Chain helper white top pulse", 8],
            [1, "Green top", 3.7, .4, 0],
            [1, "Red top", 2.66, 0, .6],
            [3.66, "Red top", 3.7, .6, 0],
            [3.66, "Blue top", 2.66, 0, .6],
            [6.32, "Blue top", 3.7, .6, 0],
            [6.32, "Green top", 2.66, 0, .4],
        ],
    },


    "The Chainsmokers - All We Know ft. Phoebe Ryan (Virtual Riot Remix)": {
        "bpm": 175,
        "song_path": "songs/The Chainsmokers - All We Know ft. Phoebe Ryan (Virtual Riot Remix).ogg",
        "delay_lights": 0.017595,
        "skip_song": 0.0,
        "beats": [
            b(5, name='chain top pulse', length=64),
            b(69, name='chain top pulse', length=48, hue_shift=.1),
            
            b(133, name='Red top', length=48, hue_shift=.1),

            b(197, name='Blue top', length=48, hue_shift=.1),

            b(228, name='laser motor', length=17),
            b(229, name='chain laser', length=16),

            b(244, name='laser motor', length=9),
            b(245, name='chain laser 2 beat', length=8),
            b(245, name='chain disco strobe through', length=8),
            
            
            b(261, name='chain chorus', length=128),
            b(645, name='chain chorus', length=128),
        ]
    },
}