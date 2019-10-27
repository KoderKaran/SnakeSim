import pygame as pg
import random as ra
import Specs as sp
import Snake as sn

pg.init()

display = pg.display.set_mode(sp.WINDOW_SIZE, pg.RESIZABLE | pg.DOUBLEBUF)
pg.display.set_caption('Snake Population Simulator')

clock = pg.time.Clock()

crashed = False
display.fill(sp.GREEN)
snek_list = []
for i in range(10):
    snek = sn.Snake(["r"], 100, ra.randint(0, 500))
while not crashed:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
        if event == pg.MOUSEBUTTONDOWN:
            for i in snek_list:
                x = ra.randint(-15, 15)
                y = ra.randint(-15, 15)
                i.move_check(display, x, y)

    pg.display.update()
    clock.tick(sp.FPS)

pg.quit()
