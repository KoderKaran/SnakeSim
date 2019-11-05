import pygame as pg
import Specs as sp
import math as ma
import random as ra
from pygame.math import Vector2

ENERGY_TOTAL = 10000


class Snake(pg.sprite.Sprite):
    def __init__(self, display, behaviors, x, y, id):
        pg.sprite.Sprite.__init__(self)
        self.behavior_list = behaviors  # assigns behavior priority list
        self.size = 1  # size of snake
        self.growth_rate = .20  # growth rate of snake
        self.speed = 15  # speed of snake
        self.energy_total = 0  # energy total of snake
        self.maintenance_budget = ma.floor(min((ENERGY_TOTAL/2 - 1000) + ((ENERGY_TOTAL/70) * (self.size + 1)), ENERGY_TOTAL))  # energy budget of snake
        self.growth_budget = ma.floor((self.maintenance_budget/3))  # growth budget of snake
        self.mating_budget = ma.floor((ENERGY_TOTAL - self.maintenance_budget)/3)  # mating budget of snake
        self.storage_budget = max(ENERGY_TOTAL - (self.maintenance_budget + self.growth_budget + self.mating_budget), 0)  # storage budget of snake
        self.maintenance = 0  # maintenance energy totals
        self.growth = 0  # growth energy totals
        self.reproduction = 0  # reproduction energy totals
        self.storage = 0  # storage energy totals
        self.image = sp.SNAKE_IMG  # image of snake
        self.move_chance = .1  # chance that snake moves. will change as generations go
        self.maint_full = False  # checks if maintenance total is above budget
        self.reproduction_full = False  # checks if reproduction total is above budget
        self.growth_full = False  # checks if growth total is above budget
        self.storage_full = False  # checks if storage total is above budget
        self.rect = self.image.get_rect()  # hitbox of snake
        self.rect.x = x  # x coordinate of snake
        self.rect.y = y  # y coordinate of snake
        self.display = display  # window display
        self.v_range = (self.size * 20) + 30  # radius of snake vision circle
        self.vision = pg.draw.circle(display, sp.GREEN, self.rect.center, self.v_range, int(.5))  # snake vision circle
        self.target = None  # first squirrel to be in vision circle of snake
        self.target_id = None  # id number of squirrel in vision circle
        self.id = id  # snakes id number

    def distrib_energy(self):
        # function distributes energy based on behavior priority list
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
        # print("Maintenance: " + str(self.maintenance) + " " + str(self.maintenance_budget) + "\nGrowth: " + str(self.growth) + " " + str(self.growth_budget) + "\nReproduction: " +
        #       str(self.reproduction) + " " + str(self.mating_budget)  + "\nStorage: " + str(self.storage)+ " " + str(self.storage_budget))

    def in_vision(self, sqrl_list):
        # checks if squirrel in vision. if so, sets self.target and self.target_id to appropriate values
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
        # function adds energy when eats and grows when appropriate
        self.energy_total += 1000
        self.size += self.growth_rate
        self.v_range = ma.floor(self.size * 20) + 30

    def update(self, dx, dy):
        # function makes snake chase squirrel if there is one in its vision circle, if not randomly moves
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
        # function makes snake chase squirrel if in vision circle
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
        # moves snake randomly
        self.rect.x += dir_x * self.speed
        self.rect.y += dir_y * self.speed
