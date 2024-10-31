from effects.compiler import *



# cool masking effects:
    # Python: randomly getting preset /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Core/shifter - interference field v3_Phat_Darken_Pop_Edit_v4 EoS edit B dickless.milk

    # Python: loading preset Fractal/Nested Circle/Rozzor vs Esotic - Pixie Party Light (With Liquid Refreshment) Bonus Round.milk, real path: /Users/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Nested Circle/Rozzor vs Esotic - Pixie Party Light (With Liquid Refreshment) Bonus Round.milk▆▆▆


def construct_woman_melody(length):
    beats = []


    for i in range(length // 2):
        # center_x = random.randint(-4, 4)
        # center_y = random.randint(-5, 5)

        locations = [
            [random.randint(-7, 7), random.randint(-7, 7)],
            [random.randint(-7, 7), random.randint(-7, 7)],
            [random.randint(-7, 7), random.randint(-7, 7)],
            [random.randint(-7, 7), random.randint(-7, 7)],            
        ]

        beat_offset =  i * 2

        possible_colors = [GColor.blue, GColor.pink, GColor.red, GColor.seafoam, GColor.orange]

        first_color = random.choice(possible_colors)
        remaining_colors = [color for color in possible_colors if color not in first_color]
        last_color = random.choice(remaining_colors)

        beats += get_circle_pulse_beats_new(
            start_beat=1 + beat_offset, start_color=first_color, end_color=GColor.nothing, start_pos=locations[0], speed=8.5, steps=4
        )
        beats += get_circle_pulse_beats_new(
            start_beat=1.5 + beat_offset, start_color=first_color, end_color=GColor.nothing, start_pos=locations[1], speed=8.5, steps=4
        )
        beats += get_circle_pulse_beats_new(
            start_beat=1.75 + beat_offset, start_color=first_color, end_color=GColor.nothing, start_pos=locations[2], speed=8.5, steps=4
        )
        beats += get_circle_pulse_beats_new(
            start_beat=2.5 + beat_offset, start_color=last_color, end_color=GColor.nothing, start_pos=locations[3], speed=8.5, steps=4
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




    "woman intro": {
        "length": 1,
        "beats": [
            b(1, name='Green top', length=1)
        ]
    },

    "woman melody first": {
        "length": 2,
        "beats": [
            *get_circle_pulse_beats_new(start_beat=1, start_color=GColor.red, end_color=GColor.nothing, start_pos=[3, -2], speed=8.5, steps=4),
            *get_circle_pulse_beats_new(start_beat=1.5, start_color=GColor.pink, end_color=GColor.nothing, start_pos=[-3, 2], speed=8.5, steps=4),
            *get_circle_pulse_beats_new(start_beat=1.75, start_color=GColor.pink, end_color=GColor.nothing, start_pos=[0, -5], speed=8.5, steps=4),
            *get_circle_pulse_beats_new(start_beat=2.5, start_color=GColor.blue, end_color=GColor.nothing, start_pos=[-5, 0], speed=8.5, steps=4),
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
            b(1, name='RBBB 1 bar', length=4)
        ]
    },


    "Lane 8 - Woman": {
        "bpm": 124,
        "song_path": "songs/Lane 8 - Woman.ogg",
        "delay_lights": 0.04,
        "skip_song": 0.0,
        "beats": [
            b(1, name='woman intro', length=128),


            b(129, name='woman melody', length=128),

            b(385, name='woman bass drop', length=100),

        ]
    }
}