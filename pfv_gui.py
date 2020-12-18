#This file contains the pygame code that implements the interactive visualizer GUI
import pygame
import os

#GUI Colors:
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

#Other pygame variables:
pygame.init()
pygame.display.init()

screen_width = 490
screen_height = 490
box_size = 50
margin = 5

font = pygame.font.SysFont("Arial", 28)
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Path Finding Visualizer")
clock = pygame.time.Clock()

#pygame main loop:
done = False
while not done:
    #event detection:
    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = True
            pos = pygame.mouse.get_pos()

    screen.fill(BLACK)

    #draw grid:
    for i in range(0, screen_width, box_size+margin):
        for j in range(0, screen_height, box_size+margin):
            pygame.draw.rect(screen, WHITE, (i, j, box_size), 0)

    #Mouse Click:
    if clicked:

    
    pygame.display.update()

    clock.tick(60) #60FPS

pygame.quit()