from effects.compiler import *

effects = {
    "uv boi intro" : {
        "length": 1,
        "beats": [
            b(1, name='Indigo bottom', length=0.5)
        ]
    },
    "uv boi intro kick" : {
        "length": 2,
        "beats": [
            b(1, name='Orange top', length=0.5)
        ]
    },
    "uv boi intro w beats" : {
        "length": 29,
        "beats": [
            b(1, name='Pink bottom', length=1.75),
            b(2.75, name='Indigo bottom', length=0.25),
            b(3, name='Pink bottom', length=2),
            b(5, name='Indigo bottom', length=2),
            b(7, name='Pink bottom', length=2),
            b(9, name='Indigo bottom', length=1.75),
            b(10.75, name='Pink bottom', length=0.25),
            b(11, name='Indigo bottom', length=2),
            b(13, name='Red bottom', length=4),
            b(17, name='Pink bottom', length=2),
            b(18.75, name='Indigo bottom', length=0.25),
            b(19, name='Pink bottom', length=2),
            b(21, name='Indigo bottom', length=2),
            b(23, name='Pink bottom', length=2),
            b(25, name='Indigo bottom', length=1.75),
            b(26.75, name='Pink bottom', length=0.25),
            b(27, name='Indigo bottom', length=2)
        ]

    },
    "uv boi verse" : {
        "length": 2,
        "beats": [
            b(1, name='Cyan bottom', length=0.5, intensity=(1, 0)),
            b(1.5, name='Blue bottom', length=0.5, intensity=(0, 1)),
            b(2, name='Indigo bottom', length=0.5, intensity=(1, 0)),
            b(2.5, name='Purple bottom', length=0.5, intensity=(0, 1))
        ]

    },
    "uv boi ratatat" : {
        "length": 2,
        "beats": [
            b(1, name='UV Strobe', length=2)
        ]

    },
    "uv boi chorus1" : {
        "length": 16,
        "beats": [
            b(1, name='Orange bottom', length=2),
            b(3, name='Yellow bottom', length=2),
            b(5, name='Orange bottom', length=2.5),
            b(7.5, name='Cyan bottom', length=4),
            b(11.5, name='Red bottom', length=1),
            b(12.5, name='Orange bottom', length=1),
            b(13, name='Yellow bottom', length=10)
        ]
    },
    "uv boi chorus2" : {
        "length": 16,
        "beats": [
            b(1, name='Orange bottom', length=2),
            b(3, name='Yellow bottom', length=2),
            b(5, name='Orange bottom', length=2),
            b(7, name='Cyan bottom', length=4.5),
            b(11.5, name='Red bottom', length=1),
            b(12.5, name='Orange bottom', length=0.5),
            b(13, name='Yellow bottom', length=10)
        ]
    },
    "uv boi buildup" : {
        "length": 1,
        "beats": [
            b(1, name='Blue top', length=0.5)
        ]
    },
    "ll dom fade blue red bottom": {
        "length": 8,
        "beats": [
            b(1, name='Blue bottom', length=0.7, intensity=(1, 0)),
            b(1.1, name='Red bottom', length=0.7, intensity=(0, 1)),
            b(1.8, name='Red bottom', length=7.2, intensity=(1, 0)),
        ],
    },
    "ll dom windy melody": {
        "length": 2,
        "beats": [
            b(1, name='ll dom fade blue red bottom', length=5, hue_shift=.1),
            b(6, name='Red bottom', length=1, hue_shift=.35, sat_shift=-.2),
            b(7, name='Red bottom', length=1, hue_shift=.60, sat_shift=-.5),
            b(8, name='Red bottom', length=1, hue_shift=.45, sat_shift=-.2),
            b(9, name='ll dom fade blue red bottom', length=8, hue_shift=.45),
        ],
    },
    "UV boi فوق بنفسجي - Show You (ft. MTNS)": {
        "bpm": 93,
        "song_path": "songs/UV boi فوق بنفسجي - Show You (ft. MTNS).ogg",
        "delay_lights": 0.05,
        "skip_song": 0.0,
        "beats": [
            b(5, name='uv boi intro', length=14),
            b(12, name='Orange top', length=2),
            b(22, name='uv boi intro kick', length=30),
            b(23, name='uv boi intro w beats', length=29),
            b(51, name='ll dom windy melody', length=63),
            b(85, name='uv boi buildup', length=14),
            b(101, name='uv boi buildup', length=14),
            b(117, name='uv boi ratatat', length=2),
            b(119, name='uv boi chorus1', length=16),
            b(135, name='uv boi chorus2', length=16),
            b(155, name='uv boi ratatat', length=2),
            b(157, name='uv boi chorus2', length=16)
        ]
    }
}