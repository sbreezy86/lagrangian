import pygame
import numpy as np
import random
import time

class Star:
    def __init__(self, x, y, vx, vy, r, m, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.m = m
        self.color = color
        self.ax = 0
        self.ay = 0

    def update(self, dt, stars, G, space_size):
        current_x, current_y = self.x, self.y

        self.x += self.vx * dt + 0.5 * self.ax * dt**2
        self.y += self.vy * dt + 0.5 * self.ay * dt**2

        self.reflect_off_walls(space_size)

        self.ax, self.ay = 0, 0
        for other_star in stars:
            if other_star != self:
                self.apply_gravity(other_star, G)

        self.vx = (self.x - current_x) / dt
        self.vy = (self.y - current_y) / dt

        if np.isnan(self.x) or np.isnan(self.y) or np.isnan(self.vx) or np.isnan(self.vy):
            self.x = space_size / 2
            self.y = space_size / 2
            self.vx = 0
            self.vy = 0
            self.ax = 0
            self.ay = 0

    def apply_gravity(self, other_particle, G):
        dx = other_particle.x - self.x
        dy = other_particle.y - self.y
        distance = np.sqrt(dx**2 + dy**2)

        if distance > 0:
            force = G * self.m * other_particle.m / distance**2
            fx = force * dx / distance
            fy = force * dy / distance
            self.ax += fx / self.m
            self.ay += fy / self.m

    def reflect_off_walls(self, space_size):
        buffer_distance = 10

        if (self.x - self.r) < buffer_distance:
            self.vx = abs(self.vx)  # Reflect to the right
            self.x = buffer_distance + self.r
        elif (self.x + self.r) > (space_size - buffer_distance):
            self.vx = -abs(self.vx)  # Reflect to the left
            self.x = space_size - buffer_distance - self.r

        if (self.y - self.r) < buffer_distance:
            self.vy = abs(self.vy)  # Reflect downwards
            self.y = buffer_distance + self.r
        elif (self.y + self.r) > (space_size - buffer_distance):
            self.vy = -abs(self.vy)  # Reflect upwards
            self.y = space_size - buffer_distance - self.r


# Create stars
stars = [
    Star(300, 500, 0, -2, 30, 3000, (200, 50, 255)),
    Star(700, 500, 0, 2, 60, 6000, (255, 50, 200)),  # second massive star
]

# Initialize smaller stars in a circular pattern
num_stars = 100
for i in range(num_stars):
    angle = i * (2 * np.pi / num_stars)
    radius = 200  # Adjust as needed
    x = stars[0].x + radius * np.cos(angle)
    y = stars[0].y + radius * np.sin(angle)
    omega = 0.01  # Adjust as needed
    vx = -2 * omega * radius * np.sin(angle)
    vy =  2 * omega * radius * np.cos(angle)
    mass = random.uniform(1, 10)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    stars.append(Star(x, y, vx, vy, 5, mass, color))

# ... (previous code)

# ... (previous code)

start_time = time.time()
simulation_time = 0.0  # Track the simulated time
rate = 60
dt = 1 / rate
space_size = 1000
G = 0.0000000006
simulation_speed = 1.0  # Adjust as needed, 1.0 for normal speed

pygame.init()
screen = pygame.display.set_mode([space_size, space_size])
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)  # You can adjust the font size and style

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulation_speed *= 2.0  # Double the simulation speed on space key press
                print(f"Simulation speed increased to {simulation_speed}x")

    elapsed_seconds = simulation_time
    elapsed_minutes = elapsed_seconds / 60
    elapsed_hours = elapsed_minutes / 60
    elapsed_days = elapsed_hours / 24
    elapsed_years = elapsed_days / 365

    elapsed_text = font.render(
        f"Elapsed Time: {elapsed_years:.2f} years ({elapsed_days:.2f} days, {elapsed_hours:.2f} hours, {elapsed_minutes:.2f} minutes, {elapsed_seconds:.2f} seconds)",
        True,
        (255, 255, 255)
    )

    screen.fill((0, 0, 0))

    # Draw stars as circles
    for star in stars:
        pygame.draw.circle(screen, star.color, (int(star.x), int(star.y)), star.r)

    # Update particle positions and apply gravity
    for star in stars:
        star.update(dt * simulation_speed, stars, G, space_size)

    simulation_time += dt * simulation_speed  # Update simulated time

    screen.blit(elapsed_text, (10, 10))  # Display elapsed time in the top-left corner

    pygame.display.flip()
    clock.tick(rate)

pygame.quit()
