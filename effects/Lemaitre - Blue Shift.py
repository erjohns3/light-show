import random
from collections import deque

from effects.compiler import *

import grid_helpers

# Set percentage of grid to twinkle
TWINKLE_PERCENT = 0.2

# Find number of random points on grid to make twinkle
NUM_GRID_TWINKLE = int(TWINKLE_PERCENT * (grid_helpers.GRID_WIDTH * grid_helpers.GRID_HEIGHT))

# Total number of beats for twinkle effect
TWINKLE_TIME = 100

# Time for each twinkle to fade
TWINKLE_FADE = 2

# Twinkle speed, higher is slower, lower is faster
TWINKLE_SPEED = 10

# def make_twinkle_beats(color):
#     twinkle_beats = []
#     for beat in range(1, TWINKLE_TIME):
#         for j in range(int(NUM_GRID_TWINKLE)):
#             x, y = grid_helpers.random_coord()
#             # Create random offset for start beat of each twinkle
#             t_offset = random.uniform(0, beat * TWINKLE_SPEED)
#             twinkle_beats.append(
#                     grid_f(
#                         beat + t_offset,
#                         function=our_transform,
#                         object=get_rectangle_numpy(1, 1),
#                         start_pos=(y, x),
#                         start_color=color,
#                         end_color=(0, 0, 0),
#                         length=TWINKLE_FADE,
#                     )
#                 )
#     return twinkle_beats


white = (100, 100, 100)
blue = (0, 0, 100)
red = (100, 0, 0)
green = (0, 100, 0)
purple = (100, 0, 100)
yellow = (100, 100, 0)
cyan = (0, 100, 100)
orange = (100, 50, 0)
pink = (100, 0, 50)
light_blue = (0, 50, 100)
light_green = (50, 100, 0)


def twinkle(grid_info):
    num_twinkles = grid_info.num_twinkles
    twinkle_length = grid_info.twinkle_length
    twinkle_lower_wait = grid_info.twinkle_lower_wait
    twinkle_upper_wait = grid_info.twinkle_upper_wait
    if getattr(grid_info, 'twinkles', None) is None or (grid_info.curr_sub_beat == 0 and not grid_info.looped):
        grid_info.twinkles = [None] * num_twinkles
        for index in range(len(grid_info.twinkles)):
            grid_info.twinkles[index] = time.time() + (random.random() * (twinkle_upper_wait - twinkle_lower_wait))

    for index, state_or_next_time in enumerate(grid_info.twinkles):
        if isinstance(state_or_next_time, float):
            if time.time() < state_or_next_time:
                continue

            new_x, new_y = grid_helpers.random_coord()
            grid_info.twinkles[index] = (new_x, new_y, time.time(), twinkle_length)
        
        curr_x, curr_y, curr_start_time, curr_length = grid_info.twinkles[index]

        percent_done = (time.time() - curr_start_time) / curr_length
        if percent_done > 1:
            grid_info.twinkles[index] = time.time() + twinkle_lower_wait + (random.random() * twinkle_upper_wait)
            continue

        percent_done * 2
        if percent_done <= .5:
            color = interpolate_vectors_float((0, 0, 0), grid_info.color, percent_done * 2)
        else:
            color = interpolate_vectors_float(grid_info.color, (0, 0, 0), (percent_done * 2) - 1)
        grid_helpers.grid[curr_x][curr_y] += color


def twinkle_forever(color=white, twinkle_length=1, num_twinkles=40, twinkle_lower_wait=1, twinkle_upper_wait=4):
    return [grid_f(
        1,
        function=twinkle,
        color=color,
        num_twinkles=num_twinkles,
        twinkle_lower_wait=twinkle_lower_wait,
        twinkle_upper_wait=twinkle_upper_wait, 
        twinkle_length=twinkle_length,
        length=1,
    )]


def random_color():
    b = random.randint(0, 100)
    g = random.randint(0, 100)
    r = random.randint(0, 100)
    return (b, g, r)

def minus_color(color, amt):
    return (max(color[0] - amt, 0), max(color[1] - amt, 0), max(color[2] - amt, 0))

def trail_ball_fade(grid_info):
    if getattr(grid_info, 'pos', None) is None:
        grid_info.pos = grid_helpers.random_coord()
        grid_info.dir = (1 - (random.randint(0, 1) * 2), 1 - (random.randint(0, 1) * 2))
        grid_info.color = random_color()
        grid_info.trail = deque([])


    grid_helpers.grid[grid_info.pos[0]][grid_info.pos[1]] = grid_info.color
    for index, ((p_x, p_y), p_color) in enumerate(grid_info.trail):        
        grid_helpers.grid[p_x][p_y] += p_color

    speed = int(1 / getattr(grid_info, 'speed', 1))
    if grid_info.curr_sub_beat % speed == 0:
        index = 0
        while index < len(grid_info.trail):
            (p_x, p_y), p_color = grid_info.trail[index]
            p_color = minus_color(p_color, 5)
            grid_info.trail[index][1] = p_color
            if p_color == (0, 0, 0) and index == 0:
                grid_info.trail.popleft()
            else:
                index += 1

        x, y = grid_info.pos
        d_x, d_y = grid_info.dir

        if x + d_x < 0 or x + d_x >= grid_helpers.GRID_WIDTH:
            grid_info.dir = (grid_info.dir[0] * -1, grid_info.dir[1])
            d_x *= -1
            grid_info.color = random_color()

        if y + d_y < 0 or y + d_y >= grid_helpers.GRID_HEIGHT:
            grid_info.dir = (grid_info.dir[0], grid_info.dir[1] * -1)
            d_y *= -1
            grid_info.color = random_color()

        grid_info.pos = (x + d_x, y + d_y)
        grid_info.trail.append([grid_info.pos, grid_info.color])


def fire_ball_fade(grid_info):
    if grid_info.curr_sub_beat == 1 or getattr(grid_info, 'pos', None) is None:
        if random.randint(0, 1) == 0:
            start_x, x_dir = random.sample([(0, 1), (grid_helpers.GRID_WIDTH - 1, -1)], k=1)[0]
            start_y = random.randint(0, grid_helpers.GRID_HEIGHT - 1)
            y_dir = 1 - (random.randint(0, 1) * 2)
        else:
            start_x = random.randint(0, grid_helpers.GRID_WIDTH - 1)
            x_dir = 1 - (random.randint(0, 1) * 2)
            start_y, y_dir = random.sample([(0, 1), (grid_helpers.GRID_HEIGHT - 1, -1)], k=1)[0]

        grid_info.pos = (start_x, start_y)
        grid_info.dir = (x_dir, y_dir)
        # grid_info.pos = (random.randint(0, grid_helpers.GRID_WIDTH - 1), random.randint(0, grid_helpers.GRID_HEIGHT - 1))
        # grid_info.dir = (1 - (random.randint(0, 1) * 2), 1 - (random.randint(0, 1) * 2))
        grid_info.color = random_color()
        grid_info.trail = deque([])

    speed = int(1 / getattr(grid_info, 'speed', 1))

    if grid_info.curr_sub_beat % speed == 0:
        index = 0
        while index < len(grid_info.trail):
            (p_x, p_y), p_color = grid_info.trail[index]
            p_color = minus_color(p_color, 5)
            grid_info.trail[index][1] = p_color
            grid_helpers.grid[p_x][p_y] += p_color
            if p_color == (0, 0, 0) and index == 0:
                grid_info.trail.popleft()
            else:
                index += 1

        x, y = grid_info.pos
        d_x, d_y = grid_info.dir
        if x + d_x < 0 or x + d_x >= grid_helpers.GRID_WIDTH or y + d_y < 0 or y + d_y >= grid_helpers.GRID_HEIGHT:
            return
        grid_info.pos = (x + d_x, y + d_y)

    grid_helpers.grid[grid_info.pos[0]][grid_info.pos[1]] = grid_info.color

    if grid_info.curr_sub_beat % speed == 0:
        grid_info.trail.append([grid_info.pos, grid_info.color])

white = (100, 100, 100)
blue = (0, 0, 100)
red = (100, 0, 0)
green = (0, 100, 0)
purple = (100, 0, 100)
yellow = (100, 100, 0)
cyan = (0, 100, 100)
orange = (100, 50, 0)
pink = (100, 0, 50)
light_blue = (0, 50, 100)
light_green = (50, 100, 0)
effects = {
    "twinkle white": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=white)},
    "twinkle blue": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=blue)},
    "twinkle green": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=green)},
    "twinkle red": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=red)},
    "twinkle purple": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=purple)},
    "twinkle yellow": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=yellow)},
    "twinkle cyan": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=cyan)},
    "twinkle orange": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=orange)},
    "twinkle pink": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=pink)},
    "twinkle light_blue": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=light_blue)},
    "twinkle light_green": {"profiles": ['Twinkle'], "loop": True, "beats": twinkle_forever(color=light_green)},

    
    "trail ball fast": {
        "profiles": ['Emma'],
        "trigger": "toggle",
        "loop": True,
        'beats': [
            grid_f(1, function=trail_ball_fade, length=64, speed=1),
        ],
    },
    "trail ball mid": {
        "profiles": ['Emma'],
        "trigger": "toggle",
        "loop": True,
        'beats': [
            grid_f(1, function=trail_ball_fade, length=64, speed=.5),
        ],
    },
    "trail ball slow": {
        "profiles": ['Emma'],
        "trigger": "toggle",
        "loop": True,
        'beats': [
            grid_f(1, function=trail_ball_fade, length=64, speed=.25),
        ],
    },
    "fire ball fade": {
        "profiles": ['Emma'],
        "trigger": "hold",
        'beats': [
            grid_f(1, function=fire_ball_fade, length=8, speed=1),
        ],
    },
    "blue shift - circle pulse 1": {
        "profiles": ['Emma'],
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy(radius=10, color=blue, offset_y=-8),
                name='Ok 1',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (.01, .01),
                end_scale = (1, 1),
                length=1,
            ),
            grid_f(
                2,
                function=our_transform,
                object='Ok 1',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (1, 1),
                end_scale = (.01, .01),
                length=1,
            ),
        ],
    },
    "blue shift - circle pulse 2": {
        "profiles": ['Emma'],
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy(radius=10, color=green, offset_y=8),
                name='Ok 2',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (.01, .01),
                end_scale = (1, 1),
                length=1,
            ),
            grid_f(
                2,
                function=our_transform,
                object='Ok 2',
                start_pos=(0, 0),
                # start_color=random.choice(hard_colors),
                # end_color=(0, 0, 0),
                start_scale = (1, 1),
                end_scale = (.01, .01),
                length=1,
            ),
        ],
    },
    "Lemaitre - Blue Shift": {
        "bpm": 118,
        "song_path": "songs/Lemaitre - Blue Shift.ogg",
        "delay_lights": 0.4043245762711864,
        "skip_song": 0.0,
        "beats": [
            # grid_f(1, function=trail_ball_fade, length=64, speed=1, clear=False),
            # b(1, name="blue shift - circle pulse 1", length=32, offset=1),
            # b(1, name="blue shift - circle pulse 2", length=32),
            b(1, name="twinkle white", length=1),
            b(3, name="twinkle blue", length=1),
            b(5, name="twinkle white", length=1),
            b(7, name="twinkle blue", length=1),
            # b(name="twinkle blue", length=32),
        ],
    }
}