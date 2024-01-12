from effects.compiler import *



effects = {
    "woman sidechain_test": {
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_rectangle_numpy(14, 13),
                name='sidechain_test',
                color=(1, 1, 1),
                start_rot=0,
                end_rot=6.28,
                # start_pos=(0, 0),
                # end_pos=(10, 10),
                length=8,
            ),
            grid_f(
                1, 
                function=sidechain_grid_shape,
                name='sidechain_test',
                length=8,
            ),
        ]
    },


    "Lane 8 - Woman": {
        "bpm": 124,
        "song_path": "songs/Lane 8 - Woman.ogg",
        "delay_lights": -0.0,
        "skip_song": 0.0,
        "beats": [
            grid_f(1, function=winamp_grid, preset='202.milk', length=400),
            b(1, name='woman sidechain_test', length=4000)

        ]
    }
}