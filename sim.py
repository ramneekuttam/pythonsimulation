import pygame
import math

pygame.init()
#hey how are you 
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation ")

YELLOW = (255, 187, 0)
BLUE = (0, 60, 255)
RED = (255, 0, 0)
DARKGREY = (121, 123, 130)
WHITE = (255, 255 , 255)

class Planet():
   AU = 149.6e6 * 1000
   G = 6.67428e-11
   SCALE = 250 / AU #1AU = 250 px
   TIMESTEP = 3600 * 24 #1day

   def __init__(self, x, y, radius, color, mass):
      self.x = x
      self.y = y
      self.radius = radius 
      self.color = color 
      self.mass = mass

      self.orbit = []
      self.sun = False
      self.distanceTosun = 0

      self.xvel = 0
      self.yvel = 0

   def draw(self, win):
      x = self.x * self.SCALE + WIDTH/2 
      y = self.y * self.SCALE + WIDTH/2

      if len(self.orbit) > 2:
         updated_point = []
         for point in self.orbit:
            x, y = point 
            x = x * self.SCALE + WIDTH / 2
            y = y * self.SCALE + HEIGHT / 2
            updated_point.append((x, y))
      
         pygame.draw.lines(win, self.color, False, updated_point, 2)

      pygame.draw.circle(win, self.color, (x,y), self.radius, )

   def attraction(self, other):
      other_x , other_y = other.x , other.y
      distance_x = other_x - self.x
      distance_y = other_y - self.y
      distance = math.sqrt(distance_x**2 + distance_y**2)
      
      if other.sun:
         self.distanceTosun = distance
      
      force = self.G * self.mass * other.mass / distance**2
      theta = math.atan2(distance_y, distance_x)
      force_x = math.cos(theta) * force
      force_y = math.sin(theta) * force

      return force_x, force_y
   
   def update_pos(self, planets):
      total_fx = total_fy = 0
      for planet in planets:
         if self == planet:
            continue
         fx, fy = self.attraction(planet)
         total_fx += fx
         total_fy += fy
      
      self.xvel += total_fx / self.mass * self.TIMESTEP
      self.yvel += total_fy / self.mass * self.TIMESTEP

      self.x += self.xvel * self.TIMESTEP
      self.y += self.yvel * self.TIMESTEP
      self.orbit.append((self.x, self.y))

def main():
   run = True
   clock = pygame.time.Clock()

   sun = Planet(0, 0, 5, YELLOW, 1.98892 * 10**30)
   sun.sun = True

   earth = Planet(-1 * Planet.AU, 0, 4, BLUE, 5.9742 * 10**24)
   earth.yvel = 9.983  * 1000
   # earth.xvel = 90000 for gravitational assist
   
   mars = Planet(-1.524 * Planet.AU, 0, 4, RED, 6.39 * 10**23)
   mars.yvel = 24.077 * 1000

   mercury = Planet(0.387 * Planet.AU, 0, 4, DARKGREY, 3.30 * 10**24)
   mercury.yvel = -47.4 * 1000

   venus = Planet(-0.723 * Planet.AU, 0, 4, WHITE, 4.8685 * 10**24)
   venus.yvel = -35.02 * 1000

   planets = [venus, earth, mars, mercury, sun]

   while run:
      clock.tick(60)

      WIN.fill((0, 0, 0))
      # pygame.display.update()

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
   
      for planet in planets:
         planet.update_pos(planets)
         planet.draw(WIN)

      pygame.display.update()

   pygame.QUIT()

main()