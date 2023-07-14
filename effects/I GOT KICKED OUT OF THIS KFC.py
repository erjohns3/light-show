from effects.compiler import *

effects = {
    "looper": {
        "length": 16,
        "beats": [
            grid_f(
                1,
                function=our_transform,
                # object=get_rectangle_numpy(3, 3),
                object=grid_helpers.get_2d_arr_from_text('🫡', font_size=12),
                name='mine',
                start_pos=(12, 0),
                end_pos=(-12, 0),
                # start_scale=(1, 1),
                # end_scale=(2, 2),
                start_rot=0,
                end_rot=6.28,
                length=8,
            ),
            grid_f(
                9,
                function=our_transform,
                object='mine',
                end_pos=(12, 0),
                # end_scale=(1, 1),
                end_rot=0,
                length=8,
            ),
        ]
    },
    "I GOT KICKED OUT OF THIS KFC": {
        "bpm": 140,
        "song_path": "songs/I GOT KICKED OUT OF THIS KFC.ogg",
        "delay_lights": 0.31862142857142856,
        "skip_song": 0.0,
        "beats": [
            b(1, name='looper', length=1000)
        ]
    }
}