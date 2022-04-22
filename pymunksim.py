import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 800, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(space, window, draw_options, line):
    window.fill("white")
    
    
    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)
    
    space.debug_draw(draw_options)
    pygame.display.update()
    
def create_boundaries(space, WIDTH, HEIGHT):
    rects = [
        [(WIDTH/2,  HEIGHT - 10), (WIDTH, 20)],
        [(WIDTH/2, 10), (WIDTH, 20)],
        [(10, HEIGHT/2), (20, HEIGHT)],
        [(WIDTH - 10, HEIGHT/2), (20, HEIGHT)]
    ]
    
    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)
        
def create_structure(space, WIDTH, HEIGHT):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(400, HEIGHT - 120), (40, 200), BROWN, 100],
        [(700, HEIGHT - 120), (40, 200), BROWN, 100],
        [(550, HEIGHT - 240), (340,  40), BROWN, 150]
    ]
    
    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius = 1.5)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)
        
                
def create_desk(space, WIDTH, HEIGHT):
    BROWN = (139, 69, 19, 100)
    rects = [
        [(600, HEIGHT - 120), (40, 200), BROWN, 100],
        [(200, HEIGHT - 120), (45, 245), BROWN, 100]
    ]
    
    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius = 1.5)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 1
        shape.friction = 1
        space.add(body, shape)
        
def create_swinging_ball(space):
    rotation_center_body = pymunk.Body(body_type = pymunk.Body.STATIC)
    rotation_center_body.position = (200, 235)
    
    body = pymunk.Body()
    body.position = (200, 235)
    line = pymunk.Segment(body, (0, 0), (200, 0), 5)
    circle = pymunk.Circle(body, 30, (200, 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)

def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape
    
    
def run(window, HEIGHT, WIDTH):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps
    
    space = pymunk.Space()
    space.gravity  = (0, 981)
    
    create_boundaries(space, WIDTH, HEIGHT)
    create_structure(space, WIDTH, HEIGHT)
    create_swinging_ball(space)
    create_desk(space, WIDTH, HEIGHT)
    
    draw_options = pymunk.pygame_util.DrawOptions(window)
    
    pressed_pos = None
    ball = None
    
    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 100
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None
        
        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)
        
    pygame.quit()

if __name__ == "__main__":
    run(window, HEIGHT, WIDTH)
         

