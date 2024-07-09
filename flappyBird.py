import pygame
import sys
import random
from pygame.locals import *

class RectPipe:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = -5
        self.flag = False

class Player:
    def __init__(self, x, y):
        self.sprite = pygame.image.load('mynewBird.png')
        scaling_factor = 1.5  # Adjust this factor as needed
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * scaling_factor), int(self.sprite.get_height() * scaling_factor)))
        self.rect = pygame.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())
        self.velocity = 5

class Pipe:
    def __init__(self, image, y, height, isUpperPipe):
        if isUpperPipe:
            image = pygame.transform.flip(image, False, True)
        self.sprite = pygame.transform.scale(image, (image.get_width(), height))
        self.rect = pygame.Rect(screen_width, y, self.sprite.get_width(), height)
        self.velocity = -5

pygame.init()

screen_width = 1280
screen_height = 720
background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
pipe_image = pygame.image.load('pipe.png')

screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Initializing the player
player = Player(100, 100)

gravity = 0.5

pipes = []
rectPipes = []

def create_pipes():
    height1 = random.randint(0, screen_height - (2 * int(screen_height / 3)))
    height2 = screen_height - (height1 + 150)
    pipe1 = Pipe(pipe_image, 0, height1, True)
    pipe2 = Pipe(pipe_image, height1 + 150, height2, False)
    pipes.append(pipe1)
    pipes.append(pipe2)
    rectPipe = RectPipe(pipe1.rect.x, 0, pipe1.rect.width, screen_height)
    rectPipes.append(rectPipe)

ADD_PIPE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_PIPE_EVENT, 1200)
game_over = False
score = 0

# Font setup for score text
score_font = pygame.font.SysFont(None, 50)

def display_score():
    score_text = score_font.render(f'Score: {score}', True, black)
    score_rect = score_text.get_rect(center=(screen_width // 2, 50))
    screen.blit(score_text, score_rect)

# Font setup for game over text
game_over_font = pygame.font.SysFont(None, 150)

def display_game_over():
    game_over_text = game_over_font.render('Game Over', True, red)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, game_over_rect)

# Font setup for restart text
restart_font = pygame.font.SysFont(None, 75)

def display_restart():
    restart_text = restart_font.render('Press ENTER to restart', True, green)
    restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 1.5))
    screen.blit(restart_text, restart_rect)

def reset_game():
    global player, pipes, rectPipes, game_over, score
    player = Player(100, 100)
    pipes = []
    rectPipes = []
    game_over = False
    score = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.velocity = -10
            if event.key == pygame.K_RETURN and game_over:
                reset_game()
        if event.type == ADD_PIPE_EVENT:
            create_pipes()
    if score<1: gravity = 0.4
    player.velocity += gravity
    if not game_over:
        if player.rect.y + player.rect.height < screen_height - 10:
            player.rect.y += player.velocity

        for pipe in pipes:
            pipe.rect.x += pipe.velocity
            if player.rect.colliderect(pipe.rect):
                game_over = True
                print("Game Over")
                break
        
        for rectPipe in rectPipes:
            rectPipe.rect.x += rectPipe.velocity
            if player.rect.colliderect(rectPipe.rect):
                rectPipe.flag = True
            else:
                if rectPipe.flag:
                    score += 1
                    print(score)
                    rectPipe.flag = False    

    screen.fill(white)
    screen.blit(background, (0, 0))
    screen.blit(player.sprite, player.rect)

    for pipe in pipes:
        screen.blit(pipe.sprite, pipe.rect)

    if game_over:
        display_game_over()
        display_restart()
    else:
        display_score()  # Display score during the game

    pygame.display.update()

    clock.tick(60)
