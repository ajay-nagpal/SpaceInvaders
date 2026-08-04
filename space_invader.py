import pygame

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

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("$p@¢£ !nv@d£r$")

# Load bg image
background = pygame.image.load("img/background.png").convert()

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

#group instances
spaceship_group = pygame.sprite.Group()
spaceship_bullet_group = pygame.sprite.Group()

spaceship = Spaceship(SCREEN_WIDTH//2, SCREEN_HEIGHT-80,3)
spaceship_group.add(spaceship)

run = True
while run:

    clock.tick(fps)

    #draw background
    draw_background()

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update spaceship
    spaceship_group.update()
    #update bullets
    spaceship_bullet_group.update()
    #draw spaceship
    spaceship_group.draw(screen)
    #draw bullets
    spaceship_bullet_group.draw(screen)
    #update display
    pygame.display.update()

pygame.quit()