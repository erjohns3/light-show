import random
from collections import deque

from effects.compiler import *

import grid_helpers

# Set percentage of grid to twinkle
TWINKLE_PERCENT = 0.1

# Find number of random points on grid to make twinkle
NUM_GRID_TWINKLE = int(TWINKLE_PERCENT * (grid_helpers.GRID_WIDTH * grid_helpers.GRID_HEIGHT))

# Total number of beats for twinkle effect
TWINKLE_TIME = 100

# Time for each twinkle to fade
TWINKLE_FADE = 5

# Twinkle speed, higher is slower, lower is faster
TWINKLE_SPEED = 10

white = (100,100,100)


def make_twinkle_beats(color):
    twinkle_beats = []
    for i in range(1, TWINKLE_TIME, TWINKLE_SPEED):
        for j in range(int(NUM_GRID_TWINKLE)):
            # Get random point on grid
            x = random.randint(-(grid_helpers.GRID_WIDTH/2), (grid_helpers.GRID_WIDTH/2))
            y = random.randint(-(grid_helpers.GRID_HEIGHT/2), (grid_helpers.GRID_HEIGHT/2))
            # Create random offset for start beat of each twinkle
            t_offset = random.uniform(0, TWINKLE_SPEED)
            twinkle_beats.append(
                    grid_f(
                        i + t_offset,
                        function=our_transform,
                        object=get_rectangle_numpy(1, 1),
                        start_pos=(y,x),
                        start_color=color,
                        end_color=(0, 0, 0),
                        length=TWINKLE_FADE,
                    )
                )
    return twinkle_beats


def random_color():
    b = random.randint(0, 100)
    g = random.randint(0, 100)
    r = random.randint(0, 100)
    return (b, g, r)

def minus_color(color, amt):
    return (max(color[0] - amt, 0), max(color[1] - amt, 0), max(color[2] - amt, 0))

def trail_ball_fade(grid_info):
    if getattr(grid_info, 'pos', None) is None:
        grid_info.pos = (random.randint(0, grid_helpers.GRID_WIDTH - 1), random.randint(0, grid_helpers.GRID_HEIGHT - 1))
        grid_info.dir = (1 - (random.randint(0, 1) * 2), 1 - (random.randint(0, 1) * 2))
        grid_info.color = random_color()
        grid_info.trail = deque([])
    speed = int(1 / getattr(grid_info, 'speed', 1))

    if grid_info.curr_sub_beat % speed == 0:
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

        index = 0
        while index < len(grid_info.trail):
            (p_x, p_y), p_color = grid_info.trail[index]
            
            p_color = minus_color(p_color, 5)

            grid_info.trail[index][1] = p_color
            
            grid_helpers.grid[p_x][p_y] = p_color
            if p_color == (0, 0, 0) and index == 0:
                grid_info.trail.popleft()
            else:
                index += 1
        grid_info.pos = (x + d_x, y + d_y)
        grid_helpers.grid[grid_info.pos[0]][grid_info.pos[1]] = grid_info.color

        grid_info.trail.append([grid_info.pos, grid_info.color])


effects = {
    "blue shift - twinkle": {
        "beats": make_twinkle_beats(white),
    },
    "blue shift - twinkle blue": {
        "beats": make_twinkle_beats((0, 0, 100)),
    },
    "Lemaitre - Blue Shift": {
        "bpm": 118,
        "song_path": "songs/Lemaitre - Blue Shift.ogg",
        "delay_lights": 0.4043245762711864,
        "skip_song": 0.0,
        "beats": [
            grid_f(1, function=trail_ball_fade, length=64, speed=1, clear=False),
            # b(name="blue shift - twinkle", length=8),
            # b(name="blue shift - twinkle blue", length=8),
        ],
    }
}