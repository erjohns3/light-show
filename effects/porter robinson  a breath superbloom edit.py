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
            [1, 'porter flubs 1', 6],
            [7, 'porter flubs 2', 2],
            [9, 'porter flubs 1', 6],
            [15, 'porter flubs 3', 2],
        ],
    },
    'porter flubs phrase rotating': {
        'beats': [
            [1, 'porter flubs phrase', 16, 1, 1, 0, .2],
            [17, 'porter flubs phrase', 16, 1, 1, 0, .4],
            [33, 'porter flubs phrase', 16, 1, 1, 0, .6],
            [49, 'porter flubs phrase', 16, 1, 1, 0, .8],
        ],
    },
    'porter piano melody': {
        'length': 32,
        'beats': [
            [1, 'Seafoam bottom', 7, 1, 0],
            [9, 'Seafoam bottom', 4, 1, 0],
            [13, 'Seafoam bottom', 4, 1, 0, 0, 0, -.6],
            [15, 'Seafoam bottom', 2, 1, 0, 0, 0, -.2],
            [17, 'Seafoam bottom', 4, 1, 0],
            [21, 'Seafoam bottom', 4, 1, 0],
            [25, 'Seafoam bottom', 4, 1, 0],
            [29, 'Seafoam bottom', 2, 1, 0, 0, 0, -.6],
            [31, 'Seafoam bottom', 2, 1, 0, 0, 0, -.2],
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
            # [14, 'Seafoam top', 2, 1, 0],
            # [7, 'Blue top', 3, 1, 0],
            # [9, 'Blue top', 4, 1, 0],
            # [13, 'Blue bottom', 4, 1, 0],
            # [15, 'Blue bottom', 2, 1, 0],
            # [17, 'Blue bottom', 4, 1, 0],
            # [21, 'Blue bottom', 4, 1, 0],
            # [25, 'Blue bottom', 4, 1, 0],
            # [29, 'Blue bottom', 2, 1, 0],
            # [31, 'Blue bottom', 2, 1, 0],
        ],
    },
    'porter robinson  a breath superbloom edit show': {
        'bpm': 126,
        'song_path': 'songs/porter robinson  a breath superbloom edit.ogg',
        'delay_lights': 0.12,
        'skip_song': 0.0,
        'beats': [
            [1, 'porter flubs phrase rotating', 80],
            [17, 'porter piano melody', 32],
            [49, 'porter piano melody', 32, 1, 1, 0, .15],
            [81, 'porter high melody', 64],
            [81, 'porter piano melody', 32, 1, 1, 0, .45, -.2],
            [113, 'porter piano melody', 32],
            # [81, 'Red top', 1],
            [145, 'Red top', 1], # kicks
        ],
    }
}