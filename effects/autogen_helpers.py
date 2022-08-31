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

    "g_solid mixed double": {
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