import random

import pygame

from .colors import BLACK
from .dimensions import VMAX


class Ball(pygame.sprite.Sprite):
    def __init__(self, color, w, h):
        super().__init__()

        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, (0, 0, w, h))

        self.v = [random.randint(VMAX // 2, VMAX), random.randint(-VMAX, VMAX)]
        self.rect = self.image.get_rect()

    def reset(self, x, y):
        self.v[1] = random.randint(-VMAX, VMAX)
        self.v[0] *= random.choice((-1, 1))
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]
