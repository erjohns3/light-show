

from __future__ import print_function


import time


begin = time.time()
import msaf
import librosa
import seaborn as sns


print(f'importing took {time.time() - begin} seconds')



# Choose an audio file and listen to it
audio_file = "songs/Notion - Hooked.ogg"

# Try one of these label algorithms
boundaries, labels = msaf.process(audio_file, boundaries_id="foote", labels_id="fmc2d")
print(boundaries)
print(labels)

print(f'boundry detection took {time.time() - begin} seconds')
