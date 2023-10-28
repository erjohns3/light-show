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



def rain(grid_info):
    if getattr(grid_info, 'rains', None) is None or (grid_info.curr_sub_beat == 0 and not grid_info.looped):
        grid_info.rains = [None] * grid_info.num_rains
        for index in range(len(grid_info.rains)):
            grid_info.rains[index] = time.time() + grid_info.lower_wait + (random.random() * grid_info.upper_wait)
        grid_info.explosions = []

    for index, state_or_next_time in enumerate(grid_info.rains):
        if isinstance(state_or_next_time, float):
            if time.time() < state_or_next_time:
                continue

            new_x = random.randint(0, grid_helpers.GRID_WIDTH - 1)
            grid_info.rains[index] = (new_x, 0, time.time(), grid_info.speed)
        
        curr_x, curr_y, curr_start_time, curr_length = grid_info.rains[index]

        percent_done = (time.time() - curr_start_time) / curr_length
        if percent_done > .9:
            grid_info.rains[index] = time.time() + grid_info.lower_wait + (random.random() * grid_info.upper_wait)
            grid_info.explosions.append((curr_x, time.time(), .24))
            continue
        
        curr_y = int(percent_done * grid_helpers.GRID_HEIGHT)

        grid_helpers.grid[curr_x][curr_y] += grid_info.color
        scale = .02
        for i in range(1, 3):
            new_y = curr_y - i
            if new_y < 0:
                break
            grid_helpers.grid[curr_x][new_y] += scale_vector(GColor.blue, scale)
            scale /= 1.2

    index = 0
    while index < len(grid_info.explosions):         
        curr_x, curr_start_time, curr_length = grid_info.explosions[index]

        percent_done = (time.time() - curr_start_time) / curr_length
        if percent_done > 1:
            del grid_info.explosions[index]
            continue
        
        radius = int(percent_done * 4)
        inner_radius = radius - 1

        grid_width, grid_height = grid_helpers.GRID_WIDTH, grid_helpers.GRID_HEIGHT
        
        mid_x = curr_x
        mid_y = grid_helpers.GRID_HEIGHT - 1
        for x in range(grid_width):
            for y in range(grid_height):
                if random.randint(1, 5) != 1:
                    continue
                distance = (x - mid_x) ** 2 + (y - mid_y) ** 2
                distance = math.sqrt(distance)
                if distance <= radius and distance >= inner_radius:
                    grid_helpers.grid[x][y] += scale_vector(GColor.blue, .04)
                    grid_helpers.grid[x][y] += scale_vector(GColor.white, .02)
        index += 1


def make_rain(start_beat=1, length=1, lower_wait=1, upper_wait=6):
    return [grid_f(
        start_beat,
        function=rain,
        num_rains=20,
        color=GColor.blue,
        lower_wait=lower_wait,
        upper_wait=upper_wait, 
        speed=1.2,
        length=length,
    )]



effects = {
    "rain": {"profiles": ['Twinkle'], "loop": True, "beats": make_rain()},

    "twinkle white": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.white)},
    "twinkle blue": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.blue)},
    "twinkle green": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.green)},
    "twinkle red": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.red)},
    "twinkle purple": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.purple)},
    "twinkle yellow": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.yellow)},
    "twinkle cyan": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.cyan)},
    "twinkle orange": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.orange)},
    "twinkle pink": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.pink)},
    "twinkle light_blue": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.light_blue)},
    "twinkle light_green": {"profiles": ['Twinkle'], "loop": True, "beats": make_twinkle(color=GColor.light_green)},

    
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
                object=get_centered_circle_numpy(radius=10, color=GColor.blue, offset_y=-8),
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
                object=get_centered_circle_numpy(radius=10, color=GColor.green, offset_y=8),
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
            *make_rain(length=108),
            # b(1, name="twinkle white", length=1),
            # b(3, name="twinkle blue", length=1),
            # b(5, name="twinkle white", length=1),
            # b(7, name="twinkle blue", length=1),
            # b(name="twinkle blue", length=32),
        ],
    }
}