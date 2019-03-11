from game_object import *
from constants import *
from sprite_tools import *
from block import *
from item import *

class Player(GameObject):

    def __init__(self, game, x, y, idx = 0):
        GameObject.__init__(self, game, x, y, 5, fps = 4)
        self.mana = 0
        self.mana_max = 5
        self.hp = 3
        self.hp_max = 3
        names = ["will", "nick", "vicky", "prava"]
        name = names[idx]
        idle = SpriteSheet(name + ".png", (2, 1), 2)
        hurt = SpriteSheet(name + "_damage.png", (1, 1), 1)
        self.sprite.add_animation({"Idle": idle})
        self.sprite.add_animation({"Hurt": hurt})
        self.sprite.start_animation("Idle")
        self.slash = Slash(self.game, 0, 0)
        self.blocks = []
        self.macros = [None, None, None]
        self.macro = None
        self.blink = -1

        self.macro_tiles = []
        self.game.editor.populate(self.macro_tiles)

        # TODO make this dependent on weapon?
        self.attack_damage = 1

    def update(self, dt):
        GameObject.update(self, dt)
        if self.blink < 0.25 and self.blink >= 0:
            self.blink += dt
        elif self.blink >= 0:
            self.sprite.start_animation("Idle")
            self.blink = -1

    def draw(self, surf):
        GameObject.draw(self, surf)

    def translate(self, dx, dy, attack=True):
        self.sprite.start_animation("Idle")
        if attack and self.attack(dx, dy):
            return True # Able to hit enemy
        if self.map.get((self.x+dx, self.y+dy), ("layer", 4), ("hittable", True)):
            return False # Enemy blocking square
        return GameObject.translate(self, dx, dy)

    def collect(self, items):
        for item in items:
            self.map.remove_from_cell(item, (self.x, self.y))
            if isinstance(item, BlockItem):
                self.blocks += [item.block]
                self.game.editor.populate(self.blocks)
                self.game.tile_pickup.play()

    def attack(self, dx, dy, swing_miss=False):
        # TODO generalize this for different weapon types/interactions
        self.sprite.start_animation("Idle")
        things_hit = self.game.map.get((self.x + dx, self.y + dy), "hittable")
        if len(things_hit) and abs(dx) > 0:
            self.flipped = dx < 0
        for thing in things_hit:
            self.hit(thing)
            self.swing(dx, dy)
        if swing_miss and not things_hit:
            self.swing(dx, dy)
        return len(things_hit)

    def hit(self, thing):
        thing.take_damage(self.attack_damage)
        self.game.camera.shake(0.5)

    def swing(self, dx, dy):
        self.slash.start_slash(self.x+dx, self.y+dy, (dx, dy))
        self.game.swish_noise.play()

    def take_damage(self, damage):
        self.game.camera.shake()
        self.hp -= damage
        self.sprite.start_animation("Hurt")
        self.blink = 0
        if self.hp <= 0:
            self.game.end_level()
        self.game.hit_noise.play()
