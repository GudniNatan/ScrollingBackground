import pygame
from pygame.locals import *
from Constants import *
from Objects import *
from Methods import *

class Player(pygame.sprite.DirtySprite):
    def __init__(self, rect, charset, sprite_size_rect):
        super(Player, self).__init__()
        self.collision_rect = rect
        self.vx = 0
        self.vy = 0
        self.realX = self.collision_rect.x
        self.realY = self.collision_rect.y
        self.startPoint = [self.collision_rect.x, self.collision_rect.y]
        self.baseSpeed = 0.003 * drawSize
        self.charset = charset
        self.sprite_size_rect = sprite_size_rect
        self.image = pygame.Surface((0, 0))
        self.direction = 180
        self.last_direction = None
        self.set_sprite_direction()
        self.rect = self.image.get_rect()
        self.rect.bottom = rect.bottom - 1
        self.collision_rect.w = self.sprite_size_rect[0]
        if self.collision_rect.w < drawSize / 2 or self.collision_rect.w > drawSize:
            self.collision_rect.w = drawSize - 1
        self.walking_phase = 1
        self.moving = False
        self.next_location = self.collision_rect

    def set_sprite_direction(self, lock_on_to=None):
        vx = self.vx
        vy = self.vy
        if vx == 0 and vy == 0 and self.last_direction is not None:
            self.moving = False
            self.walking_phase = 1
            return
        direction = self.direction
        if vx and vy:
            if vy < 0 and vx < 0:
                direction = 315
            if vy < 0 and vx > 0:
                direction = 45
            if vy > 0 and vx < 0:
                direction = 225
            if vy > 0 and vx > 0:
                direction = 135
        else:
            if vx > 0:
                direction = 90
            elif vx < 0:
                direction = 270
            if vy > 0:
                direction = 180
            elif vy < 0:
                direction = 0
        if vx == 0 and vy == 0:
            self.moving = False
            self.walking_phase = 1
        else:
            self.moving = True
        if direction == self.last_direction:
            return
        self.direction = direction
        self.last_direction = direction
        self.update_sprite()

    def update_sprite(self):
        sprite = 0
        direction = self.direction
        (width, height, desired_width) = self.sprite_size_rect
        self.walking_phase %= 4
        phase = int(self.walking_phase)
        if phase == 3:
            phase = 1

        if 45 > (direction % 360) or (direction % 360) >= 315:
            sprite = self.charset.subsurface(Rect(phase * width, height * 0, width-1, height))
        elif 45 <= (direction % 360) < 135:
            sprite = self.charset.subsurface(Rect(phase * width, height * 1, width-1, height))
        elif 135 <= (direction % 360) < 225:
            sprite = self.charset.subsurface(Rect(phase * width, height * 2, width-1, height))
        elif 225 <= (direction % 360) < 315:
            sprite = self.charset.subsurface(Rect(phase * width, height * 3, width-1, height))
        sprite = aspect_scale(sprite, (desired_width, 100))
        self.image = sprite

    def update_speed(self):
        keys = pygame.key.get_pressed()
        speed = self.baseSpeed
        if keys[K_UP]:
            self.vy = -speed
        if keys[K_DOWN]:
            self.vy = speed
        if keys[K_LEFT]:
            self.vx = -speed
        if keys[K_RIGHT]:
            self.vx = speed
        if keys[K_UP] == keys[K_DOWN]:
            self.vy = 0
        if keys[K_RIGHT] == keys[K_LEFT]:
            self.vx = 0
        self.set_sprite_direction()

    def update_position(self, time):
        if self.vx == 0 and self.vy == 0:
            return
        if time == 0:
            pygame.time.wait(1)
            time = 1
        pixellimit = drawSize / 4  # should not ever be higher than min(drawsize / 2, self.width / 2)
        if -pixellimit < self.vx * time < pixellimit:
            self.realX += self.vx * time
        elif self.vx < 0:
            self.realX -= pixellimit
        else:
            self.realX += pixellimit
        if -pixellimit < self.vy * time < pixellimit:
            self.realY += self.vy * time
        elif self.vy < 0:
            self.realY -= pixellimit
        else:
            self.realY += pixellimit
        rect = self.collision_rect
        rect.x = self.realX
        rect.y = self.realY
        self.rect.midbottom = (rect.centerx, rect.bottom - 1)

    def set_position(self, topleft):
        self.collision_rect.topleft = topleft
        (self.realX, self.realY) = topleft
        self.gridPos = [self.collision_rect.center[0] / drawSize, self.collision_rect.center[1] / drawSize]
        self.rect.midbottom = (self.collision_rect.centerx, self.collision_rect.bottom - 1)
