effects = {
    "g_Strobe": {
        "length": 1,
        "autogen": 'strobe',
        "beats": [
            [1, 'Strobe', 1],
        ],
    },
    "g_UV Strobe": {
        "length": 1,
        "autogen": 'strobe',
        "beats": [
            [1, 'UV Strobe', 1],
        ],
    },

    "g_UV": {
        "length": 1,
        "autogen": 'UV',
        "beats": [
            [1, 'UV', 1],
        ],
    },
    "g_UV pulse": {
        "length": 1,
        "autogen": 'UV pulse',
        "beats": [
            [1, 'UV pulse', 1],
        ],
    },

    # rainbows
    "g_rainbow good top": {
        "length": 8,
        "autogen": 'rainbow top',
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
        "length": 16,
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
        "length": 4,
        "autogen": 'downbeat bottom',
        "beats": [
            [1, "Cyan bottom", 1],
            [2, "Pink bottom", 1],
            [3, "Yellow bottom", 1],
            [4, "Green bottom", 1],
        ],
    },

    "g_pulse top brown": {
        "length": 1,
        "autogen": 'downbeat top',
        "beats": [
            [1, 'Rosy brown top', .2, 1, 0],
        ],
    },
    "g_pulse bottom brown": {
        "length": 1,
        "autogen": 'downbeat bottom',
        "beats": [
            [1, 'Rosy brown bottom', .2, 1, 0],
        ],
    },

    "g_solid top cycle": {
        "length": 4,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Firebrick top", 1],
            [2, "Pink top", 1],
            [3, "Red top", 1],
            [4, "Green top", 1],
        ],
    },

    "g_solid mixed 1": {
        "length": 4,
        "autogen": 'downbeat mixed',
        "beats": [
            [1, "Green top", 1],
            [2, "Pink bottom", .5],
            [2.5, "Firebrick bottom", .5],
            [3, "Green top", 1],
            [4, "Blue bottom", .5],
            [4.5, "Orange bottom", .5],
        ],
    },

    "g_solid mixed 2": {
        "length": 4,
        "autogen": 'downbeat mixed',
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
        "length": 4,
        "autogen": 'downbeat mixed',
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
        "length": 1,
        "autogen": 'downbeat top',
        "beats": [
            [1, "Cyan top", 1, 0.42, .2],
        ],
    },
    "g_purple green bottom pulse": {
        "length": 2,
        "autogen": 'downbeat bottom',
        "beats": [
            [1, "Purple bottom", 1, 0.42, .2],
            [2, "Green bottom", 1, 0.42, .2],
        ],
    },
    "g_green sidechain bottom pulse": {
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