import pygame as pg
import Specs as sp
import math as ma
import random as ra
from pygame.math import Vector2

ENERGY_TOTAL = 10000
# Work on snake


class Snake(pg.sprite.Sprite):
    def __init__(self, behaviors, x, y):
        pg.sprite.Sprite.__init__(self)
        self.behavior_list = behaviors
        self.size = 1
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

        # print(self.maintenance_budget + self.growth_budget + self.mating_budget + self.storage_budget)
        # print(self.maintenance_budget, self.growth_budget, self.mating_budget, self.storage_budget )
        # print("\n")

    def eat(self):
        self.energy_total += 1000

    def update(self, dx, dy):
        if not self.reproduction_full:
            check = ra.uniform(0, 1)
            if check <= self.move_chance:
                self.move(dx, dy)
        else:
            self.move(dx, dy)

    def move(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y
