import pygame
import time
from random import randint
from pygame import mixer as bgm

SIZE = 40
SURFACE_X = 1000
SURFACE_Y = 800


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("images audio/apple.jpg")
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = randint(1, int(SURFACE_X/SIZE-1))*SIZE
        self.y = randint(1, int(SURFACE_Y/SIZE-1))*SIZE
        self.draw()


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("images audio/block.jpg")
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = "right"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()

    def move_left(self):
        if self.direction != "right":
            self.direction = "left"

    def move_right(self):
        if self.direction != "left":
            self.direction = "right"

    def move_up(self):
        if self.direction != "down":
            self.direction = "up"

    def move_down(self):
        if self.direction != "up":
            self.direction = "down"

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "left":
            if self.x[0] <= 0:
                self.x[0] = SURFACE_X-SIZE
            else:
                self.x[0] -= SIZE
        if self.direction == "right":
            if self.x[0] >= SURFACE_X-SIZE:
                self.x[0] = 0
            else:
                self.x[0] += SIZE
        if self.direction == "up":
            if self.y[0] <= 0:
                self.y[0] = SURFACE_Y-SIZE
            else:
                self.y[0] -= SIZE
        if self.direction == "down":
            if self.y[0] >= SURFACE_Y-SIZE:
                self.y[0] = 0
            else:
                self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((SURFACE_X, SURFACE_Y))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.play_bgm()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(
            f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def gameOver(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 100)
        gameOverText = font.render("GAME OVER", True, (255, 255, 255))
        self.surface.blit(gameOverText, (SURFACE_X/3-50, SURFACE_Y/3+50))
        pygame.display.update()
        bgm.music.stop()

    def play_bgm(self):
        bgm.music.load("images audio/bg_music_1.mp3")
        bgm.music.set_volume(0.3)
        bgm.music.play()

    def render_background(self):
        bg = pygame.image.load("images audio/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()

        # snake collide with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple.move()
            self.snake.increase_length()
            eat_apple_sound = bgm.Sound(
                "images audio/1_snake_game_resources_ding.mp3")
            eat_apple_sound.set_volume(0.3)
            bgm.Sound.play(eat_apple_sound)

        # snake collide with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.gameOver()
                crash_sound = bgm.Sound(
                    "images audio/1_snake_game_resources_crash.mp3")
                crash_sound.set_volume(0.25)
                bgm.Sound.play(crash_sound)
                raise "game over"

        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_RETURN:
                        if pause == True:
                            pause = False
                            self.play_bgm()

                    if event.key == pygame.K_UP:
                        self.snake.move_up()

                    if event.key == pygame.K_DOWN:
                        self.snake.move_down()

                    if event.key == pygame.K_LEFT:
                        self.snake.move_left()

                    if event.key == pygame.K_RIGHT:
                        self.snake.move_right()

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.gameOver()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()
