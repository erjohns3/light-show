from effects.compiler import b

effects = {
    "dayglow kicks": {
        "length": 4,
        "beats": [
            b(2, name='Purple bottom', length=1, intensity=(1,0)),
            b(4, name='Green bottom', length=1, intensity=(1,0)),
        ],
    },

    "dayglow slow laser": {
        "length": 1,
        "beats": [
            b(1, name='laser motor', length=1, intensity=.2),
            b(1, name='green laser', length=1),
        ],
    },

    "dayglow guitar": {
        "length": 8,
        "beats": [
            b(1.5, name='Purple top', length=.3, intensity=(1, .6)),
            b(2, name='Green top', length=.3, intensity=(1, .6)),
            b(3, name='Yellow top', length=.3, intensity=(1, .6)),
            b(4, name='Red top', length=.3, intensity=(1, .6)),
            b(5, name='Yellow top', length=.3, intensity=(1, .6)),
            b(6, name='Green top', length=.3, intensity=(1, .6)),
            b(7, name='Purple top', length=.3, intensity=(1, .6)),
            b(7.5, name='Red top', length=.3, intensity=(1, .6)),
            b(8.5, name='Green top', length=.3, intensity=(1, .6)),
        ],
    },


    "dayglow full chorus": {
        "length": 32,
        "beats": [
            b(1, name='dayglow kicks', length=32),
            b(1, name='dayglow guitar', length=32),
        ],
    },

    "dayglow fade blue red bottom": {
        "length": 8,
        "beats": [
            b(1, 'Blue bottom', length=.9, intensity=(1, 0)),
            b(1.1, 'Red bottom', length=.9, intensity=(0, 1)),
            b(2, 'Red bottom', length=2.2, intensity=(1, 0)),
        ],
    },
    "dayglow breakdown": {
        "length": 8.5,
        "beats": [
            b(1, name='dayglow fade blue red bottom', length=1.9),
            b(2.9, name='Green bottom', length=1),
        ],
    },

    "dayglow_close_to_you": {
        "bpm": 140,
        "delay_lights": 0.1,
        "skip_song": 0.0,
        "beats": [
            b(5, name='dayglow kicks', length=64),
            b(21, name='dayglow guitar', length=96),
            b(117, name='dayglow slow laser', length=32),
            b(181, name='dayglow full chorus', length=64),
            b(245, name='RBBB 1 bar', length=63),
            b(253, name='dayglow kicks', length=55),
            b(308.5, name='dayglow breakdown', length=8.5),
            b(317, name='dayglow full chorus', length=32),
        ],
        "song_path": "songs/Dayglow - Close to You (Official Video).ogg",
        "length": 458,
    },
}