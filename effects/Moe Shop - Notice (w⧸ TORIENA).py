from effects.compiler import *

effects = {
    "Repeat": {
        "length": 16,
        "beats": [
            *make_twinkle(start_beat=7.75, length=1.25, color=GColor.pink, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),
            *make_twinkle(start_beat=7.75, length=1.25, color=GColor.green, twinkle_length=.25, num_twinkles=40, twinkle_lower_wait=0, twinkle_upper_wait=.5),

            b(7.75, 'Sidechain top', length=1.25),
            b(7.75, 'Sidechain bottom', length=1.25),

            b(1, 'RBBB 1 bar', length=16),
        ]
    },
    "Twinkle": {
        "length": 64,
        "beats": [
            *make_twinkle(start_beat=1, length=64, color=GColor.pink, twinkle_length=.75, num_twinkles=20, twinkle_lower_wait=0.25, twinkle_upper_wait=.75),
            *make_twinkle(start_beat=1, length=64, color=GColor.green, twinkle_length=.75, num_twinkles=20, twinkle_lower_wait=0.25, twinkle_upper_wait=.75),
            *make_twinkle(start_beat=1, length=64, color=GColor.light_blue, twinkle_length=.75, num_twinkles=30, twinkle_lower_wait=0.25, twinkle_upper_wait=.75),
        ]
    },
    "Verse bass": {
        "length": 1,
        "beats": [
            b(1, name='Indigo bottom', length=0.75, sat_shift=-.25, intensity=(1, 0)),
        ]
    },
    "Tunnel": {
        "length": 32,
        "beats": [
            *get_circle_pulse_beats(start_beat=1, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=2, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=3, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=4, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=5, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=6, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=7, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=8, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=9, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=10, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=11, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=12, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=13, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=14, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=15, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=16, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=17, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=18, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=19, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=20, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=21, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=22, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=23, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=24, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=25, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=26, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=27, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=28, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=29, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=30, start_color=GColor.blue, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=31, start_color=GColor.pink, end_color=GColor.purple, length=6),
            *get_circle_pulse_beats(start_beat=32, start_color=GColor.blue, end_color=GColor.purple, length=6),
        ]
    },
    "Intro": {
        "length": 16,
        "beats":[
            b(1, 'UV pulse', length=0.5),
            b(2, 'UV pulse', length=0.5),
            b(3, 'UV pulse', length=0.5),
            b(3.5, 'Red top', length=0.5),
            b(5, 'UV pulse', length=0.5),
            b(6, 'UV pulse', length=0.5),
            b(7, 'UV pulse', length=0.5),
            b(7.5, 'Red top', length=1),
            b(9, 'UV pulse', length=0.5),
            b(10, 'UV pulse', length=0.5),
            b(11, 'UV pulse', length=0.5),
            b(11.5, 'Red top', length=0.5),
            b(13, 'UV pulse', length=0.5),
            b(14, 'UV pulse', length=0.5),
            b(15, 'UV pulse', length=0.5),
            b(15.75, 'Red top', length=0.3),
        ]
    },

    "Moe Shop - Notice (w\u29f8 TORIENA)": {
        "bpm": 125,
        "song_path": "songs/Moe Shop - Notice (w\u29f8 TORIENA).ogg",
        "delay_lights": 0.15, # Andrew HELP: I tried my best here, it still feels slightly off tho
        "skip_song": 0.0,
        "beats": [
            # Intro
            # Andrew HELP: Ok I tabbed out close to where all of the hits are... I kind of like
            # the UV pulse but I think we need something special for the other hits. Each one could be
            # special in its own way?
            b(2, 'Intro', length=30),
            
            # Verse
            # Andrew HELP: I want this to just be smooth and continuous but I cant get it to 
            # loop and leave the circles on the grid becasue like the old ones need to finish / remain on
            # but there has to be a better way than typing out 64 beats on it in the Tunnel function...
            b(33, 'Tunnel', length=64),
            b(33, 'Verse bass', length=64),

            # Verse break
            # Andrew HELP: Something cooler here? Maybe its fine
            b(98, 'UV pulse', length=4),

            # Back to verse
            # Keep with the tunnel? Something similar to intro with off-beats?
            b(102, 'Verse bass', length=64),

            
            # quiet part
            # Thinking about making a more subtle twinkle here? Not sure where I even want to do this anymore
            b(165.5, 'Twinkle', length=64),
            

            # "Moe sempai notice me"
            #b(229)

            # back to verse
            #b(261)

            # verse break
            #b(325)

            # end

            #b(33, 'Repeat', length=128)
        ]
    }
}