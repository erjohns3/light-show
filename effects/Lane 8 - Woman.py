from effects.compiler import *



# cool masking effects:
    # Python: randomly getting preset /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Core/shifter - interference field v3_Phat_Darken_Pop_Edit_v4 EoS edit B dickless.milk

    # Python: loading preset Fractal/Nested Circle/Rozzor vs Esotic - Pixie Party Light (With Liquid Refreshment) Bonus Round.milk, real path: /Users/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Nested Circle/Rozzor vs Esotic - Pixie Party Light (With Liquid Refreshment) Bonus Round.milk▆▆▆


effects = {
    "woman sidechain_test": {
        "beats": [
            grid_f(
                1,
                function=our_transform,
                object=get_rectangle_numpy(14, 13),
                color=(1, 1, 1),
                start_rot=0,
                end_rot=6.28,
                length=8,
            ),
            grid_f(
                1, 
                function=grid_winamp_mask,
                preset='202.milk',
                priority=10000,
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
            b(1, name='woman sidechain_test', length=4000)

        ]
    }
}