import pygame
import math
import time
import random
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
points = []

def tree_gen(length, angle, x_init = 0, y_init = 0):
    if length < 1:
        return None
    
    x = int(x_init+length*math.cos(angle))
    y = int(y_init+length*math.sin(angle))

    
    
    tree_gen(length/random.uniform(1.3,2), random.uniform(angle-math.pi/10, angle+math.pi/10), x, y)
    pygame.draw.line(screen, (255, 255, 255), (x_init, y_init), (x, y))
    tree_gen(length/random.uniform(1.3,2), -random.uniform(angle-math.pi/10, angle+math.pi/10), x, y)




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
mouse_x = 0
mouse_y = 0
magnitude = 100
mouse_poses = []




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
   
    screen.fill(black)


    
    theta += 1
    theta2 += 0.1

    magnitude /= 1.1
    amplitudes = []

    tree_gen(200, math.pi/5, 100, 150)


    

    # Update displacy
    pygame.display.flip()    

    

# Quit Pygame
pygame.quit()