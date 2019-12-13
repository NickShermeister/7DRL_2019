import pygame

WINDOW_WIDTH = 240
WINDOW_HEIGHT = 180
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
SCALE = 3
BLIT_SIZE = (WINDOW_WIDTH*SCALE, WINDOW_HEIGHT*SCALE)
X_GIRTH, Y_GIRTH = 10, 8

FLOOR_LAYER = 0
FLOOR_DETAIL_LAYER = 1
WALL_LAYER = 2
ITEM_LAYER = 3
PLAYER_LAYER = 4
ENEMY_LAYER = 5
FACE_MONKEY_LAYER = 6

PLAYER_DELAY = 1

TILE_SIZE = 20
REBOUND = 12
HOP = 12
REBOUND_DURATION = 0.18
HOP_DURATION = 0.1

RIGHT = (1,0)
LEFT = (-1,0)
DOWN = (0,1)
UP = (0,-1)
SPACE = (0,0)
directions = [UP, DOWN, LEFT, RIGHT]
ACTIONS = [UP, DOWN, LEFT, RIGHT, SPACE]
corners = [ (-1, -1), (1, 1), (-1, 1), (1, -1) ]
far_squares = [(0,2), (2,0), (0, -2), (-2,0)]
neighbors = directions + corners + [(0,0)]
all_squares = directions + corners + far_squares
far_squares2 = [(-3,0), (-2,1), (-1,2), (0,3), (1,2), (2,1), (3,0), (2,-1), (1,-2), (0,-3), (-1,-2), (-2,-1)]
all_squares2 = all_squares + far_squares2
"""
			03
		-12	02	12
	-21	-11	01	11	21
-30	-20	-10	00	10	20	30
	-2-1-1-10-1	1-1	2-1
		-1-20-2	1-2
			0-3
"""
KEYDICT = {pygame.K_a: "a",
           pygame.K_b: "b",
           pygame.K_c: "c",
           pygame.K_d: "d",
           pygame.K_e: "e",
           pygame.K_f: "f",
           pygame.K_g: "g",
           pygame.K_h: "h",
           pygame.K_i: "i",
           pygame.K_j: "j",
           pygame.K_k: "k",
           pygame.K_l: "l",
           pygame.K_m: "m",
           pygame.K_n: "n",
           pygame.K_o: "o",
           pygame.K_p: "p",
           pygame.K_q: "q",
           pygame.K_r: "r",
           pygame.K_s: "s",
           pygame.K_t: "t",
           pygame.K_u: "u",
           pygame.K_v: "v",
           pygame.K_w: "w",
           pygame.K_x: "x",
           pygame.K_y: "y",
           pygame.K_z: "z",
           pygame.K_SPACE: " "}
