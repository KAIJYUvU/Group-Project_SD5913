import pygame
import sys
import random

# Init
pygame.init()
pacman_image = pygame.image.load('pacman.png')
speed_up_image = pygame.image.load('speed_up.png')
freeze_image = pygame.image.load('freeze.png')
power_image = pygame.image.load('power.png')
monster_images = [
    pygame.image.load('monster1.png'),
    pygame.image.load('monster2.png'),
    pygame.image.load('monster3.png'),
    pygame.image.load('monster4.png')
]
background_image = pygame.image.load('background1.png')
background_image2 = pygame.image.load('background2.png')

monster_freeze_image = pygame.image.load('monster_freeze.png')
monster_freeze_image = pygame.transform.scale(monster_freeze_image, (40, 40))

monster_images = [pygame.transform.scale(img, (40, 40)) for img in monster_images]
pacman_image = pygame.transform.scale(pacman_image, (40, 40))
speed_up_image = pygame.transform.scale(speed_up_image, (30, 30))
freeze_image = pygame.transform.scale(freeze_image, (30, 30))
power_image = pygame.transform.scale(power_image, (30, 30))
background_image = pygame.transform.scale(background_image, (600, 600))
background_image2 = pygame.transform.scale(background_image2, (600, 600))


WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PACCAT")

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)


font = pygame.font.SysFont(None, 36)

walls = []
wall_width = 20


walls.append(pygame.Rect(0, 0, WIDTH, wall_width))  # 上
walls.append(pygame.Rect(0, 0, wall_width, HEIGHT))  # 左
walls.append(pygame.Rect(0, HEIGHT - wall_width, WIDTH, wall_width))  # 下
walls.append(pygame.Rect(WIDTH - wall_width, 0, wall_width, HEIGHT))  # 右

walls.append(pygame.Rect(0, 450, 520,  wall_width))
walls.append(pygame.Rect(80, 60, wall_width, 250))
walls.append(pygame.Rect(80, 60, 440, wall_width))
walls.append(pygame.Rect(500, 150, wall_width, 300))
walls.append(pygame.Rect(430, 60, wall_width, 140))
walls.append(pygame.Rect(80, 310, 110, wall_width))
walls.append(pygame.Rect(160, 150, 210, wall_width))
walls.append(pygame.Rect(160, 150, 220, wall_width))
walls.append(pygame.Rect(360, 150, wall_width, 210))
walls.append(pygame.Rect(260, 340, 100, wall_width))
walls.append(pygame.Rect(260, 260, wall_width, 100))


dot_size = 6
special_dot_size = 12
beans = []

NORMAL_BEAN = 'normal'
SPEED_UP_BEAN = 'speed_up'
FREEZE_BEAN = 'freeze'
POWER_BEAN = 'power'


monster_size = 20
monsters = []
monster_speed = 2
normal_monster_speed = monster_speed
freeze_duration = 0  # 冻结效果持续时间
monster_respawn_timers = []


game_started = False
game_over = False
win = False


score = 0


pacman_size = 20
normal_pacman_speed = 5
pacman_speed = normal_pacman_speed
speed_up_duration = 0
power_up_duration = 0
powered_up = False


pacman_x = WIDTH // 2
pacman_y = HEIGHT // 2

def reset_game():
    global pacman_x, pacman_y, pacman_size, pacman_speed, speed_up_duration, power_up_duration, powered_up
    global freeze_duration, score, monster_respawn_timers, beans, monsters, game_over, win, game_started
    global monster_speed


    pacman_x = WIDTH // 2
    pacman_y = HEIGHT // 2
    pacman_size = 20
    pacman_speed = normal_pacman_speed
    speed_up_duration = 0
    power_up_duration = 0
    powered_up = False


    monster_speed = normal_monster_speed
    freeze_duration = 0


    score = 0
    monster_respawn_timers.clear()
    game_over = False
    win = False
    game_started = True  # 游戏重新开始


    beans.clear()
    generate_beans()


    monsters.clear()
    create_monsters()


def generate_beans():
    while len(beans) < 50:
        x = random.randint(0, WIDTH - dot_size)
        y = random.randint(0, HEIGHT - dot_size)
        bean_rect = pygame.Rect(x, y, dot_size, dot_size)

        collision = False
        for wall in walls:
            if wall.colliderect(bean_rect):
                collision = True
                break
        if not collision:

            rand = random.random()
            if rand < 0.05:
                bean_type = SPEED_UP_BEAN
                size = special_dot_size
            elif rand < 0.10:
                bean_type = FREEZE_BEAN
                size = special_dot_size
            elif rand < 0.15:
                bean_type = POWER_BEAN
                size = special_dot_size
            else:
                bean_type = NORMAL_BEAN
                size = dot_size
            bean_rect = pygame.Rect(x, y, size, size)
            beans.append({'rect': bean_rect, 'type': bean_type})


def create_monsters():
    for _ in range(3):
        while True:
            x = random.randint(0, WIDTH - monster_size)
            y = random.randint(0, HEIGHT - monster_size)
            monster_rect = pygame.Rect(x, y, monster_size, monster_size)
            collision = False
            for wall in walls:
                if wall.colliderect(monster_rect):
                    collision = True
                    break
            if not collision:

                monster_image = random.choice(monster_images)
                monsters.append({'rect': monster_rect, 'image': monster_image})
                break


reset_game()


clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
            elif not game_started:
                if event.key == pygame.K_SPACE:
                    game_started = True

    if not game_started:

        screen.fill(BLACK)
        title_text = font.render("Press'Space'to start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        continue

    if game_over:

        screen.blit(background_image2, (0, 0))
        if win:
            victory_text = font.render("YOU WIN!", True, YELLOW)
            screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2,
                                       HEIGHT // 2 - victory_text.get_height()))
        else:
            game_over_text = font.render("GAMEOVER", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                         HEIGHT // 2 - game_over_text.get_height()))
        final_score_text = font.render(f"FINAL SCORE: {score}", True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 40))

        instruction_text = font.render("PRESS 'R' TO RESTART", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 80))
        pygame.display.flip()
        continue


    if speed_up_duration > 0:
        speed_up_duration -= 1
        if speed_up_duration == 0:
            pacman_speed = normal_pacman_speed
    if freeze_duration > 0:
        freeze_duration -= 1
        if freeze_duration == 0:
            monster_speed = normal_monster_speed
    if power_up_duration > 0:
        power_up_duration -= 1
        if power_up_duration == 0:
            powered_up = False
            pacman_size = 20

            for monster in monsters:
                monster['image'] = random.choice(monster_images)


    for timer in monster_respawn_timers[:]:
        timer['timer'] -= 1
        if timer['timer'] <= 0:

            while True:
                x = random.randint(0, WIDTH - monster_size)
                y = random.randint(0, HEIGHT - monster_size)
                monster_rect = pygame.Rect(x, y, monster_size, monster_size)
                collision = False
                for wall in walls:
                    if wall.colliderect(monster_rect):
                        collision = True
                        break
                if not collision:

                    monster_image = random.choice(monster_images)
                    monsters.append({'rect': monster_rect, 'image': monster_image})
                    break
            monster_respawn_timers.remove(timer)


    keys = pygame.key.get_pressed()
    new_pacman_x = pacman_x
    new_pacman_y = pacman_y
    if keys[pygame.K_LEFT]:
        new_pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        new_pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        new_pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        new_pacman_y += pacman_speed


    pacman_rect = pygame.Rect(new_pacman_x, new_pacman_y, pacman_size, pacman_size)


    collision = False
    for wall in walls:
        if wall.colliderect(pacman_rect):
            collision = True
            break
    if not collision:
        pacman_x = new_pacman_x
        pacman_y = new_pacman_y
    else:
        pacman_rect = pygame.Rect(pacman_x, pacman_y, pacman_size, pacman_size)


    for bean in beans[:]:
        if pacman_rect.colliderect(bean['rect']):
            beans.remove(bean)
            if bean['type'] == NORMAL_BEAN:
                score += 10
            elif bean['type'] == SPEED_UP_BEAN:
                score += 20
                pacman_speed = normal_pacman_speed * 2
                speed_up_duration = 300
            elif bean['type'] == FREEZE_BEAN:
                score += 20
                monster_speed = 0
                freeze_duration = 300
            elif bean['type'] == POWER_BEAN:
                score += 30
                powered_up = True
                pacman_size = 40
                power_up_duration = 300
                for monster in monsters:
                    monster['image'] = monster_freeze_image


    pacman_rect = pygame.Rect(pacman_x, pacman_y, pacman_size, pacman_size)


    for monster in monsters[:]:
        monster_rect = monster['rect']
        if freeze_duration > 0:
            if pacman_rect.colliderect(monster_rect):
                if powered_up:
                    monsters.remove(monster)
                    monster_respawn_timers.append({'timer': 300})
                else:
                    game_over = True
                    break
            continue

        if powered_up:
            dx = monster_rect.centerx - pacman_rect.centerx
            dy = monster_rect.centery - pacman_rect.centery
        else:
            dx = pacman_rect.centerx - monster_rect.centerx
            dy = pacman_rect.centery - monster_rect.centery

        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx /= distance
            dy /= distance
        new_monster_x = monster_rect.x + dx * monster_speed
        new_monster_y = monster_rect.y + dy * monster_speed
        new_monster_rect = pygame.Rect(new_monster_x, new_monster_y, monster_size, monster_size)
        collision = False
        for wall in walls:
            if wall.colliderect(new_monster_rect):
                collision = True
                break
        if not collision:
            monster['rect'].x = new_monster_x
            monster['rect'].y = new_monster_y

        if monster_rect.colliderect(pacman_rect):
            if powered_up:
                monsters.remove(monster)
                monster_respawn_timers.append({'timer': 300})
            else:
                game_over = True
                break

    screen.blit(background_image, (0, 0))

    WALL_COLOR = (44, 71, 24)
    for wall in walls:
        pygame.draw.rect(screen, WALL_COLOR, wall)


    for bean in beans:
        if bean['type'] == NORMAL_BEAN:
            pygame.draw.rect(screen, WHITE, bean['rect'])
        elif bean['type'] == SPEED_UP_BEAN:
            screen.blit(speed_up_image, bean['rect'].topleft)
        elif bean['type'] == FREEZE_BEAN:
            screen.blit(freeze_image, bean['rect'].topleft)
        elif bean['type'] == POWER_BEAN:
            screen.blit(power_image, bean['rect'].topleft)

    screen.blit(pacman_image, pacman_rect.topleft)

    for monster in monsters:
        screen.blit(monster['image'], monster['rect'].topleft)

    score_text = font.render(f"SCORE: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    y_offset = 50
    if speed_up_duration > 0:
        speed_text = font.render(f"Speed up remaining time: {speed_up_duration // 60}", True, GREEN)
        screen.blit(speed_text, (10, y_offset))
        y_offset += 40
    if freeze_duration > 0:
        freeze_text = font.render(f"Frozen remaining time: {freeze_duration // 60}", True, PURPLE)
        screen.blit(freeze_text, (10, y_offset))
        y_offset += 40
    if power_up_duration > 0:
        power_text = font.render(f"Killer remaining time: {power_up_duration // 60}", True, ORANGE)
        screen.blit(power_text, (10, y_offset))
        y_offset += 40

    if len(beans) == 0:
        game_over = True
        win = True

    pygame.display.flip()

pygame.quit()
sys.exit()
