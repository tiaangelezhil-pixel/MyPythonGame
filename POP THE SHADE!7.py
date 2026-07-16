import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
width = 900
height = 600
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
pygame.display.set_caption("Pop The Shade")

# Load logo
logo = pygame.image.load(r"C:\Users\tisha\AppData\Local\Programs\Python\Python310\schoollogo.png.png")
logo_height = int(height * 0.1)
logo = pygame.transform.scale(
    logo,
    (int(logo_height * (logo.get_width() / logo.get_height())), logo_height))

# Define bright colors
red = pygame.Color(255, 0, 0)
burnt_orange = pygame.Color(204, 85, 0)
yellow = pygame.Color(255, 255, 0)
green = pygame.Color(0, 200, 0)

colors = [red, burnt_orange, yellow, green] 

# Arrow drawing function (with shaft + head)
def draw_arrow(surface, direction):
    arrow_color = (0, 0, 0)
    center_x = width // 2
    center_y = height // 2

    shaft_length = 120
    head_size = 30
    thickness = 8

    if direction == "right":
        # Draw shaft
        pygame.draw.line(
            surface,
            arrow_color,
            (center_x - shaft_length // 2, center_y),
            (center_x + shaft_length // 2, center_y),
            thickness
        )

        # Draw head
        pygame.draw.polygon(
            surface,
            arrow_color,
            [
                (center_x + shaft_length // 2 + head_size, center_y),
                (center_x + shaft_length // 2, center_y - head_size),
                (center_x + shaft_length // 2, center_y + head_size)
            ]
        )

    else:  # left
        # Draw shaft
        pygame.draw.line(
            surface,
            arrow_color,
            (center_x + shaft_length // 2, center_y),
            (center_x - shaft_length // 2, center_y),
            thickness
        )

        # Draw head
        pygame.draw.polygon(
            surface,
            arrow_color,
            [
                (center_x - shaft_length // 2 - head_size, center_y),
                (center_x - shaft_length // 2, center_y - head_size),
                (center_x - shaft_length // 2, center_y + head_size)
            ]
        )

font = pygame.font.SysFont("monospace", 100)
timer_font = pygame.font.SysFont("monospace", 50)

# Pause button
pause_button_color = (200, 200, 200)
pause_button_rect = pygame.Rect(20, 20, 150, 50)
pause_font = pygame.font.SysFont("monospace", 40)

paused = False

# Time settings
total_time = 30
display_time = 2

# Countdown
for count in range(5, 0, -1):
    screen.fill((255, 255, 255))
    countdown_text = font.render(str(count), True, (0, 0, 0))
    screen.blit(
        countdown_text,
        (width // 2 - countdown_text.get_width() // 2,
         height // 2 - countdown_text.get_height() // 2)
    )
    pygame.display.flip()
    pygame.time.delay(1000)

# Start game
start_time = time.time()
color_change_time = time.time()
color = random.choice(colors)
last_color = color
arrow_direction = random.choice(["left", "right"])  # RANDOM start

pause_start_time = 0
running = True
clock = pygame.time.Clock()

while running:

    clock.tick(60)

    if not paused:
        elapsed_time = time.time() - start_time
    else:
        elapsed_time = pause_start_time - start_time

    if elapsed_time >= total_time:
        running = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pause_start_time = time.time()
                else:
                    start_time += time.time() - pause_start_time

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
                if paused:
                    pause_start_time = time.time()
                else:
                    start_time += time.time() - pause_start_time

    if not paused:
        current_time = time.time()

        if current_time - color_change_time >= display_time:
            new_color = random.choice(colors)
            while new_color == last_color:
                new_color = random.choice(colors)

            color = new_color
            last_color = color
            color_change_time = current_time

            # RANDOM arrow direction
            arrow_direction = random.choice(["left", "right"])

    screen.fill(color)

    # Logo
    logo_x = (width - logo.get_width()) // 2
    screen.blit(logo, (logo_x, 0))

    # Draw arrow
    draw_arrow(screen, arrow_direction)

    # Timer
    remaining_time = max(0, total_time - int(elapsed_time))
    minutes = remaining_time // 60
    seconds = remaining_time % 60
    timer_text = timer_font.render(f'{minutes:02}:{seconds:02}', True, (0, 0, 0))
    screen.blit(timer_text, (width - timer_text.get_width() - 20, 20))

    # Pause Button
    pygame.draw.rect(screen, pause_button_color, pause_button_rect)
    button_label = "Resume" if paused else "Pause"
    button_text = pause_font.render(button_label, True, (0, 0, 0))
    button_text_rect = button_text.get_rect(center=pause_button_rect.center)
    screen.blit(button_text, button_text_rect)

    pygame.display.flip()

# Game Over
screen.fill((255, 255, 255))
message = font.render("Good Try!!!", True, (0, 0, 0))
screen.blit(
    message,
    (width // 2 - message.get_width() // 2,
     height // 2 - message.get_height() // 2)
)
pygame.display.flip()

pygame.time.delay(3000)
pygame.quit()
