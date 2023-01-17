from effects.compiler import b

effects = {

    "v white pulse fast front": {
        "length": .2,
        "beats": [
            b(1, name='White front', length=.1, intensity=(1,0)),   
        ]
    },

    "v white pulse fast back": {
        "length": .2,
        "beats": [
            b(1, name='White back', length=.1, intensity=(1,0)),   
        ]
    },

    "v white pulse slow front": {
        "length": .4,
        "beats": [
            b(1, name='White front', length=.2, intensity=(1,0)),   
        ]
    },

    "v white pulse slow back": {
        "length": .4,
        "beats": [
            b(1, name='White back', length=.2, intensity=(1,0)),   
        ]
    },

    "v wrist top": {
        "length": 4,
        "beats": [
            b(1, name='White front', length=1, intensity=(1,0)), 
            b(2, name='White front', length=1, intensity=(1,0)), 
            b(3, name='White back', length=1, intensity=(1,0)), 
            b(4, name='White back', length=1, intensity=(1,0)),   
        ]
    },

    "v disco slow triplets": {
        "length": 4,
        "beats": [ 
            b(1, name='Red disco', length=.33, intensity=(1,0)),  
            b(1.75, name='Green disco', length=.33, intensity=(1,0)),  
            b(2.5, name='Blue disco', length=.33, intensity=(1,0)),  
            b(3.5, name='Green disco', length=.33, intensity=(1,0)),  
            b(4.25, name='Red disco', length=.33, intensity=(1,0)), 
        ]
    },

    "v bottom slow triplets": {
        "length": 4,
        "beats": [
            b(1, name='Red bottom', length=.75, intensity=(1,0), hue_shift=0),  
            b(1.75, name='Red bottom', length=.75, intensity=(1,0), hue_shift=0.2),  
            b(2.5, name='Red bottom', length=.75, intensity=(1,0), hue_shift=0.4),  
            b(3.5, name='Red bottom', length=.75, intensity=(1,0), hue_shift=0.6),  
            b(4.25, name='Red bottom', length=.75, intensity=(1,0), hue_shift=0.8),   
        ]
    },

    "v bottom slow pulse": {
        "length": 8,
        "beats": [
            b(2, name='Red bottom', length=1, intensity=(1,0), hue_shift=0),  
            b(4, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.25),  
            b(6, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.5),  
            b(8, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.75),  
        ]
    },

    "v UV slow triplets": {
        "length": 4,
        "beats": [
            # b(1, name='UV', length=.66, intensity=(1,0)),  
            # b(1.66, name='UV', length=.66, intensity=(1,0)),  
            # b(2.33, name='UV', length=.66, intensity=(1,0)),  
            # b(3.66, name='UV', length=.66, intensity=(1,0)),  
            # b(4.33, name='UV', length=.66, intensity=(1,0)),   
            b(1, name='UV', length=.75, intensity=(1,0)),  
            b(1.75, name='UV', length=.75, intensity=(1,0)),  
            b(2.5, name='UV', length=.75, intensity=(1,0)),  
            b(3.5, name='UV', length=.75, intensity=(1,0)),  
            b(4.25, name='UV', length=.75, intensity=(1,0)),   
        ]
    },

    "v bottom pulse": {
        "length": 8,
        "beats": [
            b(1, name='Red bottom', length=1, intensity=(1,0), hue_shift=0),  
            b(3, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.125),  
            b(5, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.25),  
            b(7, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.375), 
            b(2, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.5), 
            b(4, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.625), 
            b(6, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.75), 
            b(8, name='Red bottom', length=1, intensity=(1,0), hue_shift=0.875),  
        ]
    },

    "v rainbow fast bottom": {
        "length": 2,
        "beats": [
            [1, "Green bottom", 3.7/4, 1, 0],
            [1, "Red bottom", 2.66/4, 0, 1],
            [1+2.66/4, "Red bottom", 3.7/4, 1, 0],
            [1+2.66/4, "Blue bottom", 2.66/4, 0, 1],
            [1+5.32/4, "Blue bottom", 3.7/4, 1, 0],
            [1+5.32/4, "Green bottom", 2.66/4, 0, 1],
        ],
    },

    "v bottom swish": {
        "length": 4,
        "beats": [
            b(1, name='White bottom', length=4),  
            b(1, name='Sidechain bottom b', length=.5, intensity=(1,0)),  
            b(1.5, name='Sidechain bottom g', length=.5, intensity=(0,1)),  
            b(2, name='Sidechain bottom r', length=.5, intensity=(1,0)),  
            b(2.5, name='Sidechain bottom gb', length=.5, intensity=(0,1)),
            b(3, name='Sidechain bottom rg', length=.5, intensity=(1,0)),  
            b(3.5, name='Sidechain bottom rb', length=.5, intensity=(0,1)),
            b(4, name='Sidechain bottom r', length=.5, intensity=(1,0)),  
            b(4.5, name='Sidechain bottom rg', length=.5, intensity=(0,1)),
        ]
    },

    "v firebrick steps bottom": {
        "length": 4,
        "beats": [
            b(1, name='Firebrick bottom', length=1, intensity=(1,1)),  
            b(2, name='Firebrick bottom', length=1, intensity=(.5, .5)),  
            b(3, name='Firebrick bottom', length=1, intensity=(.25, .25)),  
        ]
    },

    "v tongue thing": {
        "length": 4,
        "beats": [
            b(1, name='v white pulse fast front', length=1),   
            b(2, name='v white pulse fast back', length=1),  
            b(3, name='White front', length=.5, intensity=(1,0)),  
            b(3.5, name='White back', length=.5, intensity=(1,0)),  
            b(4, name='White front', length=1, intensity=(1,0)),  
        ]
    },

    "v tongue thing full body": {
        "length": 4,
        "beats": [
            b(1, name='Strobe', length=2),   
            b(1, name='Strobe bottom', length=2, offset=0.1),  
            b(3, name='White top', length=.5, intensity=(1,0)),  
            b(3.5, name='White bottom', length=.5, intensity=(1,0)),  
            b(4, name='White top', length=1, intensity=(1,0)),  
        ]
    },

    "v ahs 1": {
        "length": 16,
        "beats": [
            b(1, name='v wrist top', length=12, intensity=.5),   
            b(1, name='v bottom slow pulse', length=12),
            b(13, name='v tongue thing', length=4),  
        ]
    },

    "v ahs 2": {
        "length": 16,
        "beats": [
            b(1, name='v wrist top', length=12, intensity=.5),   
            b(1, name='v bottom slow pulse', length=12),
            b(13, name='v tongue thing full body', length=4),  
        ]
    },

    "v chum drum 2": {
        "length": 32,
        "beats": [
            b(1, name='Seafoam bottom', length=8, intensity=(1,0)),   
            b(9, name='v UV slow triplets', length=24),
            b(13, name='Seafoam bottom', length=4, intensity=(0,1)),
        ]
    },

    "v chum drum 1": {
        "length": 16,
        "beats": [
            b(1, name='v rainbow fast bottom', length=8, intensity=(.25,1)),   
            b(9, name='v firebrick steps bottom', length=4),
            b(13, name='v UV slow triplets', length=4),
        ]
    },

    "v subdued singing": {
        "length": 16,
        "beats": [
            b(1, name='Red disco', length=10),   
            b(3, name='Green disco', length=10),  
            b(5, name='Blue disco', length=10),    
        ]
    },

    "v laser fast pulsing": {
        "length": 2,
        "beats": [
            b(1, name='laser motor', length=1, intensity=(1, 1)), 
            b(2, name='laser motor', length=1, intensity=(.6, .6)),   
            b(1, name='green laser', length=2),  
        ]
    },

    "v fast circle": {
        "length": 0.75,
        "beats": [
            b(1, name='White bottom', length=.25, intensity=(1, 0)), 
            b(1.25, name='White front', length=.25, intensity=(1,0)),   
            b(1.5, name='White back', length=.25, intensity=(1,0)),  
        ]
    },
    "v circle": {
        "length": 1.5,
        "beats": [
            b(1, name='White bottom', length=.5, intensity=(1, 0)), 
            b(1.5, name='White front', length=.5, intensity=(1,0)),   
            b(2, name='White back', length=.5, intensity=(1,0)),  
        ]
    },
    "v circle slower": {
        "length": 3,
        "beats": [
            b(1, name='White bottom', length=1, intensity=(1, 0)), 
            b(2, name='White front', length=1, intensity=(1,0)),   
            b(3, name='White back', length=1, intensity=(1,0)),  
        ]
    },

    "v goblin mode": {
        "length": 64,
        "beats": [
            b(1, name='v laser fast pulsing', length=64),    
            b(17, name='v fast circle', length=24),  
            b(49, name='v circle', length=8),
            b(57, name='v fast circle', length=8),      
        ]
    },

    "v dash": {
        "length": 8,
        "beats": [
            b(1, name='red laser', length=4,intensity=(1,0)),
            b(5, name='White bottom', length=1, intensity=(1,.5)),
            b(6, name='White bottom', length=1, intensity=(.7,.3)),
            b(7, name='White bottom', length=1, intensity=(.5,.1)),   
            b(8, name='White bottom', length=1, intensity=(.3,0)),   
        ]
    },

    "v bottom sidechain pulse": {
        "length": .5,
        "beats": [
            [1.1, "Sidechain bottom rbg", .1], 
            [1.3, "Sidechain bottom rbg", .1], 
        ],
    },

    "v intro 1": {
        "length": 16,
        "beats": [
            b(1, name='v disco slow triplets', length=16), 
            b(9, name='White bottom', length=4,intensity=(0, .6)),
            b(13, name='White bottom', length=4,intensity=(.6, 0)),
            b(9, name='v bottom sidechain pulse', length=8),
        ]
    },

    "v intro 2": {
        "length": 16,
        "beats": [
            b(1, name='Red disco', length=2), 
            b(3, name='Green disco', length=2), 
            b(5, name='Blue disco', length=2), 
            b(7, name='Rgb disco', length=2), 
            b(9, name='Rgb disco', length=8, intensity=(1,0)), 
        ]
    },

# 1-11 intro
# 12 - Starting beat
#76 - Ahs ( 16 beats repeated)
# 140 - chum drum bedrum 
# 204 - singing more subdued
# 268 - Ahs
# 332 - chum drum bedrum
# 364 - Rap?
# 428 - dash, dash, dash
# 436 - instrumental with symbols
# 460 - Just instrumental (beat cuts out)

    "Vitas - The 7th Element": {
        "bpm": 128,
        "song_path": "songs/Vitas - The 7th Element.ogg",
        "delay_lights": 0.16799999999999998,
        "skip_song": 0.0,
        "beats": [
            b(12, name='v intro 1', length=32),  
            b(44, name='v intro 2', length=32),  
            b(76, name='v ahs 1', length=64) ,
            b(140, name='v chum drum 1', length=64),
            b(204, name='v subdued singing', length=64),
            b(204+32, name='v UV slow triplets', length=32),
            b(268, name='v ahs 2', length=64),
            b(332, name='v chum drum 2', length=32),
            b(364, name='v goblin mode', length=64),
            b(428, name='v dash', length=8),
            b(436, name='Rgb disco pulse', length=24),
            b(436, name='v bottom slow triplets', length=56, intensity=(0.7, 0)),
        ]
    }
}