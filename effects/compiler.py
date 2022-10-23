# start_beat: this is the beat that the pattern will start on
# effect_name: this is the effect that will play
# len: the length in beats
# beat_skip: how many beats in to skip to in the pattern
# hue_shift: -1 - 1
# sat_shift: -1 - 1
# bright_shift: -1 - 1
# rgb: 0 - 100
# green laser: 0 - 100
# red laser: 0 - 100
# laser motor: 0 - 100

def b(start_beat, name=None, length=None, intensity=None, beat_skip=None, hue_shift=None, sat_shift=None, bright_shift=None, top_rgb=None, front_rgb=None, back_rgb=None, bottom_rgb=None, uv=None, green_laser=None, red_laser=None, laser_motor=None):
    if length is None:
        print('length must be defined')
        raise Exception()
    
    if (name or intensity or beat_skip or hue_shift or sat_shift or bright_shift) and (top_rgb or front_rgb or back_rgb or bottom_rgb or uv or green_laser or red_laser or laser_motor):
        print(f'Anything between the sets "name intensity beat_skip hue_shift sat_shift bright_shift" and top_rgb front_rgb back_rgb bottom_rgb uv,  green_laser red_laser laser_motor" cannot be used together, dont use them in the same call')
        raise Exception()
    
    if (back_rgb or front_rgb) and top_rgb:
        print('Cannot define back_rgb or front_rgb if top_rgb is defined')
        raise Exception()


    if name is None:
        if top_rgb:
            front_rgb = top_rgb
            back_rgb = top_rgb
        channel = back_rgb[:] + front_rgb[:] + bottom_rgb[:] + [uv, green_laser, red_laser, laser_motor]
        return [start_beat, channel, length]

    if intensity is None:
        intensity = 1

    if type(intensity) == int:
        intensity = (intensity, intensity)

    if beat_skip is None:
        beat_skip = 0

    if hue_shift is None:
        hue_shift = 0

    if sat_shift is None:
        sat_shift = 0

    if bright_shift is None:
        bright_shift = 0

    final = [
        start_beat,
        name,
        length,
    ] + list(intensity[:]) + [
        beat_skip,
        hue_shift,
        sat_shift,
        bright_shift,
    ]
    return final


# beat(1, 'porter flubs phrase', length=16, intensity=(1, 1), skip=2, hue_shift=, sat_shift=, bright_shift=),
