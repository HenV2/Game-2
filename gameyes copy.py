import pygame
import random
import math 

pygame.init()


screen_info = pygame.display.Info()

screen_width = screen_info.current_w
screen_height = screen_info.current_h

# WIDTH, HEIGHT = screen_width*0.8, screen_height *0.8
WIDTH, HEIGHT = 1000, 800
SPACESHIP_SPEED = 5
ASTEROID_SIZE = 25
COLLECTIBLE_SIZE = 10
BACKGROUND_COLOR = (50, 100, 100)
health_SIZE_w = 100
health_SIZE_h = 30
        
BASE_PATH = '/Users/henry/Desktop/Game 2/Assets/'

# Initial Setup for the background
screen_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Void Voyager")
# background_image = pygame.image.load(BASE_PATH+"background_img.png") 
# background_image = pygame.transform.scale(background_image, screen_size)  




# main_player_img = None
player_scale = (40, 30)

player_img = pygame.image.load("Assets/spaceship.png")
player_img = pygame.transform.scale(player_img, player_scale)

player_img_plain = pygame.image.load("Assets/spaceship.png")
player_img_plain = pygame.transform.scale(player_img, player_scale)

player_img_thurst1 = pygame.image.load("Assets/spaceship1.png")
player_img_thurst1 = pygame.transform.scale(player_img_thurst1, player_scale)

player_img_thurst2 = pygame.image.load("Assets/spaceship2.png")
player_img_thurst2 = pygame.transform.scale(player_img_thurst2, player_scale)

player_img_left = pygame.image.load("Assets/spaceshipleft.png")
player_img_left = pygame.transform.scale(player_img_left, player_scale)

player_img_right = pygame.image.load("Assets/spaceshipright.png")
player_img_right = pygame.transform.scale(player_img_right, player_scale)

asteroid_img = pygame.image.load("Assets/asteroid.png")
asteroid_img = pygame.transform.scale(asteroid_img, (ASTEROID_SIZE, ASTEROID_SIZE))
hole_img = pygame.image.load("Assets/hole.png")
hole_img = pygame.transform.scale(hole_img, (80, 80))
collectible_img = pygame.image.load("Assets/collectible.png")
collectible_img = pygame.transform.scale(collectible_img, (COLLECTIBLE_SIZE, COLLECTIBLE_SIZE))
repair_img = pygame.image.load("Assets/repair.png")
repair_img = pygame.transform.scale(repair_img, (COLLECTIBLE_SIZE, COLLECTIBLE_SIZE))

# health_img = pygame.image.load("Assets/health.png")
# health_img = pygame.transform.scale(health_img, (health_SIZE, health_SIZE))

health0_img = pygame.image.load("Assets/health0.png")
health0_img = pygame.transform.scale(health0_img, (health_SIZE_w, health_SIZE_h))
health1_img = pygame.image.load("Assets/health1.png")
health1_img = pygame.transform.scale(health1_img, (health_SIZE_w, health_SIZE_h))
health2_img = pygame.image.load("Assets/health2.png")
health2_img = pygame.transform.scale(health2_img, (health_SIZE_w, health_SIZE_h))
health3_img = pygame.image.load("Assets/health3.png")
health3_img = pygame.transform.scale(health3_img, (health_SIZE_w, health_SIZE_h))

player_x, player_y = WIDTH // 2, HEIGHT // 2 - 50  # Initial y position is slightly above the center  # Initial angle

spaceship_angle = 0
spaceship_speed_x = 0
spaceship_speed_y = 0
is_thrusting = False

ANGLE_SPEED = 6
THRUST = 0.3
DECEL = 0.98

asteroids = []

n_astroids = 5

initial_distance = 500

black_hole_radius = 300


def create_astroids():
        global asteroids
            # Check if there are fewer asteroids than a certain number and add new asteroids off-screen
        while len(asteroids) < n_astroids:
            # Generate random initial parameters for the asteroids and add them to the asteroids list
            asteroid_distance = random.randint(initial_distance, initial_distance)  # Initial distance from the black hole
            asteroid_angle = random.uniform(0, 2 * math.pi)  # Initial angle
            # asteroid_angle = random.random()*2*math.pi 
            # print(asteroid_angle)
            asteroid_x = WIDTH // 2 - asteroid_distance * math.cos(asteroid_angle)
            # asteroid_x = WIDTH // 2 - asteroid_distance * math.cos(asteroid_angle)
            asteroid_y = HEIGHT // 2 - asteroid_distance * math.sin(asteroid_angle)

            # random_factor = random.uniform(0.8, 1.2)
            # asteroid_x = WIDTH // 2 - asteroid_distance * random_factor * math.cos(asteroid_angle)
            # random_factor = random.uniform(0.8, 1.2)
            # asteroid_y = HEIGHT // 2 - asteroid_distance * math.sin(asteroid_angle)
            asteroids.append([asteroid_x, asteroid_y, asteroid_angle, asteroid_distance])



clock = pygame.time.Clock()

asteroids = []
collectibles = []
repairs = []

game_over = False
player_lives = 3
score = 0

invincible = False
invincibility_timer = 0

running = True

while running:
    player_img=player_img_plain
    # set background
    # screen.blit(background_image, (0, 0))

    if player_lives==3:
        screen.blit(health3_img, (WIDTH-health_SIZE_w-20, 20))
    elif player_lives==2:
        screen.blit(health2_img, (WIDTH-health_SIZE_w-20, 20))
    elif player_lives==1:
        screen.blit(health1_img, (WIDTH-health_SIZE_w-20, 20))
    else:
        screen.blit(health0_img, (WIDTH-health_SIZE_w-20, 20))




    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()

        # Handle spaceship movement
        if keys[pygame.K_LEFT]:
            spaceship_angle += ANGLE_SPEED
            player_img=player_img_left
        if keys[pygame.K_RIGHT]:
            spaceship_angle -= ANGLE_SPEED
            player_img=player_img_right
        if keys[pygame.K_SPACE]:
            is_thrusting = True
            player_img = player_img_thurst1
        else:
            is_thrusting = False

        
        
        # Calculate new player position
        if is_thrusting:
            spaceship_speed_x += THRUST * math.cos(math.radians(spaceship_angle))
            spaceship_speed_y -= THRUST * math.sin(math.radians(spaceship_angle))

        spaceship_speed = math.sqrt(spaceship_speed_x**2 + spaceship_speed_y**2)
        if spaceship_speed >4:
             player_img=player_img_thurst2
        # print(spaceship_speed_x)
        # print(spaceship_speed_y)
        spaceship_speed_x *= DECEL
        spaceship_speed_y *= DECEL

        player_x += spaceship_speed_x
        player_y += spaceship_speed_y

        player_x = max(0, min(WIDTH, player_x))
        player_y = max(0, min(HEIGHT, player_y))

        if invincibility_timer > 0:
            invincibility_timer -= 1

        if invincibility_timer <= 0:
            invincible = False

        for collectible in collectibles:
            collectible_x, collectible_y, _, _ = collectible
            player_rect = player_img.get_rect(center=(int(player_x), int(player_y)))
            collectible_rect = collectible_img.get_rect(center=(int(collectible_x), int(collectible_y)))
            if player_rect.colliderect(collectible_rect):
                score += 10
                collectibles.remove(collectible)

        for repair in repairs:
            repair_x, repair_y, _, _ = repair
            player_rect = player_img.get_rect(center=(int(player_x), int(player_y)))
            repair_rect = repair_img.get_rect(center=(int(repair_x), int(repair_y)))
            if player_rect.colliderect(repair_rect):
                player_lives = 3
                repairs.remove(repair)

        if not invincible:
            for asteroid in asteroids:
                asteroid_x, asteroid_y, _, _ = asteroid
                player_rect = player_img.get_rect(center=(int(player_x), int(player_y)))
                asteroid_rect = asteroid_img.get_rect(center=(int(asteroid_x), int(asteroid_y)))
                if player_rect.colliderect(asteroid_rect):
                    player_lives -= 1
                    if player_lives <= 0:
                        game_over = True
                    else:
                        invincible = True
                        invincibility_timer = 60 

    for asteroid in asteroids:
        asteroid_x, asteroid_y, _, _ = asteroid
        screen.blit(asteroid_img, (int(asteroid_x), int(asteroid_y)))

    for collectible in collectibles:
        collectible_x, collectible_y, _, _ = collectible
        screen.blit(collectible_img, (int(collectible_x), int(collectible_y)))

    for repair in repairs:
        repair_x, repair_y, _, _ = repair
        screen.blit(repair_img, (int(repair_x), int(repair_y)))
    

    # Draw the spaceship
    if not invincible or (invincible and invincibility_timer % 10 < 5):
        rotated_spaceship = pygame.transform.rotate(player_img, spaceship_angle)
        rect = rotated_spaceship.get_rect()
        rect.center = (player_x, player_y)
        screen.blit(rotated_spaceship, rect)
    # for i in range(player_lives):
    #     screen.blit(health_img, (WIDTH - (i + 1) * health_SIZE, 0))

    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if game_over:
        # Game over menu
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)
        text = font.render("Press R to Restart", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(text, text_rect)
        text = font.render("Press Q to Quit", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_lives = 3
            game_over = False
            asteroids.clear()
            collectibles.clear()
            repairs.clear()
            player_x, player_y = WIDTH // 2, HEIGHT // 2 - 50
            score = 0
        elif keys[pygame.K_q]:
            running = False

    # Update the display
    pygame.display.update()

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Set the frame rate
    clock.tick(50)

# Quit Pygame
pygame.quit()

        