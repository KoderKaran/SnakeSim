import pygame as pg
import random as ra
import Specs as sp
import Snake as sn
import time as tm
import Food as fd

pg.init()
# ^^^ Initializes pygame

display = pg.display.set_mode((sp.WIDTH, sp.HEIGHT), pg.RESIZABLE | pg.DOUBLEBUF)
pg.display.set_caption('Snake Population Simulator')
# ^^^ Display initialization

clock = pg.time.Clock()
crashed = False
# ^^^ More Pygame initialization

possible_behaviors = ["m", "s", "g", "r"]
# ^^^ Possible behaviors for snakes.
# m=maintenance s=storage g=growth r=reproduction

sprite_snek = pg.sprite.Group()
sprite_sqrl = pg.sprite.Group()
# ^^^ Group of snakes and squirrels

for i in range(sp.POPULATION_SIZE):  # Runs below code POPULATION_SIZE amount of times.
    behave = ra.sample(possible_behaviors, len(possible_behaviors))
    # ^^^ randomizes the order of behaviors for each snake
    snek = sn.Snake(display, behave, ra.randint(0, sp.WIDTH), ra.randint(0, sp.HEIGHT), i)
    sprite_snek.add(snek)
    # ^^^ makes snake and adds it to snakes group

for i in range(sp.SQRL_POP):  # Runs below code SQRL_POP amount of times.
    sqrl = fd.Squirrel(display, ra.randint(0, sp.WIDTH), ra.randint(0, sp.HEIGHT), i)
    sprite_sqrl.add(sqrl)
    # ^^^ makes snake and adds it to squirrel group

day = 0
sqrl_count = 1
start_time = tm.time()
# ^^^ more variables to initialize
while not crashed:  # loop to keep simulation going until crashed is True
    display.fill(sp.GREEN)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True
    # ^^^ If user clicks x button, window closes
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                sprite_snek.update(-1, 0)
            elif event.key == pg.K_RIGHT:
                sprite_snek.update(1, 0)
            elif event.key == pg.K_UP:
                sprite_snek.update(0, -1)
            elif event.key == pg.K_DOWN:
                sprite_snek.update(0, 1)
        # ^^^ ability to move snake with arrow keys. for testing

    for i in sprite_snek:
        snek_sees = i.in_vision(sprite_sqrl)
    # ^^^ checks if snake sees squirrel

    for i in sprite_sqrl:
        i.in_vision(sprite_snek)
    # ^^^ checks to see if squirrel sees snake

    for i in sprite_snek:
        i.update(ra.randint(-1, 1), ra.randint(-1, 1))
    # ^^^ moves snake randomly

    for i in sprite_sqrl:
        i.update(ra.randint(-1, 1), ra.randint(-1, 1))
    # ^^^ moves squirrel randomly

    for snake in pg.sprite.groupcollide(sprite_snek, sprite_sqrl, 0, 1).keys():
        snake.eat()
    # ^^^ every time snake collides with squirrel, squirrel is eaten

    for sqrl in pg.sprite.groupcollide(sprite_sqrl, sprite_sqrl, 0, 0).keys():
        if len(sprite_sqrl) < sp.SQRL_POP:
            chance = ra.uniform(0, 1)
            if chance <= sp.SQRL_MATE_CHANCE:
                sqrl = fd.Squirrel(display, sqrl.rect.x, sqrl.rect.y, sp.SQRL_POP + sqrl_count)
                sprite_sqrl.add(sqrl)
                sqrl_count+=1
    # ^^^ if squirrel population is under initial amount, and two squirrels
    #     touch, there is a chance for them to reproduce

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
    # ^^^ above two for loops make sure all sprites stay within the window

    sprite_snek.draw(display)
    sprite_sqrl.draw(display)
    # ^^^ draws all sprites

    if tm.time() - start_time > 30:
        print("End of day " + str(day))
        start_time = tm.time()
        day += 1
        for i in sprite_snek:
            i.distrib_energy()
    # ^^^ ends day and distributes energy with snakes

    pg.display.flip()
    clock.tick(sp.FPS)
    # ^^^ updates sprites depending on FPS

pg.quit()
# ^^^ closes window on x click
