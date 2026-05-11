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

# Generate a sphere of points for better visibility
def generate_sphere_points(radius=150, density=15):
    points = []
    for i in range(density):
        lat = np.pi * (i / density)
        for j in range(density * 2):
            lon = 2 * np.pi * (j / (density * 2))
            x = radius * np.sin(lat) * np.cos(lon)
            y = radius * np.sin(lat) * np.sin(lon)
            z = radius * np.cos(lat)
            points.append([x, y, z])
    return np.array(points)

points = generate_sphere_points()
empty_col = np.zeros((points.shape[0], 1))
points = np.hstack((points, empty_col))

theta_x = 0
theta_y = 0
x_transform = WIDTH // 2
y_transform = HEIGHT // 2
background = (20, 20, 30)
points_color = (100, 200, 255)

async def main():
    global theta_x, theta_y, points
    
    running = True
    frame = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        frame += 1
        # Update rotation
        theta_x = frame * 0.5
        theta_y = frame * 0.7
        
        # Apply transformations
        rotated_points = rotate_x(points, theta_x)
        rotated_points = rotate_y(rotated_points, theta_y)
        
        # Clear screen
        screen.fill(background)
        
        # Project and draw points with depth sorting
        projected = []
        for point in rotated_points:
            z = point[2]
            x = int(point[0] * 1.0 / (1 + z / 500)) + x_transform
            y = int(point[1] * 1.0 / (1 + z / 500)) + y_transform
            
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                brightness = int(150 + z / 3)
                brightness = max(50, min(255, brightness))
                color = (brightness // 2, brightness, brightness)
                pygame.draw.circle(screen, color, (x, y), 1)
        
        # Draw title
        font = pygame.font.Font(None, 24)
        text = font.render("3D Sphere - Pygbag", True, (200, 200, 200))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

# Run with pygbag compatibility
asyncio.run(main())
