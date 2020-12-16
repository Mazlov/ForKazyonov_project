import pygame
import sys
import pygame.draw
import os
import math

FPS = 60

screen_width = 1400
screen_height = 950
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
black = (0, 0, 0)
white = (255, 255, 255)
hero_size = {'x': 56, 'y': 56}
hero_velocity = 500
mouse_pos = {'x':  screen_width/2,'y': screen_height/2}
mouse_impact = 0.15
hero_sprite = ["player_stand.png", "player_walk1.png", "player_walk2.png", "player_walk3.png", "player_walk4.png"]
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.jpg")), (screen_width, screen_height))
STAN_BUTTON = pygame.image.load(os.path.join("sprites", "stan.png"))
BULLET_RED = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
BULLET_GREEN = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BULLET_YELLOW = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
BULLET_BLUE = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
COLOR_MAP = {
            "red": BULLET_RED,
            "green": BULLET_GREEN,
            "blue": BULLET_BLUE,
            "yellow": BULLET_YELLOW,
}
bullets = []
new_bullets = []
angle = math.pi
sin = 1
cos = 0
ability_cooldown = 10
stan_cooldown = 0
stan_range = 60


class all_map():
    def __init__(self, objects):
        """ Конструктор класса all_map
        придает всем объектам нна карте класс all_map, чтобы их можно
        было все одновременно двигать, не двигая персоннажа
        Args:
        objects - объект класса all_map
        """
        self.objects = objects
        self.color = black
        
    def render(self):
        screen.fill((255, 255, 255))
        for object in self.objects:
            object.draw()

    def forward(self, axis_x, axis_y):
        #функция движения всей карты вперед
        t = True
        for object in self.objects:
            t = t and not (object.x + object.width >= hero.x and object.x <= hero.x and object.y + object.height * 0.4 >= hero.y and object.y <= hero.y + 35)
        for object in self.objects:
            if t:
                if axis_y == 1:
                    object.y -= hero_velocity / FPS / (2**0.5)
                else:
                    object.y -= hero_velocity / FPS
            else:
                pass
        
    def backward(self, axis_x, axis_y):
        #функция движения всей карты вниз
        t = True
        for object in self.objects:
            t = t and not (object.x + object.width >= hero.x and object.x <= hero.x and object.y + object.height >= hero.y - 15 and object.y + object.height * 0.6 <= hero.y)
        for object in self.objects:
            if t:
                if axis_y == 1:
                    object.y += hero_velocity / FPS / (2**0.5)
                else:
                    object.y += hero_velocity / FPS
            else:
                pass
            
    def left(self, axis_x, axis_y):
        #функция движения всей карты влево
        t = True
        for object in self.objects:
            t = t and not (object.x <= hero.x + 35 and object.x + object.width * 0.4 >= hero.x and object.y <= hero.y and object.y + object.height >= hero.y)
        for object in self.objects:
            if t:
                if axis_x == 1:
                    object.x -= hero_velocity / FPS / (2**0.5)
                else:
                    object.x -= hero_velocity / FPS
            else:
                pass
            
    def right(self, axis_x, axis_y):
        #функция движения всей карты вправо
        t = True
        for object in self.objects:
            t = t and not (object.x + object.width * 0.6 <= hero.x and object.x + object.width >= hero.x - 15 and object.y <= hero.y and object.y + object.height >= hero.y)
        for object in self.objects:
            if t:
                if axis_x == 1:
                    object.x += hero_velocity / FPS / (2**0.5)
                else:
                    object.x += hero_velocity / FPS
            else:
                pass
            

class Wall():
    def __init__(self, x, y, width, height):
        """ Конструктор класса wall
        Args:
        x - положение стены по горизонтали
        y - положение стены по вертикали
        width - длина
        height - высота
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = black
        
    def draw(self):
        #функция рисования стены на карте
        pygame.draw.rect(screen, black, (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact, self.width, self.height))


class Hero():
    def __init__(self, cos, sin, angle):
        """ Конструктор класса hero
        """
        self.length = 56
        self.height = 56
        self.x = screen_width/2
        self.y = screen_height/2
        self.color = black
        self.cos = cos
        self.sin = sin
        self.angle =  (angle / math.pi)*180 - 90
        self.time = 0
        self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
    
    def rotate(self, cos, sin, angle):
        self.cos = cos
        self.sin = sin
        self.angle = (angle / math.pi)*180 - 90
        self.img = pygame.transform.rotate(self.img_0, self.angle)
        
    def draw(self, cos, sin, angle):
        screen.blit(self.img, (self.x - mouse_pos['x'] * mouse_impact - self.length / 2, self.y - mouse_pos['y'] * mouse_impact - self.height / 2))
        self.mask = pygame.mask.from_surface(self.img)
        
    def hero_update(self, x, y):
        self.x += mouse_pos['x'] * mouse_impact
        self.y += mouse_pos['y'] * mouse_impact
        
    def sprite_update(self):
        if (self.time // 8) % 5 == 1:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[1]))
        elif (self.time // 8) % 5 == 2:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[2]))
        elif (self.time // 8) % 5 == 3:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[3]))
        elif (self.time // 8) % 5 == 4:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[4]))
        else:
            self.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
            
class Enemy():
    def __init__(self, x, y, angle, traectory, number):
        self.traectory = traectory
        self.tr_len = len(self.traectory) / 2
        self.angle = angle
        self.width = 0
        self.height = 0
        self.x = x
        self.y = y
        self.x_from = self.x
        self.y_from = self.y
        self.velocity = 50 / FPS
        self.img = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
        self.trace = 0
        self.number = number
        self.stan_time = 0
        self.img = pygame.transform.rotate(self.img,  self.angle)
        self.moving = 0
        
    def draw(self):
        screen.blit(self.img, (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact))
        
    def vision(self, a):
        if not self.trace and self.stan_time == 0:
            self.trace = Trace(self.x + hero.length / 2, self.y + hero.height / 2, self.angle)
            a.append(self.trace)
            self.index = len(a) - 1
        elif self.stan_time == 0:
            self.trace.move()
            self.trace.check(self.index, a, self.number)
            
    def stan(self, stan_time):
        self.stan_time = stan_time * FPS
        if self.trace != 0:
            self.trace.delete(self.index)
        if self.stan_time >= 0:
            self.trace = 0
            
    def move(self):
        if self.tr_len > 0:
            self.x_to = self.x_from + self.traectory[0]
            self.y_to = self.y_from + self.traectory[1]
            if self.x > self.x_from + self.x_to - 10 and self.x < self.x_from + self.x_to + 10 and self.y > self.y_from + self.y_to - 10 and self.y < self.y_from + self.y_to + 10:
                self.moving = 0
            elif self.moving == 0:
                self.img = pygame.transform.rotate(self.img,  -self.angle)
                self.sin = (self.y_to - self.y_from) / ((self.x_to - self.x_from) ** 2 + (self.y_to - self.y_from) ** 2) ** 0.5
                if self.sin < 0:
                    self.angle = (math.pi - math.asin((self.y_to - self.y_from) / ((self.x_to - self.x_from) ** 2 + (self.y_to - self.y_from) ** 2) ** 0.5)) * 180 - 90
                else:
                    self.angle = (math.asin((self.y_to - self.y_from) / ((self.x_to - self.x_from) ** 2 + (self.y_to - self.y_from) ** 2) ** 0.5)) * 180 - 90
                print(self.angle)
                self.img = pygame.transform.rotate(self.img, self.angle)
                self.moving = 1
            pygame.draw.rect(screen, black, (self.x_to - mouse_pos['x'] * mouse_impact, self.y_to - mouse_pos['y'] * mouse_impact, 20, 20))
            self.x += self.velocity * math.cos(self.angle)
            self.y += self.velocity * math.sin(self.angle)

class Trace():
    def __init__(self, x, y, angle):
        self.angle = angle
        self.width = 0
        self.height = 0
        self.bx = x
        self.by = y
        self.x = x
        self.y = y
        self.vx = 50 * math.sin(angle / 180 * math.pi) / FPS * 60
        self.vy = 50 * math.cos(angle / 180 * math.pi) / FPS * 60
        self.time = 0
        self.killed = 0
    
    def move(self):
        self.x += self.vx
        self.y += self.vy
    
    def check(self, index, a, enemy):
        if self.killed:
            enemies[enemy].trace = 0
            self.delete(index)
        for wall in walls:
            if self.x > wall.x - wall.width and self.x < wall.x + wall.width * 2 and self.y > wall.y - wall.height and self.y < wall.y + wall.height * 2:
                self.killed = 1
    
    def delete(self, index):
        walls.pop(index)
        for enemy in enemies:
            if index < enemy.index:
                enemy.index -= 1
    
    def draw(self):
        pygame.draw.rect(screen, black, (self.x - mouse_pos['x'] * mouse_impact, self.y - mouse_pos['y'] * mouse_impact, 50, 50))
        return
            
class Bullet():
    def __init__ (self, x, y, cos, sin, angle, color, speed = 20):
        self.x = x
        self.y = y
        self.cos = cos
        self.sin = sin
        self.speed = speed
        self.type = COLOR_MAP[color]
        self.angle = - (angle / math.pi)*180 - 90

    def move(self):
        self.y += self.speed * self.cos
        self.x += self.speed * self.sin

    def draw(self):
        self.img = pygame.transform.rotate(self.type, self.angle)
        screen.blit(self.img, (self.x, self.y))
        
def stan(stan_time):
    for enemy in enemies:
        if hero.x < enemy.x + 28 + stan_range and hero.x > enemy.x + 28 - stan_range and hero.y < enemy.y + 28 + stan_range and hero.y > enemy.y + 28 - stan_range:
            enemy.stan(stan_time)

enemies = [Enemy(400, 230, 250, [], 0), Enemy(520, 280, 30, [], 1), Enemy(270, 320, 180, [], 2)] #
hero = Hero(sin, cos, angle)
walls = enemies + [Wall(200, 200, 600, 16), Wall(200, 200, 16, 200), Wall(200, 400, 200, 16), Wall(800, 200, 16, 200), Wall(470, 400, 346, 16)]
mymap = all_map(walls)

flag = {'forward': 0, 'backward': 0, 'left': 0, 'right': 0}
scripts = {'forward': mymap.forward, 'backward': mymap.backward, 'left': mymap.left, 'right': mymap.right}
buttons = {'forward': pygame.K_s, 'backward': pygame.K_w, 'left': pygame.K_d, 'right': pygame.K_a}
axis = {'Ox': 0, 'Oy': 0}

pygame.display.update()
clock = pygame.time.Clock()
while 1:
    clock.tick(FPS)
    hero.time += 1
    if mouse_pos['x'] != 0:
        if sin > 0:
            angle = math.pi - math.asin ((mouse_pos['y']) / ((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2) ** 0.5)
            sin = (mouse_pos['x']) / math.sqrt( (mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2 )
            cos = (mouse_pos['y']) / math.sqrt( (mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2 )
        else:
            angle = math.asin ((mouse_pos['y']) / ((mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2) ** 0.5)
            sin = (mouse_pos['x']) / math.sqrt( (mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2 )
            cos = (mouse_pos['y']) / math.sqrt( (mouse_pos['x']) ** 2 + (mouse_pos['y']) ** 2 )
    elif cos // 1 == -1:
        angle = -math.pi / 2
        sin = 0
        cos = -1
    else:
        angle = math.pi /2
        sin = 0
        cos = 1
    print(angle)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            for key in buttons:
                if event.key == buttons[key]:
                    flag[key] = 1
                    if (flag['left'] == 1 or flag['right'] == 1) and flag['left'] != flag['right']:
                        axis['Oy'] = 1
                    if (flag['forward'] == 1 or flag['backward'] == 1) and flag['forward'] != flag['backward']:
                        axis['Ox'] = 1
                if event.key == pygame.K_f:
                    if stan_cooldown == 0:
                        stan(5)
                        stan_cooldown = ability_cooldown * FPS
                        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos['x'], mouse_pos['y'] = event.pos[0] - screen_width/2, event.pos[1] - screen_height/2
            
        if event.type == pygame.KEYUP:
            for key in buttons:
                if event.key == buttons[key]:
                    flag[key] = 0
                    if (flag['left'] != 1 and flag['right'] != 1) or flag['left'] == flag['right']:
                        axis['Oy'] = 0
                    if (flag['forward'] != 1 and flag['backward'] != 1) or flag['forward'] == flag['backward']:
                        axis['Ox'] = 0
    
    for key in flag:
        if flag[key]:
            scripts[key](axis['Ox'], axis['Oy'])
            hero.sprite_update()
    
    mymap.render()
    hero.rotate(sin, cos, angle)
    hero.draw(sin, cos, angle)
    if stan_cooldown > 0:
        stan_cooldown -= 1
    for enemy in enemies:
        enemy.vision(walls)
        enemy.move()
        if enemy.stan_time > 0:
            enemy.stan_time -= 1
        if stan_cooldown == 0 and hero.x < enemy.x + 28 + stan_range and hero.x > enemy.x + 28 - stan_range and hero.y < enemy.y + 28 + stan_range and hero.y > enemy.y + 28 - stan_range:
            pygame.draw.rect(screen, (255, 255, 255), (hero.x - 70, hero.y * 2 - 85, 140, 50))
            screen.blit(STAN_BUTTON, (hero.x - 80, hero.y * 2 - 95))
            font = pygame.font.Font(None, 30)
            name_text = font.render('ОГЛУШИТЬ F', 1, (0, 0, 0))
            screen.blit(name_text, (hero.x - 70, hero.y * 2 - 69))
    pygame.display.update()
    hero.img_0 = pygame.image.load(os.path.join("sprites", "PNG", "Player", "Poses", hero_sprite[0]))
