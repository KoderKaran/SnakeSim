import pygame as pg
import Specs as sp


class Squirrel(pg.sprite.Sprite):
    def __init__(self, display, x, y, id):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.reg_speed = 7
        self.flight_speed = 7
        self.image = sp.SQRL_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vision = pg.draw.circle(display, sp.BLACK, self.rect.center, 50, 1)
        self.id = id

    def update(self, v_movement, h_movement):   # v_movement is vertical, h_movement is horizontal
        self.rect.x += self.reg_speed * v_movement
        self.rect.y += self.reg_speed * h_movement
        self.vision = pg.draw.circle(self.display, sp.BLACK, self.rect.center, 30, 1)

