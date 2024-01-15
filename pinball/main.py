import pygame
from pathlib import Path
from pinball.objects.ball import Ball
from pinball.objects.line import Line
from pinball.objects.spring import Spring

# Initialize PyGame
pygame.init()

# Initial window size
s_width = 600
s_height = 1000

# Define spacetime
GRAVITY_X = 0.0
GRAVITY_Y = 0.3
DT = 1  # ms (discretization of time)

# Making display screen
screen = pygame.display.set_mode((s_width, s_height), pygame.RESIZABLE)
bg_orig = pygame.image.load(
    Path(__file__).parents[1] / "data" / Path("industry.jpg")
).convert()
clock = pygame.time.Clock()

# Setup
running = True

# You could declare components (the initial ball, the other items, ...) here

# ball = Ball(
#     x=400,
#     y=950,
#     colour="black",
#     r=30,
#     vx=3,
#     vy=0,
# )

ball = Ball(x=550, y=750, colour="black", r=30)

spring = Spring(screen=screen)
# spring.state = "releasing"
# ball_y = ball_y + ball_vy*DT + 0.5 * GRAVITY_Y*DT**2
# ball_x = ball_x + ball_vx
# pygame.draw.circle(screen, (0, 0, 10), [ball_x,ball_y] , ball_radius)


# Done! Time to quit.


# Main event loop
while running:
    for event in pygame.event.get():
        # Get's all the user action (keyboard, mouse, joysticks, ...)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            spring.state = "compressing"
        if pressed[pygame.K_b]:
            spring.state = "compressing"
        elif pressed[pygame.K_ESCAPE]:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spring.state = "releasing"
            if event.key == pygame.K_b:
                spring.state = "releasing"
        if event.type == pygame.QUIT:
            """Schliesst das Pygame Fenster wenn wir oben auf das x drücken"""
            running = False

        continue

    # Adjust screen
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0))  # redraws background image

    # Here the action could take place
    ball.calculate_collision(spring)

    ball.move(GRAVITY_Y, DT, screen)
    ball.draw(screen)

    spring.update()
    spring.draw()

    pygame.display.flip()  # Update the display of the full screen
    clock.tick(60)  # 60 frames per second

    # ball_vy = ball_vy + GRAVITY_Y*DT

    # if ball_x >= screen.get_width() - ball_radius or ball_x <= ball_radius:
    #     ball_vx = ball_vx * (-1)
    #     ball_vy = ball_vy * (-1)

    # #if ball_x == spring.rect.x
