import pygame
import numpy as np
import time
from pygame._sdl2 import Renderer, Texture, Image, Window

import random

# 1. Initialize and Setup
pygame.init()
WIDTH, HEIGHT = 1920, 1080
clock = pygame.time.Clock()

# SDL2 requires a renderer object, used to draw and display everything:


maximum_vertices = 369968
magnification = 1

def rotate_x(points, theta_deg):
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)

    R = np.array(((1, 0, 0, 0),
                  (0, c, -s, 0),
                  (0, s, c, 0),
                  (0, 0, 0, 1)))

    return points @ R.T

def rotate_y(points, theta_deg):
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)

    R = np.array(((c, 0, -s, 0),
                  (0, 1, 0, 0),
                  (s, 0, c, 0),
                  (0, 0, 0, 1)))

    return points @ R.T

def move_right(points, how_much):

    # Define the rotation matrix for the X-axis
    R = np.array(((1, 0, 0, 0),
                  (0, 1, 0, 0),
                  (0, 0, 1, 0),
                  (0, 0, 0, 1)))

    # Apply rotation (assuming points is an Nx3 array)
    return points @ R.T

def scale(points, magnification):
    # Define the rotation matrix for the X-axis
    R = np.array(((magnification, 0, 0, 0),
                  (0, magnification, 0, 0),
                  (0, 0, magnification, 0),
                  (0, 0, 0, 1)))
    
    #for now let's leave matrices in this form in case the other kinds of transformations will be harder to implement


    # Apply rotation (assuming points is an Nx3 array)
    return points @ R.T


def threeD_converter(model):
    models = ["../Human skeleton_ascii.ply", "../Lone Sailor Memorial_ascii.ply", "../Brain_Model_no_normals.ply", "../Knight_no_normals.ply"]
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
                if vertex_count>maximum_vertices:
                    if line_count % (vertex_count//maximum_vertices) == 0:
                        vertext_coordinates.append([magnification*int(float(v)/2) for v in line.strip().split()])
                else:
                    vertext_coordinates.append([magnification*int(float(v)/ 2) for v in line.strip().split()])
            if "end_header" in line.strip():
                counting_lines = True
    return vertext_coordinates


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN |pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)

surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)


# 2. Generate 1,000,000 random coordinates
# Shape is (N, 2), where N is number of points
num_points = 1000000


font = pygame.font.SysFont(None, 24)



points = threeD_converter(1)

points = np.array(points)
empty_col = np.zeros((points.shape[0], 1))
points = np.hstack((points, empty_col))


# 3. Access pixels using surfarray
# Shape is (width, height, rgb)


pixel_array = pygame.surfarray.pixels3d(screen)


theta1 = 0
delta_time = 0

# 4. Modify pixels efficiently (e.g., white color)
# Only draw points within screen bounds
valid_points = points[(points[:, 0] < WIDTH) & (points[:, 1] < HEIGHT)]

valid_points = valid_points.astype(int)

pixel_array[valid_points[:, 0], valid_points[:, 1]] = (255, 255, 255)
sinusoid_points =  np.zeros((99, 99))
theta1 = 0
theta2 = 0
x_transform = WIDTH//2
y_transform = HEIGHT//2
background = (0, 0, 0)
points_color = (255, 255, 255)
d = 0
points_temp = np.array(points)

# 5. Display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    start = time.perf_counter()

    magnification = 0

    theta1 = 0
    theta2 = 0

    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        theta1 = 400*(delta_time)
    if keys[pygame.K_DOWN]:
        theta1 = -400*(delta_time)
    if keys[pygame.K_LEFT]:
        theta2 = 400*(delta_time)
    if keys[pygame.K_RIGHT]:
        theta2 = -400*(delta_time)
    if keys[pygame.K_z]:
        magnification += 0.5
    if keys[pygame.K_x]:
        magnification -= 0.5
    if keys[pygame.K_a]:
        x_transform -= 10
    if keys[pygame.K_d]:
        x_transform += 10
    if keys[pygame.K_s]:
        y_transform += 10
    if keys[pygame.K_w]:
        y_transform -= 10
    if keys[pygame.K_1]:
        points = threeD_converter(1)
    if keys[pygame.K_2]:
        points = threeD_converter(2)
    if keys[pygame.K_3]:
        points = threeD_converter(3)
    if keys[pygame.K_4]:
        points = threeD_converter(4)
    if keys[pygame.K_e]:
        background = (0, 0, 0)
        points_color = (255, 255, 255)
    if keys[pygame.K_r]:
        background = (255, 255, 255)
        points_color = (0, 0, 0)
    




    points = scale(points, 1+(magnification*(delta_time)))
    points = rotate_x(points, theta1*((delta_time)))
    points = rotate_y(points, theta2*((delta_time)))

    pixel_array = pygame.surfarray.pixels3d(screen)

    pixel_array[:] = background



    points_temp[:, 0] = points[:, 0] + x_transform
    points_temp[:, 1] = points[:, 1]+ y_transform

    
    valid_points = points_temp[(points_temp[:, 0]< WIDTH) & (points_temp[:, 1]< HEIGHT) & (points_temp[:, 0]> 0) & (points_temp[:, 1] > 0) ]




    new_points = valid_points.astype(int)

    pixel_array[new_points[:, 0], new_points[:, 1]] = points_color

    '''
    x_points = np.array(range(1, 100))
    y_points = 100*np.cos(np.pi*np.array(range(1, 180))/180).astype(int)


    sinusoid_points = sinusoid_points[x_points, y_points]

    sinusoid_points = sinusoid_points.astype(int)

    pixel_array[:100, :100] = points_color
    '''


    end = time.perf_counter()
   
    #text_surface = font.render('FPS:'+str(1//(end-start))+",  vertices:"+str(maximum_vertices), True, (0, 128, 0))

    

    delta_time = (end-start)
    print(len(new_points))




    del pixel_array 



    screen.blit(screen, (0, 0))

    

    pygame.display.flip()
    # Free the lock on the pixel array


pygame.quit()
