import pygame
import sys


class Ball:

    def __init__(self, surface, pos):

        self.surface = surface
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.speedX = 1
        self.speedY = 1

    def draw_ball(self):
        self.circle = pygame.draw.circle(self.surface, (255, 255, 0), (self.x, self.y), 10)


class Player:

    speed = 2

    def __init__(self, surface, color, x, y):

        self.point = 0
        self.color = color
        self.surface = surface
        self.width = 20
        self.height = 80
        self.x = x
        self.y = y
        self.is_winner = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_player(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, self.color, self.rect)


class Game:
    def __init__(self):

        self.is_run = True

        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 120

        self.width = 600
        self.height = 400

        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Paddle game')

        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.text = self.font.render('PaddleGame', True, self.green, self.blue)

        self.win1 = self.font.render('Player 1 Won', True, self.green, self.blue)
        self.win2 = self.font.render('Player 2 Won', True, self.green, self.blue)
        self.winRect = self.win1.get_rect()
        self.winRect.center = (self.width // 2, self.height // 2)

        self.textRect = self.text.get_rect()
        self.textRect.center = (self.width // 2, 20)

        self.player1 = Player(self.surface, (255, 0, 0), 30, self.height/2-40)
        self.player2 = Player(self.surface, (0, 0, 255), self.width - 50, self.height/2-40)
        self.ball = Ball(self.surface, (self.width/2-5, self.height/2+5))

        self.result1 = self.font.render('{}'.format(self.player1.point), True, self.green, self.blue)
        self.result2 = self.font.render('{}'.format(self.player2.point), True, self.green, self.blue)
        self.result_rect1 = self.result1.get_rect()
        self.result_rect2 = self.result2.get_rect()

    def refresh(self):
        pygame.display.flip()
        self.surface.fill((0, 0, 0))

    def set_default(self):
        self.fps = 120
        self.ball.x = self.width / 2 - 5
        self.ball.y = self.height / 2 + 5

    def run(self):

        while True:
            self.surface.blit(self.text, self.textRect)

            self.player1.draw_player()
            self.player2.draw_player()
            self.ball.draw_ball()

            is_collide1 = self.ball.circle.colliderect(self.player1)
            is_collide2 = self.ball.circle.colliderect(self.player2)

            if is_collide1:
                self.ball.speedX = 1
                self.fps += 5

            if is_collide2:
                self.ball.speedX = -1
                self.fps += 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()

            # movement player 1

            if keys[pygame.K_w] and self.player1.y > 0:
                self.player1.y -= Player.speed

            if keys[pygame.K_s] and self.player1.y < self.height - self.player1.height:
                self.player1.y += Player.speed

            # movement player 2

            if keys[pygame.K_UP] and self.player2.y > 0:
                self.player2.y -= Player.speed

            if keys[pygame.K_DOWN] and self.player2.y < self.height - self.player2.height:
                self.player2.y += Player.speed

            self.ball.x += self.ball.speedX
            self.ball.y += self.ball.speedY

            # y change

            if self.ball.y > self.height-10:
                self.ball.speedY *= -1

            if self.ball.y < 0:
                self.ball.speedY *= -1

            # x change

            if self.ball.x == self.width + 10:
                self.player1.point += 1
                self.result1 = self.font.render('{}'.format(self.player1.point), True, self.green, self.blue)
                if self.player1.point < 3:
                    self.set_default()
                else:
                    self.player1.is_winner = True

            if self.ball.x == -10:
                self.player2.point += 1
                self.result2 = self.font.render('{}'.format(self.player2.point), True, self.green, self.blue)
                if self.player2.point < 3:
                    self.set_default()
                else:
                    self.player2.is_winner = True

            if self.player1.is_winner:
                self.surface.blit(self.win1, self.winRect)
            if self.player2.is_winner:
                self.surface.blit(self.win2, self.winRect)

            self.surface.blit(self.result1, self.result_rect1)
            self.surface.blit(self.result2, (self.width - self.result2.get_width(), 0))
            self.refresh()

            self.clock.tick(self.fps)


game = Game()
game.run()
