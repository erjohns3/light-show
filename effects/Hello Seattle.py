from effects.compiler import *

effects = {
    "Hello Seattle": {
        "bpm": 120,
        "song_path": "songs/Hello Seattle.ogg",
        "delay_lights": 0.23099999999999998,
        "skip_song": 0.0,
        "beats": [
            # grid_f(1, filename='ricardo.gif', length=100),
            # grid_f(1, filename='nyan.webp', rotate_90=True, length=100),
            # grid_f(1, filename='bart.png', length=100),
            # grid_f(1, filename='dog.jpg', length=100),
            # grid_f(1, text='lmfao', font_size=8, length=100),
            # grid_f(1, function=winamp_grid, preset='202.milk', length=400),
            # grid_f(1, function=winamp_grid, preset='202.milk', length=400),

            # b(1, name='autogen circle pulsing', length=400),

            grid_f(1, function=winamp_grid, preset='300-beatdetect-bassmidtreb.milk', length=400),
        ]
    }
}

# tests
# 000-empty.milk           110-per_pixel.milk  207-wave.milk             251-wavecode-spectrum.milk
# 001-line.milk            200-wave.milk       210-wave-smooth-00.milk   260-compshader-noise_lq.milk
# 100-square.milk          201-wave.milk       210-wave-smooth-01.milk   261-compshader-noisevol_lq.milk
# 101-per_frame.milk       202-wave.milk       210-wave-smooth-100.milk  300-beatdetect-bassmidtreb.milk
# 102-per_frame3.milk      203-wave.milk       210-wave-smooth-80.milk   README.md
# 103-multiple-eqn.milk    204-wave.milk       210-wave-smooth-90.milk
# 104-continued-eqn.milk   205-wave.milk       210-wave-smooth-99.milk
# 105-per_frame_init.milk  206-wave.milk       250-wavecode.milk