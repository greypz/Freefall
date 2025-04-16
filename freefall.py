import pygame
import math

import random
from pygame.font import Font as F

# Initialize Pygame
pygame.init()
pygame.mixer.init()

settings_inputs = {
    "duration": "5",
    "sfx_volume": "30",
    "bgm_volume": "20",
}
active_input = None  # Tracks which input box is currently active

# Load your icon image
icon = pygame.image.load('images/keddy.png')  # Replace with your icon's path
sound_effect = pygame.mixer.Sound("contents/phaserUp3.wav")
sound_effect.set_volume(float(settings_inputs["sfx_volume"]) / 100)

wining_sound_effect = pygame.mixer.Sound("contents/wining_sound.wav")
wining_sound_effect.set_volume(float(settings_inputs["sfx_volume"]) / 100)

pygame.mixer.music.load("contents/bond_bg_music.mp3")
pygame.mixer.music.set_volume(float(settings_inputs["bgm_volume"]) / 100)

# Set the window icon
pygame.display.set_icon(icon)

# Set the window title
pygame.display.set_caption('Free Fall')
clock = pygame.time.Clock()
FPS = 150

WIDTH = 560
HEIGHT = 700
BLACK = (0, 0, 0)
GOOD_BOI = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load the pixel font
font = F('contents/gamefont.ttf', 30)
font2 = F('contents/gamefont.ttf', 50)

# Create character
man_slow1 = pygame.image.load("images/mainSlow1.png").convert_alpha()
man_image = man_slow1
man_slow_rect = man_slow1.get_rect()
man_fast = pygame.image.load("images/mainFast.png").convert_alpha()
man_fast_rect = man_fast.get_rect()
man_rect = man_slow_rect
man_slow_rect.center = (265, 150)
scroll_speed = -2
# Load image
bg = pygame.image.load("images/cloudyBG.jpg").convert_alpha()
bg_height = bg.get_height()
supplydrop_image = pygame.image.load("images/supply drop.png").convert_alpha()
crate_image = pygame.image.load("images/crate.png").convert_alpha()

# Define game variables
scroll = 0
tiles = math.ceil(HEIGHT / bg_height) + 1
counter = True

# Define constants
MAX_PLATFORMS = 4


# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        if random.randint(0, 5) == 4:
            self.image = pygame.transform.scale(crate_image, (150, 160))
            self.shape = "crate"
        else:
            self.image = pygame.transform.scale(supplydrop_image, (width, 140))
            self.shape = "supplydrop"
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        # Update platform's vertical position
        self.rect.y += scroll

        # Check if platform has gone off the screen
        if self.rect.top < -140:
            self.kill()


# Create sprite groups
platform_group = pygame.sprite.Group()

# Create temporary platform
seconds = int(settings_inputs["duration"])
current_time = seconds
start_ticks = pygame.time.get_ticks()  # Start time for countdown


def reset_game():
    global scroll, scroll_speed, counter, start_ticks, platform_group, man_rect, man_slow_rect, man_fast_rect, run, close_game, seconds, current_time, wining_sound_effect, sound_effect
    sound_effect.set_volume(float(settings_inputs["sfx_volume"]) / 100)
    wining_sound_effect.set_volume(float(settings_inputs["sfx_volume"]) / 100)
    pygame.mixer.music.set_volume(float(settings_inputs["bgm_volume"]) / 100)
    pygame.mixer.music.play(-1)
    scroll = 0
    scroll_speed = -2
    counter = True
    start_ticks = pygame.time.get_ticks()
    platform_group.empty()
    man_rect = man_slow1.get_rect()
    man_slow_rect = man_slow1.get_rect()
    man_fast_rect = man_fast.get_rect()
    man_slow_rect.center = (265, 150)
    man_rect = man_slow_rect
    seconds = int(settings_inputs["duration"])
    current_time = seconds
    run = True
    close_game = True


def main_menu():
    screen.fill((30, 30, 30))  # dark background

    font = pygame.font.SysFont("Arial", 60)
    title = font.render("Main Menu", True, (255, 255, 255))

    play_text = font.render("Play", True, (0, 255, 0))
    settings_text = font.render("Settings", True, (0, 150, 255))

    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    settings_rect = settings_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))

    screen.blit(title, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(settings_text, settings_rect)

    # Detect click
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        if play_rect.collidepoint(mouse_pos):
            return "game"  # Switch to game state
        if settings_rect.collidepoint(mouse_pos):
            return "settings"  # Switch to settings state (you can define this)

    return "menu"  # Stay in menu


def settings_menu():
    global active_input

    screen.fill((40, 40, 40))
    font = pygame.font.SysFont("Arial", 20)
    small_font = pygame.font.SysFont("Arial", 30)

    # Back button
    back_text = small_font.render("<", True, (255, 255, 255))
    back_rect = back_text.get_rect(topleft=(20, 20))
    screen.blit(back_text, back_rect)

    # Settings labels and input boxes
    labels = [

        "Duration of the game:",
        "Sound effect volume (0-1):",
        "Background music volume (0-1):"
    ]
    keys = ["duration", "sfx_volume", "bgm_volume"]

    start_y = HEIGHT // 3
    for i, label in enumerate(labels):
        y = start_y + i * 60
        label_render = font.render(label, True, (255, 255, 255))
        screen.blit(label_render, (50, y))

        # Input box
        input_text = font.render(settings_inputs[keys[i]], True, (0, 255, 255))
        input_rect = pygame.Rect(WIDTH // 6 + 200, y, 200, 40)
        color = (255, 255, 255) if active_input == keys[i] else (180, 180, 180)
        pygame.draw.rect(screen, color, input_rect, 2)
        screen.blit(input_text, (input_rect.x + 10, input_rect.y + 5))

    # Event handling
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:
        if back_rect.collidepoint(mouse_pos):
            return "menu"
        for i, key in enumerate(keys):
            y = start_y + i * 60
            input_rect = pygame.Rect(WIDTH // 6 + 200, y, 200, 40)
            if input_rect.collidepoint(mouse_pos):
                active_input = key
                break
        else:
            active_input = None

    return "settings"


game_status = "menu"

# reset_game()

# Game loop
run = True
close_game = True
while close_game:

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not run:
                reset_game()
            if event.key == pygame.K_SPACE and current_time == 0:
                reset_game()
            if active_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        settings_inputs[active_input] = settings_inputs[active_input][:-1]
                    elif event.key == pygame.K_RETURN:
                        # Validate the input when the user confirms the entry.
                        if active_input == "height":
                            try:
                                value = int(settings_inputs["height"])
                                # Clamp height to allowed range [1, 5]
                                if value <= 1:
                                    value = 1
                                elif value > 5:
                                    value = 5
                                settings_inputs["height"] = str(value)
                            except ValueError:
                                # If conversion fails, do nothing (or reset to default if preferred)
                                settings_inputs[active_input] = "1"
                        elif active_input in ("sfx_volume", "bgm_volume"):
                            try:
                                value = int(settings_inputs[active_input])
                                # Clamp volume to allowed range [1, 100]
                                if value <= 0:
                                    value = 0
                                elif value >= 100:
                                    value = 100
                                settings_inputs[active_input] = str(value)
                            except ValueError:
                                settings_inputs[active_input] ="0"
                        # For "duration" there is no limit, so we do not apply any clamping.
                        active_input = None  # Exit the input box after validating

                    # Allow only valid characters (digits and a decimal point if you allow floats for duration)
                    # In our case, "height", "sfx_volume", and "bgm_volume" use integer values.
                    elif event.unicode.isdigit() or (event.unicode == "." and "." not in settings_inputs[active_input]):
                        settings_inputs[active_input] += event.unicode
    if game_status == "menu":
        game_status = main_menu()
        pygame.display.update()
        if game_status == "game":
            pygame.mixer.music.play(-1)
        start_ticks = pygame.time.get_ticks()  # Start time for countdown
        # clock.tick(FPS)
    if game_status == "settings":
        game_status = settings_menu()
        pygame.display.update()
        if game_status == "menu":
            reset_game()
        pygame.mixer.music.stop()
        # clock.tick(FPS)
    if game_status == "game":
        if run:
            # Draw scrolling background
            for i in range(0, tiles):
                screen.blit(bg, (0, i * bg_height + scroll))

                if len(platform_group) < MAX_PLATFORMS:
                    p_w = 100
                    p_x = random.randint(0, 4) * 140 + 25
                    p_y = random.randint(800, 1000)
                    if not counter:
                        p_y += 300
                        counter = True
                    else:
                        counter = False
                    platform = Platform(p_x, p_y, p_w)
                    if not any(pygame.sprite.spritecollide(platform, platform_group, False)):
                        platform_group.add(platform)
            # Scroll background
            scroll -= 5

            platform_group.update(scroll_speed)
            platform_group.draw(screen)

            # Collision detection
            for platform in platform_group:
                somerect = platform.rect.inflate(0, 0)
                if somerect.colliderect(man_rect.inflate(-35, -20)):
                    if platform.shape == "crate":
                        sound_effect.play(loops=0)
                        run = False
                    elif man_rect.bottom > platform.rect.top + 100:
                        sound_effect.play(loops=0)
                        run = False

            # Reset scroll
            if abs(scroll) > bg_height:
                scroll = 0

            keys = pygame.key.get_pressed()
            # Calculate elapsed time

            if not run:
                pygame.mixer.music.stop()
                scroll_speed = 0
                scroll = 0
                text2 = font2.render("GAME OVER", True, BLACK)
                text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                text3 = font.render("TRY AGAIN!", True, BLACK)
                text3_rect = text2.get_rect(center=(350, 480))
                screen.blit(text2, text2_rect)
                screen.blit(text3, text3_rect)

            if current_time == 0:
                pygame.mixer.music.stop()
                scroll_speed = 0
                scroll = 0
                text2 = font2.render("GAME OVER", True, BLACK)
                text2_rect = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                text3 = font2.render("YOU WIN!!", True, BLACK)
                text3_rect = text2.get_rect(center=(WIDTH // 2, 480))
                screen.blit(text2, text2_rect)
                screen.blit(text3, text3_rect)
                wining_sound_effect.play(loops=0)
                run = False

            else:

                # elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                current_time = max(0, seconds - (pygame.time.get_ticks() - start_ticks) // 1000)
                if keys[pygame.K_a]:
                    if man_rect.x >= 5:
                        man_rect.x -= 2
                    man_slow_rect, man_fast_rect = man_rect, man_rect
                if keys[pygame.K_d]:
                    if man_rect.x <= 510:
                        man_rect.x += 2
                    man_slow_rect, man_fast_rect = man_rect, man_rect
                if keys[pygame.K_s]:
                    if man_slow_rect.y >= 150:
                        man_slow_rect.y -= 2
                        FPS = man_slow_rect.y
                    man_image = man_slow1
                    man_rect = man_slow_rect
                    man_fast_rect.center = man_rect.center
                if keys[pygame.K_w]:
                    if man_slow_rect.y <= 350:
                        man_slow_rect.y += 1
                        FPS = man_slow_rect.y - 50
                    man_image = man_fast
                    man_rect = man_fast_rect
                    man_fast_rect.center = man_slow_rect.center

            screen.blit(man_image, man_rect)

            # Render the countdown text
            text = font.render(str(current_time), True, BLACK)
            text_rect = text.get_rect(center=(510, 30))
            if run:
                screen.blit(text, text_rect)

            # Update the display
            pygame.display.update()
            clock.tick(FPS)

pygame.quit()
