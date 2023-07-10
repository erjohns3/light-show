from effects.compiler import *
import random

# 9, 17, 33, 41, 49 (high) 
#65, 73, 81, 97
# 105, 113, 
# 129 beat
# 161 high hat
# 193singing
# 257 free my mind
# 320
# 440 buliding back up
# 448 kinda drop
# 513 feels like i'm draming
# 577 free my mind
# 640 quiet plus echo
# 705 lasers
# 768 if you want me
# 880 bass pulses in
#898 
# 960 lasers
# 1025 if you wan me
# 


effects = {
    "innerbloom show": {
        "bpm": 122,
        "song_path": "songs/R\u00dcF\u00dcS DU SOL \u25cf\u25cf Innerbloom (Official Video).ogg",
        "delay_lights": 0.3658032786885246,
        "skip_song": 0.0,
        "beats": [
            b(1, name='ib flickers intro 1', length=64), 
            b(65, name='ib flickers intro 2', length=64), 
            b(128.5, name='ib bassline 1 plus', length=64), 
            b(192.5, name='ib feels like', length=64), 
            b(256.5, name='ib free my mind', length=64), 
            b(320.5, name='ib bass no singing', length=64), 
            b(384.5, name='ib mainly high hat', length=64), 
            b(448.5, name='ib drop 1', length=64), 
            b(512.5, name='ib feels like', length=64), 
            b(560, name="control top purple pulse color change", length=16, intensity=(0,1)),
            b(576.5, name='ib free my mind', length=50), 
            b(626.5, name='ib calm before drop', length=128), 
            b(704.5, name='ib lasers intro', length=256),
            b(896.5, name='ib feels like', length=64),
            [960.5, 'ib lasers outro', 64, 1, 1],
            b(1024.5, name='ib flickers outro', length=128, intensity=.6), 
        ]
    },

    "ib flickers intro bottom": {
        "length": 32,
        "beats": [
            b(1, name='control bottom ripple fast', length=8, intensity=(.2, 1), hue_shift=-0.2), 
            b(9, name='control bottom ripple fast', length=8, intensity=(.2, 1),  hue_shift=-0.05), 
            b(17, name='control bottom ripple fast', length=8, intensity=(.2, 1), hue_shift=-0.2), 
            b(25, name='control bottom ripple fast', length=8, intensity=(1,.2), hue_shift=-0.2), 
        ]
    },

    "ib flickers intro bottom fading": {
        "length": 32,
        "beats": [
            b(1, name='control bottom ripple fast', length=8, intensity=(.7, .2), hue_shift=-0.2), 
            b(9, name='control bottom ripple fast', length=8, intensity=(.7, .2),  hue_shift=-0.05), 
            b(17, name='control bottom ripple fast', length=16, intensity=(.7, .2), hue_shift=-0.2), 
        ]
    },

    "ib flickers intro 1": {
        "length": 64,
        "beats": [
            b(1, name='ib flickers intro bottom', length=48), 
            b(49, name='control bottom ripple fast', length=8, intensity=(.2, 1), hue_shift=-0.35), 
            b(57, name='control bottom ripple fast', length=8, intensity=(1,.2), hue_shift=-0.35),
            b(33, name='Blue top', length=32, intensity=(.2, .6)), 
        ]
    },

    "ib flickers outro": {
        "length": 64,
        "beats": [
            b(1, name='ib flickers intro bottom', length=48), 
            b(49, name='control bottom ripple fast', length=8, intensity=(.2, 1), hue_shift=-0.35), 
            b(57, name='control bottom ripple fast', length=8, intensity=(1,.2), hue_shift=-0.35),
        ]
    },

    "ib flickers intro 2": {
        "length": 64,
        "beats": [
            b(1, name='ib flickers intro bottom', length=48), 
            b(49, name='control bottom ripple fast', length=8, intensity=(.2, 1), hue_shift=-0.35), 
            b(57, name='control bottom ripple fast', length=8, intensity=(1,.2), hue_shift=-0.35),
            b(4, name='control top flicker fade', length=6, intensity=(.2, .6)), 
        ]
    },

    "ib pulse bottom": {
        "length": 1,
        "beats": [
            b(1, name='Seafoam bottom', length=.5, intensity=(1,0)), 
        ]
    },

    "ib UV high hat": {
        "length": 1,
        "beats": [
            b(1.5, name='UV', length=.5, intensity=(1,0)), 
        ]
    },

    "ib bassline 1": {
        "length": 32,
        "beats": [
            b(1, name='ib pulse bottom', length=48, intensity=.6), 
            b(9, name='Strobe', length=3, intensity=.6, hue_shift=.6), 
            b(17, name='Strobe', length=3, intensity=.6, hue_shift=.1), 
        ]
    },

    "ib bassline 1 plus": {
        "length": 64,
        "beats": [
            b(1, name='ib bassline 1', length=64), 
            b(9, name='Strobe', length=3, intensity=.6, hue_shift=.7), 
            b(17, name='Strobe', length=3, intensity=.6, hue_shift=.9), 
            b(33, name='ib UV high hat', length=32),
        ]
    },

    "ib feels like bassline": {
        "length": 8,
        "beats": [
            b(1.5, name='White bottom', length=1, intensity=(1,0), hue_shift=.9), 
            b(2.5, name='White bottom', length=.5, intensity=(1,0), hue_shift=.9), 
            b(3, name='White bottom', length=1, intensity=(1,0), hue_shift=.9), 
            b(4.5, name='White bottom', length=.5, intensity=(1,0), hue_shift=.9), 
            b(5, name='White bottom', length=1, intensity=(1,0), hue_shift=.9), 
            b(6.5, name='White bottom', length=.5, intensity=(1,0), hue_shift=.9), 
            b(8, name='Strobe bottom', length=1, intensity=(1,0), hue_shift=.9), 
        ]
    },

    "ib feels like bassline with top": {
        "length": 8,
        "beats": [
            b(1.5, name='White bottom', length=1, intensity=(1,0), hue_shift=.9), 
            b(2.5, name='White bottom', length=.5, intensity=(1,0), hue_shift=.9), 
            b(3, name='White bottom', length=1, intensity=(1,0), hue_shift=.9), 
            b(4.5, name='White bottom', length=.5, intensity=(1,0), hue_shift=.9), 
            b(5, name='White bottom', length=1, intensity=(1,0), hue_shift=.9), 
            b(6.5, name='White bottom', length=.5, intensity=(1,0), hue_shift=.9), 
            b(7.75, name='White bottom', length=.4, intensity=(1,0), hue_shift=.9), 
            b(8.5, name='White top', length=.4, intensity=(1,0), hue_shift=.9), 
        ]
    },

    "ib feels like": {
        "length": 64,
        "beats": [
            b(1, name='ib feels like bassline', length=64), 
            b(1, name='ib UV high hat', length=64),
            b(9, name='Strobe', length=2, intensity=.6, hue_shift=.9), 
            b(17, name='Strobe', length=2, intensity=.6, hue_shift=.9), 
            b(41, name='Strobe front', length=2, intensity=.6, hue_shift=.9), 
            b(49, name='Strobe back', length=2, intensity=.6, hue_shift=.9), 
        ]
    },

    "ib free my mind": {
        "length": 64,
        "beats": [
            b(1, name='ib feels like bassline', length=64), 
            b(1, name='ib UV high hat', length=64),
            b(9, name='Strobe', length=2, intensity=.6, hue_shift=.9), 
            b(17, name='Strobe', length=2, intensity=.6, hue_shift=.9), 
            b(41, name='Strobe front', length=2, intensity=.6, hue_shift=.9), 
            b(49, name='Strobe back', length=2, intensity=.6, hue_shift=.9), 
        ]
    },

    "ib bass no singing": {
        "length": 64,
        "beats": [
            b(1, name='ib feels like bassline with top', length=48), 
            b(1, name='ib UV high hat', length=64),
            b(9, name='Strobe', length=2, intensity=.6, hue_shift=.9), 
            b(17, name='Strobe', length=2, intensity=.6, hue_shift=.9), 
            b(41, name='Strobe front', length=2, intensity=.6, hue_shift=.9), 
            b(49, name='Strobe back', length=2, intensity=.6, hue_shift=.9), 
        ]
    },

    "ib beep boop": {
        "length": 16,
        "beats": [
            b(3.5, name='White top', length=1, intensity=.6, hue_shift=.9),
            b(4.5, name='White top', length=.5, intensity=.4, hue_shift=.9),
            b(12, name='White top', length=.5, intensity=.6, hue_shift=.9),
            b(12.5, name='White top', length=.5, intensity=.4, hue_shift=.9),
            b(15.5, name='White bottom', length=.5, intensity=.4, hue_shift=.9),
        ]
    },

    "ib mainly high hat": {
        "length": 64,
        "beats": [
            b(1, name='ib UV high hat', length=64),
            b(1, name='ib beep boop', length=64),
            b(9, name='Strobe bottom', length=2, intensity=.4, hue_shift=.9), 
            b(17, name='Strobe bottom', length=2, intensity=.4, hue_shift=.9), 
            b(41, name='Strobe bottom', length=2, intensity=.4, hue_shift=.9), 
            b(49, name='Strobe bottom', length=2, intensity=.4, hue_shift=.9), 
        ]
    },

    "ib red pulse top triplet": {
        "length":2,
        "beats": [
            b(1, name='Red top', length=2/3, intensity=(1,0)),
            b(1+2/3, name='Red top', length=2/3, intensity=(1,0)),
            b(1+4/3, name='Red top', length=2/3, intensity=(1,0)),
        ]
    },

    "ib drop 1": {
        "length": 64,
        "beats": [
            b(1, name='ib UV high hat', length=64),
            b(1.5, name='control bottom purple pulse color change', length=32),
            b(1+2/3, name='ib red pulse top triplet', length=16, intensity=(.5,0)),
            b(33.5, name='Rgb disco pulse', length=32),
            #b(33.5, name='control top purple pulse color change', length=32, intensity=(.8, .2)),
            b(33, name='ib feels like bassline with top', length=32),
        ]
    },

    "ib sidechain strobe": {
        "length": .2,
        "beats": [
            b(1, name='Sidechain all but laser', length=.07),           
        ]
    },

    "ib top 8ths": {
        "length": 1/8,
        "beats": [
            b(1, name='Pink top', length=1/16),
            b(1, name='Pink bottom', length=1/16),
        ]
    },

    "ib top 4ths": {
        "length": 1/4,
        "beats": [
            b(1, name='Pink top', length=1/4, intensity=(1,0)),
            b(1, name='Pink bottom', length=1/4, intensity=(1,0)),
        ]
    },

    "ib top halves": {
        "length": 1/2,
        "beats": [
            b(1, name='Pink top', length=1/2, intensity=(1,0)),
            b(1, name='Pink bottom', length=1/2, intensity=(1,0)),
        ]
    },

    "ib get bright": {
        "length": 32,
        "beats": [
            b(1, name='Pink top', length=4),
            b(1, name='Pink bottom', length=4),
            b(4, name='ib sidechain strobe', length=1),
            b(5, name='Pink top', length=4),
            b(5, name='Pink bottom', length=4),
            b(8, name='ib sidechain strobe', length=1),
            b(9, name='ib top 8ths', length=4),
            b(13, name='ib top 4ths', length=8),
            b(21, name='ib top halves', length=12),
        ]
    },

    "ib front back red": {
        "length": 1,
        "beats": [
            b(1, name='Red front', length=.5),
            b(1.5, name='Red back', length=.5),
        ]
    },

    "ib calm before drop": {
        "length": 128,
        "beats": [
            b(1, name='ib get bright', length=32, intensity=(.3,.8)),
            b(33, name='five nights red circle', length=32, hue_shift=-.1, intensity=(.4, .7)),
            b(65, name='ib front back red', length=14, hue_shift=-.1, intensity=(.7, .2)),
        ]
    },

    "ib laser then turn": {
        "length": 1,
        "beats": [
            b(1, name='green laser', length=1),
            b(1.5, name='laser motor', length=.5),
        ]
    },

    "ib firebrick pulse": {
        "length": 1,
        "beats": [
            b(1, name='Firebrick top', length=.5, intensity=(1,.4)),
            b(1.5, name='Firebrick top', length=.5, intensity=(.4, 1)),
        ]
    },

    "ib laser melody": {
        "length": 16,
        "beats": [
            b(1, name='ib laser then turn', length=1),
            b(2.5, name='ib laser then turn', length=1),
            b(4, name='ib laser then turn', length=1),
            b(5.5, name='ib laser then turn', length=1),
            b(7, name='ib laser then turn', length=1),
            b(8.5, name='ib laser then turn', length=1),
            b(15, name='ib laser then turn', length=.5),
            b(16.5, name='ib laser then turn', length=.5),
        ]
    },

    "ib lasers intro": {
        "length": 256,
        "beats": [
            b(1, name='ib front back red', length=64, hue_shift=-.1, intensity=.2),
            b(1, name="ib laser melody", length=16),
            b(17, name='Strobe bottom', length=2, intensity=(.8, .2)),
            b(33, name="ib laser melody", length=16),
            b(49, name='Strobe bottom', length=2, intensity=(.8, .2)),
            b(65, name="ib laser melody", length=16),
            b(65, name="ib flickers intro bottom fading", length=32),
            b(97, name="ib laser melody", length=16),
            b(97, name="ib flickers intro bottom fading", length=32),

            b(129, name="ib laser melody", length=16),
            b(129, name='ib UV high hat', length=64),
            b(129, name="ib flickers intro bottom fading", length=32, hue_shift=-2.2),
            b(145, name='Firebrick top', length=12, intensity=(0,.8)),
            b(157, name='Firebrick top', length=4, intensity=(.8, .2)),
            b(159, name='ib sidechain strobe', length=2),

            b(161, name="ib flickers intro bottom fading", length=24),
            b(161, name="ib laser melody", length=16),
            b(161, name="ib firebrick pulse", length=32, intensity=.3),
            b(185, name="ib pulse bottom", length=8, intensity=(.2, .8)),
        ]
    },

    "ib lasers outro": {
        "length": 64,
        "beats": [
            b(1, name="ib laser melody", length=16),
            b(1, name='ib UV high hat', length=64),
            b(1, name='ib feels like bassline with top', length=64),
            
            b(33, name="ib laser melody", length=16),
        ]
    },

}