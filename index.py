import pygame
import math
from math import sqrt as sqrt
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



dot_radius = 5

maximum_vertices = 20000
#2000 for my pc is most optimal


magnification = 1

#unit vectors
#i = (1, 0)
#j = (0, 1)
k = (0, 0.1)
ni = 0
nj = 0
nk = 0

origin_x = 0
origin_y = 0
origin_z = 0


def draw_line(x, y, z, x1, y1, z1, color = white):
    pygame.draw.line(screen, color, (x+z*k[0], y+z*k[1]), (x1+z1*k[0], y1+z1*k[1]), 2)


def draw_coordinate_plane():
    initial_point = 50
    draw_line(initial_point+0, initial_point+100, initial_point+0,initial_point, initial_point, initial_point, pygame.Color('red'))
    draw_line(initial_point+0, initial_point+0, initial_point+100,initial_point, initial_point, initial_point, pygame.Color('green'))
    draw_line(initial_point+100, initial_point+0, initial_point+0,initial_point, initial_point, initial_point, pygame.Color('blue'))

def draw_point(x, y, z, radius = dot_radius, color = white):
    pygame.draw.circle(screen, color, (x+z*k[0], y+z*k[1]), radius)

def threeD_converter(model):
    models = ["../Human skeleton_ascii.ply", "../Lone Sailor Memorial_ascii.ply", "../Brain_Model_no_normals.ply"]
    line_count = 0
    counting_lines = False
    vertex_count = 0
    vertext_coordinates = []
    with open(models[model-1], "r") as file:
        for line in file:
            if "element vertex" in line.strip():
                vertex_count = int(line.strip().split("element vertex ")[1])

            if counting_lines and line_count <= vertex_count:
                line_count += 1
                if line_count % (vertex_count//maximum_vertices) == 0:
                    vertext_coordinates.append([float(v) / 2 for v in line.strip().split()])
            if "end_header" in line.strip():
                counting_lines = True
    return vertext_coordinates
           

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

# Game loop

running = True
theta = 0

initial_x = 100
initial_y = 300
initial_z = 100





counter = 0

points = threeD_converter(2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
   
 
    
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        magnification += 0.01
    if keys[pygame.K_DOWN]:
        magnification -= 0.01
    if keys[pygame.K_LEFT]:
        initial_x -= 10
    if keys[pygame.K_RIGHT]:
        initial_x += 10
    if keys[pygame.K_z]:
        initial_y -= 10
    if keys[pygame.K_x]:
        initial_y += 10
    if keys[pygame.K_1]:
        points = threeD_converter(1)
    if keys[pygame.K_2]:
        points = threeD_converter(2)
    if keys[pygame.K_3]:
        points = threeD_converter(3)
    
    
     # Clear screen
    screen.fill(black)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    theta1 = 0.01
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    draw_coordinate_plane()
    theta1 = 0.01*mouse_x + screen_width//2
    theta2 = -0.01*mouse_y+ screen_height//2
    theta3 = 0

    previous_mouse_x = 0
    previous_mouse_y = 0

    previous_points = []
    for x, y, z in points:
        
        counter += 0.05

        
       
    
        x0, y0, z0 = x, y, z

        x = initial_x + (x0*math.cos(theta3)*math.cos(theta1) +
                        y0*(math.cos(theta3)*math.sin(theta1)*math.sin(theta2) - math.sin(theta3)*math.cos(theta2)) +
                        z0*(math.cos(theta3)*math.sin(theta1)*math.cos(theta2) + math.sin(theta3)*math.sin(theta2))) * magnification

        y = initial_y + (x0*math.sin(theta3)*math.cos(theta1) +
                        y0*(math.sin(theta3)*math.sin(theta1)*math.sin(theta2) + math.cos(theta3)*math.cos(theta2)) +
                        z0*(math.sin(theta3)*math.sin(theta1)*math.cos(theta2) - math.cos(theta3)*math.sin(theta2))) * magnification

        z = initial_z + (x0*(-math.sin(theta1)) +
                        y0*(math.cos(theta1)*math.sin(theta2)) +
                        z0*(math.cos(theta1)*math.cos(theta2))) * magnification
       


       

        draw_point(x, y, z, 1, white)

        previous_points = [x, y, z]
    previous_mouse_x = mouse_x
    previous_mouse_y = mouse_y







    # Update displacy
    pygame.display.flip()


'''
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
'''
    

# Quit Pygame
pygame.quit()


'''
Plans include:

    - 3D model conversion to graphics
    - Adding perspective matrix

'''