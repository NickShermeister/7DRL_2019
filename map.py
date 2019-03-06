from game_object import GameObject
from sprite_tools import *
import random
from constants import *

class Map(object):

    def __init__(self, size = (60, 60)):

        self.cells = []

        self.size = size

        for i in range(size[0]):
            self.cells.append([])
            for j in range(size[1]):
                self.cells[i].append([])


    def populate_random(self, game):
        xmax = len(self.cells)
        ymax = len(self.cells[0])
        for x in range(xmax):
            Wall(game, x, 0)
            Wall(game, x, ymax-1)
        for y in range(ymax):
            Wall(game, 0, y)
            Wall(game, xmax-1, y)
        for x in range(len(self.cells)):
            for y in range(len(self.cells[0])):
                if random.random() < 0.2:
                    Wall(game, x, y)
                else:
                    Tile(game, x, y)


    def populate_rooms(self, game):
        xmax = len(self.cells)
        ymax = len(self.cells[0])
        for x in range(xmax):
            Wall(game, x, 0)
            Wall(game, x, ymax-1)
        for y in range(ymax):
            Wall(game, 0, y)
            Wall(game, xmax-1, y)
            

    def add_to_cell(self, new_item, pos):

        self.cells[pos[0]][pos[1]].append(new_item)
        self.sort_cell(pos)


    def sort_cell(self, pos):
        self.cells[pos[0]][pos[1]].sort(key=lambda a: a.layer)


    def remove_from_cell(self, remove_item, pos):
        if remove_item in self.cells[pos[0]][pos[1]]:
            self.cells[pos[0]][pos[1]].remove(remove_item)
            return remove_item


    def get(self, pos, *args):
        """ Example usage:

        map.get((0, 1), ("layer", 3), ("hidden", 0), "blocking")
        """
        
        things_at_pos = self.cells[pos[0]][pos[1]]
        return_list = []
        for thing in things_at_pos:
            add_to_list = True
            for arg in args:
                if type(arg) == str:
                    if not hasattr(thing, arg) or not getattr(thing, arg):
                        add_to_list = False
                else:
                    if not hasattr(thing, arg[0]) or getattr(thing, arg[0]) != arg[1]:
                        add_to_list = arg[1]==False
            if add_to_list:
                return_list.append(thing)
        return return_list

    def draw(self, surf, xlim, ylim):

        ## Limit bounds if off map
        if xlim[0] < 0: xlim = (0, xlim[1])
        if ylim[0] < 0: ylim = (0, ylim[1])
        if xlim[1] > self.size[1] - 1: xlim = (xlim[0], self.size[1] - 1)
        if ylim[1] > self.size[0] - 1: ylim = (ylim[0], self.size[0] - 1)

        # Draw all tile and detail tiles first
        for x in [i + xlim[0] for i in range(xlim[1] - xlim[0])]:
            for y in [j + ylim[0] for j in range(ylim[1] - ylim[0])]:
                for item in self.get((y, x)):
                    if item.layer in [FLOOR_LAYER, FLOOR_DETAIL_LAYER]:
                        item.draw(surf)

        # Then draw enemies, players, items, etc
        for x in [i + xlim[0] for i in range(xlim[1] - xlim[0])]:
            for y in [j + ylim[0] for j in range(ylim[1] - ylim[0])]:
                for item in self.get((y, x)):
                    if not item.layer in [FLOOR_LAYER, FLOOR_DETAIL_LAYER]:
                        item.draw(surf)


class Tile(GameObject):

    def __init__(self, game, x, y, fps=4):
        GameObject.__init__(self, game, x, y, layer=0, fps=fps)
        self.layer = FLOOR_LAYER
        sprite_paths = [("default_tile" + str(a) + ".png") for a in ["", 0, 1, 2, 3, 4]]
        static = SpriteSheet(random.choice(sprite_paths), (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True

    def draw(self, surf):
        GameObject.draw(self, surf)

class Wall(Tile):

    def __init__(self, game, x, y, fps=4):
        Tile.__init__(self, game, x, y, fps=fps)
        self.layer = WALL_LAYER
        self.blocking = True
        static = SpriteSheet("wall_tile.png", (1, 1), 1)
        self.sprite.add_animation({"Static": static})
        self.sprite.start_animation("Static")
        self.static = True
    


if __name__=="__main__":

    m = Map()
    a = Map()
    a.hidden = True

    m.add_to_cell(a, (3, 3))

