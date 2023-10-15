from effects.compiler import *
import grid_helpers

def get_circle_pulse_beats(start_beat=1, start_color=GColor.white, end_color=GColor.red):
    arr = []
    total = 16
    for i in range(total):
        before_color = interpolate_vectors_float(start_color, end_color, i / total)
        after_color = interpolate_vectors_float(start_color, end_color, (i+1) / total)
        arr.append(grid_f(
            start_beat + (i * .125),
            function=our_transform,
            object=get_centered_circle_numpy_nofill(radius=i+1),
            start_color=before_color,
            end_color=after_color,
            length=1,
        ))
    return arr


effects = {
    "ll bass" : {
        "length": 2,
        "beats": [
            b(1, name='Indigo bottom', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),
            b(2, name='Purple bottom', length=.75, hue_shift=.85, sat_shift=-.25, intensity=(1, 0)),        
        ],
    },
    "ll fill" : {
        "length": 6,
        "beats": [
            b(1, name='Cyan top', length=1.5, sat_shift=-.25, intensity=(1, 0)),
            b(2.5, name='Pink top', length=0.5, sat_shift=-.25, intensity=(1, 0)),
            b(3, name='Purple top', length=0.75, sat_shift=-.25, intensity=(1, 0)),
            b(3.75, name='Blue top', length=2.75, sat_shift=-.25, intensity=(1, 0))
        ]
    },
    "ll dom sidechain motor halfs": {
        'length': 1,
        "beats": [
            b(1.15, name='Sidechain motor', length=.85),
        ]
    },
    "ll chorus laser green": {
        'length': 8,
        'autogen': 'laser long',
        "beats": [
            b(1, name='laser motor', length=8),
            b(1, name='ll dom sidechain motor halfs', length=8),
            b(1, name='green laser', length=8),
        ]
    },
    "ll chorus laser red": {
        'length': 8,
        'autogen': 'laser long',
        "beats": [
            b(1, name='laser motor', length=8),
            b(1, name='ll dom sidechain motor halfs', length=8),
            b(1, name='red laser', length=8),
        ]
    },
    "ll chorus": {
        'length': 16,
        'autogen': 'laser long',
        "beats": [
            b(1, name='ll chorus laser green', length=8),
            b(9, name='ll chorus laser red', length=8)
        ]
    },
    "ll pre chorus": {
        'length': 8,
        "beats": [
            b(1, name='UV pulse slow', length=5),
            b(6, name='UV pulse', length=2.5)
        ]
    },
    "ll clap": {
        'length': 2,
        "beats": [
            b(1, name='UV pulse', length=0.5),
            b(1.5, name='UV pulse', length=0.5)
        ]
    },
    "ll bridge" : {
        "length": 4,
        "beats": [
            b(1, name='Indigo bottom', length=4, sat_shift=-.25, intensity=(1, 0)),
        ],
    },
    "verse disco" : {
        "length": 8,
        "beats": [
            b(1, name='Blue disco pulse', length=2),
            b(2.5, name='Blue disco pulse', length=1),
            b(3.5, name='Blue disco pulse', length=1),
            b(5, name='Blue disco pulse', length=2),
            b(6.5, name='Blue disco pulse', length=1),
            b(7.5, name='Blue disco pulse', length=1)
        ]
    },
    "bridge disco" : {
        "length": 10,
        "beats": [
        ]
    },
    "bridge disco" : {
        "length": 10,
        "beats": [
        ]
    },
    "circle pulse": {
        "length": 6,
        "beats": [
            *get_circle_pulse_beats(start_beat=1, start_color=GColor.blue, end_color=GColor.purple),
            *get_circle_pulse_beats(start_beat=4, start_color=GColor.cyan, end_color=GColor.pink),
        ],
    },

    "Lykke Li - I Follow Rivers (The Magician Remix)": {
        "bpm": 122,
        "song_path": "songs/Lykke Li - I Follow Rivers (The Magician Remix).ogg",
        "delay_lights": 0.0252,
        "skip_song": 0.0,
        "beats": [
            # grid_f(1, filename='dog.jpg', rotate_90=False, length=16),
            # grid_f(1, text='😭', rotate_90=True, length=16),
            #grid_f(1, filename='ricardo.gif', rotate_90=False, length=32),
            # grid_f(1, filename='nyan.webp', rotate_90=True, length=8),
            # grid_f(1, function=lambda info: print('hello'), length=16),

            # grid_f(1, text='buy\n  it', font_size=8, length=8),
            b(1, name="twinkle white", length=36),
            b(9, name='ll bass', length=144),
            b(36, name='ll fill', length=6),
            b(42, name="twinkle white", length=26),
            b(68, name='ll fill', length=6),
            b(73, name='verse disco', length=72),
            b(73, name='twinkle white', length=11),
            b(84, name='ll fill', length=6),
            b(90, name='twinkle white', length=10),
            b(100, name='ll fill', length=6),
            b(106, name='twinkle white', length=10),
            b(116, name='ll fill', length=6),
            b(124, name='twinkle white', length=10),
            b(132, name='ll fill', length=6),
            b(138, name='twinkle white', length=7),
            b(145, name='ll pre chorus', length=8),
            b(153, name='circle pulse', length=32),
            b(153, name='ll bass', length=32),
            b(175, name="twinkle white", length=152),
            b(185, name='ll bass', length=48),
            b(191.5, name='ll clap', length=2),
            b(196, name='ll fill', length=6),
            b(207.5, name='ll clap', length=2),
            b(212, name='ll fill', length=6),
            b(223.5, name='ll clap', length=2),
            b(225, name='ll pre chorus', length=8),
            b(233, name='circle pulse', length=32),
            b(265, name='ll bridge', length=48),
            b(276, name='ll fill', length=6),
            b(292, name='ll fill', length=6),
            b(313, name='Blue disco pulse', length=32),
            b(345, name='Rgb disco pulse', length=32),
            b(380, name="twinkle white", length=28),
            b(380, name='Strobe bottom', length=28, sat_shift=.2, intensity=(0, 1)),
            b(372, name='ll fill', length=6),
            b(388, name='ll fill', length=6),
            b(404, name='ll fill', length=6),
            b(409, name='circle pulse', length=160),
            b(409, name='ll bass', length=160),
            b(411, name='UV pulse', length=58),
            b(471, name='ll clap', length=2),
            b(473, name='UV pulse', length=96),
            


            
        ]
    }
}