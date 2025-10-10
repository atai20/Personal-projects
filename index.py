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
k = (0, 0.1)
ni = 0
nj = 0
nk = 0

def draw_line(x, y, z, x1, y1, z1, color = white):
    pygame.draw.line(screen, color, (x+z*k[0], y+z*k[1]), (x1+z1*k[0], y1+z1*k[1]), 2)

def draw_point(x, y, z):
    pygame.draw.circle(screen, white, (x+z*k[0], y+z*k[1]), dot_radius)

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
dot_radius = 5
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

# Game loop

running = True
theta = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(black)
 
    theta1 += 0.01
    theta += 0.001


    x1 = 100*math.cos(theta)
    z1 = 100*math.sin(theta)
    x2 = 100*math.cos(theta+math.pi)
    z2 = 100*math.sin(theta+math.pi)
    # Draw the dot
    


    draw_point(dot_x+x1, y1, dot_z+z1)
    draw_point(dot_x+x2, y1, dot_z+z2)
    draw_line(dot_x+x1, y1, dot_z+z1, dot_x+x2, y1, dot_z+z2)

    draw_point(dot_x2+x1, y2, dot_z+z1)
    draw_point(dot_x2+x2, y2, dot_z+z2)

    draw_line(dot_x2+x1, y2, dot_z+z1, dot_x2+x2, y2, dot_z+z2)

    
    draw_line(dot_x+x2, y1, dot_z+z2, dot_x2+x2, y2, dot_z+z2)

    vect1_x = (dot_x+x1)-(dot_x+x2)
    vect1_y = y1 - y1
    vect1_z = (dot_z+z1)-(dot_z+z2)

    vect2_x = (dot_x+x1)-(dot_x2+x1)
    vect2_y = y1 - y2
    vect2_z = (dot_z+z1)-(dot_z+z1)


    #vect_circ_x = 
    #vect_circ_y = 
    #vect_circ_z = 


    draw_line(dot_x+x1, y1, dot_z+z1, dot_x+x2, y1, dot_z+z2, pygame.Color('red'))
    draw_line(dot_x+x1, y1, dot_z+z1, dot_x2+x1, y2, dot_z+z1, pygame.Color('red'))


    module = math.sqrt(pow(vect2_x,2)+pow(vect2_y,2)+pow(vect2_z,2))

    n_v1 = vect1_x/module
    n_v2 = vect1_y/module
    n_v3 = vect1_z/module

    n_v1_2 = vect2_x/module
    n_v2_2 = vect2_y/module
    n_v3_2 = vect2_z/module

    draw_line(dot_x+x1, y1, dot_z+z1, dot_x+x1+50*(n_v1*math.cos(theta1)+n_v1_2*math.sin(theta1)), y1+100*(n_v2*math.cos(theta1)+n_v2_2*math.sin(theta1)), dot_z+z1, pygame.Color('yellow'))
    
    #try with and without z coordinate

    n1 = cross_mult(vect1_x, vect1_y, vect1_z, vect2_x, vect2_y, vect2_z, dot_x+x1, y1, dot_z+z1)

    n2 = cross_mult(vect1_x, vect1_y, vect1_z, vect2_x, vect2_y, vect2_z, dot_x2+x2, y2, dot_z+z2)

    n3 = cross_mult(vect1_x, vect1_y, vect1_z, vect2_x, vect2_y, vect2_z, dot_x2+x1, y2, dot_z+z1)
    
    n4 = cross_mult(vect1_x, vect1_y, vect1_z, vect2_x, vect2_y, vect2_z, dot_x+x2, y1, dot_z+z2)

    draw_point(n1[0],n1[1],n1[2])
    draw_point(n2[0], n2[1],n2[2])

    draw_point(n3[0], n3[1],n3[2])
    draw_point(n4[0], n4[1],n4[2])

    draw_line(n2[0], n2[1],n2[2], n3[0], n3[1],n3[2])
    draw_line(n1[0],n1[1],n1[2], n3[0], n3[1],n3[2])
    draw_line(n4[0],n4[1],n4[2], n2[0], n2[1],n2[2])
    draw_line(n1[0],n1[1],n1[2], n4[0], n4[1],n4[2])


    

    # Update displacy
    pygame.display.flip()
    

# Quit Pygame
pygame.quit()