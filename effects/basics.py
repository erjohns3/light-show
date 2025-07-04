from effects.compiler import *

effects = {
    # pulses and strobes
    "Strobe green laser": {
        "length": 0.35,
        "beats": [
            b(1, green_laser=100, length=.04),
        ],
    },
    "Strobe": {
        "length": 0.2,
        "beats": [
            b(1, top_rgb=[100, 100, 100], length=0.07),
        ],
    },
    "Strobe bottom": {
        "length": 0.2,
        "beats": [
            b(1, bottom_rgb=[100, 100, 100], length=0.07),
        ],
    },
    "Strobe front": {
        "length": 0.2,
        "beats": [
            b(1, front_rgb=[100, 100, 100], length=0.07),
        ],
    },
    "Strobe back": {
        "length": 0.2,
        "beats": [
            b(1, back_rgb=[100, 100, 100], length=0.07),
        ],
    },
    "UV Strobe": {
        "length": 0.2,
        "beats": [
            b(1, uv=100, length=0.07),
        ],
    },

    "UV pulse": {
        "length": 1,
        "autogen": True,
        "trigger": "add",
        "loop": False,
        "profiles": ["Andrew"],
        "beats": [
            [1, "UV", 1, 1, 0, 0],
        ]
    },
    "UV pulse slow": {
        "length": 2,
        "autogen": True,
        "trigger": "add",
        "loop": False,
        "beats": [
            [1, "UV", 1, 1, 0, 0],
        ]
    },


    # laser stuff
    "green laser": {
        "length": 1,
        "beats": [
            b(1, green_laser=100, length=1),
        ],
    },
    "green laser motor": {
        "length": 1,
        "beats": [
            b(1, green_laser=100, laser_motor=100, length=1),
        ],
    },
    "red laser": {
        "length": 1,
        "beats": [
            b(1, red_laser=100, length=1),
        ],
    },
    "red laser motor": {
        "length": 1,
        "beats": [
            b(1, red_laser=100, laser_motor=100, length=1),
        ],
    },
    "laser motor": {
        "length": 1,
        "beats": [
            b(1, laser_motor=100, length=1),
        ],
    },

    # Sidechain stuff
    "Nothing": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, green_laser=-1000, red_laser=-1000, laser_motor=-1000, length=1, disco_rgb=[-1000, -1000, -1000]),
            grid_f(1, function=sidechain_grid, length=1, intensity=(1, 1), priority=5000),
        ],
    },
    "Sidechain laser": {
        "length": 1,
        "beats": [
            b(1, length=1, green_laser=-1000, red_laser=-1000),
        ],
    },
    "Sidechain all but laser": {
        "length": 1,
        "beats": [
            b(1, length=1, top_rgb=[-1000, -1000, -1000], bottom_rgb=[-1000, -1000, -1000], uv=-1000, disco_rgb=[-1000, -1000, -1000]),
        ],
    },
    "Sidechain motor": {
        "length": 1,
        "beats": [
            b(1, laser_motor=-1000, length=1),
        ],
    },
    "Sidechain top": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "Sidechain bottom": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[-1000, -1000, -1000], length=1),
        ],
    },

    "Sidechain top r": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[-1000, 0, 0], length=1),
        ],
    },
    "Sidechain top g": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[0, -1000, 0], length=1),
        ],
    },
    "Sidechain top b": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[0, 0, -1000], length=1),
        ],
    },
    "Sidechain bottom b": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[0, 0, -1000], length=1),
        ],
    },
    "Sidechain bottom rg": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[-1000, -1000, 0], length=1),
        ],
    },
    "Sidechain bottom gb": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[0, -1000, -1000], length=1),
        ],
    },
    "Sidechain bottom rb": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[-1000, 0, -1000], length=1),
        ],
    },
    "Sidechain top bg": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[0, -1000, -1000], length=1),
        ],
    },
    "Sidechain top rbg": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "Sidechain bottom rbg": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[-1000, -1000, -1000], length=1),
        ],
    },
    "Sidechain bottom g": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[0, -1000, 0], length=1),
        ],
    },
    "Sidechain bottom r": {
        "length": 1,
        "beats": [
            b(1, bottom_rgb=[-1000, 0, 0], length=1),
        ],
    },
    "Sidechain UV": {
        "length": 1,
        "beats": [
            b(1, uv=-1000, length=1),
        ],
    },
    "Sidechain top 100": {
        "length": 1,
        "beats": [
            b(1, top_rgb=[-100, -100, -100], length=1),
        ],
    },

    ################################## disco
    "Red disco": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=1, disco_rgb=[100, 0, 0])
        ]
    },

    "Green disco": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=1, disco_rgb=[0, 100, 0]),
        ]
    },

    "Blue disco": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=1, disco_rgb=[0, 0, 100]),
        ]
    },

    "Rgb disco": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "beats": [
            b(1, length=1, disco_rgb=[100, 100, 100]),
        ]
    },

    "Red disco pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=.5, disco_rgb=[100, 0, 0])
        ]
    },

    "Green disco pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=.5, disco_rgb=[0, 100, 0]),
        ]
    },

    "Blue disco pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=.5, disco_rgb=[0, 0, 100]),
        ]
    },

    "Rgb disco pulse": {
        "length": 1,
        "trigger": "toggle",
        "loop": True,
        "profiles": ["Eric"],
        "beats": [
            b(1, length=.5, disco_rgb=[100, 100, 100]),
        ]
    },

    ##################################  colors
    "UV": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, uv=100, length=1),
        ],
    },
    "White top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[100, 100, 100], length=1),
        ],
    },
    "White front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[100, 100, 100], length=1),
        ],
    },
    "White back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[100, 100, 100], length=1),
        ],
    },
    "White bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[100, 100, 100], length=1),
        ],
    },
    "Red top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[100, 0, 0], length=1),
        ],
    },
    "Red front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[100, 0, 0], length=1),
        ],
    },
    "Red back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[100, 0, 0], length=1),
        ],
    },
    "Red back sat": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[50, 30, 30], length=1),
        ],
    },
    "Red bottom sat": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[60, 20, 20], length=1),
        ],
    },
    "Red bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[100, 0, 0], length=1),
        ],
    },
    "Green top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[0, 100, 0], length=1),
        ],
    },
    "Green front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[0, 100, 0], length=1),
        ],
    },
    "Green back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[0, 100, 0], length=1),
        ],
    },
    "Green bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[0, 100, 0], length=1),
        ],
    },
    "Green red bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[100, 65, 0], length=1),
        ],
    },
    "Seafoam top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[0, 100, 50], length=1),
        ],
    },
    "Seafoam bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[0, 100, 50], length=1),
        ],
    },
    "Blue top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[0, 0, 100], length=1),
        ],
    },
    "Blue front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[0, 0, 100], length=1),
        ],
    },
    "Blue back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[0, 0, 100], length=1),
        ],
    },
    "Blue bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[0, 0, 100], length=1),
        ],
    },
    "Orange top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[100, 40, 10], length=1),
        ],
    },
    "Orange front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[100, 40, 10], length=1),
        ],
    },
    "Orange back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[100, 40, 10], length=1),
        ],
    },
    "Orange bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[100, 40, 10], length=1),
        ],
    },
    "Firebrick top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[178, 34, 34], length=1),
        ],
    },
    "Firebrick front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[178, 34, 34], length=1),
        ],
    },
    "Firebrick back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[178, 34, 34], length=1),
        ],
    },
    "Firebrick bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[178, 34, 34], length=1),
        ],
    },
    "Cyan top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[10, 50, 100], length=1),
        ],
    },
    "Cyan front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[10, 50, 100], length=1),
        ],
    },
    "Cyan back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[10, 50, 100], length=1),
        ],
    },
    "Cyan bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[10, 50, 100], length=1),
        ],
    },
    "Yellow top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[80, 100, 10], length=1),
        ],
    },
    "Yellow front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[80, 100, 10], length=1),
        ],
    },
    "Yellow back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[80, 100, 10], length=1),
        ],
    },
    "Yellow bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[80, 100, 10], length=1),
        ],
    },
    "Pink top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[100, 10, 30], length=1),
        ],
    },
    "Pink front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[100, 10, 30], length=1),
        ],
    },
    "Pink back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[100, 10, 30], length=1),
        ],
    },
    "Pink bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[100, 10, 30], length=1),
        ],
    },
    "Indigo top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[25, 0, 70], length=1),
        ],
    },
    "Indigo front": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, front_rgb=[25, 0, 70], length=1),
        ],
    },
    "Indigo back": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, back_rgb=[25, 0, 70], length=1),
        ],
    },
    "Indigo bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[40, 0, 90], length=1),
        ],
    },
    "Purple top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[100, 0, 100], length=1),
        ],
    },
    "Purple bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[100, 0, 100], length=1),
        ],
    },
    "Rosy brown top": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, top_rgb=[70, 30, 30], length=1),
        ],
    },
    "Rosy brown bottom": {
        "length": 1,
        "profiles": ["Colors"],
        "beats": [
            b(1, bottom_rgb=[70, 30, 30], length=1),
        ],
    },


    'Red bottom green laser flash': {
        'length': 1,
        'profiles': [f'All lasers'],
        'beats': [
            b(1, name='Red bottom', length=.5),    
            b(1.5, name='green laser', length=.5),    
        ],
    },



    # OTHER
    "RBBB 1 bar": {
        "length": 4,
        "beats": [
            [1, "Red top", 0.25],
            [2, "Blue top", 0.25],
            [3, "Blue top", 0.25],
            [4, "Blue top", 0.25],
        ],
    },

    "RBBB 1 bar bottom": {
        "length": 4,
        "beats": [
            [1, "Red bottom", 0.25],
            [2, "Blue bottom", 0.25],
            [3, "Blue bottom", 0.25],
            [4, "Blue bottom", 0.25],
        ],
    },

    # flashes
    "White flash": {
        "length": 1,
        "beats": [
            [1, "White top", 0.3, 0.1, 0],
            [1, "White bottom", 0.3, 0.1, 0],
        ],
    },

    "Pulse": {
        "length": 1,
        "beats": [
            [1, "White top", 0.9, 1, 0],
        ],
    },
}


for color in ['Red', 'Blue', 'Green']:
    for amt in range(1, 101):
        if amt < 25 or amt % 5 == 0:
            effects['t ' + color + f' {amt}'] = {
                'length': 1,
                'profiles': [f'zTop {color}'],
                'beats': [
                    b(1, f'{color} top', length=1, intensity=.01 * amt),
                ],
            }

for color in ['Red', 'Blue', 'Green']:
    for amt in range(1, 101):
        if amt < 25 or amt % 5 == 0:
            effects['b ' + color + f' {amt}'] = {
                'length': 1,
                'profiles': [f'zBot {color}'],
                'beats': [
                    b(1, f'{color} bottom', length=1, intensity=.01 * amt),
                ],
            }

effects[f'Red bottom flash .96'] = {
    'length': 1,
    'profiles': [f'All lasers'],
    'beats': [
        b(1, name='Red bottom', length=.96),    
    ],
}


effects[f'Red bottom flash .04'] = {
    'length': 1,
    'profiles': [f'All lasers'],
    'beats': [
        b(1, name='Red bottom', length=.04),    
    ],
}


effects[f'Laser flash .96'] = {
    'length': 1,
    'profiles': [f'All lasers'],
    'beats': [
        b(1, name='green laser', length=.96),    
    ],
}


effects[f'Laser flash .04'] = {
    'length': 1,
    'profiles': [f'All lasers'],
    'beats': [
        b(1, name='green laser', length=.04),    
    ],
}



effects[f'Green laser full'] = {
    'length': 1,
    'profiles': [f'All lasers'],
    'beats': [
        b(1, green_laser=100, length=1),
    ],
}
effects[f'Red laser full'] = {
    'length': 1,
    'profiles': [f'All lasers'],
    'beats': [
        b(1, red_laser=100, length=1),
    ],
}

for amt in range(1, 101):
    if amt < 7 or amt % 5 == 0:
        effects[f'Laser motor {amt}'] = {
            'length': 1,
            'profiles': [f'All lasers'],
            'beats': [
                b(1, laser_motor=amt, length=1),
            ],
        }

# for key, value in effects.items():
#     if len(value['beats']) != 1:
#         print(key)

# serialize the effects dictionary to a file

# import json
# fp = get_temp_dir().joinpath('AFTER_effects.json')
# with open(fp, 'w') as f:
#     json.dump(effects, f, indent=4)
# print(f'Effects saved to {fp}')
