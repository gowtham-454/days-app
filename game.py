import pygame
import math
import random

# Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.2

class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = 3
        self.vy = -8
        self.radius = 10
        self.color = (255, 0, 0)  # Initial color: Red

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class Hexagon:
    def __init__(self):
        self.center_x = WIDTH / 2
        self.center_y = HEIGHT / 2
        self.size = 200
        self.angle = 0
        self.color = (255, 255, 255)  # Initial color: White

    def update(self):
        self.angle += 1

    def draw(self, screen):
        points = []
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            px = self.center_x + math.cos(angle) * self.size
            py = self.center_y + math.sin(angle) * self.size
            points.append((px, py))
        pygame.draw.polygon(screen, self.color, points, 5)

    def get_walls(self):
        points = []
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            px = self.center_x + math.cos(angle) * self.size
            py = self.center_y + math.sin(angle) * self.size
            points.append((px, py))
        walls = []
        for i in range(6):
            p1 = points[i]
            p2 = points[(i + 1) % 6]
            walls.append((p1, p2))
        return walls

def distance_to_line(ball_x, ball_y, line_p1, line_p2):
    x0, y0 = ball_x, ball_y
    x1, y1 = line_p1
    x2, y2 = line_p2
    numerator = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1))
    denominator = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return numerator / denominator

def check_collision(ball, hexagon):
    walls = hexagon.get_walls()
    for wall in walls:
        p1, p2 = wall
        distance = distance_to_line(ball.x, ball.y, p1, p2)
        if distance < ball.radius:
            # Change colors
            ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            hexagon.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Reflect ball
            normal_x = (p2[1] - p1[1]) / math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
            normal_y = -(p2[0] - p1[0]) / math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
            dot_product = ball.vx * normal_x + ball.vy * normal_y
            ball.vx = ball.vx - 2 * dot_product * normal_x
            ball.vy = ball.vy - 2 * dot_product * normal_y
            
            # Correct ball position to be inside hexagon
            closest_point = get_closest_point_on_line(ball.x, ball.y, p1, p2)
            ball.x = closest_point[0] - normal_x * ball.radius
            ball.y = closest_point[1] - normal_y * ball.radius

def get_closest_point_on_line(ball_x, ball_y, line_p1, line_p2):
    x0, y0 = ball_x, ball_y
    x1, y1 = line_p1
    x2, y2 = line_p2
    dx = x2 - x1
    dy = y2 - y1
    t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx ** 2 + dy ** 2)
    t = max(0, min(1, t))  # Ensure t is within segment bounds
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    return (closest_x, closest_y)

def is_point_inside_hexagon(point_x, point_y, hexagon):
    walls = hexagon.get_walls()
    n = len(walls)
    inside = False
    p1x, p1y = walls[0][0]
    for i in range(n + 1):
        p2x, p2y = walls[i % n][0]
        if point_y > min(p1y, p2y):
            if point_y <= max(p1y, p2y):
                if point_x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point_y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or point_x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = Ball()
    hexagon = Hexagon()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        ball.update()
        hexagon.update()

        check_collision(ball, hexagon)

        # Ensure ball is inside hexagon
        if not is_point_inside_hexagon(ball.x, ball.y, hexagon):
            # Move ball to nearest point on hexagon boundary
            walls = hexagon.get_walls()
            min_distance = float('inf')
            closest_wall = None
            for wall in walls:
                p1, p2 = wall
                distance = distance_to_line(ball.x, ball.y, p1, p2)
                if distance < min_distance:
                    min_distance = distance
                    closest_wall = wall
            p1, p2 = closest_wall
            normal_x = (p2[1] - p1[1]) / math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
            normal_y = -(p2[0] - p1[0]) / math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)
            closest_point = get_closest_point_on_line(ball.x, ball.y, p1, p2)
            ball.x = closest_point[0] - normal_x * ball.radius
            ball.y = closest_point[1] - normal_y * ball.radius

        # Boundary checking for screen edges
        if ball.x - ball.radius < 0 or ball.x + ball.radius > WIDTH:
            ball.vx = -ball.vx
        if ball.y - ball.radius < 0 or ball.y + ball.radius > HEIGHT:
            ball.vy = -ball.vy * 0.9

        hexagon.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
