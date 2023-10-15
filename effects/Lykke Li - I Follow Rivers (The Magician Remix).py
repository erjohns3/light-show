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
        "length": 3,
        "beats": [
            *get_circle_pulse_beats(start_beat=1, start_color=GColor.blue, end_color=GColor.purple),
        ],
    },
    "circle pulse color": {
        "beats": [
            grid_f(
                0.125,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=1, color=GColor.red, offset_y=0),
                name='Ok 1',
                start_pos=(0, 0),
                start_color=(100, 0, 0),
                end_color=(0, 100, 0),
                length=1,
            ),
            grid_f(
                0.25,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=2, color=GColor.red, offset_y=0),
                name='Ok 2',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                0.375,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=3, color=GColor.red, offset_y=0),
                name='Ok 3',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                0.5,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=4, color=GColor.red, offset_y=0),
                name='Ok 4',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                .625,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=5, color=GColor.red, offset_y=0),
                name='Ok 5',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                .75,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=6, color=GColor.red, offset_y=0),
                name='Ok 6',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                .875,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=7, color=GColor.red, offset_y=0),
                name='Ok 7',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=8, color=GColor.white, offset_y=0),
                name='Ok 8',
                start_pos=(0, 0),
                end_color=(0, 0, 0),
                length=0.5,
            ),
            grid_f(
                1.125,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=9, color=GColor.white, offset_y=0),
                name='Ok 9',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1.25,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=10, color=GColor.white, offset_y=0),
                name='Ok 10',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1.375,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=11, color=GColor.white, offset_y=0),
                name='Ok 11',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1.5,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=12, color=GColor.white, offset_y=0),
                name='Ok 12',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1.625,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=13, color=GColor.white, offset_y=0),
                name='Ok 13',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1.75,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=14, color=GColor.white, offset_y=0),
                name='Ok 14',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                1.875,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=15, color=GColor.white, offset_y=0),
                name='Ok 15',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
            grid_f(
                2,
                function=our_transform,
                object=get_centered_circle_numpy_nofill(radius=16, color=GColor.white, offset_y=0),
                name='Ok 16',
                start_pos=(0, 0),
                start_color=(100,100,100),
                end_color=(0, 0, 0),
                length=1,
            ),
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
            b(1, name="circle pulse color", length=100),
            b(9, name='ll bass', length=144),

            # b(36, name='ll fill', length=6),
            # b(68, name='ll fill', length=6),
            # b(73, name='verse disco', length=72),
            # b(84, name='ll fill', length=6),
            # b(100, name='ll fill', length=6),
            # b(116, name='ll fill', length=6),
            # b(132, name='ll fill', length=6),
            # b(145, name='ll pre chorus', length=8),
            # b(153, name='ll chorus', length=32),
            # b(185, name='ll bass', length=48),
            # b(191.5, name='ll clap', length=2),
            b(196, name='ll fill', length=6),
            b(207.5, name='ll clap', length=2),
            b(212, name='ll fill', length=6),
            b(223.5, name='ll clap', length=2),
            b(225, name='ll pre chorus', length=8),
            b(233, name='ll chorus', length=32),
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
            b(409, name='ll chorus', length=160),
            b(411, name='UV pulse', length=58),
            b(471, name='ll clap', length=2),
            b(473, name='UV pulse', length=220),
            b(409, name='ll bass', length=160)


            
        ]
    }
}