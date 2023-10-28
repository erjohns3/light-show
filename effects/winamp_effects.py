from effects.compiler import *

import random



effects = {

}


known_good_set_1 = set([
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


known_good_set_2 = set([
    'flexi + geiss - bipolar vs- reaction diffusion [mirror scoped] (Jelly 5-5) threx --- Isosceles edit', # really good according to chris
    'Phat_Zylot_EoS Come_fly_with_me_vidio_echo_v2 nz+ digitalia dildoniq law divorcement.milk',
    'stahlregen - hypnotron v 0-5',
    'Hexcollie - Melodic pulsing leds - mash0000 - vegas doesn\'t make life less pointless',
    'shifter - crosshatch colony beta6 - nglasch i\'d knighthf fuckfart',
    'EVET - Targus',
    'xtramartin (961)',
    'ORB - Smoke and Fire (reflecto fuckup)',
    'suksma - n13.milk',
    'martin - crystal palace nz+',
    'Shiroijin - Unicorn Hell, Warp 9 Mr Crusher!!!',
    'EoS - 7th galaxy',
    'EoS - glowsticks v2 05 and proton lights (+Krash\'s beat code) _Phat_remix02c',
])


known_good_set_2_standalone = set([
    'AkashaDude & Geiss - Phahlsce Pseye kniqmbatlech way lots calmer',
    'suksma - dotes hostile undertake + demonlord - blood in your eyes again - flacc',
    'suksma - coal drapes - mrt fsh behooval roam3- nz+ gene phreqshough passive suggestive',
    'suksma - arrange-a-tang - shf radial tripolar swung',
    'Goody + martin - crystal palace - Schizotoxin - The Wild Iris Bloom - mess2 nz+ gordichuck',
    'suksma - satanic teleprompter - lusb',
])



def fuzzy_find(search, collection):
    import thefuzz.process
    # print_yellow('Warning: fuzzy_find doesnt prune any results based on probablity and will return a show no matter what')
    choices = thefuzz.process.extractBests(query=search, choices=collection, limit=3)
    # print_cyan(f'top 3 choices: {choices}, took {time.time() - before_fuzz:.3f} seconds')
    return choices[0][0]


all_titles = list(grid_helpers.winamp_wrapper.preset_name_to_filepath.keys())
# should_exit = True
for name in known_good_set_2:
    result = fuzzy_find(name, all_titles)
    if result != name:
        print(f'{cyan(str(result))}\n{red(str(name))}')
# exit()

# note this code is almost all duped from below
print('Making fake winamp effects because winamp is not running')
for preset_name, preset_filepath in grid_helpers.winamp_wrapper.preset_name_to_filepath.items():
    profiles = ['winamp_all']
    if 'cream-of-the-crop' not in str(preset_filepath):
        profiles.append('winamp_tests')

    autogenable = False
    if preset_name in known_good_set_1: # not forced on in production
        profiles.append('winamp_good_1')
        autogenable = True

    if preset_name in known_good_set_2: # not forced on in production
        profiles.append('winamp_good_2')
        autogenable = True

    if preset_name in known_good_set_2_standalone: # not forced on in production
        profiles.append('winamp_good_standalone')
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