#!/usr/bin/python3
import pygame, sys, time
from random import *
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

WIDTH, HEIGHT = 720,480
PIPE_PROBABILITY = 0.04
PIPE_COOLDOWN = 1 
GAMEOVER_DELAY = 1.5
FPS = 60

fps = pygame.time.Clock()
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Floppy Bird")


class Player(pygame.sprite.Sprite):
    def __init__(self, initial_pos):
        super().__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
        self.image1 = pygame.image.load("./images/flying.png")
        self.image1 = pygame.transform.scale(self.image1, (100,100))
        self.image2 = pygame.image.load("./images/not-flying.png")
        self.image2 = pygame.transform.scale(self.image2, (100,100))
        self.image = self.image1

        self.pos = vec(initial_pos)
        self.vel = 0.0
        self.acc_down = 0.2
        self.acc_up = 0.4

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            self.vel -= self.acc_up
            self.image = self.image1
        else:
            self.vel += self.acc_down
            self.image = self.image2

        self.pos.y += self.vel

        if self.pos.y - self.rect.height > HEIGHT:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.midbottom = self.pos

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.height = randint(150, 350)
        self.surf = pygame.Surface((30,self.height))
        self.surf.fill((randint(10,255),randint(10,255),randint(10,255)))
        self.rect = self.surf.get_rect()
        self.velocity = 2.0
        r = random()
        if r < 0.3:
            self.image = pygame.image.load("./images/pipe1.png")
        elif r > 0.3 and r < 0.6:
            self.image = pygame.image.load("./images/pipe2.png")
        else:
            self.image = pygame.image.load("./images/pipe3.png")

        self.image = pygame.transform.scale(self.image, (self.rect.width*2,self.rect.height))

        if random() > 0.5:
            self.top = False
            self.pos = vec(900,HEIGHT)
        else:
            self.top = True
            self.image = pygame.transform.flip(self.image, False, True)
            self.pos = vec(900,self.height)

    def move(self):
        self.pos.x -= self.velocity
        self.rect.midbottom = self.pos

class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.velocity = 3.0
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (WIDTH*4,HEIGHT))
        self.rect = self.image.get_rect()
        self.pos = vec((0,0))

    def move(self):
        self.pos.x -= self.velocity
        if self.pos.x < -WIDTH*3:
            self.pos.x = 0
        self.image.get_rect().midbottom = self.pos

class Text(pygame.sprite.Sprite):
    def __init__(self, text, size, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.text = text
        self.size = size
        self.color = color

        self.font = pygame.font.SysFont("Britannic Bold", self.size)
        self.text_surf = self.font.render(self.text, 1, self.color)
        self.surf = pygame.Surface((self.width, self.height))

    def render(self):
        self.text_surf = self.font.render(self.text, 1, self.color)
        self.surf.blit(self.text_surf, [self.width,self.height])
###
def updateFile(score):
    f = open('scores.txt', 'r')
    file = f.readlines()
    a = file[0].split(',')
    print(a)
    last = a[1]
    full = str(name) + ',' + str(score)
    if int(last) < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(full)
        file.close()
        return score
    return a[0], last

###
player = Player((WIDTH/2, HEIGHT/2))
pipes = []

game_over_text = Text("GAME OVER!", 100, (205,92,92), 72, 250)
again = Text("press space to play again", 36, (255, 195, 0), 100, 250)

score_text = Text("", 36, (0, 0, 0), 72, 250)
if random() > 0.5:
    background2 = Background("./images/background1.png")
else:
    background2 = Background("./images/background3.png")

background1 = Background("./images/background3.png")
background = background1

all_sprites = pygame.sprite.Group()

running = False
game_over = False
pause = False

use_background1 = False
score = 0
last_time = time.time()
black = (0,0,0)

name = ""
myfont = pygame.font.SysFont("Britannic Bold", 100)
small_font = pygame.font.SysFont("Britannic Bold", 50)


while running is False:
    #display_surface.fill(black)
    display_surface.blit(pygame.image.load("./images/background2.png"),(0,0))

    game_name = myfont.render("Floppy Bird", 1, (205,92,92))
    instructions = small_font.render("press space to start!", 1, (255,211,194))
    name_text = small_font.render("Username: "+ str(name), True, (50,129,232))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                name += event.unicode
            elif event.key == K_BACKSPACE:
                name = name[:-1]
            if event.key == pygame.K_SPACE:
                running = True
        elif event.type == QUIT:
            running = False
            
    display_surface.blit(name_text,(WIDTH/2-150,HEIGHT/2+20))
    display_surface.blit(game_name, (175,175))
    display_surface.blit(instructions, (190, 300))
    pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    display_surface.fill((100,100,100))
    time_delta = time.time() - last_time

        
    if not game_over:
        score += 1

    score_text.text = "Your Score: %d" % score
    score_text.render()

    if game_over and time_delta > GAMEOVER_DELAY:
        if pressed_keys[K_SPACE]:
            for pipe in pipes:
                pipe.velocity = 2
            game_over = False
            pipes.clear()
            player.pos.y = HEIGHT/2
            score = 0
            background.pos.x = 0

    if not game_over:
        player.move()
        background.move()

    if not game_over:
        if random() > 1.0 - PIPE_PROBABILITY and time_delta > PIPE_COOLDOWN:
            pipes.append(Pipe())
            last_time = time.time()

    for pipe in pipes:
        if not game_over:
            pipe.move()
        if player.pos.x + player.rect.width > pipe.pos.x and player.pos.x + player.rect.width < pipe.pos.x + pipe.rect.width or player.pos.x > pipe.pos.x and player.pos.x < pipe.pos.x + pipe.rect.width:
            if pipe.top:
                if player.pos.y < pipe.pos.y:
                        game_over = True
            elif not pipe.top:
                if player.pos.y > pipe.pos.y - pipe.rect.height:
                        game_over = True

    if game_over:
        use_background1 = not use_background1
    if use_background1:
        background = background1
    else:
        background = background2

    display_surface.blit(background.image, (background.pos.x,background.pos.y))
    for pipe in pipes:
        display_surface.blit(pipe.image, (pipe.pos.x-pipe.rect.width,pipe.pos.y-pipe.rect.height))

    display_surface.blit(player.image, (player.pos.x-2*player.rect.width,player.pos.y-2*player.rect.height))
    display_surface.blit(score_text.text_surf, (5,5))
    if game_over:
        display_surface.blit(pygame.image.load("./images/background3.png"),(0,0))
        last_name, last = updateFile(score)
        lastScore = small_font.render("High Score: "+ str(last_name) + " " + str(last), True, (35,154,166))
        
        display_surface.blit(lastScore, (WIDTH - len(str(last)+str(last_name))*20-210,10))
        display_surface.blit(game_over_text.text_surf, (WIDTH/2-game_over_text.text_surf.get_rect().width/2,HEIGHT/2-game_over_text.text_surf.get_rect().height/2-50))
        display_surface.blit(score_text.text_surf, (WIDTH/2-score_text.text_surf.get_rect().width/2,HEIGHT/2-score_text.text_surf.get_rect().height/2+20))
        display_surface.blit(again.text_surf, (WIDTH/2-again.text_surf.get_rect().width/2,HEIGHT/2-again.text_surf.get_rect().height/2 + 70))

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_SPACE]:
        PIPE_PROBABILITY += 0.01

    pygame.display.update()
    fps.tick(FPS)
pygame.quit()
sys.exit()
