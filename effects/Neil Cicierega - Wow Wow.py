from effects.compiler import *

# https://www.mathworks.com/discovery/affine-transformation.html#:~:text=Affine%20transformation%20is%20a%20linear,with%20non%2Dideal%20camera%20angles.
# Pillow.tranform

# grid_f(1,
#     function=spawn_then_move, 
#     object=arr_2d, 
#     start_pos=(1, 1), 
#     end_pos=(5, 5), 
#     start_scale= (1, 1), 
#     end_scale= (1, 1), 
#     end_pos=(5, 5), 
#     start_rot=5,
#     end_rot=5,
#     length=2,
# ),

effects = {
    "Neil Cicierega - Wow Wow": {
        "bpm": 107,
        "song_path": "songs/Neil Cicierega - Wow Wow.ogg",
        "delay_lights": 0.1725,
        "skip_song": 0.0,
        "beats": [
            grid_f(
                1,
                function=our_transform,
                # object=grid_helpers.get_2d_arr_from_image('oy.png'),
                object=grid_helpers.get_2d_arr_from_text('😋'),
                name='oy',
                start_pos=(0, 0),
                start_rot=0,
                end_rot=7,
                length=8,
            ),
            grid_f(
                9,
                function=our_transform, 
                object='oy',
                end_pos=(5, 0),
                length=8,
            ),
            grid_f(
                17,
                function=our_transform, 
                object='oy',
                start_scale= (1, 1), 
                end_scale=(.5, 1), 
                length=8,
            ),

        ]
    }
}