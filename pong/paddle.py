import random
import time

import pygame

from .colors import BLACK, WHITE
from .dimensions import AILUCK, AIRAWR, AISPEED, YMAX


class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, w, h):
        super().__init__()

        self.image = pygame.Surface((w, h))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, (0, 0, w, h))

        self.rect = self.image.get_rect()
        self.score = 0

    def __isub__(self, other):
        self.down(other)
        return self

    def __iadd__(self, other):
        self.up(other)
        return self

    def up(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
            self.rect.y = 0

    def down(self, pixels):
        self.rect.y += pixels
        if self.rect.y > YMAX:
            self.rect.y = YMAX

    def points(self, font):
        return font.render(str(self.score), 1, WHITE)


class AIPaddle(Paddle):
    def __init__(self, color, w, h):
        super().__init__(color, w, h)
        self.speed = AISPEED
        self.proebability = AILUCK
        self.rawr = AIRAWR
        self.zloy = time.time()
        self.zatup = time.time()

    def do_your_worst(self, ball):
        t = time.time()
        if t > self.zatup:
            if random.random() <= self.proebability:
                self.zloy = t + self.rawr

        speed = 0 if t > self.zloy else self.speed

        if ball.rect.top < self.rect.top:
            self.rect.centery -= speed
        elif ball.rect.bottom > self.rect.bottom:
            self.rect.centery += speed
