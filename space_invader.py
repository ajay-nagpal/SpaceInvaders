import pygame

pygame.init()
pygame.mixer.init()

# Screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

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

run = True
while run:

    clock.tick(fps)

    #draw background
    draw_background()

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        #key press
        if event.type == pygame.KEYDOWN:
            pass

    #update display
    pygame.display.update()

pygame.quit()