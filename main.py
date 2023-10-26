import pygame
import os
import math
import random
pygame.font.init()
pygame.mixer.init()
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Tussle")
FPS = 40
BULLET_VEL = 10
VEL = 3
BOUNCE_AMT = 5
MENU = ["play","quit"]
TURNING_SPEED = 3
PLAYER_WIDTH,PLAYER_HEIGHT = 64,64
WHITE = (255,255,255)
GRAY = (230,230,230)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
MAX_BULLETS = 5
MENU_MUSIC = pygame.mixer.Sound(os.path.join("assets","TankTussle_Music.wav"))
SWITCH = pygame.mixer.Sound(os.path.join("assets","switching.wav"))
SELECT = pygame.mixer.Sound(os.path.join("assets","selecting.wav"))
ROTATE = pygame.mixer.Sound(os.path.join("assets",'rotating.wav'))
MOVE = pygame.mixer.Sound(os.path.join("assets",'moving.wav'))
BOOM = pygame.mixer.Sound(os.path.join("assets",'explosion.wav'))

GREEN_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets','i01_green.png')),(PLAYER_WIDTH,PLAYER_HEIGHT)),-90)
RED_IMAGE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('assets','i02_red.png')),(PLAYER_WIDTH,PLAYER_HEIGHT)),90)
LOGO = pygame.transform.scale(pygame.image.load(os.path.join('assets','logo.png')),(800,200))
FONT = pygame.font.Font(os.path.join('assets','PublicPixel.ttf'),80)
class wall_class():
    def __init__(self,type,x,y):
        self.type = type
        if type == "vertical":
            self.pos = pygame.Rect(x,y,7,150)
        else:
            self.pos = pygame.Rect(x,y, 150, 7)
class bullet_class():
    def __init__(self, angle,x,y):
        self.shot = pygame.Rect(x + PLAYER_WIDTH, y + PLAYER_HEIGHT // 2 - 2, 10, 5)
        self.angle = angle
        self.bounces = BOUNCE_AMT
class wallbreaker_class():
    def __init__(self, angle,x,y,color):
        self.shot = pygame.Rect(x + PLAYER_WIDTH, y + PLAYER_HEIGHT // 2 - 2, 10, 5)
        self.angle = angle
        self.color = color
def draw_menu(menu_index):
    WIN.fill(GRAY)
    logo = pygame.Rect(50,100,800,100)
    play_button = pygame.Rect(250,400,400,100)
    quit_button = pygame.Rect(250, 600, 400, 100)
    if menu_index == 0:
        select = pygame.Rect(245,395,410,110)
    else:
        select = pygame.Rect(245, 595, 410, 110)
    WIN.blit(LOGO,(logo.x,logo.y))
    pygame.draw.rect(WIN,BLACK,select)
    pygame.draw.rect(WIN,WHITE,play_button)
    pygame.draw.rect(WIN, WHITE, quit_button)
    play_text = FONT.render("PLAY",1,BLACK)
    quit_text = FONT.render("QUIT", 1, BLACK)
    WIN.blit(play_text,(play_button.x+50,play_button.y+5))
    WIN.blit(quit_text,(quit_button.x+50,quit_button.y+5))
    pygame.display.update()
def draw_window(green,red,green_bullets,red_bullets,wallbreakers,red_angle,green_angle,walls):
    WIN.fill(WHITE)
    for bullet in green_bullets:
        pygame.draw.circle(WIN,BLACK,(bullet.shot.x,bullet.shot.y),5,5,5,True,True,True)
    for bullet in red_bullets:
        pygame.draw.circle(WIN,BLACK,(bullet.shot.x,bullet.shot.y),5,5,5,True,True,True)
    for wallbreaker in wallbreakers:
        pygame.draw.circle(WIN, BLUE, (wallbreaker.shot.x, wallbreaker.shot.y), 10, 10, 10, True, True, True)
    for wall in walls:
        pygame.draw.rect(WIN,BLACK,wall.pos)
    green_sprite, rect1 = rot_center(GREEN_IMAGE, green_angle, green.x, green.y)
    WIN.blit(green_sprite, (rect1.x, rect1.y))
    red_sprite, rect2 = rot_center(RED_IMAGE, red_angle, red.x, red.y)
    green = rect1
    red = rect2
    WIN.blit(red_sprite, (rect2.x, rect2.y))
    pygame.display.update()
    return green,red
def draw_winner(text):
    menu = True
    replay = False
    menuIndex = 0
    while menu:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MENU_MUSIC.stop()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or pygame.event == pygame.K_UP:
                    if menuIndex != 0:
                        SWITCH.play()
                        menuIndex -= 1
                if event.key == pygame.K_s or pygame.event == pygame.K_DOWN:
                    if menuIndex != 1:
                        SWITCH.play()
                        menuIndex += 1
                if event.key  == pygame.K_SPACE:
                    if MENU[menuIndex] == "play":
                        SELECT.play()
                        MENU_MUSIC.stop()
                        replay = True
                        menu = False
                    else:
                        menu = False
                        replay = False
        play_button = pygame.Rect(250, 400, 400, 100)
        quit_button = pygame.Rect(250, 600, 400, 100)
        if menuIndex == 0:
            select = pygame.Rect(245, 395, 410, 110)
        else:
            select = pygame.Rect(245, 595, 410, 110)
        pygame.draw.rect(WIN, WHITE, select)
        play_text = FONT.render("REPLAY", 1, WHITE)
        quit_text = FONT.render("QUIT", 1, WHITE)
        pygame.draw.rect(WIN, BLACK, play_button)
        pygame.draw.rect(WIN, BLACK, quit_button)
        WIN.blit(play_text, (play_button.x + 50, play_button.y + 5))
        WIN.blit(quit_text, (quit_button.x + 50, quit_button.y + 5))
        pygame.display.update()
    return replay
def grid_creation(walls):
    x = -2
    y = 0
    maze = [1,2,3,4,5,6,7,8,9]
    for i in range(7):
        for j in range(7):
            if random.choice(maze) == 1:
                wall = wall_class("vertical",x,y)
                wall2 = wall_class("horizontal",x,y)
                walls.append(wall)
                walls.append(wall2)
            elif random.choice(maze) == 2 or random.choice(maze) == 3 or random.choice(maze) == 4 or random.choice(maze) == 5:
                wall = wall_class("vertical", x, y)
                walls.append(wall)
            elif random.choice(maze) == 6 or random.choice(maze) == 7 or random.choice(maze) == 8 or random.choice(maze) == 9:
                wall = wall_class("horizontal", x, y)
                walls.append(wall)
            x += 150
            j += 1
        x = -2
        y += 150
        i += 1


    return walls
def rot_center(image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)
    return rotated_image, new_rect
def angle_calculation(angle,type,):
    if angle < 0:
        angle += 360
    if type == "vertical":
        if (angle > 0 and angle < 90):
            beta = 90 - angle
            alpha = 90 + beta
            angle = alpha
        elif angle > 90 and angle < 180:
            theta = 180 - angle
            beta = 180 - 90 - theta
            alpha = beta
            angle = 90 - alpha
        elif angle > 180 and angle < 270:
            theta = angle - 180
            beta = 180-90 - theta
            alpha = 90 - beta
            angle = -1*alpha
        elif angle > 270 and angle < 360:
            theta = angle - 270
            beta = 180 - 90 - theta
            alpha = 90 - beta
            angle = -1 * alpha - 90
        elif angle == 180:
            angle = 0
        elif angle == 0:
            angle = 180
    else:
        if (angle > 0 and angle < 90):
            angle = -1*angle
        elif angle > 90 and angle < 180:
            angle = -1*angle
        elif angle > 180 and angle < 270:
            angle = -1 * angle
        elif angle > 270 and angle < 360:
            angle = -1 * angle
        elif angle == 270:
            angle = 90
        elif angle == 90:
            angle = 270
    return angle
def distance(ax,ay,bx,by):
    deltax = math.fabs(ax-bx)
    deltay = math.fabs(ay-by)
    distance = math.ceil(math.sqrt(pow(deltax,2)+pow(deltay,2)))
    return distance
def wall_collision(vel_x,vel_y,hitbox,walls,color,direction,angle,bullet1):
    type = ""
    collide = False
    if bullet1 == "bullet":
        vel_x,vel_y = x_y_calculation(angle,BULLET_VEL,"bullet")
        if color == "red":
            vel_x = vel_x * -1
    #if color == "red":
    if direction == "backwards":
        vel_x = vel_x * -1
        vel_y = vel_y * -1
    for wall in walls:
        if vel_x > 0:
            if (hitbox.topright[0] + vel_x > wall.pos.bottomleft[0] and hitbox.topright[0] + vel_x < wall.pos.bottomright[0]) and (hitbox.bottomright[1] > wall.pos.topleft[1]-3 and hitbox.topright[1] < wall.pos.bottomleft[1]+3):
                collide = True
                type = wall.type
        if vel_x < 0:
            if (hitbox.topleft[0] + vel_x < wall.pos.bottomright[0] and hitbox.topleft[0] + vel_x > wall.pos.bottomleft[0]) and (hitbox.bottomleft[1] > wall.pos.topright[1]-3 and hitbox.topleft[1] < wall.pos.bottomright[1]+3):
                collide = True
                type = wall.type
        if vel_y < 0:
            if (hitbox.bottomright[1] + vel_y > wall.pos.topright[1] and hitbox.bottomright[1] + vel_y < wall.pos.bottomright[1]) and (hitbox.bottomright[0] > wall.pos.topleft[0]-3 and hitbox.bottomleft[0] < wall.pos.topright[0]+3):
                collide = True
                type = wall.type
        if vel_y > 0:
            if (hitbox.topright[1] + vel_y < wall.pos.bottomright[1] and hitbox.topright[1] + vel_y > wall.pos.topright[1]) and (hitbox.bottomright[0] > wall.pos.topleft[0]-3 and hitbox.bottomleft[0] < wall.pos.topright[0]+3):
                collide = True
                type = wall.type
    return collide,type
def player1_handle_movement(keys_pressed,green_angle,green,walls,hitbox,rotate,moving):
    if keys_pressed[pygame.K_a]:  # LEFT
        green_angle += TURNING_SPEED
        ROTATE.play()
        rotate = True
    if keys_pressed[pygame.K_d]:  # RIGHT
        green_angle -= TURNING_SPEED
        ROTATE.play()
        rotate = True
    if keys_pressed[pygame.K_w]:  # UP
        x,y = x_y_calculation(green_angle,VEL,'tank')
        collide,type = wall_collision(x,y,hitbox,walls,"green","forwards",0,"none")
        if collide == False:
            MOVE.play()
            moving = True
            green.x += x
            green.y -= y
    if keys_pressed[pygame.K_s]:  # DOWN
        x, y = x_y_calculation(green_angle, VEL,'tank')
        collide,type = wall_collision(x, y, hitbox, walls, "green", "backwards",0,"none")
        if collide == False:
            moving = True
            MOVE.play()
            green.y += y
            green.x -= x
    return green_angle,rotate,moving
def player2_handle_movement(keys_pressed,red_angle,red,walls,hitbox,rotate,moving):
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        red_angle += TURNING_SPEED
        ROTATE.play()
        rotate = True
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        red_angle -= TURNING_SPEED
        ROTATE.play()
        rotate = True
    if keys_pressed[pygame.K_DOWN]:  # UP
        x, y = x_y_calculation(red_angle, VEL,'tank')
        collide,test = wall_collision(x, y, hitbox, walls, "red", "forwards",0,"none")
        if collide == False:
            MOVE.play()
            moving = True
            red.x += x
            red.y -= y
    if keys_pressed[pygame.K_UP]:  # DOWN
        x, y = x_y_calculation(red_angle, VEL,'tank')
        collide,test = wall_collision(x, y, hitbox, walls, "red", "backwards",0,"none")
        if collide == False:
            MOVE.play()
            moving = True
            red.y += y
            red.x -= x
    return red_angle,rotate,moving
def handle_bullets(green_bullets, red_bullets, green, red,wallbreakers,walls):
    for bullet in green_bullets:
        x,y = x_y_calculation(bullet.angle,BULLET_VEL,"bullet")
        bullet.shot.x += x
        bullet.shot.y -= y
        if red.colliderect(bullet.shot):
            pygame.event.post(pygame.event.Event(RED_HIT))
            BOOM.play()
            green_bullets.remove(bullet)
        elif bullet.shot.x > WIDTH or bullet.shot.y < 0 or bullet.shot.y > HEIGHT:
            green_bullets.remove(bullet)
        elif bullet.bounces <= 0:
            green_bullets.remove(bullet)
    for bullet in red_bullets:
        x, y = x_y_calculation(bullet.angle, BULLET_VEL,"bullet")
        bullet.shot.x -= x
        bullet.shot.y += y
        if green.colliderect(bullet.shot):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            BOOM.play()
            red_bullets.remove(bullet)
        elif bullet.shot.x < 0 or bullet.shot.x > WIDTH or bullet.shot.y < 0 or bullet.shot.y > HEIGHT:
            red_bullets.remove(bullet)
        elif bullet.bounces <= 0:
            red_bullets.remove(bullet)
    for wallbreaker in wallbreakers:
        x, y = x_y_calculation(wallbreaker.angle, BULLET_VEL/2, "bullet")
        if wallbreaker.color == "green":
            wallbreaker.shot.x += x
            wallbreaker.shot.y -= y
        else:
            wallbreaker.shot.x -= x
            wallbreaker.shot.y += y
        for wall in walls:
            if wall.pos.colliderect(wallbreaker.shot):
                walls.remove(wall)
                wallbreakers.remove(wallbreaker)
def handle_ricochets(bullets,walls,color):
    for bullet in bullets:
        collision,wall_type = wall_collision(1,1,bullet.shot,walls,color,"forwards",bullet.angle,"bullet")
        if collision:
                bullet.angle = angle_calculation(bullet.angle,wall_type)
                bullet.bounces -= 1
def x_y_calculation(angle,velocity,type):
    x = (velocity*math.fabs(math.cos(math.radians(angle))))
    y = (velocity*math.fabs(math.sin(math.radians(angle))))
    if angle > 0 and angle < 90:
        x = x
        y = y
    elif (angle > 90 and angle < 180) or (angle > -270 and angle < -180):
        x = -1*x
        y = y
    elif angle == 0:
        x = VEL
        y = 0
        if type == "bullet":
            x = BULLET_VEL
    elif angle == 90 or angle == -270:
        x = 0
        y = VEL
        if type == "bullet":
            y = BULLET_VEL
    elif angle == 270 or angle == -90:
        x = 0
        y = -1*VEL
        if type == "bullet":
            y = -1*BULLET_VEL
    elif angle == 180 or angle == -180:
        x = -1*VEL
        y = 0
        if type == "bullet":
            x = -1*BULLET_VEL
    elif (angle > 180 and angle < 270) or (angle > -180 and angle < -90):
        x = -1*x
        y = -1*y
    elif (angle > 270 and angle < 360) or (angle > -90 and angle < 0):
        y = -1*y
        x = x
    return x,y
def bullet_start_coords(color,angle):
    radius = PLAYER_WIDTH//2
    y = 0
    x = 0
    if (angle > 0 and angle < 90) or (angle <-270 and angle > -360):
        beta = 90 - angle
        y = math.ceil(radius*math.fabs(math.cos(math.radians(beta))))
        x = math.ceil(math.fabs(math.sqrt(pow(radius,2)-pow(y,2))))
        y = -1*y
    elif (angle > 90 and angle < 180) or (angle <-180 and angle > -270):
        beta = angle - 90
        y = math.ceil(radius * math.fabs(math.cos(math.radians(beta))))
        x = math.ceil(math.fabs(math.sqrt(pow(radius, 2) - pow(y, 2))))
        y = -1 * y
        x = -1*x

    elif (angle > 180 and angle < 270) or (angle < -90 and angle > -180):
        beta = 90 - angle - 180
        y = math.ceil(radius * math.fabs(math.cos(math.radians(beta))))
        x = math.ceil(math.fabs(math.sqrt(pow(radius, 2) - pow(y, 2))))
        x = -1 * x

    elif (angle > 270 and angle < 360) or (angle < 0 and angle > -90):
        beta = angle - 270
        y = math.ceil(radius * math.fabs(math.cos(math.radians(beta))))
        x = math.ceil(math.fabs(math.sqrt(pow(radius, 2) - pow(y, 2))))

    elif angle == 0:
        x = 32
        y = 0
    elif angle == 90:
        x = 0
        y = 32
    elif angle == 180:
        x = -32
        y = 0
    elif angle == 270:
        x = 0
        y = -32
    if color == "red":
        x = -1*x
    return x,y
def main():
    clock = pygame.time.Clock()
    menu_run = True
    menuIndex = 0
    menu = ["play", "quit"]
    MENU_MUSIC.play()
    while menu_run:
        clock.tick(FPS)
        draw_menu(menuIndex)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                MENU_MUSIC.stop()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or pygame.event == pygame.K_UP:
                    if menuIndex != 0:
                        SWITCH.play()
                        menuIndex -= 1
                if event.key == pygame.K_s or pygame.event == pygame.K_DOWN:
                    if menuIndex != 1:
                        SWITCH.play()
                        menuIndex += 1
                if event.key  == pygame.K_SPACE:
                    if menu[menuIndex] == "play":
                        SELECT.play()
                        MENU_MUSIC.stop()
                        menu_run = False
                    else:
                        MENU_MUSIC.stop()
                        pygame.quit()
    replay = True
    while replay:
        replay = False
        green = pygame.Rect(50.0, 50.0, PLAYER_WIDTH, PLAYER_HEIGHT)
        red = pygame.Rect(850.0, 850.0, PLAYER_WIDTH, PLAYER_HEIGHT)
        grn_hitbox = pygame.Rect(1000,1000,1,1,)
        red_hitbox = pygame.Rect(1000,1000,1,1)
        green_angle = -90
        red_angle = -90
        r_rotate = False
        r_move = False
        g_rotate = False
        g_move = False
        winner_text = ""
        green_bullets = []
        green_wallbreakers = 2
        red_bullets = []
        red_wallbreakers = 2
        wallbreaker_list = []
        green_health = 1
        red_health = 1
        walls = []
        walls = grid_creation(walls)
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT and len(green_bullets) < MAX_BULLETS:
                        x,y = bullet_start_coords(green,green_angle)
                        bullet_class(3,5,1)
                        bullet = bullet_class(green_angle, (green.x - PLAYER_WIDTH) + x, (green.y-PLAYER_WIDTH//2)+y)
                        green_bullets.append(bullet)
                    if event.key == pygame.K_LCTRL and green_wallbreakers > 0:
                        x,y = bullet_start_coords(green,green_angle)
                        wallbreaker = wallbreaker_class(green_angle, (green.x - PLAYER_WIDTH) + x, (green.y-PLAYER_WIDTH//2)+y,"green")
                        wallbreaker_list.append(wallbreaker)
                        green_wallbreakers -= 1
                    if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                        x, y = bullet_start_coords("red", red_angle)

                        bullet = bullet_class(red_angle, red.x - PLAYER_WIDTH + x, (red.y-PLAYER_WIDTH//2)-y,)
                        red_bullets.append(bullet)
                    if event.key == pygame.K_m and red_wallbreakers > 0:
                        x,y = bullet_start_coords("red",red_angle)
                        wallbreaker = wallbreaker_class(red_angle, (red.x - PLAYER_WIDTH) + x, (red.y - PLAYER_WIDTH // 2) + y,"red")
                        wallbreaker_list.append(wallbreaker)
                        red_wallbreakers -= 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and g_rotate:
                        ROTATE.stop()
                    if event.key == pygame.K_d and g_rotate:
                        ROTATE.stop()
                    if event.key == pygame.K_LEFT and r_rotate:
                        ROTATE.stop()
                    if event.key == pygame.K_RIGHT and r_rotate:
                        ROTATE.stop()
                    if event.key == pygame.K_w and g_move:
                        MOVE.stop()
                    if event.key == pygame.K_s and g_move:
                        MOVE.stop()
                    if event.key == pygame.K_UP and r_move:
                        MOVE.stop()
                    if event.key == pygame.K_UP and r_move:
                        MOVE.stop()

                if event.type == GREEN_HIT:
                    green_health -= 1

                if event.type == RED_HIT:
                    red_health -= 1

                if red_health <= 0:
                    winner_text = "Green Wins!"
                if green_health <= 0:
                    winner_text = "Red Wins!"
                if winner_text != "":
                    replay = draw_winner(winner_text)
                    if replay == False:
                        pygame.quit()
                        run = False
                    if replay == True:
                        run = False
                    # SOMEONE WON
            keys_pressed = pygame.key.get_pressed()
            green_angle,g_rotate,g_move = player1_handle_movement(keys_pressed,green_angle, green,walls,grn_hitbox,g_rotate,g_move)
            red_angle,r_rotate,r_move = player2_handle_movement(keys_pressed, red_angle, red,walls,red_hitbox,r_rotate,r_move)
            if green_angle >= 360 or green_angle <= -360:
                green_angle = 0
            if red_angle >= 360 or red_angle <= -360:
                red_angle = 0
            handle_bullets(green_bullets, red_bullets, green, red,wallbreaker_list,walls)
            handle_ricochets(green_bullets,walls,"green")
            handle_ricochets(red_bullets,walls,"red")
            grn_hitbox,red_hitbox = draw_window(green, red, green_bullets, red_bullets, wallbreaker_list,red_angle,green_angle,walls)
            print(green.x)
            print(green.y)
    pygame.quit()

if __name__ == "__main__":
        main()

