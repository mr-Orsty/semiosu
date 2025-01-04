import pygame
import random
import time

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True
isMenuOpen = True
isSettingsOpen = False
isGameRunning = False
isDifficultyOpen = False  # New state to manage difficulty selection
font = pygame.font.Font(None, 36)

# Game state variables
points = 0
time_taken = 0
waiting = True
wait_start_time = time.time()

# Player Pos
player_x = 300
player_y = 300

# Rectangles
rects = [
    {"center": (300, 150), "size": (60, 80), "color": "yellow"},
    {"center": (300, 450), "size": (60, 80), "color": "yellow"},
    {"center": (150, 300), "size": (60, 80), "color": "yellow"},
    {"center": (450, 300), "size": (60, 80), "color": "yellow"},
]

# Timer for rectangle activation
last_switch_time = time.time()
start_time = 0
active_rect_index = -1

# Menu buttons
menu_button_rect = pygame.Rect(10, 10, 85, 35)
start_button_rect = pygame.Rect(240, 200, 130, 45)
settings_button_rect = pygame.Rect(240, 260, 130, 45)
exit_button_rect = pygame.Rect(240, 320, 130, 45)
back_button_rect = pygame.Rect(240, 320, 130, 45)

# Difficulty buttons
easy_button_rect = pygame.Rect(240, 200, 130, 45)
medium_button_rect = pygame.Rect(240, 260, 130, 45)
hard_button_rect = pygame.Rect(240, 320, 130, 45)

# Music volume control variables
volume_slider_rect = pygame.Rect(200, 255, 200, 10)
slider_pos = 100
music_volume = 0.5
is_dragging = False

# Load music
pygame.mixer.music.load("sounds/background_music.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(music_volume)

# Goal value based on difficulty
goal_points = 10

# Function to reset game state
def reset_game():
    global points, time_taken, waiting, wait_start_time, player_x, player_y, rects, active_rect_index, last_switch_time, start_time, goal_points
    points = 0
    time_taken = 0
    waiting = True
    wait_start_time = time.time()
    player_x, player_y = 300, 300
    rects = [
        {"center": (300, 150), "size": (60, 80), "color": "yellow"},
        {"center": (300, 450), "size": (60, 80), "color": "yellow"},
        {"center": (150, 300), "size": (60, 80), "color": "yellow"},
        {"center": (450, 300), "size": (60, 80), "color": "yellow"},
    ]
    active_rect_index = -1
    last_switch_time = time.time()
    start_time = 0

# Новый флаг для отслеживания завершения игры
isGameOver = False

# Обновление главного цикла
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if isMenuOpen:
                if start_button_rect.collidepoint(event.pos):
                    isMenuOpen = False
                    isDifficultyOpen = True  # Open difficulty selection
                elif settings_button_rect.collidepoint(event.pos):
                    isMenuOpen = False
                    isSettingsOpen = True
                elif menu_button_rect.collidepoint(event.pos):
                    isMenuOpen = True
                elif exit_button_rect.collidepoint(event.pos):
                    running = False

            elif isDifficultyOpen:  # Handle difficulty selection
                if easy_button_rect.collidepoint(event.pos):
                    goal_points = 10
                    isDifficultyOpen = False
                    isGameRunning = True  # Start the game
                    reset_game()
                elif medium_button_rect.collidepoint(event.pos):
                    goal_points = 50
                    isDifficultyOpen = False
                    isGameRunning = True
                    reset_game()
                elif hard_button_rect.collidepoint(event.pos):
                    goal_points = 100
                    isDifficultyOpen = False
                    isGameRunning = True
                    reset_game()

            elif isSettingsOpen:
                if back_button_rect.collidepoint(event.pos):
                    isSettingsOpen = False
                    isMenuOpen = True

            elif isGameOver:  # Возврат в меню после завершения игры
                if menu_button_rect.collidepoint(event.pos):
                    isGameOver = False
                    isMenuOpen = True

    screen.fill("purple")

    if isMenuOpen:
        pygame.draw.rect(screen, "yellow", start_button_rect)
        start_text = font.render("Start", True, "black")
        screen.blit(start_text, (278, 211))

        pygame.draw.rect(screen, "yellow", settings_button_rect)
        settings_text = font.render("Settings", True, "black")
        screen.blit(settings_text, (257, 271))

        pygame.draw.rect(screen, "yellow", exit_button_rect)
        exit_text = font.render("Quit", True, "black")
        screen.blit(exit_text, (278, 331))

    elif isDifficultyOpen:
        pygame.draw.rect(screen, "yellow", easy_button_rect)
        easy_text = font.render("Easy", True, "black")
        screen.blit(easy_text, (278, 211))

        pygame.draw.rect(screen, "yellow", medium_button_rect)
        medium_text = font.render("Medium", True, "black")
        screen.blit(medium_text, (257, 271))

        pygame.draw.rect(screen, "yellow", hard_button_rect)
        hard_text = font.render("Hard", True, "black")
        screen.blit(hard_text, (278, 331))

    elif isSettingsOpen:
        pygame.draw.rect(screen, "yellow", back_button_rect)
        back_text = font.render("Back", True, "black")
        screen.blit(back_text, (255, 331))

        settings_title = font.render("Settings", True, "white")
        screen.blit(settings_title, (253, 210))

        pygame.draw.rect(screen, "white", volume_slider_rect)
        pygame.draw.rect(screen, "blue", pygame.Rect(volume_slider_rect.x + slider_pos - 5, volume_slider_rect.y - 5, 10, volume_slider_rect.height + 10))

        volume_text = font.render(f"Volume: {int(music_volume * 100)}%", True, "white")
        screen.blit(volume_text, (233, 283))

    elif isGameRunning:
        current_time = time.time()

        if active_rect_index != -1 and current_time - last_switch_time >= 2:
            if rects[active_rect_index]["color"] == "green":
                points -= 1
            elif rects[active_rect_index]["color"] == "red":
                points += 1

            rects[active_rect_index]["color"] = "yellow"
            active_rect_index = -1
            waiting = True
            wait_start_time = current_time

        if active_rect_index == -1 and not waiting:
            active_rect_index = random.randint(0, len(rects) - 1)
            rects[active_rect_index]["color"] = "red" if random.random() < 0.2 else "green"
            last_switch_time = current_time
            start_time = pygame.time.get_ticks()

        if waiting and current_time - wait_start_time >= 2:
            waiting = False

        for rect in rects:
            rect_x = rect["center"][0] - rect["size"][0] // 2
            rect_y = rect["center"][1] - rect["size"][1"] // 2
            pygame.draw.rect(screen, rect["color"], pygame.Rect(rect_x, rect_y, *rect["size"]))

        pygame.draw.circle(screen, "red", (player_x, player_y), 15)

        text = font.render(f"Points: {points}", True, (255, 255, 255))
        screen.blit(text, (247, 55))

        goal_text = font.render(f"Goal: {goal_points}", True, (255, 255, 255))
        screen.blit(goal_text, (247, 90))

        if points >= goal_points:  # Проверка достижения цели
            isGameRunning = False
            isGameOver = True

    elif isGameOver:
        game_over_text = font.render("You Win!", True, (255, 255, 255))
        screen.blit(game_over_text, (250, 270))

        pygame.draw.rect(screen, "yellow", menu_button_rect)
        menu_text = font.render("Menu", True, "black")
        screen.blit(menu_text, (20, 16))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()