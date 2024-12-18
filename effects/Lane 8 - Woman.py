import random
import math

from effects.compiler import *



# cool masking effects:
    # Python: randomly getting preset /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Core/shifter - interference field v3_Phat_Darken_Pop_Edit_v4 EoS edit B dickless.milk

    # Python: loading preset Fractal/Nested Circle/Rozzor vs Esotic - Pixie Party Light (With Liquid Refreshment) Bonus Round.milk, real path: /Users/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Nested Circle/Rozzor vs Esotic - Pixie Party Light (With Liquid Refreshment) Bonus Round.milk▆▆▆


y_range = [-12, 13]
x_range = [-6, 6]

def is_far_enough(new_point, existing_points, min_distance):
    for point in existing_points:
        dx = new_point[0] - point[0]
        dy = new_point[1] - point[1]
        distance = math.hypot(dx, dy)
        if distance < min_distance:
            return False
    return True

min_distance = 5
def get_random_points(x_range, y_range, num, min_distance):
    locations = []
    for i in range(140):
        if len(locations) == num:
            break
        new_point = [random.randint(*x_range), random.randint(*y_range)]
        if is_far_enough(new_point, locations, min_distance):
            locations.append(new_point)
    # backup if we didn't get enough points
    for i in range(num - len(locations)):
        print_yellow(f'Did not get enough points, using backup. This is bad')
        new_point = [random.randint(*x_range), random.randint(*y_range)]
        locations.append(new_point)
    return locations


def get_shrinking_circle(start_beat=1, start_color=GColor.white, end_color=None, reverse=False, speed=5, steps=20, start_pos=None, start_radius=5):
    if end_color is None:
        end_color = start_color

    arr = []
    inv_speed = 1 / speed
    beats = list(zip([x * inv_speed for x in range(steps)], [inv_speed for x in range(steps)]))
    if reverse:
        beats = reversed(beats)


    for index, (beat_offset, length_of_step) in enumerate(beats):
        if start_radius - index <= 0:
            break
        before_color = interpolate_vectors_float(start_color, end_color, index / steps)
        after_color = interpolate_vectors_float(start_color, end_color, (index+1) / steps)

        thing = grid_f(
            start_beat + beat_offset,
            function=our_transform,
            object=get_centered_circle_numpy_fill(radius=start_radius - index),
            start_color=before_color,
            end_color=after_color,
            length=length_of_step,
        )
        if start_pos is not None:
            thing[1].start_pos = start_pos
        arr.append(thing)
    return arr

def construct_woman_melody(length):
    beats = []


    for i in range(length // 2):
        y_range = [-12, 13]
        x_range = [-6, 7]
        points = get_random_points(x_range, y_range, 4, min_distance)
        # points = [[0, 0], [0, 0], [0, 0], [0, 0]]
        beat_offset =  i * 2

        possible_colors = [GColor.blue, GColor.pink, GColor.red, GColor.seafoam, GColor.orange]

        first_color = random.choice(possible_colors)
        remaining_colors = [color for color in possible_colors if color not in first_color]
        last_color = random.choice(remaining_colors)

        beats += get_circle_pulse_beats_new(
            start_beat=1 + beat_offset, start_color=last_color, end_color=GColor.nothing, start_pos=points[3], speed=15.5, steps=9, start_radius=1
        )
        beats += get_shrinking_circle(
            start_beat=1.5 + beat_offset, start_color=first_color, end_color=GColor.nothing, start_pos=points[1], speed=5.5, steps=4, start_radius=4
        )
        beats += get_shrinking_circle(
            start_beat=1.75 + beat_offset, start_color=first_color, end_color=GColor.nothing, start_pos=points[2], speed=5.5, steps=4, start_radius=4
        )
        beats += get_shrinking_circle(
            start_beat=2.75 + beat_offset, start_color=first_color, end_color=GColor.nothing, start_pos=points[0], speed=5.5, steps=4, start_radius=4
        )
    return beats

effects = {
    "woman sidechain_test": {
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_rectangle_numpy(14, 13),
                color=(1, 1, 1),
                start_rot=0,
                end_rot=6.28,
                length=8,
            ),
            grid_f(
                1, 
                function=grid_winamp_mask,
                preset='202.milk',
                priority=10000,
                length=8,
            ),
        ]
    },
    # b(1, name='woman sidechain_test', length=4000),




    "woman intro/break": {
        "length": 16,
        "beats": [
            b(1, name='z_rainbow good slow top', length=16)
        ]
    },

    "woman melody": {
        "length": 128,
        "beats": [
            *construct_woman_melody(128)
        ]
    },



    "woman bass drop": {
        "length": 4,
        "beats": [
            # b(1, name='RBBB 1 bar', length=4),
            b(1, s(bottom_hori_rgb=[70, 0, 30]), length=1, intensity=[1, 0]),

            b(2, s(bottom_rgb=[50, 30, 10]), length=.5, intensity=[1, 0]),

            b(3, s(bottom_vert_rgb=[30, 0, 70]), length=1, intensity=[1, 0]),

            b(4, s(bottom_rgb=[10, 30, 50]), length=.5, intensity=[1, 0]),

        ]
    },


    "Lane 8 - Woman": {
        "bpm": 124,
        "song_path": "songs/Lane 8 - Woman.ogg",
        "delay_lights": -0.04,
        "skip_song": 0.0,
        "beats": [
            b(1, name='woman intro/break', length=128),

            b(129, name='woman melody', length=256),

            b(385, name='woman bass drop', length=256),
            b(385, name='woman melody', length=256),


            
            # b(449, name='woman high hats', length=256),


            b(641, name='woman intro/break', length=128),
            # b(641, name='RBBB 1 bar', length=128),

            b(769, name='woman melody', length=128),

            b(897, name='woman bass drop', length=256),
            b(897, name='woman melody', length=400),
        ]
    }
}