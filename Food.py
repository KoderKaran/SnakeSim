import pygame as pg
import Specs as sp
import math as ma


class Squirrel(pg.sprite.Sprite):
    def __init__(self, display, x, y, id):
        pg.sprite.Sprite.__init__(self)
        self.display = display
        self.speed = 0
        self.image = sp.SQRL_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.v_range = 50
        self.vision = pg.draw.circle(display, sp.BLACK, self.rect.center, self.v_range, 1)
        self.id = id
        self.target = None
        self.target_id = None

    def in_vision(self, snek_list):
        seen = []
        seen_id = []
        for i in snek_list:
            distance = ma.hypot(self.rect.x - i.rect.x, self.rect.y-i.rect.y)
            if distance < self.v_range:
                seen.append((i.rect.x, i.rect.y))
                seen_id.append(i.id)
        if self.target_id in seen_id:
            ind = seen_id.index(self.target_id)
            self.target = seen[ind]
        else:
            try:
                self.target = seen[0]
                self.target_id = seen_id[0]
            except IndexError:
                self.target = None
                self.target_id = None

    def update(self, dir_x, dir_y):
        self.vision = pg.draw.circle(self.display, sp.BLACK, self.rect.center, 50, 1)
        if self.target is None:
            self.movement(dir_x, dir_y)
        else:
            self.run_away()

    def run_away(self):
        dir_x = 0
        dir_y = 0
        if self.rect.x < self.target[0]:
            dir_x = -1
        elif self.rect.x > self.target[0]:
            dir_x = 1

        if self.rect.y < self.target[1]:
            dir_y = -1
        elif self.rect.y > self.target[1]:
            dir_y = 1
        self.movement(dir_x, dir_y)

    def movement(self, dir_x, dir_y):
        self.rect.x += self.speed * dir_x
        self.rect.y += self.speed * dir_y
