"""
Simple multi-player game with various characters
"""
import numpy.random as ran
from pandas import *
import sys
import copy
from math import sqrt, ceil

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
                    board_copy[i][k][l] = board_copy[i][k][l].team + " " + board_copy[i][k][l].name + ":" + str(
                        board_copy[i][k][l].HP)
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
            vector_distance = sqrt((enemies[i][0] - self_location[0]) ** 2 + (enemies[i][1] - self_location[1]) ** 2)
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
                # roll for crit hit
                if ran.randint(1, 101) < 15:
                    print(self.name + " rolled a Melee crit!")
                    entity.HP = entity.HP - 195
                else:
                    entity.HP = entity.HP - 65
                # infiltrator instakill
                if self.__class__.__name__ == "Infiltrator":
                    entity.HP = -1

    def attack(self, damage):
        shared_location = self.locate_self()
        # check for enemies in cell for melee attack
        for entity in loctracker[shared_location[0]][shared_location[1]]:
            if entity.team != self.team and self.__class__.__name__ != "Turret":  # turrets can't melee!
                self.melee_attack()
        # area attack
        # top left
        if shared_location[0] - 1 >= 0 and shared_location[1] - 1 >= 0:
            for entity in loctracker[shared_location[0] - 1][shared_location[1] - 1]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # middle left
        if shared_location[0] - 1 >= 0:
            for entity in loctracker[shared_location[0] - 1][shared_location[1]]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # bottom left
        if shared_location[0] - 1 >= 0 and shared_location[1] + 1 < field_size:
            for entity in loctracker[shared_location[0] - 1][shared_location[1] + 1]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # bottom middle
        if shared_location[1] + 1 < field_size:
            for entity in loctracker[shared_location[0]][shared_location[1] + 1]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # bottom right
        if shared_location[0] + 1 < field_size and shared_location[1] + 1 < field_size:
            for entity in loctracker[shared_location[0] + 1][shared_location[1] + 1]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # right center
        if shared_location[0] + 1 < field_size:
            for entity in loctracker[shared_location[0] + 1][shared_location[1]]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # right top
        if shared_location[0] + 1 < field_size and shared_location[1] - 1 >= 0:
            for entity in loctracker[shared_location[0] + 1][shared_location[1] - 1]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1
        # top centre
        if shared_location[1] - 1 >= 0:
            for entity in loctracker[shared_location[0]][shared_location[1] - 1]:
                if entity.team != self.team:
                    # FireMen can resist each other's attacks
                    if self.__class__.__name__ == "FireMan" and entity.__class__.__name__ == "FireMan":
                        entity.HP = entity.HP - ceil(damage * 0.3)
                    else:
                        entity.HP = entity.HP - damage
                    # infiltrator instant building destroy
                    if self.__class__.__name__ == "Infiltrator" and (
                            entity.__class__.__name__ == "Turret" or entity.__class__.__name__ == "HealthBox"):
                        entity.HP = -1

    def heal(self):
        shared_location = self.locate_self()
        # only two heroes can heal: the Healer and the HealthBox, so both are hardcoded
        # area heal
        # top left
        if shared_location[0] - 1 >= 0 and shared_location[1] - 1 >= 0:
            for entity in loctracker[shared_location[0] - 1][shared_location[1] - 1]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # middle left
        if shared_location[0] - 1 >= 0:
            for entity in loctracker[shared_location[0] - 1][shared_location[1]]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # bottom left
        if shared_location[0] - 1 >= 0 and shared_location[1] + 1 < field_size:
            for entity in loctracker[shared_location[0] - 1][shared_location[1] + 1]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # bottom middle
        if shared_location[1] + 1 < field_size:
            for entity in loctracker[shared_location[0]][shared_location[1] + 1]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # bottom right
        if shared_location[0] + 1 < field_size and shared_location[1] + 1 < field_size:
            for entity in loctracker[shared_location[0] + 1][shared_location[1] + 1]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # right center
        if shared_location[0] + 1 < field_size:
            for entity in loctracker[shared_location[0] + 1][shared_location[1]]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # right top
        if shared_location[0] + 1 < field_size and shared_location[1] - 1 >= 0:
            for entity in loctracker[shared_location[0] + 1][shared_location[1] - 1]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10
        # top centre
        if shared_location[1] - 1 >= 0:
            for entity in loctracker[shared_location[0]][shared_location[1] - 1]:
                # unlike attack, only works on friendlies
                # buildings cannot be healed
                if entity.team == self.team and entity.__class__.__name__ != "Turret" and entity.__class__.__name__ != "HealthBox":
                    # healer logic
                    if self.__class__.__name__ == "Healer":
                        if entity.HP < entity.MaxHP:
                            entity.HP = entity.HP + 20
                    else:
                        # healthbox logic
                        # healthboxes can't overheal
                        if entity.HP < entity.HP:
                            entity.HP = entity.HP + 10


class SpeedyBoy(Hero):
    HP = 125
    MaxHP = 185

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(3, 105)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)


class RocketMan(Hero):
    HP = 200
    MaxHP = 300

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(24, 112)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)
        # attacks inflict self-damage
        self.HP -= ceil(damage * 0.1)


class FireMan(Hero):
    HP = 175
    MaxHP = 255

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(30, 120)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)


class BlackDynamite(Hero):
    HP = 200
    MaxHP = 255

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(30, 101)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)
        # attacks inflict self-damage
        self.HP -= ceil(damage * 0.05)


class LargeWeapons(Hero):
    HP = 300
    MaxHP = 440

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(3, 135)
        # if damaged, can randomly heal himself to full health, skipping attacks
        if ran.randint(1, 101) < 15 and self.HP < 300:
            # self-heal logic
            self.HP = 300
        else:
            # attack logic
            # crit chance
            if ran.randint(1, 101) < 4:
                print(self.name + " rolled a crit!")
                damage *= 3
            self.attack(damage)


class Builder(Hero):
    HP = 125
    MaxHP = 185

    def build_turret(self):
        shared_location = self.locate_self()
        turr = Turret(self.team, "Turret")
        players.append(turr)
        loctracker[shared_location[0]][shared_location[1]].append(turr)

    def build_healthbox(self):
        shared_location = self.locate_self()
        healthb = HealthBox(self.team, "Turret")
        players.append(healthb)
        loctracker[shared_location[0]][shared_location[1]].append(healthb)

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(3, 90)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)
        # builder may randomly spawn buildings
        # turret detection: assume it doesn't exist and check.  this allows the builder to re-deploy destroyed buildings
        turret_exists = 0
        for player in players:
            if player.__class__.__name__ == "Turret" and player.team == self.team:
                turret_exists = 1
        if ran.randint(1, 101) < 25 and turret_exists == 0:
            self.build_turret()
        # check if healthbox exists and build it randomly
        healthbox_exists = 0
        for player in players:
            if player.__class__.__name__ == "HealthBox" and player.team == self.team:
                healthbox_exists = 1
        if ran.randint(1, 101) < 25 and healthbox_exists == 0:
            self.build_healthbox()


# Builder's spawnables
class Turret(Hero):
    HP = 100
    MaxHP = 100

    def move(self, orig_location, new_location):
        # turrets can't move! this function duplicate is empty
        pass

    def attack_cfg(self):
        # damage is constant
        damage = 48
        # turrets can't crit!
        self.attack(damage)


class HealthBox(Hero):
    HP = 100
    MaxHP = 100

    def move(self, orig_location, new_location):
        # health boxes can't move! this function duplicate is empty
        pass

    def attack_cfg(self):
        # healthbox "attack" is just a heal call
        self.heal()


class Marksman(Hero):
    HP = 125
    MaxHP = 185

    # marksman's attack is very long-ranged. he will hit all enemy players in the same column and  row
    def attack(self, damage):
        shared_location = self.locate_self()
        x_axis = shared_location[0]
        y_axis = shared_location[1]
        # check for enemies in cell for melee attack
        for entity in loctracker[x_axis][y_axis]:
            if entity.team != self.team:
                self.melee_attack()
        # area attack
        # scan x axis
        for x in range(0, field_size):
            for entity in loctracker[x][y_axis]:
                if entity.team != self.team:
                    entity.HP = entity.HP - damage
        # scan y axis
        for y in range(0, field_size):
            for entity in loctracker[x_axis][y]:
                if entity.team != self.team:
                    entity.HP = entity.HP - damage

    def attack_cfg(self):
        # damage spread
        damage = ran.randint(50, 151)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)


class Healer(Hero):
    HP = 150
    MaxHP = 220

    # unlike other heroes, Healer gravitates towards friendlies
    def locate_enemy(self):
        enemies = []
        for i in range(len(loctracker)):
            for k in range(len(loctracker[i])):
                if loctracker[i][k] != []:
                    for element in loctracker[i][k]:
                        if element.team == self.team and element != self:
                            # infiltrator turret ignore
                            if self.__class__.__name__ == "Turret" and element.__class__.__name__ == "Infiltrator":
                                pass
                            # 50% chance of avoiding detection
                            elif element.__class__.__name__ == "Infiltrator" and ran.randint(0, 101) < 50:
                                enemies.append([0, 0])
                            else:
                                enemies.append([i, k])
        return enemies

    def attack_cfg(self):
        # healer can both attack and heal
        # damage spread
        damage = ran.randint(50, 151)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)
        self.heal()
        # Healer can recover health on every move
        if self.HP < 150:
            self.HP += 4




class Infiltrator(Hero):
    HP = 125
    MaxHP = 185

    # infiltrator's melee attacks are insta-kill. Infiltrator also instantly destroys all buildings.
    # infiltrator has a 50% chance of being ignored by enemies and 100% chance of being ignored by buildings
    # these special cases are handled in the main locate_enemy(), attack() and melee_attack()
    def attack_cfg(self):
        # damage spread
        damage = ran.randint(20, 50)
        # crit chance
        if ran.randint(1, 101) < 4:
            print(self.name + " rolled a crit!")
            damage *= 3
        self.attack(damage)


# generate board
loctracker = []
for x in range(0, field_size):
    loctracker.append([[] for _ in range(field_size)])

# spawn players
players = []
a = FireMan("Red", "P1")
players.append(a)
a1 = FireMan("Blue", "P1")
players.append(a1)
c1 = Healer("Blue", "Me1")
players.append(c1)

for player in players:
    player.spawn()

# match prep
round_conter = 1
print("Round #" + str(round_conter))
round_conter += 1
print_board(loctracker)
round_over = 0
while round_over == 0:
    print("Round #" + str(round_conter))
    round_conter += 1
    # calculate remaining teams
    teams_remaining = []
    for player in players:
        teams_remaining.append(player.team)
    if len(set(teams_remaining)) <= 1:
        round_over = 1
        break
    # have all players make their move
    for player in players:
        try:
            player.move(player.locate_self(), player.new_location_calc(player.locate_self(), player.locate_enemy()))
        except:  # if move failed, it's probably a lonely Healer remaining. let him stand in place.
            pass
        player.attack_cfg()
        print_board(loctracker)
        # clean up the bodies after the move
        for player in players:
            if player.HP <= 0:
                # remove from player list
                players.remove(player)
                # remove from teh board
                for i in range(len(loctracker)):
                    for k in range(len(loctracker[i])):
                        if loctracker[i][k] != []:
                            for element in loctracker[i][k]:
                                if element == player:
                                    loctracker[i][k].remove(player)
                # remove from memory
                del player
            # check if there is only one team standing
            teams_remaining = []
            for player in players:
                teams_remaining.append(player.team)
            if len(set(teams_remaining)) <= 1:
                round_over = 1
                break
            print_board(loctracker)
print_board(loctracker)