import pygame
import math
from random import randint
pygame.init()

WIDTH, HEIGHT = 1500, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Planet Simulation")

WHITE = (255,255,255)
ORANGE = (242,131,32)
GREY = (141,138,136)
BLUE = (70, 139, 172)

class Planet:
    AU = 149.6e6 * 1000 #distance from sun in meters
    G = 6.67426e-11
    SCALE = 15 / AU #approx smaller scale of AU 
    TIMESTEP = 3600 * 24 * 5 # 5 days

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass #in kg

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        if len(self.orbit) > 2:

            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(WIN, self.color, False, updated_points, 1)
        pygame.draw.circle(WIN, self.color, (x,y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 4, ORANGE, 1.98892 * 10**30) #the sun #replace to make it bigger
    sun.sun = True

    #the planets:
    moon = Planet(0.387 * Planet.AU, 0, 1, GREY, 3.3010 * 10**23) #replace w moon's stuff
    moon.y_vel = -47.87 * 1000
    
    earth = Planet(1 * Planet.AU, 0, 2, BLUE, 5.9722 * 10**24) #replace to make it bigger
    earth.y_vel = 29.78 * 1000

    planets = [sun, earth, moon]

    while run:

        clock.tick(60)

        input()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)


    pygame.quit()

main()