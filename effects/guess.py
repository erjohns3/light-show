from effects.compiler import *

effects = {
    "guess bass" : {
        "length": 1,
        "beats": [
            b(1, name='Green bottom', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
        ],
    },
    "synth high" : {
        "length": 1,
        "beats": [
            b(1, name='Blue top', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
        ],
    },
    "synth low" : {
        "length": 1,
        "beats": [
            b(1, name='Yellow top', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
        ],
    },
    "synth higher" : {
        "length": 1,
        "beats": [
            b(1, name='Orange top', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(0.75, 0.2)), 
                  
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

    "Guess": {
        "bpm": 130,
        "song_path": "songs/Charli xcx - Guess (official lyric video).ogg",
        "delay_lights": 0.00,
        "skip_song": 4.80,
        "beats": [
            # intro w/ bass
            b(1, name='guess bass', length=17),
            # (you wanna guess the color of)

            # bass comes back (put them in your mouth)
            b(50, name='guess bass', length=32),
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
            b(114, name='synth high', length=8),
            # synth higher
            b(122, name='synth higher', length=8),
            # bass comes back (you wanna guess the color of)
            b(130, name='guess bass', length=32),
            #b(180)
            
            # b(209) # says "guess" before drop
            b(210, name='the drop', length=32),
            b(242, name='the drop 2', length=32),
            # b(210)
            # 242 repeats guess




        ]
    }
}