from effects.compiler import *



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
            the_rand_2 = random.randint(4, 8)
            building += [
                grid_f(
                    i + j,
                    function=our_transform,
                    object=get_centered_circle_numpy_fill(radius=(the_rand_2), offset_x=the_rand, offset_y=7),
                    color=GColor.blue,
                    length=.4,
                ),
                grid_f(i + j, function=sidechain_grid, length=.4, intensity=(1, .2), priority=5000),
            ]
            
            
        final += building
    return final


def bar_down(grid_info):
    """
    Draws a vertical bar moving downwards on the grid.

    Args:
        grid_info: An object containing the bar's state, including
                   y-position, color, speed, and current sub-beat.
    """
    # Initialize y if it doesn't exist or if it's the first sub-beat
    if not hasattr(grid_info, 'y') or grid_info.curr_sub_beat == 0:
        grid_info.y = 0

    # Return if the bar is already off the bottom of the grid
    if grid_info.y >= grid_helpers.GRID_HEIGHT:
        return

    # Draw the visible part of the bar
    for x_off in range(getattr(grid_info, 'x_range', 1)):
        for y_off in range(grid_info.y_range):
            current_y = grid_info.y + y_off
            if 0 <= current_y < grid_helpers.GRID_HEIGHT:
                grid_helpers.grid[grid_info.x_pos + x_off][current_y] = grid_info.color

    # Determine the speed, ensuring it's at least 1
    speed = max(1, int(1 / getattr(grid_info, 'speed', 1)))

    # Move the bar down based on the speed and sub-beat
    if grid_info.curr_sub_beat % speed == 0:
        grid_info.y += getattr(grid_info, 'step_size', 1)


def spawn_half_fallers(start_beat, total_beats, start_color, end_color=None, intensity=1, speed=1, y_range=5, step_size=1, x_range=1):
    if end_color == None:
        end_color = GColor.nothing
    building = []
    quarter_x = grid_helpers.GRID_WIDTH // 4
    for beat in range(start_beat, start_beat + total_beats + 1):
        percent_done = (beat - start_beat) / total_beats
        curr_color = interpolate_vectors_float(start_color, end_color, percent_done)
        curr_color = scale_vector(curr_color, intensity)
        random_thing = random.randint(1, 3)
        building += [
            grid_f(beat, function=bar_down, length=2, x_pos=quarter_x * random_thing, y_range=y_range, color=curr_color, speed=speed, step_size=step_size, x_range=x_range),
        ]
    return building



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

    "genesis gen top beats": {
        "length": 64,
        "beats":generate_genesis_top_beats(64)
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

    'genesis lasers': {
        "length": 8,
        "beats": [
            *spawn_half_fallers(start_beat=1, total_beats=8, start_color=GColor.blue, end_color=GColor.pink, intensity=1, speed=6, y_range=6, step_size=2),
        ]
    },

    'genesis lasers build': {
        "length": 32,
        "beats": [
            *spawn_half_fallers(start_beat=1, total_beats=32, start_color=GColor.seafoam, end_color=GColor.pink, intensity=1, speed=8, y_range=10, step_size=2),
        ]
    },

    'genesis breakdown': {
        "length": 4,
        "beats": [
            b(1, name='autogen circle pulsing', length=4)
        ]
    },

    'genesis lasers build 2': {
        "length": 32,
        "beats": [
            *spawn_half_fallers(start_beat=1, total_beats=32, start_color=GColor.light_green, end_color=GColor.cyan, intensity=1, speed=8, y_range=12, step_size=3, x_range=5),
        ]
    },

    'genesis wub': {
        "length": 3,
        "beats": [
            grid_f(1, function=bounce_line_x, length=3, wait_arr=[1, 15, 15, 30, 400], dir=3),
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
            b(2.75, name='Green bottom', length=7.25, intensity=(1, 0)), 
            # do-do-do-do-do..... equally spaced
            b(10, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(11, name='Green bottom', length=1,intensity=(1, 1)), 
            b(12, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(13, name='Green bottom', length=1, intensity=(1, 1)), 
            b(14, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(15, name='Green bottom', length=3.75, intensity=(1, 0)), 
            # do.... 
            b(18.75, name='Blue bottom', length=7.25, intensity=(1, 0)), 

            # repeat do-do-do-do-do equally spaced
            b(26, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(27, name='Green bottom', length=1,intensity=(1, 1)), 
            b(28, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(29, name='Green bottom', length=1, intensity=(1, 1)), 
            b(30, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(31, name='Green bottom', length=3.75, intensity=(1, 0)), 
            # do.... 
            b(34.75, name='Blue bottom', length=7.25, intensity=(1, 0)), 

            # repeat do-do-do-do-do equally spaced
            b(42, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(43, name='Green bottom', length=1,intensity=(1, 1)), 
            b(44, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(45, name='Green bottom', length=1, intensity=(1, 1)), 
            b(46, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(47, name='Green bottom', length=3.75, intensity=(1, 0)), 
            
            # this one is special he gets extra dooos in threes
            b(50.75, name='Blue bottom', length=1, intensity=(1, 0)), 
            b(51.75, name='Yellow bottom', length=1.5, intensity=(1, 0)), 
            b(53.25, name='Blue bottom', length=5.5, intensity=(1, 0)), 

            # Second set of 3
            b(58.75, name='Yellow bottom', length=1, intensity=(1, 1)), 
            b(59.75, name='Blue bottom', length=1.5, intensity=(1, 1)), 
            b(61.25, name='Yellow bottom', length=5, intensity=(1, 0)), 

            # second to last
            b(66.25, name='Blue bottom', length=9.75, intensity=(1, 0)), 
            
            # This beat takes us into the next section
            # b(76, name='Yellow bottom', length=1, intensity=(1, 1)), 
            #--------------------------------------------------------------#

            # This part repeats in 8 bar sections, but with some variations
            b(76, name='genesis Chorus', length = 64),

            b(132, name='genesis lasers', length=8),
            # same as before part but with laser sounds???
            b(140, name='genesis Chorus', length = 24),
            b(142.2, name='genesis wub', length=3),

            b(150.2, name='genesis wub', length=3),

            b(158.2, name='genesis wub', length=3),


            # break down part 1
            b(164, name='genesis breakdown', length = 8),

            # back to normal beat
            b(172, name='genesis Chorus', length = 24),
            b(174.2, name='genesis wub', length=3),

            b(182.2, name='genesis wub', length=3),

            b(190.2, name='genesis wub', length=3),

            # break down part 2
            b(196, name = 'genesis breakdown', length = 8),
            # back to normal beat but this one has a quieter first half



            b(204, name='genesis Chorus', length = 64),

            b(204, name='genesis lasers build', length=32),
            b(236, name='genesis lasers build 2', length=32),

            

            #-------------------------------------------------------------#
            # this part kind of trades off 1 section of 8, then second section of 8
            # on and off until the end
            grid_f(269, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(270, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            grid_f(273, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(274, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            b(278.2, name='genesis wub', length=2 ),

            grid_f(285, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(286, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            grid_f(289, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(290, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            b(294.2, name='genesis wub', length=2 ),

            grid_f(301, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(302, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            grid_f(305, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(306, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            b(310.2, name='genesis wub', length=2 ),


            grid_f(317, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(318, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            grid_f(321, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(322, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            b(326.2, name='genesis wub', length=2 ),

            grid_f(333, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(334, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            grid_f(337, filename='genesis_cross.jpeg', rotate_90=True, length=0.5), # color=.04 is multiplier
            grid_f(338, filename='genesis_cross.jpeg', rotate_90=True, length=1.5), # color=.04 is multiplier
            b(332.2, name='genesis wub', length=2 ),

        ]
    }
}