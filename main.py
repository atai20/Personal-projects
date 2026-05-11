import pygame
import numpy as np
import time
import asyncio

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Engine - Pygbag")

clock = pygame.time.Clock()
maximum_vertices = 21000
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

def scale(points, mag):
    R = np.array(((mag, 0, 0, 0),
                  (0, mag, 0, 0),
                  (0, 0, mag, 0),
                  (0, 0, 0, 1)))
    return points @ R.T

# Simple demo with generated points instead of loading files
def generate_cube_points():
    points = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                points.append([x * 100, y * 100, z * 100])
    return np.array(points)

points = generate_cube_points()
empty_col = np.zeros((points.shape[0], 1))
points = np.hstack((points, empty_col))

theta_x = 0
theta_y = 0
x_transform = WIDTH // 2
y_transform = HEIGHT // 2
background = (0, 0, 0)
points_color = (255, 255, 255)

async def main():
    global theta_x, theta_y, points
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update rotation
        theta_x += 1
        theta_y += 1.5
        
        # Apply transformations
        rotated_points = rotate_x(points, theta_x)
        rotated_points = rotate_y(rotated_points, theta_y)
        
        # Clear screen
        screen.fill(background)
        
        # Project and draw points
        for point in rotated_points:
            x = int(point[0]) + x_transform
            y = int(point[1]) + y_transform
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                pygame.draw.circle(screen, points_color, (x, y), 2)
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

# Run with pygbag compatibility
asyncio.run(main())
