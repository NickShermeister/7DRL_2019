import random
import math
from constants import *
from enemy import *


def hazard(enemy):
    enemy.take_damage(1)
    return True

def move_random(enemy):
    random.shuffle(directions)
    for d in directions:
        if enemy.translate(*d):
            return True
    return False

def approach_player(enemy):
    dx = enemy.game.player.x - enemy.x
    dy = enemy.game.player.y - enemy.y
    order = go_to(dx, dy)
    for d in order:
        if enemy.translate(*d):
            return True
    return False

def approach_player_fast(enemy, count = 2):
    for x in range(count-1):
        approach_player(enemy)
    return approach_player(enemy)

def approach_player_smart(enemy):
    dx = enemy.game.player.x - enemy.x + enemy.vx
    dy = enemy.game.player.y - enemy.y + enemy.vy
    if abs(dx - enemy.vx) + abs(dy - enemy.vy) == 1:
        enemy.translate(dx - enemy.vx, dy - enemy.vy)
        return True
    order = go_to(dx, dy)
    for d in order:
        if enemy.translate(*d):
            return True
    return False

def approach_player_smart_fast(enemy, count = 2):
    for x in range(count-1):
        approach_player_smart(enemy)
    return approach_player(enemy)

def approach_player_smart_minelay(enemy):

    enemy.spawn(enemy.x, enemy.y)
    return approach_player_smart(enemy)
    

def charge_player(enemy):
    if not hasattr(enemy, "charging"):
        enemy.charging = False
    player = enemy.game.player
    if enemy.charging:
        if player.x == enemy.x + enemy.vx:
            if player.y == enemy.y + enemy.vy: # Hit player
                enemy.charging = False
        if enemy.translate(enemy.vx, enemy.vy): # Continue charge
            return True
        enemy.charging = False # Hit wall
        return False
    if enemy.map.is_straight_path((enemy.x, enemy.y), (player.x, player.y)):
        order = go_to(player.x - enemy.x, player.y - enemy.y)
        if player.x == enemy.x + order[0][0]:
            if player.y == enemy.y + order[0][1]:
                enemy.translate(*order[0]) # Hit player
                return True
        if enemy.translate(*order[0]): # Start charge
            enemy.charging = True
            return True
    dx = player.x - enemy.x + enemy.vx
    dy = player.y - enemy.y + enemy.vy
    order = go_to(dx, dy)
    for d in order:
        if enemy.translate(*d): # Seek player
            return True
    return False

def go_to(dx, dy):
    order = directions[:]
    if abs(dx) >= abs(dy):
        order[0] = RIGHT if dx>0 else LEFT
        order[1] = DOWN if dy>0 else UP
        order[2] = UP if dy>0 else DOWN
        order[3] = LEFT if dx>0 else RIGHT
    else:
        order[0] = DOWN if dy>0 else UP
        order[1] = RIGHT if dx>0 else LEFT
        order[2] = LEFT if dx>0 else RIGHT
        order[3] = UP if dy>0 else DOWN
    return order
