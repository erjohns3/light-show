from effects.compiler import *

effects = {
    # 'porter flubs complicated': {
    #     'length': 2,
    #     'beats': [
    #         [1, 'Cyan top', 0.2],
    #         [1.45, 'Green bottom', 0.2],
    #         [1.7, 'Cyan top', 0.2],
    #         [2.2, 'Green bottom', 0.2],
    #         [2.5, 'Cyan top', 0.2],
    #     ],
    # },
    'porter flubs 1': {
        'length': 2,
        'beats': [
            [1, 'Cyan front', 0.2, .3, .3],
            [1.7, 'Red back', 0.2, .3, .3],
            [2.5, 'Cyan front', 0.2, .3, .3],
        ],
    },
    'porter flubs 2': {
        'length': 2,
        'beats': [
            [1, 'Cyan front', 0.2, .3, .3],
            [1.7, 'Red back', 0.2, .3, .3],
            [2.5, 'Yellow top', 0.2],
        ],
    },
    'porter flubs 3': {
        'length': 2,
        'beats': [
            [1, 'Cyan front', 0.2, .3, .3],
            [2, 'Green front', 0.1, .2, .2],
            [2.2, 'Green back', 0.1, .2, .2],
            [2.4, 'Green front', 0.1, .2, .2],
        ],
    },
    'porter flubs phrase': {
        'length': 16,
        'beats': [
            b(1, name='porter flubs 1', length=6),
            b(7, name='porter flubs 2', length=2),
            b(9, name='porter flubs 1', length=6),
            b(15, name='porter flubs 3', length=2),
        ],
    },
    'porter flubs phrase rotating': {
        'beats': [
            b(1, name='porter flubs phrase', length=16, hue_shift=.2),
            b(17, name='porter flubs phrase', length=16, hue_shift=.4),
            b(33, name='porter flubs phrase', length=16, hue_shift=.6),
            b(49, name='porter flubs phrase', length=16, hue_shift=.8),
        ],
    },
    'porter piano melody': {
        'length': 32,
        'beats': [
            # b(1, name='Seafoam bottom', length=7, intensity=),
            b(1, 'Seafoam bottom', length=7, intensity=(1, 0)),
            b(9, 'Seafoam bottom', length=4, intensity=(1, 0)),
            b(13, 'Seafoam bottom', length=4, intensity=(1, 0), sat_shift=-.6),
            b(15, 'Seafoam bottom', length=2, intensity=(1, 0), sat_shift=-.2),
            b(17, 'Seafoam bottom', length=4, intensity=(1, 0)),
            b(21, 'Seafoam bottom', length=4, intensity=(1, 0)),
            b(25, 'Seafoam bottom', length=4, intensity=(1, 0)),
            b(29, 'Seafoam bottom', length=2, intensity=(1, 0), sat_shift=-.6),
            b(31, 'Seafoam bottom', length=2, intensity=(1, 0), sat_shift=-.2),
        ],
    },
    'porter high melody': {
        'length': 32,
        'beats': [
            [1, 'Seafoam top', 5, 1, 0],
            [7, 'Seafoam top', 2, 1, 0],
            [9, 'Seafoam top', 3, 1, 0],
            [12, 'Seafoam top', .5, 1, 0],
            [12.5, 'Seafoam top', 4, 1, 0],
            [23, 'Seafoam top', 2, 1, 0],
            [25, 'Seafoam top', 4, 1, 0],
        ],
    },
    'porter robinson  a breath superbloom edit': {
        'bpm': 126,
        'song_path': 'songs/porter robinson  a breath superbloom edit.ogg',
        'delay_lights': 0.12,
        'skip_song': 0.0,
        'beats': [
            b(1, name='porter flubs phrase rotating', length=80),
            b(17, name='porter piano melody', length=32),
            b(49, name='porter piano melody', length=32, hue_shift=.15),
            b(81, name='porter piano melody', length=64),
            b(81, name='porter piano melody', length=32, hue_shift=.45, sat_shift=-.2),
            b(113, name='porter piano melody', length=32),
            # [81, 'Red top', 1],
            [145, 'Red top', 1], # kicks
        ],
    }
}
