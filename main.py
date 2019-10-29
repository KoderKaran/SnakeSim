import pygame as pg
import random as ra
import Specs as sp
import Snake as sn

pg.init()

display = pg.display.set_mode(sp.WINDOW_SIZE, pg.RESIZABLE | pg.DOUBLEBUF)
pg.display.set_caption('Snake Population Simulator')

clock = pg.time.Clock()

crashed = False

sprite_snek = pg.sprite.Group()
snek_list = []
for i in range(100):
    snek = sn.Snake(["r"], ra.randint(0, 500), ra.randint(0, 500))
    sprite_snek.add(snek)
    # snek_list.append(snek)

while not crashed:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
    sprite_snek.update(ra.randint(-5, 5), ra.randint(-5, 5))
    display.fill(sp.GREEN)
    sprite_snek.draw(display)
    # for i in snek_list:
    #     x = ra.randint(-5, 5)
    #     y = ra.randint(-5, 5)
    #     i.move_check(display, x, y)

    pg.display.flip()
    clock.tick(sp.FPS)

pg.quit()
