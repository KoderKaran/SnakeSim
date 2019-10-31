import pygame as pg
import random as ra
import Specs as sp
import Snake as sn
import Food as fd
import time as tm


pg.init()

display = pg.display.set_mode((sp.WIDTH, sp.HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)
pg.display.set_caption('Snake Population Simulator')

clock = pg.time.Clock()

crashed = False

sprite_snek = pg.sprite.Group()
sprite_sqrl = pg.sprite.Group()
for i in range(sp.POPULATION_SIZE):
    snek = sn.Snake(display, ["g", "m", "s", "r"], ra.randint(0, sp.WIDTH), ra.randint(0, sp.HEIGHT), i)
    sprite_snek.add(snek)

for i in range(sp.SQRL_POP):
    sqrl = fd.Squirrel(display, ra.randint(0, sp.WIDTH), ra.randint(0, sp.HEIGHT), i)
    sprite_sqrl.add(sqrl)
day = 0
sqrl_count = 1
start_time = tm.time()
while not crashed:
    display.fill(sp.GREEN)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                sprite_snek.update(-1, 0)
            elif event.key == pg.K_RIGHT:
                sprite_snek.update(1, 0)
            elif event.key == pg.K_UP:
                sprite_snek.update(0, -1)
            elif event.key == pg.K_DOWN:
                sprite_snek.update(0, 1)

    for i in sprite_snek:
        snek_sees = i.in_vision(sprite_sqrl)

    # for i in sprite_sqrl:
    #     i.in_vision(sprite_snek)

    # for i in sprite_snek:
    #     i.update(ra.randint(-1, 1), ra.randint(-1, 1))

    for i in sprite_sqrl:
        i.update(ra.randint(-1, 1), ra.randint(-1, 1))

    for snake in pg.sprite.groupcollide(sprite_snek, sprite_sqrl, 0, 1).keys():
       # print("Energy before: " + str(snake.energy_total))
        snake.eat()
       # print("Energy after: " + str(snake.energy_total))

    for sqrl in pg.sprite.groupcollide(sprite_sqrl, sprite_sqrl, 0, 0).keys():
        if len(sprite_sqrl) < sp.SQRL_POP:
            chance = ra.uniform(0, 1)
            if chance <= sp.SQRL_MATE_CHANCE:
                sqrl = fd.Squirrel(display, sqrl.rect.x, sqrl.rect.y, sp.SQRL_POP + sqrl_count)
                sprite_sqrl.add(sqrl)
                sqrl_count+=1

    for i in sprite_snek:
        if i.rect.x < 0:
            i.rect.x = 0
        if i.rect.x > sp.WIDTH - 25:
            i.rect.x = sp.WIDTH - 25
        if i.rect.y < 0:
            i.rect.y = 0
        if i.rect.y > sp.HEIGHT - 25:
            i.rect.y = sp.HEIGHT - 25

    for i in sprite_sqrl:
        if i.rect.x < 0:
            i.rect.x = 0
        if i.rect.x > sp.WIDTH - 15:
            i.rect.x = sp.WIDTH - 15
        if i.rect.y < 0:
            i.rect.y = 0
        if i.rect.y > sp.HEIGHT - 15:
            i.rect.y = sp.HEIGHT - 15

    sprite_snek.draw(display)
    sprite_sqrl.draw(display)

    if tm.time() - start_time > 30:
        print("End of day " + str(day))
        start_time = tm.time()
        day += 1
        for i in sprite_snek:
            i.distrib_energy()

    pg.display.flip()
    clock.tick(sp.FPS)


pg.quit()
