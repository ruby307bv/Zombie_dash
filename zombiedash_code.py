import pygame
from sys import exit
from random import randint
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(BASE_DIR, "music.mp3").replace('\\', '/'))
pygame.mixer.music.play(loops=-1)
screen = pygame.display.set_mode((600,300)) #tạo màn hình 600x300
pygame.display.set_caption('zombie dash')
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

ground_surface = pygame.image.load(os.path.join(BASE_DIR, "ground.png").replace('\\', '/')).convert_alpha()
text_surface = font.render('This is how you die', False, 'Red') 

bullet_surface = pygame.image.load(os.path.join(BASE_DIR, "bullet.png").replace('\\', '/')).convert_alpha()

zombie_surface = pygame.image.load(os.path.join(BASE_DIR, "zombie.png").replace('\\', '/')).convert_alpha() #zombie
# zombie_rectangle = zombie_surface.get_rect(midbottom = (randint(700,1000), 250))
flying_zombie_surface = pygame.image.load(os.path.join(BASE_DIR, "flying_zombie.png").replace('\\', '/')).convert_alpha()
obstacle_rect_list = []
bullet_rectangle_list = []

ammo_surface = pygame.image.load(os.path.join(BASE_DIR, "ammo.png").replace('\\', '/')).convert_alpha()
ammo_list = []


player_surface = pygame.image.load(os.path.join(BASE_DIR, "player.png").replace('\\', '/')) #player
player_rectangle = player_surface.get_rect(midbottom = (150,250))
player_rectangle.width = player_rectangle.width * 0.6

tire_surface = pygame.image.load(os.path.join(BASE_DIR, "tire.png").replace('\\', '/')).convert_alpha()
tire_list = []
tire_gravity = -10

player_gravity = 0
game_active = True
start_time = 0  
score = [0]
amount_bullet = 3
kill_point = 0
count = '' 
def bullet_movement(bullet_list):
    if bullet_list:
        for bullet_rectangle in bullet_list:

            bullet_rectangle.x += 10
            screen.blit(bullet_surface,bullet_rectangle)
        bullet_list = [bullet_rectangle for bullet_rectangle in bullet_list if bullet_rectangle.x < 700]
        return bullet_list
    else: return[]
def ammo_movement(ammo_list):
    if ammo_list:
        for ammo_rect in ammo_list:
            ammo_rect.x += -5
            screen.blit(ammo_surface,ammo_rect)
        ammo_list = [ammo_rect for ammo_rect in ammo_list if ammo_rect.x > -20]
        return ammo_list
    else:
        return []

def tire_movement(tire_list):
    global tire_gravity
    if tire_list:
        for tire_rectangle in tire_list:
            tire_rectangle.x += 5
            tire_gravity += 2
            tire_rectangle.y += tire_gravity
            if tire_rectangle.y > 225:
                tire_rectangle.y = 225
                tire_gravity = -10
            screen.blit(tire_surface,tire_rectangle)
        tire_list = [tire_rectangle for tire_rectangle in tire_list if tire_rectangle.x < 700]
        return tire_list
    else:
        return []



a = 0



def display_score():
    high_score = max(score)
    high_score_surface = font.render(f'high score: {high_score}',False,'Red')
    amount_bullet_surface = font.render(f'{amount_bullet}',False,'Red')
    kill_point_surface = font.render(f'kill point: {kill_point}',False,'Red')
    current_time_1 = (pygame.time.get_ticks()) // 1000
    current_time = current_time_1 - start_time
    time_surface = font.render(f'{current_time}',False,'Red')
    screen.blit(time_surface,(275,25))
    screen.blit(high_score_surface ,(0,0))
    screen.blit(amount_bullet_surface,player_rectangle.bottomleft)
    screen.blit(kill_point_surface,(0,20))
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        if 15 > display_score()  >= 0:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x += -5

                if obstacle_rect.bottom == 150:
                    screen.blit(flying_zombie_surface,obstacle_rect)
                else:
                    screen.blit(zombie_surface,obstacle_rect)
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -20]
            return obstacle_list
        if 30 > display_score()  >= 15:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x += -6

                if obstacle_rect.bottom == 150:
                    screen.blit(flying_zombie_surface,obstacle_rect)
                else:
                    screen.blit(zombie_surface,obstacle_rect)
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -20]
            return obstacle_list
        if display_score() >= 30:
            for obstacle_rect in obstacle_list:
                obstacle_rect.x += -7

                if obstacle_rect.bottom == 150:
                    screen.blit(flying_zombie_surface,obstacle_rect)
                else:
                    screen.blit(zombie_surface,obstacle_rect)
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -20]
            return obstacle_list
    else:
        return []
def collision(player_rectangle,obstacle_list,bullet_rectangle_list,tire_list):
    global kill_point
    if obstacle_list:
        for obstacle_rectangle in obstacle_list:
            if bullet_rectangle_list:
                for bullet_rectangle in bullet_rectangle_list:
                    if bullet_rectangle.colliderect(obstacle_rectangle):
                        kill_point += 2
                        bullet_rectangle_list.remove(bullet_rectangle)
                        obstacle_list.remove(obstacle_rectangle)
            for tire_rectangle in tire_list:
                if tire_rectangle.colliderect(obstacle_rectangle):
                    obstacle_list.remove(obstacle_rectangle)
                if tire_rectangle.colliderect(player_rectangle):
                    return False
            
            
            if player_rectangle.colliderect(obstacle_rectangle):
                return False
    return True
def ammo_reload(player_rectangle,ammo_list):
    global amount_bullet

    if ammo_list:
        for ammo_rectangle in ammo_list:
            if ammo_rectangle.colliderect(player_rectangle):
                amount_bullet += 3
                ammo_list.remove(ammo_rectangle)
#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1000)
ammo_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ammo_timer,10000)
tire_alarm_1 = pygame.USEREVENT + 3
tire_alarm_2 = pygame.USEREVENT + 4
tire_alarm_3 = pygame.USEREVENT + 5
tire_timer = pygame.USEREVENT + 6
random_1 = randint(8000,12000)
pygame.time.set_timer(tire_alarm_1,random_1 + 2000)
pygame.time.set_timer(tire_alarm_2,random_1+ 1000)
pygame.time.set_timer(tire_alarm_3,random_1)
pygame.time.set_timer(tire_timer,random_1+3000)

# ammo_timer = pygame.USEREVENT + 2
# pygame.time.set_timer(ammo_timer,3000)
while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rectangle.collidepoint(event.pos):
        #         print('collision')
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_active == True and amount_bullet > 0:
                bullet_rectangle_list.append(bullet_surface.get_rect(midbottom = player_rectangle.midbottom))
                amount_bullet -= 1
            elif event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                player_rectangle.midbottom = (142,250)
                # zombie_rectangle.x = 700
                start_time = (pygame.time.get_ticks()) // 1000
                random_1 = randint(8000,12000)
                pygame.time.set_timer(tire_alarm_1,random_1 + 2000)
                pygame.time.set_timer(tire_alarm_2,random_1+ 1000)
                pygame.time.set_timer(tire_alarm_3,random_1)
                pygame.time.set_timer(tire_timer,random_1+3000)
        if event.type == tire_alarm_1 and game_active:
            count = 1
        if event.type == tire_alarm_2 and game_active:
            count  = 2
        if event.type == tire_alarm_3 and game_active:
            count = 3
        if event.type == tire_timer and game_active:
            tire_rectangle = tire_surface.get_rect(midbottom = (0,250))
            tire_rectangle.width  -= 20
            tire_rectangle.height -= 20
            tire_list.append(tire_rectangle )     
            count = ''
            pygame.time.set_timer(tire_alarm_1, 0)
            pygame.time.set_timer(tire_alarm_2, 0)
            pygame.time.set_timer(tire_alarm_3, 0)
            pygame.time.set_timer(tire_timer, 0)
            random_1 = randint(8000,12000)
            pygame.time.set_timer(tire_alarm_1,random_1 + 2000)
            pygame.time.set_timer(tire_alarm_2,random_1+ 1000)
            pygame.time.set_timer(tire_alarm_3,random_1)
            pygame.time.set_timer(tire_timer,random_1+3000)




        if event.type == obstacle_timer and game_active:
            if display_score() < 15:
                if randint(0,2):
                    obstacle_rect_list.append(zombie_surface.get_rect(midbottom = (randint(700,1000), 250)))
                else:
                    obstacle_rect_list.append(flying_zombie_surface.get_rect(midbottom = (randint(700,1000), 150)))
            if 15 <= display_score():
                random = randint(0,5)
                if random == 0 or random == 1 or random == 2:
                    obstacle_rect_list.append(zombie_surface.get_rect(midbottom = (randint(700,1000), 250)))
                if random == 3:
                    obstacle_rect_list.append(flying_zombie_surface.get_rect(midbottom = (randint(700,1000), 150)))
                if random == 4:
                    two_obstacle_pos = randint(700,1000)
                    obstacle_rect_list.append(zombie_surface.get_rect(midbottom = (two_obstacle_pos, 250)))
                    obstacle_rect_list.append(flying_zombie_surface.get_rect(midbottom = (two_obstacle_pos, 150)))
        if event.type == ammo_timer and game_active:
            ammo_list.append(ammo_surface.get_rect(midbottom = (randint(700,900),250)))
        # if event.type == pygame.KEYUP:
        #     print("KEY UP")
        # if event.type == ammo_timer and game_active:
        #     ammo_list.append(ammo_surface.get_rect(midbottom = (randint(700,1000),250)))
    if game_active:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_rectangle.bottom == 250:
            player_gravity = -13
        if keys[pygame.K_LEFT]:
            player_rectangle.x -= 3

    # Di chuyển sang phải
        if keys[pygame.K_RIGHT]:
            player_rectangle.x += 3
        if player_rectangle.x < 0:
            player_rectangle.x=0
        if player_rectangle.x>550:
            player_rectangle.x=550
        screen.blit(ground_surface,(0,0))
        # pygame.draw.rect(screen, (255,0,0), zombie_rectangle, width=0)
 
        
        # zombie_rectangle.x += -5 

        # if zombie_rectangle.x < -200:
        #     zombie_rectangle.x = 700

        # pygame.draw.rect(screen, (255,0,0), player_rectangle, width=0)
        screen.blit(player_surface, player_rectangle)
        
        player_gravity += 0.7
        player_rectangle.y += player_gravity

        if player_rectangle.bottom >= 250: 
            player_rectangle.bottom = 250
        bullet_rectangle_list = bullet_movement(bullet_rectangle_list)
        obstacle_rect_list =  obstacle_movement(obstacle_rect_list)
        ammo_list = ammo_movement(ammo_list)
        # for i in obstacle_rect_list:
        #     if i.x < -14:
        #         print('a')
        #     if i.x < -21:
        #         print('b')
        game_active = collision(player_rectangle,obstacle_rect_list,bullet_rectangle_list,tire_list )
        ammo_reload(player_rectangle,ammo_list)
        display_score()

        tire_list = tire_movement(tire_list)

        # if zombie_rectangle.colliderect(player_rectangle):
        count_surface = font.render(f'{count}',False,'Red')
        screen.blit(count_surface,(10,100))
        if game_active == False:

            score.append(display_score() + kill_point)


        
                    # mouse_position = pygame.mouse.get_pos()
        # if player_rectangle.collidepoint(mouse_position):
        #     print(pygame.mouse.get_pressed())
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_SPACE]:
            #     print('jump')
    else:
        screen.blit(text_surface,(225,50))
        obstacle_rect_list.clear()
        bullet_rectangle_list.clear()
        ammo_list.clear()
        amount_bullet = 3 
        kill_point = 0
        count = ''
        tire_list.clear()
        tire_gravity =-10
        pygame.time.set_timer(tire_alarm_1, 0)
        pygame.time.set_timer(tire_alarm_2, 0)
        pygame.time.set_timer(tire_alarm_3, 0)
        pygame.time.set_timer(tire_timer, 0)
    pygame.display.update()
    clock.tick(60)