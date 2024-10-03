from effects.compiler import *

effects = {

    "Random color 1": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[10, 40, 10], length=1),
        ],
    },

    "Random color 2": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[0, 10, 40], length=1),
        ],
    },

    "Random color 3": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[40, 0, 10], length=1),
        ],
    },

    "Triplets top": {
        "length": 1,
        "beats": [
            b(1, "Random color 1", 0.33, intensity=(0.3, 0.2)),
            b(1.33, "Random color 2", 0.33, intensity=(0.3, 0.2)),
            b(1.66, "Random color 3", 0.33, intensity=(0.3, 0.2)),
        ],
    },

    "Random color 4": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[30, 30, 0], length=1),
        ],
    },

    "Yellow fade": {
        "length": 1,
        "beats": [
            b(1, "Random color 4", 1, intensity=(1, 0)),
        ],
    },

    "Random color 5": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[0, 25, 0], length=1),
        ],
    },
    "Green fade": {
        "length": 2,
        "beats": [
            b(2, "Random color 5", 0.55, intensity=(1, 0.5)),
        ],
    },


    "Random color 6": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[-30, -30, -30], length=1),
        ],
    },
    "shelter bottom sidechain": {
        "length": 1,
        "beats": [
            b(1, "Random color 6", .1, intensity=(1, .5)),
            b(1.1, "Random color 6", 0.9, intensity=(.5, 0)),
        ],
    },

    "Random color 7": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[0, 0, 255], length=1),
        ],
    },
    "top blue kick": {
        "length": 1,
        "beats": [
            b(1, "Random color 7", 0.1, intensity=(0, 0.4)),
            b(1.1, "Random color 7", 1, intensity=(0.4, 0.1)),
        ],
    },

    "Random color 8": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[114, 60, 5], length=1),
        ],
    },
    "muddy yellow ay": {
        "length": 1,
        "beats": [
            b(1, "Random color 8", 1, intensity=(0.4, 0)),
        ],
    },


    "Triplets bottom": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[10, 40, 0], length=0.33),
            b(1.33, bottom_rgb=[0, 10, 40], length=0.33),
            b(1.66, bottom_rgb=[40, 0, 10], length=0.33),
        ],
    },

    "Chorus bottom": {
        "length": 3,
        "beats": [
            b(1, "Cyan bottom", 1, intensity=(0.25, 0.25)),
            b(2, "Yellow bottom", 1, intensity=(0.25, 0.25)),
            b(3, "Pink bottom", 1, intensity=(0.35, 0.35)),
        ],
    },
    "Shelter sub Chorus": {
        "length": 16,
        "beats": [
            b(1, "shelter bottom sidechain", 12),
            b(1, "muddy yellow ay", 1),
            b(1, "Chorus bottom", 3),
            b(2, "top blue kick", 2),
            b(5, "muddy yellow ay", 1), 
            b(5, "Chorus bottom", 3),
            b(6, "top blue kick", 2),
            b(9, "muddy yellow ay", 1), 
            b(9, "Chorus bottom", 3),
            b(10, "top blue kick", 2),
            b(13, "Triplets bottom", 4),
        ],
    },
    "Shelter Chorus": {
        "length": 32,
        "beats": [
            b(1, "Shelter sub Chorus", 32),
        ],
    },

    "shelter rising uh uh uh uh": {
        "length": 4,
        "beats": [
            b(1, "Cyan top", 1, intensity=(0.1, 0.1)),
            b(2, "Cyan top", 1, intensity=(0.15, 0.15)),
            b(3, "Cyan top", 1, intensity=(0.2, 0.2)),
            b(4, "Cyan top", 1, intensity=(0.25, 0.25)),
        ],
    },
    "shelter green bottom": {
        "length": 1,
        "beats": [
            b(1, "Green bottom", 1, intensity=(0.1, 0.1)),
        ],
    },
    "shelter tambos": {
        "length": 2,
        "beats": [
            b(2, "Indigo bottom", .3, intensity=(0.3, 0.1)),
        ],
    },
    "rainbow good top": {
        "length": 8,
        "beats": [
            b(1, "Green top", 3.7, intensity=(1, 0)),
            b(1, "Red top", 2.66, intensity=(0, 1)),
            b(3.66, "Red top", 3.7, intensity=(1, 0)),
            b(3.66, "Blue top", 2.66, intensity=(0, 1)),
            b(6.32, "Blue top", 3.7, intensity=(1, 0)),
            b(6.32, "Green top", 2.66, intensity=(0, 1)),
        ],
    },
    "rainbow good slow top": {
        "length": 16,
        "autogen": True,
        "beats": [
            b(1, "Green top", 7.3, intensity=(1, 0)),
            b(1, "Red top", 5.3, intensity=(0, 1)),
            b(6.3, "Red top", 7.3, intensity=(1, 0)),
            b(6.3, "Blue top", 5.3, intensity=(0, 1)),
            b(11.6, "Blue top", 7.3, intensity=(1, 0)),
            b(11.6, "Green top", 5.4, intensity=(0, 1)),
        ],
    },
    "shelter drum build": {
        "length": 3,
        "beats": [
            b(2, "Green top", .05),
            b(2.1, "Green top", .05),
            b(2.2, "Green top", .08),
            # [2.25, "Green top", .05],
            b(2.45, "Green top", .05),
            b(2.7, "Green top", .05),
            b(2.95, "Green top", .05),
            b(3.22, "Green top", .05),
        ],
    },
    "shelter": {
        "beats": [
            b(1, "muddy yellow ay", 1),
            b(5, "muddy yellow ay", 1),
            b(9, "muddy yellow ay", 1),
            b(13, "shelter rising uh uh uh uh", 4),
            b(17, "shelter tambos", 12),
            b(17, "muddy yellow ay", 1),
            b(21, "muddy yellow ay", 1),
            b(25, "muddy yellow ay", 1),
            b(29, "UV", 4),
            b(29, "shelter rising uh uh uh uh", 4),
            b(33, "Shelter Chorus", 32),
            b(61, "Triplets bottom", 4),
            b(73, "Pulse", 8, 0.2, 0.2),
            b(81, "Yellow fade", 1),
            b(82, "Pulse", 15, 0.2, 0.2),
            b(97, "rainbow good top", 24),
            b(97, "Green fade", 16),
            b(113, "shelter tambos", 8),
            b(121, "UV", 6),
            b(126, "shelter drum build", 3),
            b(129, "Shelter Chorus", 64),
            b(161, "UV pulse slow", 32),
            b(193, "rainbow good top", 56),
            b(225, "Green fade", 24),
            b(249, "UV pulse slow", 6),
            b(257, "Pulse", 12, 0.2, 0.2),
            b(257, "shelter tambos", 28),
            b(269, "shelter rising uh uh uh uh", 4),
            b(273, "Pulse", 12, 0.2, 0.2),
            b(285, "UV Strobe", 1.7, .1, 1),
            b(286.7, "UV Strobe", 2.3, 1, 0),
            b(289, "Shelter Chorus", 32),
            b(321, 'grid color pulse .3', 24),
            b(321, '5 hours box combine color 2', 24),
        ],
        "delay_lights": 0.1,
        "skip_song": 0.21,
        "bpm": 100,
        "song_path": "songs/Porter Robinson & Madeon - Shelter (Official Audio).ogg",
        "profiles": ["Shows"],
    },
}
