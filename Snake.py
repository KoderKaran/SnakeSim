import pygame as pg
import Specs as sp
import math as ma
import random as ra
from pygame.math import Vector2

ENERGY_TOTAL = 10000
# Work on snake


class Snake(pg.sprite.Sprite):
    def __init__(self, display, behaviors, x, y):
        pg.sprite.Sprite.__init__(self)
        self.behavior_list = behaviors
        self.size = 3
        self.speed = 5
        self.energy_total = 0
        self.maintenance_budget = ma.floor(min((ENERGY_TOTAL/2 - 1000) + ((ENERGY_TOTAL/70)
                                                                          * (self.size + 1)), ENERGY_TOTAL))
        self.growth_budget = ma.floor((self.maintenance_budget/3))
        self.mating_budget = ma.floor((ENERGY_TOTAL - self.maintenance_budget)/3)
        self.storage_budget = max(ENERGY_TOTAL - (self.maintenance_budget + self.growth_budget + self.mating_budget), 0)
        self.image = sp.SNAKE_IMG
        self.move_chance = .10
        self.maint_full = False
        self.reproduction_full = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.v_range = self.size * 17
        self.vision = pg.draw.circle(display, sp.BLACK, self.rect.center, self.v_range, 1)
        self.target = None
        self.target_id = None

    def in_vision(self, sqrl_list):
        seen = []
        seen_id = []
        for i in sqrl_list:
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

    def eat(self):
        self.energy_total += 1000

    def update(self, dx, dy):
        self.vision = pg.draw.circle(self.display, sp.BLACK, self.rect.center, self.v_range, 1)
        if self.target is None:
            if not self.reproduction_full:
                check = ra.uniform(0, 1)
                if check <= self.move_chance:
                    self.move(dx, dy)
            else:
                self.move(dx, dy)
        else:
            self.chase_prey()

    def chase_prey(self):
        dir_x = 0
        dir_y = 0
        if self.rect.x < self.target[0]:
            dir_x = 1.5
        elif self.rect.x > self.target[0]:
            dir_x = -1.5

        if self.rect.y < self.target[1]:
            dir_y = 1.5
        elif self.rect.y > self.target[1]:
            dir_y = -1.5

        self.move(dir_x, dir_y)

    def move(self, dir_x, dir_y):
        self.rect.x += dir_x * self.speed
        self.rect.y += dir_y * self.speed
