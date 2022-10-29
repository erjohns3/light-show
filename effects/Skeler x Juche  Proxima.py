from effects.compiler import b

effects = {
    "Skeler x Juche  Proxima": {
        "bpm": 130,
        "song_path": "songs/Skeler x Juche  Proxima.ogg",
        "delay_lights": -0.0,
        "skip_song": 0.0,
        "beats": [
            [17, 'proxima bassline fixed', 65],
            [81, 'UV', 60],
            [113, 'proxima bass loop', 28],
            [129.5, 'proxima bass loop', 11],
            [137.25, 'proxima bass loop', 3],
            [137.75, 'proxima bass loop', 3],
            [143, 'Blue bottom', 1, 1, 0],
            [145, 'green laser', 128],
            [145, 'proxima laser motor', 128],
            [145, 'proxima bassline fixed', 128],
            [209, 'green laser', 4.5, -1],
            [273, 'UV', 60],
            [305, 'proxima bass loop', 28],
            [321.5, 'proxima bass loop', 11],
            [329.25, 'proxima bass loop', 3],
            [329.75, 'proxima bass loop', 3],
            [337, 'proxima disco loop', 59],
            [401, 'proxima bassline fixed', 192],
            [405.5, 'green laser', 59.5],
            [405.5, 'proxima laser motor', 59.5],
        ]
    },

    "proxima laser motor": {
        "length": 1,
        "beats": [
            [1, 'laser motor', 0.25],
        ]
    },

    "proxima disco loop": {
        "length": 2,
        "beats": [
            [1, 'Green disco', 1],
            [2, 'Blue disco', 1],
        ]
    },

    "proxima bassline": {
        "length": 16,
        "beats": [
            [1, 'proxima bass'],
            [3, 'proxima snare'],
            [5.5, 'proxima bass'],
            [6, 'proxima bass'],
            [7, 'proxima snare'],
            [9, 'proxima bass'],
            [11, 'proxima snare'],
            [12, 'proxima bass'],
            [13.5, 'proxima bass'],
            [13.75, 'proxima bass'],
            [14, 'proxima bass'],
            [15, 'proxima snare'],
        ]
    },

    "proxima bassline fixed": {
        "length": 64,
        "beats": [
            [1, 'proxima bassline', 64],
            [34.5, 'proxima bass'],
            [41, 'proxima bass', 1, -1],
            [42, 'proxima bass'],
        ]
    },

    "proxima bass": {
        "length": 1,
        "loop": False,
        "beats": [
            [1, 'Green bottom', 1, 1, 0],
            
        ]
    },

    "proxima bass loop": {
        "beats": [
            [1, 'proxima bass'],
        ]
    },

    "proxima snare": {
        "length": 1,
        "loop": False,
        "beats": [
            [1, 'Blue top', 1, 1, 0],
        ]
    },
}