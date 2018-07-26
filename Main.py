"""
Simple multi-player game with various characters
"""
import numpy.random as ran
from pandas import *
import sys
import copy
from math import sqrt

field_size = 5


def longest(lst):
    if type(lst) is not list:
        return 0
    max = len(lst)
    for i in lst:
        max_i = longest(i)
        if max_i > max:
            max = max_i
    return max


def print_board(board):
    # create a copy of the board and prepare it for print
    board_copy = copy.deepcopy(board)
    for i in range(len(board_copy)):
        for k in range(len(board_copy[i])):
            if board_copy[i][k] != []:
                for l in range(len(board_copy[i][k])):
                    board_copy[i][k][l] = board_copy[i][k][l].name + ":" + str(board_copy[i][k][l].HP)
    print(DataFrame(board_copy))


class Hero(object):
    """Generic class holding all Hero subclasses"""

    def __init__(self, team, name):
        self.team = team
        self.name = name

    def spawn(self):
        # usually it's bad design to control external variables with a function,
        # but here it is justified, since there's only one board
        loctracker[ran.randint(field_size)][ran.randint(field_size)].append(self)

    def locate_self(self):
        for i in range(len(loctracker)):
            for k in range(len(loctracker[i])):
                if self in loctracker[i][k]:
                    return [i, k]
        # location error catcher
        sys.exit("AI error: " + self.name + " could not find itself!")

    def locate_enemy(self):
        enemies = []
        for i in range(len(loctracker)):
            for k in range(len(loctracker[i])):
                if loctracker[i][k] != []:
                    for element in loctracker[i][k]:
                        if element.team != self.team:
                            enemies.append([i, k])
        return enemies

    def move(self, orig_location, new_location):
        # remove bot from old position
        loctracker[orig_location[0]][orig_location[1]].remove(self)
        # add bot at new position
        loctracker[new_location[0]][new_location[1]].append(self)

    def new_location_calc(self, self_location, enemies):
        # go through a list of enemies and find closest one's location
        min_distance = 99999999.0
        target = 0
        for i in range(len(enemies)):
            # use Pythagorean theorem to locate the closest enemy
            vector_distance = sqrt((enemies[i][0]-self_location[0])**2+(enemies[i][1]-self_location[1])**2)
            if vector_distance < min_distance:
                target = i
                min_distance = vector_distance
        # initiate movement
        if enemies[target] == self_location:
            # do not change the location if the closest enemy is in the same cell
            return self_location
        else:
            # x logic
            if enemies[target][0] < self_location[0]:
                # head left if the enemy x is less that player's
                new_x = self_location[0] - 1
            elif enemies[target][0] > self_location[0]:
                # head right if the enemy x is less that player's
                new_x = self_location[0] + 1
            else:
                # else do not move on x axis
                new_x = self_location[0]
            # y logic
            if enemies[target][1] < self_location[1]:
                # head up if the enemy x is less that player's
                new_y = self_location[1] - 1
            elif enemies[target][1] > self_location[1]:
                # head down if the enemy x is less that player's
                new_y = self_location[1] + 1
            else:
                # else do not move on x axis
                new_y = self_location[1]
        return [new_x, new_y]


    def melee_attack(self):
        shared_location = self.locate_self()
        for entity in loctracker[shared_location[0]][shared_location[1]]:
            if entity.team != self.team:
                entity.HP = entity.HP - 65


class SpeedyBoy(Hero):
        HP = 125


# generate board
loctracker = []
for x in range(0, field_size):
    loctracker.append([[] for _ in range(field_size)])

# spawn player
players = []
a = SpeedyBoy("Red", "H1")
players.append(a)
c = SpeedyBoy("Blue", "S1")
players.append(c)
# players.append(c)
for player in players:
    player.spawn()


print_board(loctracker)
print(a.locate_self())
print(a.new_location_calc(a.locate_self(), a.locate_enemy()))
c.move(c.locate_self(), c.new_location_calc(c.locate_self(), c.locate_enemy()))
c.melee_attack()
print_board(loctracker)