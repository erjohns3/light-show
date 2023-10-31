import sys
import time
import pathlib
import time
import random

from tqdm import tqdm

this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory))
sys.path.insert(0, str(this_file_directory.parent))
from helpers import *
import winamp_wrapper


if not winamp_wrapper.try_load_winamp_cxx_module():
    print_red(f'winamp_wrapper.try_load_winamp_cxx_module() failed')
    exit()

if not winamp_wrapper.try_load_audio_device():
    print_red(f'winamp_wrapper.try_load_audio_device() failed')
    exit()


random.seed(5)
random.shuffle(winamp_wrapper.all_presets)

time_per_preset = {}
start_time = time.time()
for index, (_, path) in enumerate(tqdm(winamp_wrapper.all_presets)):
    # if index > 100:
    #     break
    winamp_wrapper.load_preset(path, quiet=True)
    winamp_wrapper.compute_frame()

    t1 = time.time()
    winamp_wrapper.load_preset(path, quiet=True)
    winamp_wrapper.compute_frame()
    time_per_preset[path] = time.time() - t1

for path, time_taken in sorted(time_per_preset.items(), key=lambda item: item[1]):
    print(f'{time_taken:.2f} seconds on second run, {path}')
print_green(f'TOTAL load_all_presets.py took {time.time() - start_time:.2f} seconds')




# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo, Martin, Orb, Flexi - Star Forge v7 (HAKAN mash-up) 2-55 [mixwithv6v1bass] remade7d 4.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v14d.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo, Martin, Orb, Flexi - Star Forge v7 (HAKAN mash-up) 2-55 [mixwithv6v1bass] remade7d [[pixel theme]] 0-1 v1.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo - Star Forge v7 (HAKAN mash-up) [[Martin's new theme]].milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v6 tamed.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v6 adagio v2.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v5a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v10.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v9.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v6a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 6-11.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Acid Mandala v1c.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v14a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v12.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v11b.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v10a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v5.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 8-1.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Acid Mandala.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 6-12.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/martin - pixies party.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo, Martin, Orb, Flexi - Star Forge v7 (HAKAN mash-up) 2-55 [mixwithv6v1bass] remade7d [[pixel theme]] 0-7 v2 {more active}.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v13b.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v13c.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 9-1.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/martin - pixies party filth edition.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Cope, Flexi, Martin, Orb - Star Forge v8 hue shifter.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 7.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Acid Mandala v1a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v12a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 6-9.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/Martin - Pixies Party (Hakan mash-up) 8-7.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v5.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4e.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb - Star Forge v14.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Wave Interference/amandio c - interference pattern 3.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v3d.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4d.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v3a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v5a.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v3c.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v5b.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/martin - pixies party d-strux wille.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/martin - pixies party linkwurst love.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4c.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4f.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4b.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Grid/Martin - QBikal - Surface Turbulence nz+ unlinked error.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v3e.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4g.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v4.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Particles/Spaz/martin - pixies party d-strux wille itunes.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Swarm/martin - sphery tales slow version.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Wave Interference/amandio c - interference pattern 2.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v3b.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Swarm/martin - sphery tales.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Waveform/Wire Spirograph/Fumbling_Foo & Flexi, Martin, Orb, Unchained - Acid Mandala v3.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Fractal/Wave Interference/amandio c - interference pattern 4.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Swarm/martin - sphery tales slow version nz+.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Swarm/martin - sphery tales slow version nz.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Sparkle/Squares/amandio c - mosaic 7 - my eyes are glazed over because i am dumb - amber digital colony.milk
# 0.02 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Reaction/Growth/amandio c - prime forms 2 minor full.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Geometric/Squares/amandio c - epicenter zero improvement hackery.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Shapes/Flexi - the vista soap bubble screen saver sucks.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Geometric/Squares/amandio c - epicenter the end of the world we never knew.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Shapes/Flexi - going processing nz.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Dancer/Shapes/Flexi - going processing nz+.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Drawing/Explosions/EVET + Flexi - Dreamsicles.milk
# 0.04 seconds, /home/andrew/programming/python/light-show/winamp/projectm/presets/presets-cream-of-the-crop/Drawing/Explosions/Flexi + geiss - botnet nz+ let us out fractal spiders2 pure opulenth pony.milk
# TOTAL load_all_presets.py