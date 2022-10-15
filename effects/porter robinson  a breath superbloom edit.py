effects = {
    'porter flubs complicated': {
        'length': 2,
        'beats': [
            [1, 'Cyan top', 0.2],
            [1.45, 'Green bottom', 0.2],
            [1.7, 'Cyan top', 0.2],
            [2.2, 'Green bottom', 0.2],
            [2.5, 'Cyan top', 0.2],
        ],
    },
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
    'porter piano melody': {
        'length': 32,
        'beats': [
            [1, 'Seafoam bottom', 7, 1, 0],
            [9, 'Green red bottom', 4, 1, 0],
            [13, 'Green red bottom', 4, 1, 0],
            [15, 'Green red bottom', 2, 1, 0],
            [17, 'Green red bottom', 4, 1, 0],
            [21, 'Seafoam bottom', 4, 1, 0],
            [25, 'Green red bottom', 4, 1, 0],
            [29, 'Green red bottom', 2, 1, 0],
            [31, 'Green red bottom', 2, 1, 0],
        ],
    },
    'porter robinson  a breath superbloom edit show': {
        'bpm': 126,
        'song_path': 'songs/porter robinson  a breath superbloom edit.ogg',
        'delay_lights': 0.12,
        'skip_song': 0.0,
        'beats': [
            [1, 'porter flubs phrase', 128],
            [17, 'porter piano melody', 128],
            [81, 'Red top', 1],
            # [120, 'Red top', 1], bg melody
            [145, 'Red top', 1], # kicks
        ],
    }
}