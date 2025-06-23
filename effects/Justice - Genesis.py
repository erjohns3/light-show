from effects.compiler import *

effects = {
    "Justice - Genesis": {
        "bpm": 117,
        "song_path": "songs/Justice - Genesis.ogg",
        "delay_lights": 0.237,
        "skip_song": 0.0,
        "beats": [

            # Intro
            # dooooooooooo
            b(2.75, name='Green bottom', length=7.25, intensity=(1, 1)), 
            # do-do-do-do-do..... equally spaced
            b(10, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(11, name='Green bottom', length=1,intensity=(1, 1)), 
            b(12, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(13, name='Green bottom', length=1, intensity=(1, 1)), 
            b(14, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(15, name='Green bottom', length=3.75, intensity=(1, 1)), 
            # do.... 
            b(18.75, name='Blue bottom', length=7.25, intensity=(1, 1)), 

            # repeat do-do-do-do-do equally spaced
            b(26, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(27, name='Green bottom', length=1,intensity=(1, 1)), 
            b(28, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(29, name='Green bottom', length=1, intensity=(1, 1)), 
            b(30, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(31, name='Green bottom', length=3.75, intensity=(1, 1)), 
            # do.... 
            b(34.75, name='Blue bottom', length=7.25, intensity=(1, 1)), 

            # repeat do-do-do-do-do equally spaced
            b(42, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(43, name='Green bottom', length=1,intensity=(1, 1)), 
            b(44, name='Pink bottom', length=1, intensity=(1, 1)), 
            b(45, name='Green bottom', length=1, intensity=(1, 1)), 
            b(46, name='Pink bottom', length=1,  intensity=(1, 1)), 
            b(47, name='Green bottom', length=3.75, intensity=(1, 1)), 
            
            # this one is special he gets extra dooos in threes
            b(50.75, name='Blue bottom', length=1, intensity=(1, 1)), 
            b(51.75, name='Yellow bottom', length=1.5, intensity=(1, 1)), 
            b(53.25, name='Blue bottom', length=5.5, intensity=(1, 1)), 

            # Second set of 3
            b(58.75, name='Yellow bottom', length=1, intensity=(1, 1)), 
            b(59.75, name='Blue bottom', length=1.5, intensity=(1, 1)), 
            b(61.25, name='Yellow bottom', length=5, intensity=(1, 1)), 

            # second to last
            b(66.25, name='Blue bottom', length=9.75, intensity=(1, 1)), 
            
            # This beat takes us into the next section
            b(76, name='Yellow bottom', length=1, intensity=(1, 1)), 
            #--------------------------------------------------------------#
            # This part repeats in 8 bar sections, but with some variations
            b(76, name='Red top', length = 64),
            # same as before part but with laser sounds???
            b(140, name='Blue top', length = 24),
            # break down part 1
            b(164, name='Green top', length = 8),
            # back to normal beat
            b(172, name='Blue top', length = 24),
            # break down part 2
            b(196, name = 'Green top', length = 8),
            # back to normal beat but this one has a quieter first half
            b(204, name='Blue top', length = 64),
            #-------------------------------------------------------------#
            # this part kind of trades off 1 section of 8, then second section of 8
            # on and off until the end
            b(268, name='Pink bottom', length = 110),
            


        ]
    }
}