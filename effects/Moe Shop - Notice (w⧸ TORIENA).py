from effects.compiler import *

effects = {
    "Fast twinkle": {
        "length": 1,
        "beats": [
            *make_twinkle(start_beat=1, length=1, color=GColor.pink, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
            *make_twinkle(start_beat=1, length=1, color=GColor.green, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
        ]
    },

    # "Repeat": {
    #     "length": 16,
    #     "beats": [


    #         b(7.75, 'Sidechain top', length=1.25),
    #         b(7.75, 'Sidechain bottom', length=1.25),

    #         b(1, 'RBBB 1 bar', length=16),
    #     ]
    # },
    "Slow twinkle": {
        "length": 64,
        "beats": [
            *make_twinkle(start_beat=1, length=64, color=GColor.pink, twinkle_length=.75, num_twinkles=20, twinkle_lower_wait=0.25, twinkle_upper_wait=2),
            *make_twinkle(start_beat=1, length=64, color=GColor.green, twinkle_length=.75, num_twinkles=20, twinkle_lower_wait=0.25, twinkle_upper_wait=2),
            *make_twinkle(start_beat=1, length=64, color=GColor.light_blue, twinkle_length=.75, num_twinkles=30, twinkle_lower_wait=0.25, twinkle_upper_wait=2),
        ]
    },
    "Verse bass": {
        "length": 1,
        "beats": [
            b(1, name='Indigo bottom', length=0.75, sat_shift=-.25, intensity=(1, 0)),
        ]
    },
    "Tunnel": {
        "length": 64,
        "beats": [
            *get_circle_pulse_beats_new(start_beat=1, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=2, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=3, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=4, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=5, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=6, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=7, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=8, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=9, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=10, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=11, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=12, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=13, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=14, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=15, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=16, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=17, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=18, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=19, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=20, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=21, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=22, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=23, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=24, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=25, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=26, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=27, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=28, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=29, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=30, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=31, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=32, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=33, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=34, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=35, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=36, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=37, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=38, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=39, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=40, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=41, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=42, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=43, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=44, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=45, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=46, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=47, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=48, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=49, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=50, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=51, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=52, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=53, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=54, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=55, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=56, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=57, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=58, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=59, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=60, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=61, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=62, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=63, start_color=GColor.pink, end_color=GColor.purple, speed=5.5),
            *get_circle_pulse_beats_new(start_beat=64, start_color=GColor.blue, end_color=GColor.purple, speed=5.5),
        ]
    },
    "Intro": {
        "length": 16,
        "beats":[
            b(1, 'UV', length=0.5, intensity=(1, 0)),
            b(2, 'UV', length=0.5, intensity=(1, 0)),
            b(3, 'UV', length=0.5, intensity=(1, 0)),
            b(3.75, 'Green top', length=0.5),            
            b(5, 'UV', length=0.5, intensity=(1, 0)),
            b(6, 'UV', length=0.5, intensity=(1, 0)),
            b(7, 'UV', length=0.5, intensity=(1, 0)),
            b(7.5, 'Fast twinkle', length=1),

            b(9, 'UV', length=0.5, intensity=(1, 0)),
            b(10, 'UV', length=0.5, intensity=(1, 0)),
            b(11, 'UV', length=0.5, intensity=(1, 0)),
            b(11.75, 'Green top', length=0.5),
            b(13, 'UV', length=0.5, intensity=(1, 0)),
            b(14, 'UV', length=0.5, intensity=(1, 0)),
            b(15, 'UV', length=0.5, intensity=(1, 0)),
            b(16, 'Red top', length=0.3),
        ]
    },

    "Verse break": {
        "length": 4,
        "beats":[
            b(1, 'UV pulse', length=4),
        ]
    },

    "Verse": {
        "length": 16,
        "beats":[
            b(1, 'Pink top', length=.5),

            b(4.5, 'Pink top', length=.5),
            b(5, 'Blue top', length=.5),

            b(8.25, 'Pink top', length=.12),
            b(8.5, 'Pink top', length=.12),
            b(8.75, 'Pink top', length=.12),
            b(9, 'Blue top', length=.5),

            b(12.5, 'Pink top', length=.5),
            b(13, 'Blue top', length=.5),
            b(14, 'Green top', length=.5),
            b(15, 'Yellow top', length=.5),
            b(16, 'Orange top', length=.5),


            b(2, 'Verse bass', length=1),
            b(3, 'Verse bass', length=1),
            b(4, 'Verse bass', length=1),
            b(6, 'Verse bass', length=1),
            b(7, 'Verse bass', length=1),
            b(10, 'Verse bass', length=1),
            b(11, 'Verse bass', length=1),
        ]
    },

    "Moe Shop - Notice (w\u29f8 TORIENA)": {
        "bpm": 125,
        "song_path": "songs/Moe Shop - Notice (w\u29f8 TORIENA).ogg",
        "delay_lights": 0.02, 
        "skip_song": 0.0,
        "beats": [
            # Intro
            # Andrew HELP: Ok I tabbed out close to where all of the hits are... I kind of like
            # the UV pulse but I think we need something special for the other hits. Each one could be
            # special in its own way?
            b(2, 'Intro', length=32),
            
            # Verse
            b(34, 'Tunnel', length=64), # !TODO fix looping somehow
            b(34, 'Verse bass', length=64),

            # Verse break
            # Andrew HELP: Something cooler here? Maybe its fine
            b(98, 'Verse break', length=4),


            # Back to verse
            # Keep with the tunnel? Something similar to intro with off-beats?
            b(102, 'Verse', length=64),

            
            # quiet part
            # Thinking about making a more subtle twinkle here? Not sure where I even want to do this anymore
            b(165.5, 'Slow twinkle', length=64),
            

            # "Moe sempai notice me"
            # !TODO maybe different, this section doesn't have filter, + has vocals
            b(230, 'Intro', length=32),

            #b(230)

            # back to verse
            b(262, 'Verse bass', length=64),
            b(262, 'Tunnel', length=64),


            # verse break
            b(326, 'Verse break', length=4),
            b(330, 'Verse', length=64),

            # end
        ]
    }
}