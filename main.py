import pygame
import time
from pygame.locals import *
import random

from pygame import event, font
from pygame.constants import KEYDOWN, QUIT

SIZE = 40


class Apple:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.surface = surface
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 20)*SIZE
        self.y = random.randint(1, 20)*SIZE


class Snake:
    def __init__(self, surface, lenght):
        self.lenght = lenght
        self.parent_screen = surface
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*lenght
        self.y = [SIZE]*lenght
        self.direction = 'down'

    def inc_len(self):
        self.lenght += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.lenght-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill((160, 232, 65))

        for i in range(self.lenght):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((800, 800))
        self.snake = Snake(self.surface, 7)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collide(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display()
        pygame.display.flip()

        if self.is_collide(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.inc_len()
            self.apple.move()

        for i in range(3, self.snake.lenght):
            if self.is_collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Collision occured"

    def display(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"score:{self.snake.lenght}", True, (225, 225, 225))
        self.surface.blit(score, (600, 10))

    def game_over(self):
        # self.surface.fill(255,255,255)
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(
            f"Game is over! Your score is {self.snake.lenght}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(
            "To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pass

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for x in pygame.event.get():
                if x.type == KEYDOWN:
                    if x.type == K_ESCAPE:
                        running = False

                    if x.key == K_RETURN:
                        pause = False

                    if not pause:
                        if x.key == K_UP:
                            self.snake.move_up()
                        if x.key == K_DOWN:
                            self.snake.move_down()
                        if x.key == K_LEFT:
                            self.snake.move_left()
                        if x.key == K_RIGHT:
                            self.snake.move_right()

                elif x.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()
