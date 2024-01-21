import pygame
from pathlib import Path
from pinball.objects.ball import Ball
from pinball.objects.court import Court
from pinball.objects.flipper import LeftFlipper, RightFlipper
from pinball.objects.vector import Vector
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
DT = 0.5  # ms (discretization of time)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
bg_orig = pygame.image.load(
    Path(__file__).parents[1] / "data" / Path("industry.jpg")
).convert()
clock = pygame.time.Clock()
running = True

# You could declare components (the initial ball, the other items, ...) here

# ball = Ball(
#     x=95,
#     y=200,
#     colour="black",
#     r=30,
#     vy=6,
#     vx=-6,
# )

ball = Ball(
    pos=Vector(x=550, y=700),
    v=Vector(x=0, y=0),
    colour="black",
    radius=30,
    screen=screen,
)

objects = {
    "court": Court(screen=screen),
    "spring": Spring(screen=screen),
    "left_flipper": LeftFlipper(screen=screen, dt=DT),
    "right_flipper": RightFlipper(screen=screen, dt=DT),
}


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                paused = False


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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                objects["right_flipper"].state = "hitting"
            if event.key == pygame.K_f:
                objects["left_flipper"].state = "hitting"
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
    objects["spring"].update()
    objects["right_flipper"].update()
    objects["left_flipper"].update()

    ball.draw(screen)

    for obj in objects.values():
        obj.draw()
    # objects["spring"].draw()
    # objects["court"].draw()

    # Adjust screen
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()

    pygame.display.flip()  # Update the display of the full screen
    clock.tick(60)  # 60 frames per second
    # clock.tick(300)  # 60 frames per second
