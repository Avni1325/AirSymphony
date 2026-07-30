import pygame
import time

pygame.init()

pygame.mixer.music.load("songs/song1.mp3")

pygame.mixer.music.play()

print("Playing song...")

while pygame.mixer.music.get_busy():
    time.sleep(1)

print("Song finished")