import random
from copy import deepcopy

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

beats = []

for i in range(1, TWINKLE_TIME, TWINKLE_SPEED):
    for j in range(int(NUM_GRID_TWINKLE)):
        # Get random point on grid
        x = random.randint(-(grid_helpers.GRID_WIDTH/2), (grid_helpers.GRID_WIDTH/2))
        y = random.randint(-(grid_helpers.GRID_HEIGHT/2), (grid_helpers.GRID_HEIGHT/2))
        # Create random offset for start beat of each twinkle
        t_offset = random.uniform(0, TWINKLE_SPEED)
        beats.append(
                grid_f(
                    i + t_offset,
                    function=our_transform,
                    object=get_rectangle_numpy(1, 1),
                    start_pos=(y,x),
                    start_color=white,
                    end_color=(0, 0, 0),
                    length=TWINKLE_FADE,
                )
            )

effects = {
    "Lemaitre - Blue Shift": {
        "bpm": 118,
        "song_path": "songs/Lemaitre - Blue Shift.ogg",
        "delay_lights": 0.4043245762711864,
        "skip_song": 0.0,
        "beats": beats,
    }
}