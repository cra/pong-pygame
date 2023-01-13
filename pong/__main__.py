import random

import pygame

from .ball import Ball
from .colors import BLACK, WHITE
from .dimensions import LX0, LY0, RIGHT, RX0, RY0, SCORE_LEFT_XY, SCORE_RIGHT_XY, SIZE, SPEED, TOP, VMAX, XMID, YMID
from .paddle import AIPaddle, Paddle


class Pong:
    def __init__(self):
        size = SIZE
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pong")

        self.clock = pygame.time.Clock()

        left = Paddle(WHITE, 10, 100)
        left.rect.x = LX0
        left.rect.y = LY0
        self.left = left

        right = AIPaddle(WHITE, 10, 100)
        right.rect.x = RX0
        right.rect.y = RY0
        self.right = right

        ball = Ball(WHITE, 10, 10)
        ball.rect.x = XMID
        ball.rect.y = YMID
        self.ball = ball

        sprites = pygame.sprite.Group()
        sprites.add(left)
        sprites.add(right)
        sprites.add(ball)
        self.sprites = sprites

        self.font = pygame.font.Font(None, 74)

        self.it_is_on = True
        self.alone = True

    def keys(self, pressed):
        # dvorak idiots
        if pressed[pygame.K_COMMA]:
            self.left += SPEED
        if pressed[pygame.K_o]:
            self.left -= SPEED

        # normies
        if pressed[pygame.K_w]:
            self.left += SPEED
        if pressed[pygame.K_s]:
            self.left -= SPEED

        # weird people with friends
        if pressed[pygame.K_UP] and not self.alone:
            self.right += SPEED
        if pressed[pygame.K_DOWN] and not self.alone:
            self.right -= SPEED

        # skynet predecessor switch
        if pressed[pygame.K_SPACE]:
            self.alone = not self.alone

    def game(self):
        # your move, ai
        if self.alone:
            self.right.do_your_worst(self.ball)

        # handle boundaries
        if self.ball.rect.x <= 0:
            self.right.score += 1
            self.ball.reset(XMID, YMID)
        if self.ball.rect.x >= RIGHT:
            self.left.score += 1
            self.ball.reset(XMID, YMID)
        if self.ball.rect.y < 0 or self.ball.rect.y > TOP:
            self.ball.v[1] = -self.ball.v[1]

        # bounce of the paddles
        if any(map(lambda p: pygame.sprite.collide_mask(self.ball, p), (self.left, self.right))):
            self.ball.v[0] = -self.ball.v[0]
            self.ball.v[1] = random.randint(-VMAX, VMAX)

    def scores(self):
        self.screen.blit(self.left.points(self.font), SCORE_LEFT_XY)
        self.screen.blit(self.right.points(self.font), SCORE_RIGHT_XY)

    def __call__(self):
        while self.it_is_on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.it_is_on = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.it_is_on = False

            self.keys(pygame.key.get_pressed())
            self.sprites.update()

            self.game()

            self.screen.fill(BLACK)
            pygame.draw.line(self.screen, WHITE, (SIZE[0] / 2, 0), (SIZE[0] / 2, SIZE[1]), 3)

            self.sprites.draw(self.screen)

            self.scores()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    pygame.init()
    game = Pong()
    game()
    pygame.quit()
