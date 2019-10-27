import pygame as pg
import Specs as sp
import math as ma
import random as ra

ENERGY_TOTAL = 10000


class Snake:
    def __init__(self, behaviors, x, y):
        self.behavior_list = behaviors
        self.size = 1
        self.energy_total = 0
        self.maintenance_budget = ma.floor(min((ENERGY_TOTAL/2 - 1000) + ((ENERGY_TOTAL/70) * (self.size + 1)), ENERGY_TOTAL))
        self.growth_budget = ma.floor((self.maintenance_budget/3))
        self.mating_budget = ma.floor((ENERGY_TOTAL - self.maintenance_budget)/3)
        self.storage_budget = max(ENERGY_TOTAL - (self.maintenance_budget + self.growth_budget + self.mating_budget), 0)
        self.image = sp.SNAKE_IMG
        self.curr_x = x
        self.curr_y = y
        self.move_chance = .10
        self.maint_full = False
        self.reproduction_full = False
        # print(self.maintenance_budget + self.growth_budget + self.mating_budget + self.storage_budget)
        # print(self.maintenance_budget, self.growth_budget, self.mating_budget, self.storage_budget )
        # print("\n")

    def move_check(self, display, dx, dy):
        if not self.reproduction_full:
            check = ra.uniform(0, 1)
            if check <= self.move_chance:
                self.move(display, dx, dy)
        else:
            self.move(display, dx, dy)

    def move(self, display, delta_x, delta_y):
        new_x = self.curr_x + delta_x
        new_y = self.curr_y + delta_y
        self.curr_x = new_x
        self.curr_y = new_y
        display.blit(self.image, (new_x, new_y))
