import pygame
import random

pygame.init()
pygame.mixer.init()

# Screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

#define colors use for health abr
GREEN = (0, 255, 0)
RED = (255, 0, 0) #spaceship about to destroyed

#define clock and fps
clock = pygame.time.Clock()
fps = 60

#define game variables
rows=6
cols=6# rows cols for aliens

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("$p@¢£ !nv@d£r$")

# Load bg image
background = pygame.image.load("img/background.png")

def draw_background():
    screen.blit(background, (0, 0))

#create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self,x,y,health):
        super().__init__()
        self.image = pygame.image.load("img/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.health_start=health
        self.health_remaining=health
        self.last_bullet_created=pygame.time.get_ticks()#initnially no bullet
        self.bullet_freq=300 #in milliseconds, 0.5 sec

    def update(self):
        #set speed
        speed=8
        #get key press
        key = pygame.key.get_pressed()
        #move spaceship left/right/up/down smoothly
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed #300-8., 292-8...left movement
        if key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += speed
        if key[pygame.K_UP] and self.rect.top > SCREEN_HEIGHT//2:
            self.rect.y -= speed 
        if key[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT-40:
            self.rect.y += speed

        #shoot
        time_now=pygame.time.get_ticks()
        if key[pygame.K_SPACE] and time_now - self.last_bullet_created > self.bullet_freq:
            bullet = SpaceshipBullet(self.rect.centerx,self.rect.top)
            spaceship_bullet_group.add(bullet)
            self.last_bullet_created=time_now

        #draw healthbar
        pygame.draw.rect(screen,RED,(self.rect.x,self.rect.bottom,self.rect.width,5))
        #initnally complte bar will be green
        #with health remaining it will uncover the red part as both overlap
        if self.health_remaining>0:
            pygame.draw.rect(screen,GREEN,(self.rect.x,self.rect.bottom,\
                int(self.rect.width *(self.health_remaining/self.health_start)),5))

#create bullet calss for spaceship bullets
class SpaceshipBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("img/spaceship_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        #move bullet up each iteration
        self.rect.y -= 10
        #remove bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()

#alien class
class Aliens(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("img/alien"+str(random.randint(1,5))+".png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.move_counter=0
        self.move_dir = 1 #1=right, -1=left


    def update(self):
        #move left and right 
        self.rect.x+=self.move_dir
        self.move_counter+=1
        if abs(self.move_counter)>30:
            self.move_dir*=-1
            #reset it some value
            self.move_counter*=self.move_dir

def create_aliens():
    for row in range(rows):
        for col in range(cols):
            #start form 100 pixel form left, adn create some gap bw
            #two alien
            alien=Aliens(50+col*100 , 40+row*70)
            alien_group.add(alien)

#group instances
spaceship_group = pygame.sprite.Group()
spaceship_bullet_group = pygame.sprite.Group()

spaceship = Spaceship(SCREEN_WIDTH//2, SCREEN_HEIGHT-80,3)
spaceship_group.add(spaceship)

alien_group=pygame.sprite.Group()
#we dont ned to create this again and agian so outside of loop
create_aliens()


run = True
while run:

    clock.tick(fps)

    #draw background
    draw_background()

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update 
    spaceship_group.update()
    spaceship_bullet_group.update()
    alien_group.update()

    #draw 
    spaceship_group.draw(screen)
    spaceship_bullet_group.draw(screen)
    alien_group.draw(screen)

    #update display
    pygame.display.update()

pygame.quit()