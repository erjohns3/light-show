import sys
import time
import os

import pygame
 
pygame.init()
pygame.joystick.init()

# pygame.display.set_mode((1,1))
 
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("joystick initialized")

# display = pygame.display.set_mode((300, 300))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        print(f'{event}')
        if event.type == pygame.KEYDOWN:
            print(f'{event} was KEYDOWN')

        if event.type == pygame.JOYBUTTONDOWN:
            print(f'{event} was JOYBUTTONDOWN')

    time.sleep(.01)