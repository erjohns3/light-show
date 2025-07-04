from effects.compiler import *


# def generate_genesis_top_beats(length):
#     final = []
#     pattern_length = 8
#     for i in range(0, length, pattern_length):
#         building = [
#             grid_f(
#                 i + 1,
#                 function=our_transform,
#                 object=get_centered_circle_numpy_nofill(radius=(6), offset_x=0, offset_y=-7),
#                 color=GColor.pink,
#                 length=.55,
#             ),
#             grid_f(i + 1, function=sidechain_grid, length=1, intensity=(1, .2), priority=5000),
#             grid_f(
#                 i + 5,
#                 function=our_transform,
#                 object=get_centered_circle_numpy_nofill(radius=(6), offset_x=0, offset_y=7),
#                 color=GColor.green,
#                 length=.55,
#             ),
#             grid_f(i + 5, function=sidechain_grid, length=1, intensity=(1, .2), priority=5000),
#         ]
#         final += building
#     return final


def generate_genesis_top_beats(length):
    final = []
    pattern_length = 8
    for i in range(0, length, pattern_length):
        building = [
            grid_f(
                i + 1,
                function=our_transform,
                object=get_centered_circle_numpy_fill(radius=(6), offset_x=0, offset_y=-7),
                color=GColor.pink,
                length=1.2,
            ),
            grid_f(i + 1, function=sidechain_grid, length=1.2, intensity=(1, .2), priority=5000),
        ]

        randoms = [5.3, 6.3, 7, 8.3]

        for j in randoms:
            the_rand = random.randint(-10, 10)
            the_rand_2 = random.randint(5, 9)
            building += [
                grid_f(
                    i + j,
                    function=our_transform,
                    object=get_centered_circle_numpy_nofill(radius=(the_rand_2), offset_x=the_rand, offset_y=7),
                    color=GColor.blue,
                    length=.4,
                ),
                grid_f(i + j, function=sidechain_grid, length=.4, intensity=(1, .2), priority=5000),
            ]
            
            
        final += building
    return final


effects = {
    "genesis circle": {
        "length": 2,
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(6)),
                color=GColor.pink,
                length=.55,
            )
        ],
    },

    # "genesis gen top beats": {
    #     "length": 2,
    #     "beats": [
    #         grid_f(
    #             1,
    #             function=our_transform,
    #             object=get_centered_circle_numpy_nofill(radius=(6)),
    #             color=GColor.pink,
    #             length=.55,
    #         ),
    #         grid_f(1, function=sidechain_grid, length=1, intensity=(1, .2), priority=5000),
    #     ]
    # },

    "genesis gen top beats": {
        "length": 8,
        "beats":generate_genesis_top_beats(8)
    },

    "genesis vert green": {
        "length": 1,
        "beats": [
            b(1, bottom_vert_rgb=GColor.green, length=1)
        ],
    },
    "genesis hori pink": {
        "length": 1,
        "beats": [
            b(1, bottom_hori_rgb=GColor.pink, length=1)
        ],
    },

    "genesis chorus bottom": {
        "length": 4,
        "beats": [
            b(2, name="genesis hori pink", length=1, intensity=(1, 0)),
            b(4, name="genesis vert green", length=1, intensity=(1, 0)),
        ]
    },


    "genesis Chorus": {
        "length": 64,
        "beats": [
            b(1, name='genesis gen top beats', length=64),
            b(1, name='genesis chorus bottom', length=64),
        ]
    },


    "Justice - Genesis": {
        "bpm": 117,
        "song_path": "songs/Justice - Genesis.ogg",
        "delay_lights": 0.237,
        "skip_song": 0.0,
        "beats": [

            # Intro
            # dooooooooooo
            b(2.75, name='Green bottom', length=7.25, intensity=(1, 1)), 
            # do-do-do-do-do..... equally spaced
            b(10, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(11, name='Green bottom', length=1,intensity=(1, 1)), 
            b(12, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(13, name='Green bottom', length=1, intensity=(1, 1)), 
            b(14, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(15, name='Green bottom', length=3.75, intensity=(1, 1)), 
            # do.... 
            b(18.75, name='Blue bottom', length=7.25, intensity=(1, 1)), 

            # repeat do-do-do-do-do equally spaced
            b(26, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(27, name='Green bottom', length=1,intensity=(1, 1)), 
            b(28, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(29, name='Green bottom', length=1, intensity=(1, 1)), 
            b(30, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(31, name='Green bottom', length=3.75, intensity=(1, 1)), 
            # do.... 
            b(34.75, name='Blue bottom', length=7.25, intensity=(1, 1)), 

            # repeat do-do-do-do-do equally spaced
            b(42, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(43, name='Green bottom', length=1,intensity=(1, 1)), 
            b(44, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(45, name='Green bottom', length=1, intensity=(1, 1)), 
            b(46, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(47, name='Green bottom', length=3.75, intensity=(1, 1)), 
            
            # this one is special he gets extra dooos in threes
            b(50.75, name='Blue bottom', length=1, intensity=(1, 1)), 
            b(51.75, name='Yellow bottom', length=1.5, intensity=(1, 1)), 
            b(53.25, name='Blue bottom', length=5.5, intensity=(1, 1)), 

            # Second set of 3
            b(58.75, name='Yellow bottom', length=1, intensity=(1, 1)), 
            b(59.75, name='Blue bottom', length=1.5, intensity=(1, 1)), 
            b(61.25, name='Yellow bottom', length=5, intensity=(1, 1)), 

            # second to last
            b(66.25, name='Blue bottom', length=9.75, intensity=(1, 1)), 
            
            # This beat takes us into the next section
            # b(76, name='Yellow bottom', length=1, intensity=(1, 1)), 
            #--------------------------------------------------------------#
            # This part repeats in 8 bar sections, but with some variations
            b(76, name='genesis Chorus', length = 64),
            # same as before part but with laser sounds???
            b(140, name='Blue top', length = 24),
            # break down part 1
            b(164, name='Green top', length = 8),
            # back to normal beat
            b(172, name='Blue top', length = 24),
            # break down part 2
            b(196, name = 'Green top', length = 8),
            # back to normal beat but this one has a quieter first half
            b(204, name='Blue top', length = 64),
            #-------------------------------------------------------------#
            # this part kind of trades off 1 section of 8, then second section of 8
            # on and off until the end
            b(268, name='Pink bottom', length = 110),
            


        ]
    }
}