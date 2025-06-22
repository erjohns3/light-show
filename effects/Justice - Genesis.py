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
            b(76, name='Yellow bottom', length=8, intensity=(1, 1)), 
            #--------------------------------------------------------------#

        ]
    }
}