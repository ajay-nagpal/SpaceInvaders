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
WHITE = (255, 255, 255)

#define clock and fps
clock = pygame.time.Clock()
fps = 60

#define game variables
rows=6
cols=6# rows cols for aliens

font30=pygame.font.SysFont("constantia",30)
font40=pygame.font.SysFont("constantia",40)
font100=pygame.font.SysFont("constantia",100)

countdown=3# 3 seconds countdown before game start
last_count=pygame.time.get_ticks()#get time in milliseconds

game_over=0#0=run, 1=won, -1=lost
pause=False

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("$p@¢£ !nv@d£r$")

# Load bg image
background = pygame.image.load("img/background.png")

def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))
    
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
        global game_over
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
            laser_sound.play()
            bullet = SpaceshipBullet(self.rect.centerx,self.rect.top)
            spaceship_bullet_group.add(bullet)
            self.last_bullet_created=time_now

        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        #draw healthbar
        pygame.draw.rect(screen,RED,(self.rect.x,self.rect.bottom,self.rect.width,5))
        #initnally complte bar will be green
        #with health remaining it will uncover the red part as both overlap
        if self.health_remaining>0:
            pygame.draw.rect(screen,GREEN,(self.rect.x,self.rect.bottom,\
                int(self.rect.width *(self.health_remaining/self.health_start)),5))
        elif self.health_remaining<=0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            explosion_sound2.play()
            self.kill()
            game_over=-1

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

        for alien in alien_group:
            if pygame.sprite.collide_mask(self, alien):
                self.kill()
                explosion_sound.play()
                alien.kill()
                if len(alien_group)==0:
                    global game_over
                    game_over=1
                explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosion)
                break #exit the loop after collision to avoid checking other aliens

#alien class
class Aliens(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("img/alien"+str(random.randint(1,5))+".png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.move_counter=0
        self.move_dir = 1 #1=right, -1=left

        self.last_bullet_created=pygame.time.get_ticks()#initnially no bullet
        self.bullet_freq=2000 #in milliseconds, 2 sec

    def update(self):

        #move left and right 
        self.rect.x+=self.move_dir
        self.move_counter+=1
        if abs(self.move_counter)>30:
            self.move_dir*=-1
            #reset it some value
            self.move_counter*=self.move_dir

        #shoot limit  to 5 bullets, 2 seconds, need at least one alien
        time_now=pygame.time.get_ticks()
        if time_now - self.last_bullet_created > self.bullet_freq and \
            len(alien_bullet_group)<5 and len(alien_group)>0:

            attacking_alien=random.choice(alien_group.sprites())
            alien_bullet = AliensBullet(attacking_alien.rect.centerx,attacking_alien.rect.bottom)

            alien_bullet_group.add(alien_bullet)
            self.last_bullet_created=time_now

def create_aliens():
    for row in range(rows):
        for col in range(cols):
            #start form 100 pixel form left, adn create some gap bw
            #two alien
            alien=Aliens(50+col*100 , 40+row*70)
            alien_group.add(alien)

#create bullet calss for spaceship bullets
class AliensBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("img/alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        #move bullet down each iteration
        self.rect.y += 2
        #remove bullet if it goes off screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

        if pygame.sprite.collide_mask(self, spaceship):
            self.kill()
            #reduce spaceship health
            spaceship.health_remaining -= 1
            explosion_sound.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

#create explosion class
#explosion will be after colllision, so imnstance will be ther in collision part of code
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,size):
        super().__init__()
        self.images=[]

        for num in range(1,6):
            image = pygame.image.load(f"img/exp{num}.png")
            if size==1:
                image=pygame.transform.scale(image,(30,30))
            if size==2:
                image=pygame.transform.scale(image,(60,60))
            if size==3:
                image=pygame.transform.scale(image,(120,120))

            #add image in list
            self.images.append(image)

        #track which index in a list we are at
        self.index=0
        self.image=self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        #counter to congtrol speed of animation
        self.counter=0

    def update(self):
        #threshold to control speed of animation
        explosion_speed=3
        #update explosion animation
        self.counter+=1
        if self.counter>=explosion_speed and self.index<len(self.images)-1:
            #flip to next image form list
            self.counter=0
            #update image to next in list
            self.index+=1
            self.image=self.images[self.index]

        #if animation completed remove it
        if self.counter>=explosion_speed and self.index>=len(self.images)-1:
            self.kill()

#group instances
spaceship_group = pygame.sprite.Group()
spaceship_bullet_group = pygame.sprite.Group()
alien_group=pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

spaceship = Spaceship(SCREEN_WIDTH//2, SCREEN_HEIGHT-80,3)
spaceship_group.add(spaceship)

#we dont ned to create this again and agian so outside of loop
create_aliens()

#load sounds
laser_sound=pygame.mixer.Sound('sound/laser.wav')
laser_sound.set_volume(0.2)
explosion_sound=pygame.mixer.Sound('sound/explosion.wav')
explosion_sound.set_volume(0.2)
explosion_sound2=pygame.mixer.Sound('sound/explosion2.wav')
explosion_sound2.set_volume(1)

run = True
while run:

    clock.tick(fps)

    #draw background
    draw_background()
    
    if not game_over and not pause:
        if countdown==0:
            #update 
            spaceship_group.update()
            spaceship_bullet_group.update()
            alien_group.update()
            alien_bullet_group.update()
            explosion_group.update()
        if countdown>0:
            draw_text("Get Ready!",font40,WHITE,SCREEN_WIDTH//2-110,SCREEN_HEIGHT//2+50)
            draw_text(str(countdown),font40,WHITE,SCREEN_WIDTH//2-20,SCREEN_HEIGHT//2+90)
            count_timer=pygame.time.get_ticks()
            if count_timer-last_count>1000:
                countdown-=1
                last_count=count_timer
    else:
        draw_text("Game Over!",font100,WHITE,SCREEN_WIDTH//2-250,SCREEN_HEIGHT//2+50)

        if game_over==1:
            draw_text("YOU WON!",font40,WHITE,SCREEN_WIDTH//2-110,SCREEN_HEIGHT//2+145)
        if game_over==-1:
            draw_text("YOU LOSE!",font40,WHITE,SCREEN_WIDTH//2-110,SCREEN_HEIGHT//2+145)

    #draw 
    spaceship_group.draw(screen)
    spaceship_bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

pygame.quit()