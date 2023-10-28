from effects.compiler import *


effects = {

}


known_good = set([
    'PieturP - HSL-tunnelvisions_morphing3.milk',
    '$$$ Royal - Mashup (236).milk',
    '203.milk',
    'mrt ei cynical engineers working for a backward system unite in circle jerk oink.milk',
    '389.milk',
    'EoS - skylight a3 [trip colors flux2]_phat_Multi_shaped2_zoe_colours3.milk',
    'Adam Fx 2 Zylot -  FierceFX Glowworld 7.milk',
    'suksma - negative infinity for not flinching - thr.milk',
    'Wire Mirror/Serge + Jc - Neon Star Formation003.milk',
    'suksma - dotes hostile undertake - fake rivals real2.milk',
    'fiShbRaiN - witchcraft (metropolish remix) - test - tillex  - bob boyce \'the cell\', pulstar, singh grooves, motor up, pre-filter cyclone.milk',
    'suksma - ignore butte des mortes prayer heap.milk',
    'suksma - satanic teleprompter - sth shd - salientanic FLE.milk',
    '200.milk',
    '207 mrt get out to where the shooting\'s going on.milk',
    'Geiss - Skin Dots 6 (Jelly).milk',
    'drugsincombat - liquifried squid i.milk',
])

if not grid_helpers.winamp_wrapper.winamp_visual_loaded:
    # note this code is almost all duped from below
    print('Making fake winamp effects because winamp is not running')
    for preset_name, preset_filepath in grid_helpers.winamp_wrapper.preset_name_to_filepath.items():
        profiles = ['winamp_all']
        if 'cream-of-the-crop' not in str(preset_filepath):
            profiles.append('winamp_tests')

        autogenable = False
        if preset_name in known_good or True: # not forced on in production
            profiles.append('winamp_good')
            autogenable = True
        
        effects[preset_name] = {
            'length': 1,
            'loop': True,
            'profiles': profiles,
            "autogen": "winamp top" if autogenable else None,
            'beats': [
                [1, "twinkle green", 1]
            ],
        }
else:
    for preset_name, preset_filepath in grid_helpers.winamp_wrapper.preset_name_to_filepath.items():
        profiles = ['winamp_all']
        if 'cream-of-the-crop' not in str(preset_filepath):
            profiles.append('winamp_tests')
        
        if preset_name in known_good:
            profiles.append('winamp_good')

        autogenable = False
        if preset_name in known_good:
            profiles.append('winamp_good')
            autogenable = True
        effects[preset_name] = {
            'length': 1,
            'loop': True,
            'profiles': profiles,
            "autogen": "winamp top" if autogenable else None,
            'beats': [
                grid_f(1, function=winamp, preset=preset_name, priority=-50, length=1),
            ],
        }
