import math
import random
from pathlib import Path

import numpy as np
import pygame

ASSET_DIR = Path(__file__).resolve().parent

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("3D Engine - Web")
font = pygame.font.Font(str(ASSET_DIR / "ISOCT.ttf"), 22)
clock = pygame.time.Clock()

models = [
    ASSET_DIR / "embrio_ascii_scaled100.ply",
    ASSET_DIR / "Woman_Doctor_ascii.ply",
    ASSET_DIR / "embrio_ascii_scaled10.ply",
    ASSET_DIR / "embrio_ascii.ply",
    ASSET_DIR / "embrio_ascii_scaled100.ply",
]


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


def scale(points, factor):
    R = np.array(((factor, 0, 0, 0),
                  (0, factor, 0, 0),
                  (0, 0, factor, 0),
                  (0, 0, 0, 1)))
    return points @ R.T


def load_model(model_index):
    path = models[model_index]
    coordinates = []
    vertex_count = 0
    reading = False
    with open(path, "r") as file:
        for line in file:
            if "element vertex" in line:
                vertex_count = int(line.strip().split("element vertex ")[1])
            elif line.strip() == "end_header":
                reading = True
                continue
            elif reading and len(coordinates) < vertex_count:
                values = line.split()
                if len(values) >= 3:
                    coordinates.append([float(values[0]) / 2.0,
                                        float(values[1]) / 2.0,
                                        float(values[2]) / 2.0])
    if len(coordinates) == 0:
        return np.zeros((0, 4), dtype=float)
    if len(coordinates) > 8000:
        step = max(1, len(coordinates) // 8000)
        coordinates = coordinates[::step]
    points = np.array(coordinates, dtype=float)
    points -= np.mean(points, axis=0)
    return np.hstack((points, np.ones((points.shape[0], 1), dtype=float)))


def project(points):
    z = points[:, 2] + 450.0
    z = np.maximum(z, 1.0)
    factor = 750.0 / z
    x = points[:, 0] * factor + WIDTH * 0.5
    y = -points[:, 1] * factor + HEIGHT * 0.5
    return np.vstack((x, y, z)).T


def draw_points(points, color):
    projected = project(points)
    visible = projected[(projected[:, 0] >= 0) & (projected[:, 0] < WIDTH) &
                        (projected[:, 1] >= 0) & (projected[:, 1] < HEIGHT)]
    for px, py, pz in visible:
        brightness = int(120 + min(135, (pz / 450.0) * 135.0))
        shade = max(40, min(255, brightness))
        pygame.draw.circle(screen, (shade, shade, shade), (int(px), int(py)), 1)


def neuron_gen(length, angle, x_init=0, y_init=0, depth=0):
    if depth > 4 or length < 2:
        return
    x = int(x_init + length * math.cos(angle))
    y = int(y_init + length * math.sin(angle))
    pygame.draw.line(screen, (255, 255, 255), (x_init, y_init), (x, y), 1)
    next_length = length / random.uniform(1.3, 2.0)
    for next_angle in (random.uniform(angle - math.pi / 2, angle + math.pi / 2),
                       random.uniform(angle - math.pi / 2, angle + math.pi / 2)):
        if abs(next_angle - angle) > math.pi / 20:
            neuron_gen(next_length, next_angle, x, y, depth + 1)


def main():
    selected_model = 0
    points = load_model(selected_model)
    angle_x = 0.0
    angle_y = 0.0
    zoom = 1.5
    translate_x = 0.0
    translate_y = 0.0
    background = (10, 10, 30)
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_model = 0
                    points = load_model(selected_model)
                elif event.key == pygame.K_2:
                    selected_model = 1
                    points = load_model(selected_model)
                elif event.key == pygame.K_3:
                    selected_model = 2
                    points = load_model(selected_model)
                elif event.key == pygame.K_4:
                    selected_model = 3
                    points = load_model(selected_model)
                elif event.key == pygame.K_5:
                    selected_model = 4
                    points = load_model(selected_model)
                elif event.key == pygame.K_r:
                    background = (255, 255, 255)
                elif event.key == pygame.K_e:
                    background = (10, 10, 30)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            angle_x -= 80.0 * dt
        if keys[pygame.K_DOWN]:
            angle_x += 80.0 * dt
        if keys[pygame.K_LEFT]:
            angle_y -= 80.0 * dt
        if keys[pygame.K_RIGHT]:
            angle_y += 80.0 * dt
        if keys[pygame.K_z]:
            zoom = min(4.0, zoom + 1.5 * dt)
        if keys[pygame.K_x]:
            zoom = max(0.4, zoom - 1.5 * dt)
        if keys[pygame.K_a]:
            translate_x -= 220.0 * dt
        if keys[pygame.K_d]:
            translate_x += 220.0 * dt
        if keys[pygame.K_w]:
            translate_y += 220.0 * dt
        if keys[pygame.K_s]:
            translate_y -= 220.0 * dt

        transformed = scale(points, zoom)
        transformed = rotate_x(transformed, angle_x)
        transformed = rotate_y(transformed, angle_y)
        transformed[:, 0] += translate_x
        transformed[:, 1] += translate_y

        screen.fill(background)
        draw_points(transformed, (255, 255, 255))
        neuron_gen(180, math.pi / 5, 180, 140)

        fps_text = font.render(f"FPS {int(clock.get_fps()):02d}", True, (220, 220, 220))
        info_text = font.render("Arrows rotate, Z/X zoom, WASD move, 1-5 models", True, (220, 220, 220))
        screen.blit(fps_text, (20, 20))
        screen.blit(info_text, (20, 50))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
