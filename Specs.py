import pygame as pg

WIDTH, HEIGHT = 1000, 800
FPS = 15
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (46, 139, 87)

SNAKE_IMG = pg.image.load("snek.png")
SQRL_IMG = pg.image.load("sqrl.png")

POPULATION_SIZE = 1
SQRL_POP = 30
SQRL_MATE_CHANCE = .25
