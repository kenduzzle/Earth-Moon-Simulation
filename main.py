import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Earth-Moon Simulation")

WHITE = (255, 255, 255)

class Body:
    AU = 149.6e6 * 1000  # Astronomical Unit in meters
    SCALE = 50 / (AU / 1496)  # 100 pixels = 100,000 km
    G = 6.67428e-11  # Gravitational Constant
    TIMESTEP = 3600 # 1 hour

    def __init__(self, x, y, radius, color, mass):
        self.x = x #meters away from earth
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass #in kg

        self.orbit = []
        self.earth = False
        self.distance_to_earth = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((int(x), int(y)))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

    def attraction_position(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        # Prevent extremely small distances
        if distance < 1e3:  # Minimum distance threshold (1km)
            distance = 1e3

        if self.earth:
            self.distance_to_earth = distance

        # Gravitational force calculation
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        self.x_vel += force_x / self.mass * self.TIMESTEP
        self.y_vel += force_y / self.mass * self.TIMESTEP

        #makes sure earth doesn't move out of the screen
        if not self.earth:
            self.x += self.x_vel * self.TIMESTEP
            self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))

def main(): 
    run = True
    clock = pygame.time.Clock()

    earth = Body(0, 0, 16, (100, 149, 237), 5.972 * 10 **24)
    earth.earth = True

    moon = Body(0.0026 * Body.AU, 0, 6, (90,90,90), 7.342 * 10 **22)
    moon.y_vel = 1022  # speed of the moon orbitting around earth
    bodies = [earth, moon]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for body in bodies:
            for other_body in bodies:
                if body != other_body:
                    body.attraction_position(other_body)
            body.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
