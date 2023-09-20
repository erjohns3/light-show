import time
import sys
import pathlib
import os

this_file_directory = pathlib.Path(__file__).parent.resolve()
above_file_directory = this_file_directory.parent.resolve()
sys.path.insert(0, str(above_file_directory))

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

from helpers import *


inited_stuff = None
def ensure_init():
    global inited_stuff
    if inited_stuff is None:
        try:
            pygame.init()
            pygame.joystick.init()
            inited_stuff = True
            return True
        except:
            print_stacktrace()
            print_red('PYGAME COULDNT INITIALIZE JOYSTICKS RETURNING NONE')
            return None
    return True

has_inited = set()
def get_avail_joystick():
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        if joystick not in has_inited:
            joystick.init()
            has_inited.add(joystick)
        return joystick

def get_all_events():
    if not ensure_init():
        return

    all_events = []
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            all_events.append(event.type)
            print("Joystick button pressed.")
    return all_events

while True:
    get_all_events()
    time.sleep(.04)


pygame.quit()