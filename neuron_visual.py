import pygame
import math
import time
import random
import numpy as np
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

def neuron_gen(length, angle, x_init = 0, y_init = 0):
    if length < 1:
        return None
    
    x = int(x_init+length*math.cos(angle))
    y = int(y_init+length*math.sin(angle))
    min_angle = math.pi/15

    random.uniform(angle-math.pi/2, angle+math.pi/2)

    angle_pos = random.uniform(angle-math.pi/2, angle+math.pi/2)
    if angle_pos>angle+min_angle or angle_pos<angle-min_angle:
        neuron_gen(length/random.uniform(1.3,2), angle_pos, x, y)
    points.append((x_init, y_init, 0, 1))
    points.append((x, y, 0, 1))
    angle_neg = random.uniform(angle-math.pi/2, angle+math.pi/2)
    if angle_neg>angle+min_angle or angle_neg<angle-min_angle:
        neuron_gen(length/random.uniform(1.3,2), angle_neg, x, y)


def pressed_anim(x, y):
    for i in range(100, 110):
        pygame.draw.rect(screen, (0, 0, 0), (x-(i-1)//2, y-(i-1)//2, i-1, i-1), 2)
        pygame.draw.rect(screen, (255, 255, 255), (x-i//2, y-i//2, i, i), 2)
        pygame.display.flip() 
        time.sleep(0.01)


def scale(points, magnification, x=0, y=0):
    # Define the rotation matrix for the X-axis
    R = np.array(((magnification, 0, 0, -x),
                  (0, magnification, 0, -y),
                  (0, 0, magnification, 0),
                  (0, 0, 0, 1)))
    return points @ R.T



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
pressed = False

neuron_gen(200, math.pi/5, 100, 150)

points = np.array(points)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
   
    screen.fill(black)

    for i in range(0, len(points)-1, 2):
        pygame.draw.line(screen, (255, 255, 255), (points[i][0], points[i][1]), (points[i+1][0], points[i+1][1]))



    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            print(theta)
            pressed_anim(mouse_x, mouse_y)
            points = scale(points, 1.2, -screen_width//2+mouse_x, -screen_height//2+mouse_y)
    
        
    
    theta += 1
    theta2 += 0.1

    magnitude /= 1.1
    amplitudes = []

    
    


    

    # Update displacy
    pygame.display.flip()    

    

# Quit Pygame
pygame.quit()