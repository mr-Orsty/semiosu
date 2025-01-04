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
back_button_rect = pygame.Rect(240, 380, 130, 45)

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
rectangle_delay = 2  # Время, через которое появляется зеленый прямоугольник (в секундах)
hit_wait_time = 1  # Время ожидания нажатия на прямоугольник (в секундах)

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

# Main Loop
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

            elif isDifficultyOpen:
                if easy_button_rect.collidepoint(event.pos):
                    goal_points = 10
                    rectangle_delay = 2.4  # Устанавливаем стандартное значение для легкого уровня
                    hit_wait_time = 1.4  # Устанавливаем стандартное значение для легкого уровня
                    isDifficultyOpen = False
                    isGameRunning = True  # Start the game
                    reset_game()

                elif medium_button_rect.collidepoint(event.pos):
                    goal_points = 50
                    rectangle_delay = 1.5  # Для среднего уровня
                    hit_wait_time = 1  # Для среднего уровня
                    isDifficultyOpen = False
                    isGameRunning = True
                    reset_game()

                elif hard_button_rect.collidepoint(event.pos):
                    goal_points = 100
                    rectangle_delay = 0.8  # Для сложного уровня (по аналогии)
                    hit_wait_time = 0.5  # Для сложного уровня (по аналогии)
                    isDifficultyOpen = False
                    isGameRunning = True
                    reset_game()

                elif back_button_rect.collidepoint(event.pos):
                    isDifficultyOpen = False
                    isMenuOpen = True

            elif isSettingsOpen:
                if back_button_rect.collidepoint(event.pos):
                    isSettingsOpen = False
                    isMenuOpen = True

                if volume_slider_rect.collidepoint(event.pos):
                    is_dragging = True
                    slider_pos = max(0, min(200, event.pos[0] - volume_slider_rect.x))
                    music_volume = slider_pos / 200
                    pygame.mixer.music.set_volume(music_volume)

            elif isGameRunning:
                if menu_button_rect.collidepoint(event.pos):
                    isGameRunning = False
                    isMenuOpen = True

                if active_rect_index != -1:
                    active_rect = rects[active_rect_index]
                    if (player_x, player_y) == active_rect["center"]:
                        if active_rect["color"] == "green":
                            points += 1
                        elif active_rect["color"] == "red":
                            points -= 2
                        time_taken = pygame.time.get_ticks() - start_time
                    else:
                        points -= 1

                    player_x, player_y = 300, 300
                    active_rect_index = -1
                    for rect in rects:
                        rect["color"] = "yellow"
                    waiting = True
                    wait_start_time = time.time()

            elif volume_slider_rect.collidepoint(event.pos):
                if is_dragging:
                    slider_pos = max(0, min(200, event.pos[0] - volume_slider_rect.x))
                    music_volume = slider_pos / 200
                    pygame.mixer.music.set_volume(music_volume)

        elif event.type == pygame.MOUSEBUTTONUP:
            is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if is_dragging:
                slider_pos = max(0, min(200, event.pos[0] - volume_slider_rect.x))
                music_volume = slider_pos / 200
                pygame.mixer.music.set_volume(music_volume)

    screen.fill("purple")

    # Check if points have reached the goal here (outside event handling)
    if isGameRunning and points >= goal_points:
        print(f"Goal reached. Points: {points}, Goal: {goal_points}")  # Debug message
        isGameRunning = False
        isDifficultyOpen = True
        reset_game()

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

    elif isDifficultyOpen:  # Difficulty buttons for Easy, Medium, Hard
        pygame.draw.rect(screen, "yellow", easy_button_rect)
        easy_text = font.render("Easy", True, "black")
        screen.blit(easy_text, (278, 211))

        pygame.draw.rect(screen, "yellow", medium_button_rect)
        medium_text = font.render("Medium", True, "black")
        screen.blit(medium_text, (257, 271))

        pygame.draw.rect(screen, "yellow", hard_button_rect)
        hard_text = font.render("Hard", True, "black")
        screen.blit(hard_text, (278, 331))

        pygame.draw.rect(screen, "yellow", back_button_rect)
        back_text = font.render("Back", True, "black")
        screen.blit(back_text, (278, 391))

    elif isSettingsOpen:
        pygame.draw.rect(screen, "yellow", back_button_rect)
        back_text = font.render("Back", True, "black")
        screen.blit(back_text, (255, 391))

        settings_title = font.render("Settings", True, "white")
        screen.blit(settings_title, (253, 210))

        pygame.draw.rect(screen, "white", volume_slider_rect)
        pygame.draw.rect(screen, "blue", pygame.Rect(volume_slider_rect.x + slider_pos - 5, volume_slider_rect.y - 5, 10, volume_slider_rect.height + 10))

        volume_text = font.render(f"Volume: {int(music_volume * 100)}%", True, "white")
        screen.blit(volume_text, (233, 283))

    elif isGameRunning:
        current_time = time.time()

        if active_rect_index != -1 and current_time - last_switch_time >= rectangle_delay:
            if rects[active_rect_index]["color"] == "green":
                points -= 1
            elif rects[active_rect_index]["color"] == "red":
                points += 1

            rects[active_rect_index]["color"] = "yellow"
            active_rect_index = -1
            waiting = True
            wait_start_time = current_time

            player_x, player_y = 300, 300

        if active_rect_index == -1 and not waiting:
            active_rect_index = random.randint(0, len(rects) - 1)
            rects[active_rect_index]["color"] = "red" if random.random() < 0.1 else "green"
            last_switch_time = current_time
            start_time = pygame.time.get_ticks()

        if waiting and current_time - wait_start_time >= hit_wait_time:
            waiting = False

        for rect in rects:
            rect_x = rect["center"][0] - rect["size"][0] // 2
            rect_y = rect["center"][1] - rect["size"][1] // 2
            pygame.draw.rect(screen, rect["color"], pygame.Rect(rect_x, rect_y, *rect["size"]))

        pygame.draw.circle(screen, "red", (player_x, player_y), 15)

        text = font.render(f"Points: {points}", True, (255, 255, 255))
        screen.blit(text, (247, 47))

        time_text = font.render(f"{time_taken / 1000:.4f} s", True, (255, 255, 255))
        screen.blit(time_text, (247, 550))

        pygame.draw.rect(screen, "yellow", menu_button_rect)
        menu_text = font.render("Menu", True, "black")
        screen.blit(menu_text, (20, 16))

        goal_text = font.render(f"Goal: {goal_points}", True, (255, 255, 255))
        screen.blit(goal_text, (250, 75))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            player_x, player_y = 300, 300
        if not waiting:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_x, player_y = 300, 150
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_x, player_y = 300, 450
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_x, player_y = 150, 300
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_x, player_y = 450, 300

        if keys[pygame.K_SPACE] and active_rect_index != -1:
            active_rect = rects[active_rect_index]
            if (player_x, player_y) == active_rect["center"]:
                if active_rect["color"] == "green":
                    points += 1
                elif active_rect["color"] == "red":
                    points -= 2
                time_taken = pygame.time.get_ticks() - start_time
            else:
                points -= 1

            player_x, player_y = 300, 300
            active_rect_index = -1
            for rect in rects:
                rect["color"] = "yellow"
            waiting = True
            wait_start_time = time.time()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
