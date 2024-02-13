import pygame, sys, os, random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "images", "cat_player.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT)
        self.speed = 7

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed

    def update(self):
        self.move_player()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, location):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "images", "sphere_blue.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.speed = 7

    def move_bullet(self):
        self.rect.y -= self.speed

    def destroy_bullet(self):
        if self.rect.top < 0:
            self.kill()
    
    def update(self):
        self.move_bullet()
        self.destroy_bullet()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        if enemy_type == 1:
            self.image = pygame.image.load(os.path.join("assets", "images", "JellyBabes_01", "JellyBabes_01_48x64_01.png")).convert_alpha()
        elif enemy_type == 2:
            self.image = pygame.image.load(os.path.join("assets", "images", "JellyBabes_01", "JellyBabes_01_48x64_02.png")).convert_alpha()
        elif enemy_type == 3:
            self.image = pygame.image.load(os.path.join("assets", "images", "JellyBabes_01", "JellyBabes_01_48x64_03.png")).convert_alpha()
        elif enemy_type == 4:
            self.image = pygame.image.load(os.path.join("assets", "images", "JellyBabes_01", "JellyBabes_01_48x64_04.png")).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join("assets", "images", "JellyBabes_01", "JellyBabes_01_48x64_05.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = 0 - self.rect.height
        lane = random.randint(1,WIDTH - self.rect.width)
        self.rect.x = lane
        self.speed = 5

    def move_enemy(self):
        self.rect.y += self.speed

    def destroy_enemy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.move_enemy()
        self.destroy_enemy()

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
PLAYER_SPEED = 5
BACKGROUND_SCROLL_SPEED = 2
FPS = 60
BULLET_SPEED = 7

# Create a Pygame window and set its dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the window title
pygame.display.set_caption("Space Attack")

# Clock
clock = pygame.time.Clock()

# Background
background = pygame.image.load(os.path.join("assets", "images", "space_bg.png")).convert()
background_rect_one = background.get_rect()
background_rect_one.y = 0
background_rect_two = background.get_rect()
background_rect_two.y = -600

# Player
player_sprite = pygame.sprite.GroupSingle()
player_sprite.add(Player())

# Enemies
enemy_sprites = pygame.sprite.Group()
spawn_enemy = 3000
last_enemy_spawned = 0

# Bullets
bullet_sprites = pygame.sprite.Group()
bullet_cooldown = 800
last_bullet_fired = 0

# Score
score = 0
spaceship = pygame.image.load(os.path.join("assets", "images", "JellyBabes_01", "JellyBabes_01_48x64_06.png")).convert_alpha()
spaceship_rect = spaceship.get_rect()
spaceship_rect.topleft = (25, 25)
score_font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 32)
high_score = 0

# Lives
heart_frame_one = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-1.png")).convert_alpha()
heart_frame_two = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-2.png")).convert_alpha()
heart_frame_three = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-3.png")).convert_alpha()
heart_frame_four = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-4.png")).convert_alpha()
heart_frame_five = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-5.png")).convert_alpha()
heart_frame_six = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-6.png")).convert_alpha()
heart_frame_seven = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-7.png")).convert_alpha()
heart_frame_eight = pygame.image.load(os.path.join("assets", "images", "hearts", "frame-8.png")).convert_alpha()
heart_frame_list = [heart_frame_one, heart_frame_two, heart_frame_three, heart_frame_four, heart_frame_five, heart_frame_six, heart_frame_seven, heart_frame_eight]
heart_rect = heart_frame_one.get_rect()
heart_rect.bottomleft = (25, 575)
current_frame = 0
frame_delay = 200
last_frame_time = 0
lives = 3

# Title screen
title_font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 72)
instructions_font = pygame.font.Font(os.path.join("assets", "fonts", "LuckiestGuy-Regular.ttf"), 32)
title_text = title_font.render("JELLY ALIEN ATTACK!", True, "white")
high_score_text = instructions_font.render(f"Current High Score is {high_score}!", True, "white")
instructions_text = instructions_font.render("Press ENTER to begin", True, "white")
title_rect = title_text.get_rect()
instructions_rect = instructions_text.get_rect()
high_score_rect = high_score_text.get_rect()
high_score_rect.center = (WIDTH // 2, 550)
title_rect.center = (WIDTH // 2, 120)
instructions_rect.center = (WIDTH // 2, 480)
title_image = pygame.image.load(os.path.join("assets", "images", "cat_player.png")).convert_alpha()
title_image_rect = title_image.get_rect()
title_image_rect.center = (WIDTH // 2, HEIGHT // 2)

# Sounds
pygame.mixer.music.load(os.path.join("assets", "sounds", "music.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
boom = pygame.mixer.Sound(os.path.join("assets", "sounds", "squeak.mp3"))
boom.set_volume(0.2)
shoot = pygame.mixer.Sound(os.path.join("assets", "sounds", "classic-piouh-2-135674.mp3"))
shoot.set_volume(0.2)

# Main game loop
running = True
game_over = True

while running:
    
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game over
    if not game_over: 
        # Game logic
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        # Background scroll
        screen.blit(background, background_rect_one)
        screen.blit(background, background_rect_two)
        if background_rect_one.y > 600:
            background_rect_one.y = -600
        if background_rect_two.y > 600:
            background_rect_two.y = -600

        # # Generate bullets
        if keys[pygame.K_SPACE] and current_time - last_bullet_fired >= bullet_cooldown:
            bullet_sprites.add(Bullet(player_sprite.sprite.rect.center))
            last_bullet_fired = current_time
            shoot.play()

        # Spawn enemies
        if current_time - last_enemy_spawned >= spawn_enemy:
            enemy_sprites.add(Enemy(random.randint(1,5)))
            last_enemy_spawned = current_time

        # # Detect collisions
        if pygame.sprite.spritecollide(player_sprite.sprite, enemy_sprites, True):
            lives -= 1
            boom.play()
        if pygame.sprite.groupcollide(bullet_sprites, enemy_sprites, True, True):
            score += 1
            boom.play()
            if score > high_score:
                high_score += score

        # Update score
        score_text = score_font.render(f"{score}", True, "white")
        if score > 5:
            spawn_enemy = 2500
        if score > 10:
            spawn_enemy = 2000
        if score > 15:
            spawn_enemy = 1500
        if score > 20:
            spawn_enemy = 1000        

        # Update lives
        lives_text = score_font.render(f"{lives}", True, "white")
        if lives < 1:
            game_over = True

        # Update hearts
        if current_time - last_frame_time >= frame_delay:
            current_frame = (current_frame + 1) % len(heart_frame_list)
            last_frame_time = current_time

        # Update high score
            
        high_score_text = instructions_font.render(f"Current High Score is {high_score}!", True, "white")

        # Draw surfaces 
        
        background_rect_one.y += BACKGROUND_SCROLL_SPEED
        background_rect_two.y += BACKGROUND_SCROLL_SPEED

        bullet_sprites.draw(screen)
        bullet_sprites.update()

        player_sprite.draw(screen)
        player_sprite.update()

        enemy_sprites.draw(screen)
        enemy_sprites.update()

        screen.blit(spaceship, spaceship_rect)
        screen.blit(score_text, (80, 25))
        screen.blit(heart_frame_list[current_frame], heart_rect)
        screen.blit(lives_text, (80, 540))


    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game_over = False
            lives = 3
            score = 0
        screen.fill("darkslateblue")
        screen.blit(title_text, title_rect)
        screen.blit(instructions_text, instructions_rect)
        screen.blit(high_score_text, high_score_rect)
        screen.blit(title_image, title_image_rect)

    
    # Update dispay
    pygame.display.update()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()

