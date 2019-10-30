import pygame as pg
import Specs as sp


class Squirrel(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.reg_speed = 7
        self.flight_speed = 7
        self.image = sp.SQRL_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, v_movement, h_movement):   # v_movement is vertical, h_movement is horizontal
        self.rect.x += self.reg_speed * v_movement
        self.rect.y += self.reg_speed * h_movement

