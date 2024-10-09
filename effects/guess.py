from effects.compiler import *




effects = {
    # "guess circles" : {
    #     "length": 4,
    #     "beats": [
    #         *get_circle_pulse_beats(start_beat=1, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=1.2, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=1.4, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=1.6, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=1.8, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=2, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=2.2, start_color=GColor.light_green, end_color=GColor.purple),
    #         *get_circle_pulse_beats(start_beat=2.4, start_color=GColor.light_green, end_color=GColor.purple),
    #     ],
    # },

    "guess pink circle": {
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

    "guess circles": {
        "length": 8,
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(4)),
                color=GColor.light_green,
                length=.55,
            ),
            grid_f(
                3,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(6)),
                color=GColor.light_green,
                length=.55,
            ),
            grid_f(
                5,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(7)),
                color=GColor.light_green,
                length=.55,
            ),
            grid_f(
                7,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(9)),
                color=GColor.light_green,
                length=.55,
            ),
        ],
    },

    "guess circles 2": {
        "length": 4,
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(9)),
                color=GColor.blue,
                length=.3,
            ),
            grid_f(
                1.5,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(7)),
                color=GColor.blue,
                length=.55,
            ),
            grid_f(
                2.5,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(5)),
                color=GColor.blue,
                length=.55,
            ),
        ],
    },
    "extra circles": {
        "length": 2,
        "beats": [
            grid_f(
                1.3,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(4)),
                color=GColor.light_green,
                length=.17,
            ),
            grid_f(
                1.6,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(4)),
                color=GColor.light_green,
                length=.17,
            ),

            grid_f(
                1.85,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(4)),
                color=GColor.light_green,
                length=.17,
            ),

            grid_f(
                2.05,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=(4)),
                color=GColor.light_green,
                length=.17,
            ),
        ],
    },

    "guess intro" : {
        "length": 50,
        "beats": [
            #*make_rain(start_beat=1, length=15, speed=.35, lower_wait=2, upper_wait=6, color=GColor.light_green, num_rains=40),
            b(18, name='guess circles', length=12),
            b(30, name='guess circles 2', length=4),
            b(34, name='guess circles', length=2),
            b(36, name='guess pink circle', length=2),
            # beat 36 pink circle
            b(38, name='guess circles 2', length=4),
            b(42, name='guess circles', length=4),
            b(46, name='guess circles 2', length=4),
        ],
    },
    "guess bass" : {
        "length": 1,
        "beats": [
            b(1, name='Green bottom', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
        ],
    },
    "synth high" : {
        "length": 1,
        "beats": [
            b(1, name='Green top', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
        ],
    },
    "synth low" : {
        "length": 1,
        "beats": [
            b(1, name='Green bottom', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
        ],
    },
    "synth higher" : {
        "length": 1,
        "beats": [
            b(1, name='Red top', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
        ],
    },
    "the drop" : {
        "length": 1,
        "beats": [
            b(1, name='green laser', length=1),
            b(1, name='green laser motor', length=.5),
        ],
    },
    "the drop 2" : {
        "length": 1,
        "beats": [
            b(1, name='green laser', length=1),
            b(1, name='green laser motor', length=.5),
            b(1, name='Sidechain laser', length=.5, intensity=(1, 0)),
        ],
    },
    "wub" : {
        "length": 2,
        "beats": [
            *get_circle_pulse_beats(start_beat=1, total=12, start_color=GColor.green, length=15),
            *get_circle_pulse_beats(start_beat=2, total=12, start_color=GColor.green, length=15, reverse=True),
            # grid_f(
            #     1,
            #     function=our_transform,
            #     object=get_centered_circle_numpy_nofill(radius=11, color=GColor.green, offset_y=0),
            #     name='Ok 2',
            #     start_pos=(0, 0),
            #     start_scale = (.01, .01),
            #     end_scale = (1, 1),
            #     length=1,
            # ),
            # grid_f(
            #     2,
            #     function=our_transform,
            #     object=get_centered_circle_numpy_nofill(radius=11, color=GColor.green, offset_y=0),
            #     name='Ok 2',
            #     start_pos=(0, 0),
            #     start_scale = (1, 1),
            #     end_scale = (.01, .01),
            #     length=1,
            # ),
        ]
    },

    "Guess": {
        "bpm": 130,
        "song_path": "songs/Charli xcx - Guess (official lyric video).ogg",
        "delay_lights": 0.00,
        "skip_song": 4.80,
        "beats": [

            # intro w/ bass
            b(1, name='guess intro', length=49),
            # bass comes back (put them in your mouth)
            b(50, name='guess bass', length=32),
            b(50, name='guess circles', length=12),
            b(62, name='guess circles 2', length=2),

            b(65, name="extra circles", length=2),
            b(66, name='guess circles', length=16),

            # synth high (buy it, bite it, lick it, slipt it)
            b(82, name='synth high', length=8),
            # synth low (wear them)
            b(90, name='synth low', length=8),
            # synth high (buy it, bite it, lick it, slipt it)
            b(98, name='synth high', length=8),
            # synth low (wear them)
            b(106, name='synth low', length=4),
            # Send it to the Dare yeah I think hes with it
            #
            # synth high 
            b(114, name='synth high', length=10),
            # synth higher
            b(122, name='synth higher', length=6),
            # bass comes back (you wanna guess the color of)
            b(130, name='guess bass', length=48),
            #b(180)
            #b(210) (GUESS)
            b(210, name="the drop", length=32),
            b(242, name="the drop 2", length=64),
            b(278, name="wub", length=4),
            b(286, name="wub", length=4),
            b(294, name="wub", length=4),
            b(302, name="wub", length=4)




        ]
    }
}