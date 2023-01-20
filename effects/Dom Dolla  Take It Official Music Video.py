from effects.compiler import b

effects = {
    "dom sidechain motor halfs": {
        'length': 1,
        "beats": [
            b(1.15, name='Sidechain motor', length=.85),
        ]
    },
    "dom chorus laser": {
        'length': 16,
        'autogen': 'laser long',
        "beats": [
            b(1, name='laser motor', length=16),
            b(1, name='dom sidechain motor halfs', length=16),
            b(1, name='green laser', length=8.5),
            b(13, name='red laser', length=1),
        ]
    },
    "dom chorus": {
        'length': 16,
        'autogen': 'laser long',
        "beats": [
            b(1, name='dom chorus laser', length=16),
            b(10, name='UV pulse', length=3),
            b(14, name='UV pulse', length=3),
        ]
    },
    "dom effect": {
        "length": 2,
        "beats": [
            # [1, 'Pink bottom', .7, 1, 0],
            b(1, name='Pink bottom', length=.7, intensity=(1, 0)),
            b(2, name='Cyan top', length=.8, intensity=(1, .2), bright_shift=-.9),
        ],
    },
    "dom repeated claps": {
        'length': 1,
        "beats": [
            b(1.5, name='Blue bottom', length=.15, intensity=(1, 0)),
            b(1.5, name='Sidechain bottom rg', length=.15, intensity=(1, 0)),
        ]
    },
    "dom chorus 2": {
        "length": 64,
        "beats": [
            b(1, name='dom effect', length=32),
            b(33, name='dom effect', length=32, hue_shift=.5),
            b(33, name='dom repeated claps', length=32),
        ],
    },
    "dom breakdown": {
        'length': 16,
        "beats": [
            b(1, name='dom chorus laser', length=16),
            # b(1, name='RBBB 1 bar', length=16),
            b(10, name='UV pulse', length=3),
            b(14, name='UV pulse', length=3),
        ]
    },
    "dom fade blue red bottom": {
        "length": 8,
        "beats": [
            [1, "Blue bottom", .7, 1, 0],
            [1.1, "Red bottom", .7, 0, 1],
            b(1.8, name='Red bottom', length=7.2, intensity=(1, 0)),
        ],
    },
    "dom windy melody": {
        "length": 16,
        "beats": [
            b(1, name='dom fade blue red bottom', length=5, hue_shift=.1),
            b(6, name='Red bottom', length=1, hue_shift=.35, sat_shift=-.2),
            b(7, name='Red bottom', length=1, hue_shift=.60, sat_shift=-.5),
            b(8, name='Red bottom', length=1, hue_shift=.45, sat_shift=-.2),
            b(9, name='dom fade blue red bottom', length=8, hue_shift=.45),
        ],
    },

    "dom kicks": {
        "length": 4,
        "beats": [
            b(2, name='Red top', length=.2, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),
            b(4, name='Red top', length=.2, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),        
        ],
    },
    "dom intro bassline": {
        "length": 4,
        "beats": [
            b(1, name='Red top', length=1, hue_shift=.1, intensity=(1, 0)),
            b(1, name='dom kicks', length=4),
        ],
    },
    "dom drop sidechain": {
        "length": 8,
        "beats": [
            b(1.1, name='Nothing', length=.2, intensity=1),
            b(1.8, name='Nothing', length=.3, intensity=1),
            b(2.9, name='Nothing', length=.5, intensity=1),
            b(4, name='Nothing', length=.2, intensity=1),
            b(4.7, name='Nothing', length=.2, intensity=1),
            b(5.1, name='Nothing', length=.4, intensity=1),
            b(5.8, name='Nothing', length=.2, intensity=1),
            b(6.2, name='Nothing', length=.2, intensity=1),
            b(6.6, name='Nothing', length=.1, intensity=1),
            b(6.8, name='Nothing', length=.1, intensity=1),
            b(7, name='Nothing', length=.1, intensity=1),
            b(7.2, name='Nothing', length=.3, intensity=1),
            b(7.6, name='Nothing', length=.1, intensity=1),
            b(7.8, name='Nothing', length=.4, intensity=1),
            b(8.5, name='Nothing', length=.5, intensity=1),
        ],
    },
    # "me new": {
    #     "length": 2,
    #     "beats": [
    #         b(-20, name='Red top', length=.2, intensity=1),
    #     ],
    # },
    "Dom Dolla - Take It (Official Music Video)": {
        "bpm": 123,
        "song_path": "songs/Dom Dolla - Take It (Official Music Video).ogg",
        "delay_lights": 0.15150000000000002,
        "skip_song": 0.0,
        "beats": [
            b(16, name='dom windy melody', length=64),
            b(48, name='dom intro bassline', length=32),
            # b(40, name='me new', length=8),
            b(71, name='dom drop sidechain', length=8),
            b(80, name='dom chorus', length=64),
            # b(78.8, name='dom chorus', length=64),
            b(144, name='dom chorus 2', length=64),
            b(200, name='dom drop sidechain', length=8),
            b(207, name='Nothing', length=1),
            b(208, name='dom chorus', length=64),
            b(272, name='UV pulse', length=32),            
            b(304, name='dom windy melody', length=64),
            b(304, name='dom kicks', length=32, hue_shift=.3),
            b(360, name='dom drop sidechain', length=8),
            b(368, name='dom chorus', length=64),
            b(432, name='dom windy melody', length=64),
            b(432, name='dom intro bassline', length=64),
        ]
    }
}