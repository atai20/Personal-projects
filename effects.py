import pygame
import math
import time
# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)


#unit vectors
#i = (1, 0)
#j = (0, 1)
k = (0, -1)
ni = 0
nj = 0
nk = 0

dot_radius = 1


def draw_line(x, y, z, x1, y1, z1, color = white):
    pygame.draw.line(screen, color, (x+z*k[0], y+z*k[1]), (x1+z1*k[0], y1+z1*k[1]), 2)

def draw_point(x, y, z, rad = dot_radius):
    pygame.draw.circle(screen, white, (x-y+z*k[0], x*0.7+y*0.7+z*k[1]), rad)

def cross_mult(x, y, z, x1, y1, z1, x_i, y_i, z_i):
    ni = y*z1-z*y1
    nj = -x*z1+x1*z
    nk = x*y1-x1*y
    module = math.sqrt(pow(ni,2)+pow(nj,2)+pow(nk,2))
    
    ni = 200*ni/module
    nj = 200*nj/module
    nk = 200*nk/module

    

    draw_line(x_i, y_i, z_i, x_i+ni, y_i+nj, z_i+nk)
    return (x_i+ni, y_i+nj, z_i+nk)

# Create a dot

dot_x = 150
dot_y = 150
dot_x2 = 150
dot_y2 = 450
dot_z = 150
x1=0
y1=150
x2=0
y2=250

z1=0
z2=0
theta1 = 0

x = 0
y = 0
z = 0

# Game loop

running = True
theta = 0
theta2 = 0
my_theta = 0.001
my_theta2 = 0
my_theta_horiz = 0
my_theta_horiz2 = 0
magnitude = 100
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
   
    screen.fill(black)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left click
            magnitude = 100
 
    theta += 1
    theta2 += 0.1

    magnitude /= 1.1

    for x in range(-100, 100,2):
        for y in range(-100, 100,2):
            #cool waves from all sides
            draw_point(400+x,200+y, 200+15*math.sin(x/20+theta2)*math.cos(y/20+theta2))

            #cool central point wave
            #cos( √ (x^2 + y^2) - 0.04 * π) / √ (x^2 + y^2)
            if not (x == 0 and y == 0):
                draw_point(600+x,y, 200+magnitude*math.cos((math.sqrt(x**2+y**2)-0.04*math.pi)/5+theta)/math.sqrt(x**2+y**2))
                draw_point(600, 0, 200)
            if not (x == 0 and y == 0):
                draw_point(460+x,y+60, magnitude*math.cos((math.sqrt(x**2+y**2)-0.04*math.pi)/5+theta)/math.sqrt(x**2+y**2)+2*math.sin(x/20+theta2)*math.cos(y/20+theta2))
                draw_point(460, 60, 0)


    # Update displacy
    pygame.display.flip()    

    

# Quit Pygame
pygame.quit()