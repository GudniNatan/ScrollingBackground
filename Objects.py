import pygame
from Constants import *
from pygame.locals import *

class SimpleSprite(pygame.sprite.DirtySprite):  # Molds rect to sprite
    def __init__(self, top_left_point, surface):
        super(SimpleSprite, self).__init__()
        self.image = surface
        self.rect = surface.get_rect()
        self.rect.topleft = top_left_point


class SimpleRectSprite(pygame.sprite.DirtySprite):  # Molds sprite to rect, either by cropping or rescaling
    def __init__(self, rect, surface, scale=False):
        super(SimpleRectSprite, self).__init__()
        self.rect = pygame.Rect(rect)
        self.image = surface
        rect.topleft = (0, 0)
        if not scale:
            self.image = surface.subsurface(rect)
        else:
            self.image = pygame.transform.scale(surface, (rect.w, rect.h))

    def move(self, (x, y)):
        self.rect.x += x
        self.rect.y += y

    def move_to(self, (x, y)):
        self.move((x - self.rect.x, y - self.rect.y))

    def rotate_90_degrees_N_times(self, n=1):
        self.image = pygame.transform.rotate(self.image, 90 * n)
        if n % 2 == 1:
            self.rect.size = (self.rect.height, self.rect.width)

