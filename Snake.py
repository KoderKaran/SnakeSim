import pygame as pg
import Specs as sp
import math as ma
import random as ra
from pygame.math import Vector2

ENERGY_TOTAL = 10000
# Work on snake


class Snake(pg.sprite.Sprite):
    def __init__(self, display, behaviors, x, y, id):
        pg.sprite.Sprite.__init__(self)
        self.behavior_list = behaviors
        print(self.behavior_list)
        self.size = 1
        self.growth_rate = .20
        self.speed = 15
        self.energy_total = 0
        self.maintenance_budget = ma.floor(min((ENERGY_TOTAL/2 - 1000) + ((ENERGY_TOTAL/70)
                                                                          * (self.size + 1)), ENERGY_TOTAL))
        self.growth_budget = ma.floor((self.maintenance_budget/3))
        self.mating_budget = ma.floor((ENERGY_TOTAL - self.maintenance_budget)/3)
        self.storage_budget = max(ENERGY_TOTAL - (self.maintenance_budget + self.growth_budget + self.mating_budget), 0)
        self.maintenance = 0
        self.growth = 0
        self.reproduction = 0
        self.storage = 0
        self.image = sp.SNAKE_IMG
        self.move_chance = .1
        self.maint_full = False
        self.reproduction_full = False
        self.growth_full = False
        self.storage_full = False
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.display = display
        self.v_range = (self.size * 20) + 30
        self.vision = pg.draw.circle(display, sp.GREEN, self.rect.center, self.v_range, int(.5))
        self.target = None
        self.target_id = None
        self.id = id

    def distrib_energy(self):
        for i in self.behavior_list:
            if i == "m":
                if self.energy_total >= self.maintenance_budget:
                    self.maintenance = self.maintenance_budget
                    self.maint_full = True
                else:
                    self.maint_full = False
                    self.maintenance = self.energy_total
                self.energy_total = self.energy_total - self.maintenance
            if i == "r":
                if self.energy_total >= self.mating_budget:
                    self.reproduction = self.mating_budget
                    self.reproduction_full = True
                else:
                    self.reproduction_full = False
                    self.reproduction = self.energy_total
                self.energy_total = self.energy_total - self.reproduction
            if i == "g":
                if self.energy_total >= self.growth_budget:
                    self.growth = self.growth_budget
                    self.growth_full = True
                else:
                    self.growth_full = False
                    self.growth = self.energy_total
                self.energy_total = self.energy_total - self.growth
            if i == "s":
                if self.energy_total >= self.storage_budget:
                    self.storage = self.storage_budget
                    self.storage_full = True
                else:
                    self.storage_full = False
                    self.storage = self.energy_total
                self.energy_total = self.energy_total - self.storage
        print("Maintenance: " + str(self.maintenance) + " " + str(self.maintenance_budget) + "\nGrowth: " + str(self.growth) + " " + str(self.growth_budget) + "\nReproduction: " +
              str(self.reproduction) + " " + str(self.mating_budget)  + "\nStorage: " + str(self.storage)+ " " + str(self.storage_budget))

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
        self.size += self.growth_rate
        self.v_range = ma.floor(self.size * 20) + 30

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
