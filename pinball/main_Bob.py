import pygame
from pathlib import Path
import pinball.objects.ball as ball
import pinball.objects.obstacle as obstacle


# Initialize PyGame
pygame.init()

# Initial window size
s_width = 600
s_height = 800

# Define spacetime 
GRAVITY_X = 0.0
GRAVITY_Y = 0.3
DT = 1 # ms (discretization of time) 
timer =0

# Making display screen
screen = pygame.display.set_mode((s_width, s_height), pygame.RESIZABLE)
bg_orig=pygame.image.load(Path(__file__).parents[0] / Path("bkg.jpg")).convert()
clock = pygame.time.Clock()

# Setup 
running = True

# You could declare components (the initial ball, the other items, ...) here

ball_x = 100
ball_y = 150
ball_vx = 3
ball_vy = 0

ball_radius = 30

ball2_x = 200
ball2_y = 150
ball2_vx = -3
ball2_vy = 0

ball2_radius = 40
ball1=ball.Ball(ball_x,ball_y,ball_radius,(35, 161, 224),ball_vx,ball_vy)
ball2=ball.Ball(ball2_x,ball2_y,ball_radius,(35, 161, 224),ball2_vx,ball2_vy)
pendulum = obstacle.Pendulum(screen.get_width()-200,100,50,200,screen,colour=(35, 161, 224))
ball_liste=[ball1,ball2]
rectangle = obstacle.Rectangle(screen.get_width()-100,screen.get_height()-100,100,20,colour=(35, 161, 224))
triangle = obstacle.RightTriangle((200,540),(380,400),(380,540),(35, 161, 224))
triangle2 =obstacle.RightTriangle((300,540),(100,400),(30,500),(35, 161, 224))
# Main event loop
while running:
    for event in pygame.event.get():
        # Get's all the user action (keyboard, mouse, joysticks, ...)
        if event.type == pygame.QUIT :
            """Schliesst das Pygame Fenster wenn wir oben auf das x drücken
            """
            running = False

    # Adjust screen
    s_width, s_height = screen.get_width(), screen.get_height()
    bg = pygame.transform.scale(bg_orig, (s_width, s_height))
    screen.blit(bg, (0, 0)) # redraws background image
    timer +=DT
    timer /=60
    # Here the action could take place

    # s = s0 + v0*t + 1/2a*t**2
    for ball in ball_liste:

        ball.collides_with_pendulum(pendulum)
        ball.collides_with_triangle(triangle)
        #ball.collides_with_triangle(triangle2)

        ball.collides_with_other(ball_liste)
        ball.move(GRAVITY_Y,DT,screen)
        ball.draw(screen)
    pendulum.move(screen,GRAVITY_Y)
    #rectangle.rotate()
    #rectangle.draw(screen)
    triangle.draw(screen)
    #triangle2.draw(screen)
   
    pendulum.draw(screen)

    pygame.display.flip() # Update the display of the full screen
    clock.tick(60) # 60 frames per second

# Done! Time to quit.
