import pygame
import numpy as np
import time
from pygame._sdl2 import Renderer, Texture, Image, Window

import random

# 1. Initialize and Setup
pygame.init()
WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()

# SDL2 requires a renderer object, used to draw and display everything:


maximum_vertices = 684990
magnification = 1

def rotate_x(points, theta_deg):
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)

    # Define the rotation matrix for the X-axis
    R = np.array(((1, 0, 0),
                  (0, c, -s),
                  (0, s, c)))

    # Apply rotation (assuming points is an Nx3 array)
    return points @ R.T

def rotate_y(points, theta_deg):
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)

    # Define the rotation matrix for the X-axis
    R = np.array(((c, -s, 0),
                  (s, c, 0),
                  (0, 0, 1)))

    # Apply rotation (assuming points is an Nx3 array)
    return points @ R.T

def scale(points, magnification):
    # Define the rotation matrix for the X-axis
    R = np.array(((magnification, 0, 0),
                  (0, magnification, 0),
                  (0, 0, magnification)))

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


screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)


# 2. Generate 1,000,000 random coordinates
# Shape is (N, 2), where N is number of points
num_points = 1000000
points = np.random.randint(0, [WIDTH, HEIGHT], size=(num_points, 2))


font = pygame.font.SysFont(None, 24)



print(points)

points = np.array(threeD_converter(1))


# 3. Access pixels using surfarray
# Shape is (width, height, rgb)


pixel_array = pygame.surfarray.pixels3d(screen)


theta1 = 0

# 4. Modify pixels efficiently (e.g., white color)
# Only draw points within screen bounds
valid_points = points[(points[:, 0] < WIDTH) & (points[:, 1] < HEIGHT)]


pixel_array[valid_points[:, 0], valid_points[:, 1]] = (255, 255, 255)



# 5. Display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    start = time.perf_counter()

    theta1 = 1


    points = scale(points, 1.001)
    points = rotate_x(points, theta1)
    points = rotate_y(points, theta1)

    pixel_array = pygame.surfarray.pixels3d(screen)

    pixel_array[:] = (0, 0, 0)

    
    valid_points = points[(points[:, 0] < WIDTH) & (points[:, 1] < HEIGHT) & (points[:, 0] > 0) & (points[:, 1] > 0) ]

    new_points = valid_points.astype(int)

    pixel_array[new_points[:, 0], new_points[:, 1]] = (255, 255, 255)


    end = time.perf_counter()
   
    text_surface = font.render('FPS:'+str(1//(end-start))+",  vertices:"+str(maximum_vertices), True, (0, 128, 0))

    print(1//(end-start))

    del pixel_array 

    screen.blit(screen, (0, 0))

    

    pygame.display.flip()
    # Free the lock on the pixel array


pygame.quit()
