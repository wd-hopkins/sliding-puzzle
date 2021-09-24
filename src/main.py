import pygame
from pygame.locals import *

from board import Board

win_size = win_width, win_height = 310, 311
white = (255,255,255)
board_size = 5
clock = pygame.time.Clock() 
fps = 30
running = True

pygame.init()
window = pygame.display.set_mode(win_size, pygame.HWSURFACE | pygame.DOUBLEBUF)
board = Board(board_size)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.on_click(event)
    window.fill(white)
    board.render(window)
    pygame.display.update()
    clock.tick(fps)
pygame.quit()

