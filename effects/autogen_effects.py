import grid_helpers
from effects.compiler import *
import random

# [beat, effect, length, start intensity, end intensity, beat skip, hue[-1, 1], sat, brightness]

effects = {
    # "complex grid test": {
    #     "length": 8,
    #     "autogen": "complex grid",
    #     "intensity": "low",
    #     "beats": [
    #         grid_f(
    #             1,
    #             function=our_transform,
    #             object=get_rectangle_numpy(4, 4),
    #             start_pos=(-10, 0),
    #             end_pos=(10, 0),
    #             start_rot = 0,
    #             end_rot = 6.24,
    #             length=8,
    #         ),
    #     ],
    # },


    "autogen test": {
        "length": 8,
        "autogen": "complex grid",
        "intensity": "low",
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_rectangle_numpy(14, 13),
                color=(1, 1, 1),
                start_rot=0,
                end_rot=6.28,
                length=8,
            ),
        ],
    },


    "autogen twinkle": {
        "length": 8,
        "autogen": "complex grid",
        "intensity": "low",
        "beats": [
            *make_twinkle(start_beat=1, length=8, color=GColor.seafoam, twinkle_length=2, num_twinkles=25, twinkle_lower_wait=0.25, twinkle_upper_wait=2),
        ]
    },

    "autogen s circle": {
        "length": 2,
        "autogen": "complex grid",
        "intensity": "low",
        "beats": [
            *get_circle_pulse_beats(start_beat=1, start_color=GColor.red, end_color=GColor.yellow),
        ],
    },

    "autogen s circle 2": {
        "length": 2,
        "autogen": "complex grid",
        "intensity": "low",
        "beats": [
            *get_circle_pulse_beats(start_beat=1, start_color=GColor.blue, end_color=GColor.red),
        ],
    },




    # dimmers
    "z_dimmer all": {
        "length": 1,
        "autogen": "dimmers",
        "beats": [
            [1.5, "Sidechain top 100", .5, 0, .5],
            # [1.5, "Sidechain bottom rbg", .5, 0, .8],
            # [1.5, "Sidechain UV", .5, 0, .8],
        ],
    },
    # fillers
    "z_Strobe": {
        "length": 1,
        "autogen": "strobe",
        "beats": [
            [1, "Strobe", 1],
        ],
    },
    "z_UV Strobe": {
        "length": 1,
        "autogen": "strobe",
        "beats": [
            [1, "UV Strobe", 1],
        ],
    },

    "z_UV": {
        "length": 1,
        "autogen": "UV",
        "beats": [
            [1, "UV", 1],
        ],
    },
    "z_UV pulse": {
        "length": 1,
        "autogen": "UV pulse single",
        "beats": [
            [1, "UV pulse", 1],
        ],
    },

    "z_UV pulse copy": {
        "length": 1,
        "autogen": "UV pulse",
        "beats": [
            [1, "UV pulse", 1],
        ],
    },

    "1_2 UV Pulse": {
        "length": 2,
        "autogen": "UV pulse",
        "beats": [
            [1, "UV pulse", 2],
        ],
    },

    "z_white bottom": {
        "autogen": "filler",
        "length": 1,
        "beats": [
            [1, "White bottom", .9, .7, .1],
        ],
    },


    "z_filler laser 1": {
        "length": 1,
        "autogen": "filler laser",
        "intensity": "high",
        "beats": [
            b(1, "green laser motor", length=1),
        ],
    },

    "z_filler laser 2": {
        "length": 1,
        "autogen": "filler laser",
        "intensity": "high",
        "beats": [
            b(1, "Strobe green laser", length=1),
        ],
    },

    "z_filler 1": {
        "length": 1,
        "autogen": "filler",
        "intensity": "high",
        "beats": [
            [1, "Pink bottom", .25, 1, 0],
            [1.25, "Pink bottom", .25, 1, 0],
            [1.5, "Cyan front", .5, 1, .2],
            [1.5, "Cyan back", .5, 1, .2],
        ],
    },

    "z_filler 2": {
        "length": 2,
        "autogen": "filler",
        "intensity": "high",
        "beats": [
            [1, "Red front", .25, 1, 0],
            [1.25, "Blue back", .25, 1, 0],
            [1.75, "Green bottom", .25, 1, 0],
            [2, "Firebrick top", .75, 1, 0],
            [2, "Firebrick bottom", .75, 1, 0],
        ],
    },

    "z_filler 3": {
        "length": 2,
        "autogen": "filler",
        "intensity": "low",
        "beats": [
            [1, "Pink bottom", .25, 1, 0],
            [2, "Cyan front", .5, 1, .2],
            [2, "Cyan back", .5, 1, .2],
        ],
    },
    

    "Autogen helper white top pulse 1": {
        "length": 4,
        "beats": [
            [1, "White top", .4, .8, 0],
            [3, "White top", .4, .8, 0],
        ],
    },

    "z_rainbow good top pulse 1": {
        "length": 8,
        "autogen": "downbeat top",
        "intensity": "low",
        # "profiles": ["Andrew"],
        "beats": [
            [1, "Autogen helper white top pulse 1", 8],
            [1, "Green top", 3.7, .4, 0],
            [1, "Red top", 2.66, 0, .6],
            [3.66, "Red top", 3.7, .6, 0],
            [3.66, "Blue top", 2.66, 0, .6],
            [6.32, "Blue top", 3.7, .6, 0],
            [6.32, "Green top", 2.66, 0, .4],
        ],
    },
    "Autogen helper white top pulse 2": {
        "length": 4,
        "beats": [
            [2, "White top", .4, 1, 0],
            [4, "White top", .4, 1, 0],
        ],
    },
    "z_rainbow good top pulse 2": {
        "length": 8,
        "autogen": "downbeat top",
        "intensity": "low",
        "beats": [
            [1, "Autogen helper white top pulse 2", 8],
            [1, "Green top", 3.7, .4, 0],
            [1, "Red top", 2.66, 0, .6],
            [3.66, "Red top", 3.7, .6, 0],
            [3.66, "Blue top", 2.66, 0, .6],
            [6.32, "Blue top", 3.7, .6, 0],
            [6.32, "Green top", 2.66, 0, .4],
        ],
    },



    # rainbows
    "z_rainbow good top": {
        "length": 8,
        "autogen": "rainbow top",
        "intensity": "low",
        # "profiles": ["Andrew"],
        "beats": [
            [1, "Green top", 3.7, 1, 0],
            [1, "Red top", 2.66, 0, 1],
            [3.66, "Red top", 3.7, 1, 0],
            [3.66, "Blue top", 2.66, 0, 1],
            [6.32, "Blue top", 3.7, 1, 0],
            [6.32, "Green top", 2.66, 0, 1],
        ],
    },
    "z_rainbow good slow top": {
        "length": 16,
        "intensity": "low",
        "autogen": "rainbow top",
        "beats": [
            [1, "Green top", 7.3, 1, 0],
            [1, "Red top", 5.3, 0, 1],
            [6.3, "Red top", 7.3, 1, 0],
            [6.3, "Blue top", 5.3, 0, 1],
            [11.6, "Blue top", 7.3, 1, 0],
            [11.6, "Green top", 5.4, 0, 1],
        ],
    },

    # misc
    # "Yellow Top to Bottom hang": {
    #     "length": 3,
    #     "beats": [
    #         [1, [100, 30, 5, 0, 25, 0, 0], .2, 0, .5],
    #         [1.2, [100, 30, 5, 0, 25, 0, 0], 1.1, .5, 0],
    #         [1.3, [0, 0, 0, 100, 30, 5, 0], 1.3, 0, .6],
    #         [2.6, [0, 0, 0, 100, 30, 5, 0], 38, .6, .6],
    #     ],
    # },

    # downbeat tops and bottoms
    "z_solid bottom cycle": {
        "length": 4,
        "autogen": "downbeat bottom",
        "beats": [
            [1, "Cyan bottom", .8],
            [1.8, "Cyan bottom", .2, 1, .2],
            [2, "Pink bottom", .8],
            [2.8, "Pink bottom", .2, 1, .2],
            [3, "Yellow bottom", .8],
            [3.8, "Yellow bottom", .2, 1, .2],
            [4, "Green bottom", .8],
            [4.8, "Green bottom", .2, 1, .2],
        ],
    },

    "z_solid bottom cycle down then up": {
        "length": 4,
        "autogen": "downbeat bottom",
        "beats": [
            [1, "Cyan bottom", .3],
            [1.3, "Cyan bottom", .5, 1, .2],
            [1.8, "Cyan bottom", .2, .2, 1],

            [2, "Green bottom", .3],
            [2.3, "Green bottom", .5, 1, .2],
            [2.8, "Green bottom", .2, .2, 1],

            [3, "Pink bottom", .3],
            [3.3, "Pink bottom", .5, 1, .2],
            [3.8, "Pink bottom", .2, .2, 1],

            [4, "Yellow bottom", .3],
            [4.3, "Yellow bottom", .5, 1, .2],
            [4.8, "Yellow bottom", .2, .2, 1],
        ],
    },

    "z_pulse top swap 1": {
        "length": 4,
        "autogen": "downbeat top",
        "beats": [
            [1, "Orange front", .3, 1, 0],
            [2, "Orange back", .3, 1, 0],
            [3, "Green back", .3, 1, 0],
            [4, "Green front", .3, 1, 0],
        ],
    },

    "z_pulse top swap 2": {
        "length": 4,
        "autogen": "downbeat top",
        "beats": [
            [1, "Firebrick back", .3, 1, 0],
            [2, "Firebrick front", .3, 1, 0],
            [3, "Indigo front", .3, 1, 0],
            [4, "Indigo back", .3, 1, 0],
        ],
    },

    #  i think bad
    "z_pulse top swap 3": {
        "length": 2,
        "autogen": "downbeat top",
        "beats": [
            [1, "Pink top", .3, 1, 0],
            [2, "Green front", .3, 1, 0],
            [2.5, "Green back", .3, 1, 0],
        ],
    },


    # andrew i think this sucks
    # "z_solid top cycle 1": {
    #     "length": 4,
    #     "autogen": "downbeat top",
    #     "beats": [
    #         [1, "Firebrick top", 1, .6],
    #         [2, "Pink top", 1],
    #         [3, "Red top", 1, .6],
    #         [4, "Green top", 1, .4],
    #     ],
    # },

    "z_solid top cycle 2": {
        "length": 4,
        "autogen": "downbeat top",
        "beats": [
            [1, "Firebrick top", .5, 1, 0],
            [2, "Pink top", .3],
            [3, "Red top", .3],
            [4, "Green top", .3],
        ],
    },

    "z_solid mixed 1": {
        "length": 4,
        "autogen": "downbeat mixed",
        "beats": [
            [1, "Green top", 1, .2],
            [2, "Pink bottom", .5],
            [2.5, "Firebrick bottom", .5],
            [3, "Green top", 1, .2],
            [4, "Blue bottom", .5],
            [4.5, "Orange bottom", .5],
        ],
    },

    "z_solid mixed 2": {
        "length": 4,
        "autogen": "downbeat mixed",
        "beats": [
            [1, "Blue bottom", 1, 1, .2],
            [2, "Blue bottom", 1, .2, .2],
            [2, "Orange top", .4, .6, 0],
            [2.5, "Yellow top", .4, .6, 0],
            [3, "Blue bottom", 1, 1, .2],
            [4, "Blue bottom", 1, .2, .2],
            [4, "Firebrick top", .4, .6, .6],
            [4.5, "Cyan top", .4, .6, .6],
        ],
    },

    "z_solid mixed 3": {
        "length": 4,
        "autogen": "downbeat mixed",
        "beats": [
            [1, "Blue top", 1, 1, .2],
            [2, "Blue top", 1, .2, .2],
            [2, "Orange bottom", .4, .6, 0],
            [2.5, "Yellow bottom", .4, .6, 0],
            [3, "Blue top", 1, 1, .2],
            [4, "Blue top", 1, .2, .2],
            [4, "Firebrick bottom", .4, .6, 0],
            [4.5, "Cyan bottom", .4, .6, 0],
        ],
    },

    # "z_solid mixed 4": {
    #     "length": 4,
    #     "autogen": "downbeat mixed",
    #     "beats": [
    #         [1, "Yellow Top to Bottom hang", 3],
    #         [2, "Sidechain top b", .5, 1, 0],
    #         [2, "Green bottom", .2, .2, 0],
    #         [3, "Sidechain bottom b", .5, 1, 0],
    #         [3, "Green bottom", .2, .2, 0],
    #         [4, "Blue top", .8, 1, 0],
    #     ],
    # },

    "z_solid mixed cycle": {
        "length": 4,
        "autogen": "downbeat mixed",
        "beats": [
            [1, "Firebrick top", 1],
            [2, "Indigo bottom", 1],
            [3, "Firebrick top", 1],
            [4, "Yellow bottom", 1],
        ],
    },

    "z_cyan top pulse": {
        "length": 1,
        "autogen": "downbeat top",
        "beats": [
            [1, "Cyan top", 1, 0.42, .2],
        ],
    },
    "z_purple purple yellow top pulse": {
        "length": 2,
        "autogen": "downbeat top",
        "beats": [
            [1, "Purple top", 1, 0.42, .2],
            [2, "Yellow top", 1, 0.42, .2],
        ],
    },

    "z_green sidechain top pulse": {
        "length": 2,
        "autogen": "downbeat top",
        "beats": [
            [1, "Green top", 0.1, 0.6, 0.17],
            [1.1, "Green top", 3, 0.17, 0.17],
            [2, "Sidechain top g", 0.5, 1, 0], 
            [2, "Some color top", 0.3, 1, .7],
        ],
    },


    "z_purple green bottom pulse": {
        "length": 2,
        "autogen": "downbeat bottom",
        "beats": [
            [1, "Purple bottom", 1, 0.42, .2],
            [2, "Green bottom", 1, 0.42, .2],
        ],
    },
    "z_green sidechain bottom pulse": {
        "length": 2,
        "autogen": "downbeat bottom",
        "beats": [
            [1, "Green bottom", 0.1, 0.6, 0.17],
            [1.1, "Green bottom", 3, 0.17, 0.17],
            [2, "Sidechain bottom g", 0.5, 1, 0], 
            [2, "Some color bottom", 0.3, 1, .7],
        ],
    },


    # disco
    "z_z_green disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Green disco', length=8),
        ],
    },
    "z_z_red disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Red disco', length=8),
        ],
    },
    "z_z_blue disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Blue disco', length=8),
        ],
    },
    
    "z_z_green_red disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Green disco', length=8),
            b(1, name='Red disco', length=8),
        ],
    },
    "z_z_green_blue disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Green disco', length=8),
            b(1, name='Blue disco', length=8),
        ],
    },

    "z_z_blue_red disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Blue disco', length=8),
            b(1, name='Red disco', length=8),
        ],
    },
    "z_z_blue_green disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Blue disco', length=8),
            b(1, name='Green disco', length=8),
        ],
    },

    "z_z_red_blue disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Red disco', length=8),
            b(1, name='Blue disco', length=8),
        ],
    },
    "z_z_red_green disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Red disco', length=8),
            b(1, name='Green disco', length=8),
        ],
    },

    "z_z_red_green_blue disco": {
        "length": 8,
        "autogen": "disco",
        "beats": [
            b(1, name='Red disco', length=8),
            b(1, name='Green disco', length=8),
            b(1, name='Blue disco', length=8),
        ],
    },


    # disco 2 (strobers)
    "z_z_green disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Green disco pulse', length=8),
        ],
    },
    "z_z_red disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8),
        ],
    },
    "z_z_blue disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Blue disco pulse', length=8),
        ],
    },
    
    "z_z_green_red disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Green disco pulse', length=8),
            b(1, name='Red disco pulse', length=8),
        ],
    },
    "z_z_green_blue disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Green disco pulse', length=8),
            b(1, name='Blue disco pulse', length=8),
        ],
    },

    "z_z_blue_red disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Blue disco pulse', length=8),
            b(1, name='Red disco pulse', length=8),
        ],
    },
    "z_z_blue_green disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Blue disco pulse', length=8),
            b(1, name='Green disco pulse', length=8),
        ],
    },

    "z_z_red_blue disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8),
            b(1, name='Blue disco pulse', length=8),
        ],
    },
    "z_z_red_green disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8),
            b(1, name='Green disco pulse', length=8),
        ],
    },

    "z_z_red_green_blue disco strobe": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8),
            b(1, name='Green disco pulse', length=8),
            b(1, name='Blue disco pulse', length=8),
        ],
    },


    "z_z_green disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Green disco pulse', length=8, offset=.5),
        ],
    },
    "z_z_red disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8, offset=.5),
        ],
    },
    "z_z_blue disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Blue disco pulse', length=8, offset=.5),
        ],
    },
    
    "z_z_green_red disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Green disco pulse', length=8, offset=.5),
            b(1, name='Red disco pulse', length=8, offset=.5),
        ],
    },
    "z_z_green_blue disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Green disco pulse', length=8, offset=.5),
            b(1, name='Blue disco pulse', length=8, offset=.5),
        ],
    },

    "z_z_blue_red disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Blue disco pulse', length=8, offset=.5),
            b(1, name='Red disco pulse', length=8, offset=.5),
        ],
    },
    "z_z_blue_green disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Blue disco pulse', length=8, offset=.5),
            b(1, name='Green disco pulse', length=8, offset=.5),
        ],
    },

    "z_z_red_blue disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8, offset=.5),
            b(1, name='Blue disco pulse', length=8, offset=.5),
        ],
    },
    "z_z_red_green disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8, offset=.5),
            b(1, name='Green disco pulse', length=8, offset=.5),
        ],
    },

    "z_z_red_green_blue disco strobe offset": {
        "length": 8,
        "autogen": "disco strobe",
        "beats": [
            b(1, name='Red disco pulse', length=8, offset=.5),
            b(1, name='Green disco pulse', length=8, offset=.5),
            b(1, name='Blue disco pulse', length=8, offset=.5),
        ],
    },

    "autogen winamp sidechain": {
        "length": 2,
        "autogen": "winamp sidechain",
        "intensity": "low",
        "beats": [
            grid_f(1, function=sidechain_grid, length=1, intensity=(0, 0))
        ],
    },
    
}


hard_colors = [
    (100, 0, 0),
    (0, 100, 0),
    (0, 0, 100),
    (100, 0, 100),
    (0, 100, 100),
    (100, 100, 0),
]


for i in range(0):
    beats = []
    
    for j in range(2):
        y = 11 - (j * 24)
        for p in range(8):
            beats.append(
                grid_f(
                    p + 1,
                    function=our_transform,
                    object=get_rectangle_numpy(20, 5),
                    start_pos=(y, 0),
                    start_color=random.choice(hard_colors),
                    end_color=(0, 0, 0),
                    # start_rot = 0,
                    # end_rot = 6.24,
                    length=1,
                )
            )
            # if random.randint(1, 2) == 1:
            # beats[-1][1].end_color = random.choice(hard_colors)


    effects[f'complex grid test {i}'] = {
            "length": 8,
            "autogen": "complex grid",
            "beats": beats,
        }