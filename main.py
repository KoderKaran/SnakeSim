import pygame as pg
import random as ra
import Specs as sp
import Snake as sn

pg.init()

display = pg.display.set_mode((sp.WIDTH, sp.HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)
pg.display.set_caption('Snake Population Simulator')

clock = pg.time.Clock()

crashed = False

sprite_snek = pg.sprite.Group()
snek_list = []
for i in range(sp.POPULATION_SIZE):
    snek = sn.Snake(["r"], ra.randint(0, sp.WIDTH), ra.randint(0, sp.HEIGHT))
    sprite_snek.add(snek)


while not crashed:
    display.fill(sp.GREEN)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
        # if event.type == pg.KEYDOWN:
        #     if event.key == pg.K_LEFT:
        #         sprite_snek.update(-25, 0)
        #     elif event.key == pg.K_RIGHT:
        #         sprite_snek.update(25, 0)
        #     elif event.key == pg.K_UP:
        #         sprite_snek.update(0, -25)
        #     elif event.key == pg.K_DOWN:
        #         sprite_snek.update(0, 25)

    sprite_snek.update(ra.randint(-5, 5), ra.randint(-5, 5))
    for i in sprite_snek:
        if i.rect.x < 0:
            i.rect.x = 0
        if i.rect.x > sp.WIDTH - 25:
            i.rect.x = sp.WIDTH - 25
        if i.rect.y < 0:
            i.rect.y = 0
        if i.rect.y > sp.HEIGHT - 25:
            i.rect.y = sp.HEIGHT - 25

    sprite_snek.draw(display)


    pg.display.update()
    clock.tick(sp.FPS)

pg.quit()
