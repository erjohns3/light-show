import pathlib
import sys
import os
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

pygame.mixer.init(frequency=48000)


this_file_directory = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(this_file_directory.parent))

from helpers import * 


def play_song(audio_path, start_time, volume=1):
    print(f'Playing {audio_path}')
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(pathlib.Path(audio_path))
    # ffmpeg -i songs/musician2.mp3 -c:a libvorbis -q:a 4 songs/musician2.ogg
    # ffplay songs/shelter.mp3 -ss 215 -nodisp -autoexit
    pygame.mixer.music.play(start=start_time)


def stop_song():
    pygame.mixer.music.stop()


# Starting music "/home/andrew/programming/python/light-show/temp/RIOT - Overkill [Monstercat Release]_asetrate_0.999.ogg" at 4.487245866556211 seconds at 30% volum
# Starting music "songs/RIOT - Overkill [Monstercat Release].ogg" at 4.482758620689656 seconds at 30% volume


before_astrate_path = pathlib.Path("/home/andrew/programming/python/light-show/songs/RIOT - Overkill [Monstercat Release].ogg")
after_astrate_path = pathlib.Path("/home/andrew/programming/python/light-show/temp/RIOT - Overkill [Monstercat Release]_asetrate_0.999.ogg")


volume = .3
og_start = 4.482758620689656
after_start = 4.487245866556211

for i in range(10):
    play_song(before_astrate_path, og_start, volume=volume)
    time.sleep(.2)
    stop_song()
    play_song(after_astrate_path, after_start, volume=volume)
    time.sleep(.2)
    stop_song()

time.sleep(10000)

