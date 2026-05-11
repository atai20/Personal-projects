import pygame
import numpy as np
import math
import time
from scipy import signal
from pygame._sdl2 import Renderer, Texture, Image, Window

import random

# 1. Initialize and Setup
pygame.init()
WIDTH, HEIGHT = 1920, 1080
clock = pygame.time.Clock()

# SDL2 requires a renderer object, used to draw and display everything:


maximum_vertices = 300598
magnification = 1
index = 0
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


def move_x(points, moving):

    R = np.array(((1, 0, 0, moving),
                  (0, 1, 0, 0),
                  (0, 0, 1, 0),
                  (0, 0, 0, 1)))
    

    return points @ R.T

def move_y(points, moving):

    R = np.array(((1, 0, 0, 0),
                  (0, 1, 0, moving),
                  (0, 0, 1, 0),
                  (0, 0, 0, 1)))

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




aspect = WIDTH/HEIGHT
z_far = 2000
z_near = 0.5
field_of_view = 90

def perspective(points):

    x = (1/(aspect*math.tan(field_of_view/2)))
    y = (1/(math.tan(field_of_view/2)))
    z = (-(z_far+z_near)/(z_far-z_near))
    t = -2*z_near*z_far/(z_far-z_near)

    R = np.array(((x, 0, 0, 0),
                  (0, y, 0, 0),
                  (0, 0, z, t),
                  (0, 0, -1, 1)))
    

    # Apply rotation (assuming points is an Nx3 array)
    return points @ R.T
 
    

def neuron_gen(length, angle, x_init = 0, y_init = 0):
    if length < 1:
        return None
    
    x = int(x_init+length*math.cos(angle))
    y = int(y_init+length*math.sin(angle))
    min_angle = math.pi/20

    random.uniform(angle-math.pi/2, angle+math.pi/2)

    angle_pos = random.uniform(angle-math.pi/2, angle+math.pi/2)
    if angle_pos>angle+min_angle or angle_pos<angle-min_angle:
        neuron_gen(length/random.uniform(1.3,2), angle_pos, x, y)
    pygame.draw.line(screen, (255, 255, 255), (x_init, y_init), (x, y))
    angle_neg = random.uniform(angle-math.pi/2, angle+math.pi/2)
    if angle_neg>angle+min_angle or angle_neg<angle-min_angle:
        neuron_gen(length/random.uniform(1.3,2), angle_neg, x, y)




def threeD_converter(model):
    models = ["../Human skeleton_ascii.ply", "../Lone Sailor Memorial_ascii.ply", "../Brain_Model_no_normals.ply", "../Knight_no_normals.ply", "embrio_ascii_scaled100.ply", "Woman_Doctor_ascii.ply"]
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



font = pygame.font.Font("ISOCT.ttf", 24)
font.set_bold(True)



points = threeD_converter(1)

points = np.array(points)
empty_col = np.ones((points.shape[0], 1))
points = np.hstack((points, empty_col))


# 3. Access pixels using surfarray
# Shape is (width, height, rgb)


pixel_array = pygame.surfarray.pixels3d(screen)


theta1 = 0
delta_time = 0

# 4. Modify pixels efficiently (e.g., white color)
# Only draw points within screen bounds





'''

Different systems:

main one will be nurological
the rest will be to add up when some systems fail

TODO:
- add cool visuals for neurons that basically goes around the 3d model's skeleton
- get and use same 3d model of the brain for all or just same things in design
- make zooming to specific part of the body when choosing in menu
- figure out why some models are not being loaded(just google it or use chat)
- add new models of your own design like conjoint twins, the guy without a head and other entities like centaur
- add different parts of the brain as mechanics very close to how it looks like in real world, like trying to 
measure resistance, connect to yourself to get the understanding and other similar stuff
- add possibility for modifications in detection, and possibility to play as the entity, for example if it's conjoined twin
your screen is divided, if you play as some other there will be other
- for step the one before make perspective matrix work somehow and add the terrain afterwards
- come up with simple gameplay per entity
- there are different stages of growth per entity make sure you can either make or find them.





'''






sinusoid_points =  np.ones((99, 99))
theta1 = 0
theta2 = 0
x_transform = WIDTH//2
y_transform = HEIGHT//2
background = (0, 0, 0)
points_color = (255, 255, 255)
d = 0
points_temp = np.array(points)



x_sinus = np.linspace(0, 2 * np.pi, 100)
y_sinus = np.sin(x_sinus)


t = np.linspace(-1, 1, 100)
# Generate a 5 Hz Gaussian pulse
i, q, e = signal.gausspulse(t, fc=5, retquad=True, retenv=True)
# 5. Display
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    start = time.perf_counter()

    

    
    index += 0.1
    
    
    
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        theta1 = 0
        theta1 = -4000*(delta_time)
        points = rotate_x(points, theta1*((delta_time)))
        
        
    if keys[pygame.K_DOWN]:
        theta1 = 0
        theta1 = 4000*(delta_time)
        points = rotate_x(points, theta1*((delta_time)))
        
        
    if keys[pygame.K_LEFT]:
        theta2 = 0
        theta2 = -4000*(delta_time)
        points = rotate_y(points, theta2*((delta_time)))
        

    if keys[pygame.K_RIGHT]:
        theta2 = 0
        theta2 = 4000*(delta_time)
        points = rotate_y(points, theta2*((delta_time)))
    if keys[pygame.K_z]:
        magnification = 0
        magnification += 4
        points = scale(points, 1+(magnification*(delta_time)))
    if keys[pygame.K_x]:
        magnification = 0
        magnification -= 4
        points = scale(points, 1+(magnification*(delta_time)))
    if keys[pygame.K_a]:
        right_move = 0
        right_move = -1000*(delta_time)
        points = move_x(points, right_move)
    if keys[pygame.K_d]:
        right_move = 0
        right_move = 1000*(delta_time)
        points = move_x(points, right_move)
    if keys[pygame.K_s]:
        up_move = 0
        up_move = 1000*(delta_time)
        points = move_y(points, up_move)
    if keys[pygame.K_w]:
        up_move = 0
        up_move = -1000*(delta_time)
        points = move_y(points, up_move)
        
    if keys[pygame.K_1]:
        points = threeD_converter(1)
    if keys[pygame.K_2]:
        points = threeD_converter(2)
    if keys[pygame.K_3]:
        points = threeD_converter(3)
    if keys[pygame.K_4]:
        points = threeD_converter(4)
    if keys[pygame.K_5]:
        points = threeD_converter(5)
    if keys[pygame.K_e]:
        background = (0, 0, 0)
        points_color = (255, 255, 255)
    if keys[pygame.K_r]:
        background = (255, 255, 255)
        points_color = (0, 0, 0)
    
    




    pixel_array = pygame.surfarray.pixels3d(screen)

    pixel_array[:] = background


    
    points_temp[:, 0] = points[:, 0]
    points_temp[:, 1] = points[:, 1]

    
    valid_points = points_temp[(points_temp[:, 0]< WIDTH) & (points_temp[:, 1]< HEIGHT) & (points_temp[:, 0]> 0) & (points_temp[:, 1] > 0) ]



    valid_points = valid_points.astype(int)
    

    # Apply to the pixel array
    pixel_array[valid_points[:, 0], valid_points[:, 1]] = points_color
    '''
    x_points = np.array(range(1, 100))
    y_points = 100*np.cos(np.pi*np.array(range(1, 180))/180).astype(int)


    sinusoid_points = sinusoid_points[x_points, y_points]

    sinusoid_points = sinusoid_points.astype(int)

    pixel_array[:100, :100] = points_color
    '''


    end = time.perf_counter()
   
    text_surface = font.render('FPS:'+str(1//(end-start))+",  vertices:"+str(maximum_vertices), True, points_color)

    body_part_text = font.render("Test Subject #7", True, points_color)

    delta_time = abs((delta_time-(end-start))/2)

    del pixel_array 
    pygame.draw.line(screen, points_color, (np.mean(points[:, 0]), np.min(points[:, 1])+((np.max(points[:, 1]) - np.min(points[:, 1]))/6)//2),( WIDTH - 500, 120), width=1)
    pygame.draw.rect(screen, points_color, (WIDTH-500, 75, 450, 100), width=1, border_radius=0)


    for x in range(300):
        if x>1:
            pygame.draw.line(screen, points_color, (x+WIDTH-500, int(300+0.9*math.sin(index+x/10)*math.sqrt(abs(3-x**2)))), (x+WIDTH-500,int(300+0.9*math.sin(index+(x-1)/10)*math.sqrt(abs(3-(x-1)**2)))), 1)

    neuron_gen(200, math.pi/5, 100, 150)

    screen.blit(body_part_text, (WIDTH - 400, 100))
    screen.blit(text_surface, (10, 10))




    



    

    

    pygame.display.flip()
    # Free the lock on the pixel array


pygame.quit()
