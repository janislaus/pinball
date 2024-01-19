import pygame
from pathlib import Path
from pinball.objects.ball import Ball
from pinball.objects.court import Court
from pinball.objects.spring import Spring
from pinball.objects.utils import draw_lines


# Initialize PyGame
pygame.init()

# Initial window size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000

# Define spacetime
GRAVITY_X = 0.0
GRAVITY = 0.3
# DT = 1  # ms (discretization of time)
DT = 0.1  # ms (discretization of time)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
bg_orig = pygame.image.load(
    Path(__file__).parents[1] / "data" / Path("industry.jpg")
).convert()
clock = pygame.time.Clock()
running = True

# You could declare components (the initial ball, the other items, ...) here

ball = Ball(
    x=95,
    y=200,
    colour="black",
    r=30,
    vy=200,
    vx=-6,
)

# ball = Ball(x=550, y=750, colour="black", r=30)

objects = {"court": Court(screen=screen), "spring": Spring(screen=screen)}
timer = 5

# Main event loop
while running:
    for event in pygame.event.get():
        # Get's all the user action (keyboard, mouse, joysticks, ...)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            objects["spring"].state = "compressing"
        if pressed[pygame.K_b]:
            objects["spring"].state = "compressing"
        elif pressed[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                objects["spring"].state = "releasing"
            if event.key == pygame.K_b:
                objects["spring"].state = "releasing"
        if event.type == pygame.QUIT:
            """Schliesst das Pygame Fenster wenn wir oben auf das x drücken"""
            running = False

        # continue

    bg = pygame.transform.scale(bg_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(bg, (0, 0))  # redraws background image

    boundaries = []
    for obj in objects.values():
        boundaries += obj.boundaries

    ball.move(boundaries=boundaries, gravity=GRAVITY, dt=DT)
    ball.draw(screen)

    objects["spring"].update()
    objects["spring"].draw()
    objects["court"].draw()

    # Adjust screen
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()

    pygame.display.flip()  # Update the display of the full screen
    # clock.tick(60)  # 60 frames per second
    clock.tick(600)  # 60 frames per second
