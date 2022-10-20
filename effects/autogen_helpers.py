effects = {
    # fillers
    "g_Strobe": {
        "profiles": ["autogen helpers"],
        "length": 1,
        "autogen": 'strobe',
        "beats": [
            [1, 'Strobe', 1],
        ],
    },
    "g_UV Strobe": {
        "profiles": ["autogen helpers"],
        "length": 1,
        "autogen": 'strobe',
        "beats": [
            [1, 'UV Strobe', 1],
        ],
    },

    "g_UV": {
        "profiles": ["autogen helpers"],
        "length": 1,
        "autogen": 'UV',
        "beats": [
            [1, 'UV', 1],
        ],
    },
    "g_UV pulse": {
        "profiles": ["autogen helpers"],
        "length": 1,
        "autogen": 'UV pulse',
        "beats": [
            [1, 'UV pulse', 1],
        ],
    },

    "g_filler 1": {
        "profiles": ["autogen helpers"],
        "length": 1,
        "autogen": 'filler',
        "intensity": 'high',
        "beats": [
            [1, 'Pink bottom', .25, 1, 0],
            [1.25, 'Pink bottom', .25, 1, 0],
            [1.5, 'Cyan front', .5, 1, .2],
            [1.5, 'Cyan back', .5, 1, .2],
        ],
    },

    "g_filler 2": {
        "profiles": ["autogen helpers"],
        "length": 2,
        "autogen": 'filler',
        "intensity": 'high',
        "beats": [
            [1, 'Red front', .25, 1, 0],
            [1.25, 'Blue back', .25, 1, 0],
            [1.75, 'Green bottom', .25, 1, 0],
            [2, 'Firebrick top', .75, 1, 0],
            [2, 'Firebrick bottom', .75, 1, 0],
        ],
    },

    "Autogen helper white top pulse 1": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "beats": [
            [1, 'White top', .4, 1, 0],
            [3, 'White top', .4, 1, 0],
        ],
    },
    "g_rainbow good top pulse 1": {
        "profiles": ["autogen helpers"],
        "length": 8,
        "autogen": 'downbeat top',
        "intensity": 'low',
        "profiles": ['Andrew'],
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
        "profiles": ["autogen helpers"],
        "length": 4,
        "beats": [
            [2, "White top", .4, 1, 0],
            [4, "White top", .4, 1, 0],
        ],
    },
    "g_rainbow good top pulse 2": {
        "profiles": ["autogen helpers"],
        "length": 8,
        "autogen": 'downbeat top',
        "intensity": 'low',
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
    "g_rainbow good top": {
        "profiles": ["autogen helpers"],
        "length": 8,
        "autogen": 'rainbow top',
        "intensity": 'low',
        "profiles": ['Andrew'],
        "beats": [
            [1, "Green top", 3.7, 1, 0],
            [1, "Red top", 2.66, 0, 1],
            [3.66, "Red top", 3.7, 1, 0],
            [3.66, "Blue top", 2.66, 0, 1],
            [6.32, "Blue top", 3.7, 1, 0],
            [6.32, "Green top", 2.66, 0, 1],
        ],
    },
    "g_rainbow good slow top": {
        "profiles": ["autogen helpers"],
        "length": 16,
        "intensity": 'low',
        "autogen": 'rainbow top',
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
    "Yellow Top to Bottom hang": {
        "profiles": ["autogen helpers"],
        "length": 3,
        "beats": [
            [1, [100, 30, 5, 0, 25, 0, 0], .2, 0, .5],
            [1.2, [100, 30, 5, 0, 25, 0, 0], 1.1, .5, 0],
            [1.3, [0, 0, 0, 100, 30, 5, 0], 1.3, 0, .6],
            [2.6, [0, 0, 0, 100, 30, 5, 0], 38, .6, .6],
        ],
    },

    # downbeat tops and bottoms
    "g_solid bottom cycle": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat bottom',
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

    "g_solid bottom cycle down then up": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat bottom',
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

    "g_pulse top swap 1": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat top',
        "beats": [
            [1, 'Orange front', .3, 1, 0],
            [2, 'Orange back', .3, 1, 0],
            [3, 'Green back', .3, 1, 0],
            [4, 'Green front', .3, 1, 0],
        ],
    },

    "g_pulse top swap 2": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat top',
        "beats": [
            [1, 'Firebrick back', .3, 1, 0],
            [2, 'Firebrick front', .3, 1, 0],
            [3, 'Indigo front', .3, 1, 0],
            [4, 'Indigo back', .3, 1, 0],
        ],
    },

    "g_pulse top swap 3": {
        "profiles": ["autogen helpers"],
        "length": 2,
        "autogen": 'downbeat top',
        "beats": [
            [1, 'Pink top', .3, 1, 0],
            [2, 'Green front', .3, 1, 0],
            [2.5, 'Green back', .3, 1, 0],
        ],
    },

    # "g_pulse top brown": {
    #     "profiles": ["autogen helpers"],
    #     "length": 1,
    #     "autogen": 'downbeat top',
    #     "beats": [
    #         [1, 'Rosy brown top', .2, 1, 0],
    #     ],
    # },
    # "g_pulse bottom brown": {
    #     "profiles": ["autogen helpers"],
    #     "length": 1,
    #     "autogen": 'downbeat bottom',
    #     "beats": [
    #         [1, 'Rosy brown bottom', .2, 1, 0],
    #     ],
    # },

    "g_solid top cycle 1": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Firebrick top", 1, .6],
            [2, "Pink top", 1],
            [3, "Red top", 1, .6],
            [4, "Green top", 1, .4],
        ],
    },

    "g_solid top cycle 2": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Firebrick top", .5, 1, 0],
            [2, "Pink top", .3],
            [3, "Red top", .3],
            [4, "Green top", .3],
        ],
    },

    "g_solid mixed 1": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat mixed',
        "beats": [
            [1, "Green top", 1, .2],
            [2, "Pink bottom", .5],
            [2.5, "Firebrick bottom", .5],
            [3, "Green top", 1, .2],
            [4, "Blue bottom", .5],
            [4.5, "Orange bottom", .5],
        ],
    },

    "g_solid mixed 2": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat mixed',
        "profiles": ['Andrew'],
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

    "g_solid mixed 3": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat mixed',
        "profiles": ['Andrew'],
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

    "g_solid mixed 4": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat mixed',
        "beats": [
            [1, "Yellow Top to Bottom hang", 3],
            [2, "Sidechain top b", .5, 1, 0],
            [2, "Green bottom", .2, .2, 0],
            [3, "Sidechain bottom b", .5, 1, 0],
            [3, "Green bottom", .2, .2, 0],
            [4, "Blue top", .8, 1, 0],
        ],
    },

    "g_solid mixed cycle": {
        "profiles": ["autogen helpers"],
        "length": 4,
        "autogen": 'downbeat mixed',
        "beats": [
            [1, "Firebrick top", 1],
            [2, "Indigo bottom", 1],
            [3, "Firebrick top", 1],
            [4, "Yellow bottom", 1],
        ],
    },

    "g_cyan top pulse": {
        "profiles": ["autogen helpers"],
        "length": 1,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Cyan top", 1, 0.42, .2],
        ],
    },
    "g_purple purple yellow top pulse": {
        "profiles": ["autogen helpers"],
        "length": 2,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Purple top", 1, 0.42, .2],
            [2, "Yellow top", 1, 0.42, .2],
        ],
    },

    "g_green sidechain top pulse": {
        "profiles": ["autogen helpers"],
        "length": 2,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Green top", 0.1, 0.6, 0.17],
            [1.1, "Green top", 3, 0.17, 0.17],
            [2, "Sidechain top g", 0.5, 1, 0], 
            [2, "Some color top", 0.3, 1, .7],
        ],
    },


    "g_purple green bottom pulse": {
        "profiles": ["autogen helpers"],
        "length": 2,
        "autogen": 'downbeat bottom',
        "beats": [
            [1, "Purple bottom", 1, 0.42, .2],
            [2, "Green bottom", 1, 0.42, .2],
        ],
    },
    "g_green sidechain bottom pulse": {
        "profiles": ["autogen helpers"],
        "length": 2,
        "autogen": 'downbeat bottom',
        "beats": [
            [1, "Green bottom", 0.1, 0.6, 0.17],
            [1.1, "Green bottom", 3, 0.17, 0.17],
            [2, "Sidechain bottom g", 0.5, 1, 0], 
            [2, "Some color bottom", 0.3, 1, .7],
        ],
    },
}