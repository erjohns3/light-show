from effects.compiler import *


effects = {

}



if not grid_helpers.winamp_wrapper.winamp_visual_loaded:
    print('Not generating winamp effects because winamp_visual module not loaded')
else:
    for preset_name, preset_filepath in grid_helpers.winamp_wrapper.preset_name_to_filepath.items():
        effects[preset_name] = {
            'length': 1,
            'profiles': ['winamp'],
            'beats': [
                grid_f(1, function=winamp, preset=preset_name, length=400),
            ],
        }