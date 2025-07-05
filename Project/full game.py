import pygame
import random
pygame.init()

def menu():
    screen.blit(menu_background_surface, (0, 0))
    start_button.update()
    settings_button.update()
    quit_button.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.click(pygame.mouse.get_pos()) == True:
                    print("Start button clicked")
                    game()
                if settings_button.click(pygame.mouse.get_pos()) == True:
                    print("Settings button clicked")
                if quit_button.click(pygame.mouse.get_pos()) == True:
                    pygame.quit()



        # start_button.change_color(pygame.mouse.get_pos())
        # settings_button.change_color(pygame.mouse.get_pos())
        # quit_button.change_color(pygame.mouse.get_pos())

        pygame.display.update()


def game():
    game_screen()

    while True:
        for i in GRID[0]:
            if i == 1:
                print("Game Over")
                game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Escape button pressed")
                    pause_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.click(pygame.mouse.get_pos()) == True:
                    print("Pause button clicked")
                    pause_game()

        pause_button.update()
        screen.blit(GRID_BACKGROUND, (WIDTH_OFFSET, HEIGHT_OFFSET))
        draw_shape(current_shape, current_pos[0], current_pos[1])
        draw_next_shape(next_shape)
        movement(current_shape)
        drop_shape(current_shape)
        draw_final_shape()
        remove_rows()
        info_bar()

        column(COLUMNS)
        row(ROWS)
        rotate()
        pygame.display.update()
        clock.tick(120)


def pause_game():
    # global pause
    # if pause:
    #     pause = False
    # else:
    #     pause = True
    #
    # importing a pause menu screen image
    pause_menu_screen = pygame.image.load("paused.png").convert_alpha()
    pause_menu_screen = pygame.transform.scale(
        pause_menu_screen, (SCREEN_WIDTH // 2, SCREEN_WIDTH // 2)
    )

    # takes the size of the pause menu screen
    bg_width, bg_height = pause_menu_screen.get_size()

    # getting the x and y coordinates for the pause menu screen
    bg_x = (SCREEN_WIDTH - bg_width) // 2
    bg_y = (SCREEN_HEIGHT - bg_height) // 2

    # creating a transparent background
    transparent_background = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
    )
    transparent_background.fill((0, 0, 0, 128))

    # transferring the transparent background and pause menu screen onto the pause screen
    pause_screen.blit(transparent_background, (0, 0))
    pause_screen.blit(pause_menu_screen, (bg_x, bg_y))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if p_home_button.click(pygame.mouse.get_pos()) == True:
                    print("Home button clicked")
                if p_resume_button.click(pygame.mouse.get_pos()) == True:
                    print("Resume button clicked")
                if p_restart_button.click(pygame.mouse.get_pos()) == True:
                    print("Restart button clicked")
                if p_settings_button.click(pygame.mouse.get_pos()) == True:
                    print("Settings button clicked")

    p_home_button.update()
    p_resume_button.update()
    p_restart_button.update()
    p_settings_button.update()

    pygame.display.update()


def game_over():
    transparent_background = pygame.Surface(
        (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
    )
    transparent_background.fill((0, 0, 0, 175))
    pause_screen.blit(transparent_background, (0, 0))
    # game_over_screen_bg = pygame.image.load("game_over.png").convert()
    # game_over_screen.blit(game_over_screen_bg, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if g_home_button.click(pygame.mouse.get_pos()) == True:
                    print("Home button clicked")
                    menu()
                if g_restart_button.click(pygame.mouse.get_pos()) == True:
                    print("Restart button clicked")
                    game()
        g_home_button.update()
        g_restart_button.update()
        pygame.display.update()



# all shapes
L_SHAPE = [
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
]
L_MIRROR_SHAPE = [
    [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ],
]
Z_SHAPE = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
]
Z_MIRROR_SHAPE = [
    [
        [0, 0, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ],
]
SQUARE_SHAPE = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]
]
T_SHAPE = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 0, 1, 0],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
]
STRAIGHT_SHAPE = [
    [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
    ],
    [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ],
]

SHAPES = [
    L_SHAPE,
    L_MIRROR_SHAPE,
    Z_SHAPE,
    Z_MIRROR_SHAPE,
    T_SHAPE,
    SQUARE_SHAPE,
    STRAIGHT_SHAPE,
]

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

BLOCK_DIMENSION = 35

ROWS = 18
COLUMNS = 9

WIDTH_OFFSET = (SCREEN_WIDTH - (COLUMNS * BLOCK_DIMENSION)) // 2
HEIGHT_OFFSET = (SCREEN_HEIGHT - (ROWS * BLOCK_DIMENSION)) // 2

REFRESH_MOVE_TIME = 0.1
NEXT_MOVE_TIME = 0

REFRESH_DROP_TIME = 0.5
NEXT_DROP_TIME = 0

REFRESH_ROTATE_TIME = 0.15
NEXT_ROTATE_TIME = 0

# to create a grid
GRID = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
GRID_COLOR = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

GRID_BACKGROUND = pygame.Surface(
    (SCREEN_WIDTH - WIDTH_OFFSET * 2, SCREEN_HEIGHT - HEIGHT_OFFSET * 2)
)

clock = pygame.time.Clock()
pause = False
current_pos = [COLUMNS // 2 - 2, -4]
current_time = pygame.time.get_ticks() / 1000
current_score = 0

# initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# to set name of the application
pygame.display.set_caption("Tetris")

# game_over_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

button_font = pygame.font.SysFont("Arial", 30)


class Button:
    def __init__(self, image, x, y, text_input):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        self.text = button_font.render(text_input, True, "grey")
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def click(self, position):
        action = False
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0]:
                action = True
        return action

    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[
            1
        ] in range(self.rect.top, self.rect.bottom):
            self.text = button_font.render(self.text_input, True, (75, 230, 75))
        else:
            self.text = button_font.render(self.text_input, True, "white")


menu_background_surface = pygame.image.load("menu_background.jpeg").convert()
menu_background_surface = pygame.transform.scale(
    menu_background_surface, (SCREEN_WIDTH, SCREEN_HEIGHT + 30)
)
pause_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
home_button_bg = pygame.draw.rect(
    pause_screen, (0, 0, 0), (0, SCREEN_HEIGHT - 75, 75, 75)
)

button_surface = pygame.image.load("button.png").convert_alpha()
button_surface = pygame.transform.scale(button_surface, (300, 75))

start_button = Button(button_surface, SCREEN_WIDTH // 2, 300, "Start")
settings_button = Button(button_surface, SCREEN_WIDTH // 2, 400, "Settings")
quit_button = Button(button_surface, SCREEN_WIDTH // 2, 500, "Quit")

home_button_bg = pygame.draw.rect(
    pause_screen, (0, 0, 0), (0, SCREEN_HEIGHT - 70, 70, 70)
)
resume_button_bg = pygame.draw.rect(pause_screen, (0, 0, 0), (0, 0, 70, 70))
restart_button_bg = pygame.draw.rect(
    pause_screen, (0, 0, 0), (SCREEN_WIDTH - 70, 0, 70, 70)
)
settings_button_bg = pygame.draw.rect(
    pause_screen, (0, 0, 0), (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 70, 70, 70)
)

pause_button_bg = pygame.draw.rect(screen, (0, 0, 0), (0, 0, 70, 70))

home_button_surf = pygame.image.load("home_button.png").convert_alpha()
home_button_surf = pygame.transform.scale(home_button_surf, (75, 75))

resume_button_surf = pygame.image.load("resume_button.png").convert_alpha()
resume_button_surf = pygame.transform.scale(resume_button_surf, (75, 75))

restart_button_surf = pygame.image.load("restart_button.png").convert_alpha()
restart_button_surf = pygame.transform.scale(restart_button_surf, (75, 75))

settings_button_surf = pygame.image.load("settings_button.png").convert_alpha()
settings_button_surf = pygame.transform.scale(settings_button_surf, (75, 75))

pause_button_surf = pygame.image.load("pause_button.png").convert_alpha()
pause_button_surf = pygame.transform.scale(settings_button_surf, (75, 75))

p_home_button = Button(home_button_surf, 75 / 2, SCREEN_HEIGHT - 75 / 2, "")
p_resume_button = Button(resume_button_surf, 75 / 2, 75 / 2, "")
p_restart_button = Button(restart_button_surf, SCREEN_WIDTH - 75 / 2, 75 / 2, "")
p_settings_button = Button(
    settings_button_surf, SCREEN_WIDTH - 75 / 2, SCREEN_HEIGHT - 75 / 2, ""
)

pause_button = Button(pause_button_surf, 75 / 2, 75 / 2, "")

g_home_button = Button(
    home_button_surf, SCREEN_WIDTH // 2 + 70, SCREEN_HEIGHT // 2 + 235, ""
)
g_restart_button = Button(
    restart_button_surf, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 235, ""
)



# to initialize font
def create_text(font_name, font_size, text, color, surface_size):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, surface_size)


# to make the game UI
def game_screen():
    background = pygame.image.load("map1.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))


# to draw a background for showing the next shape
def next_shape_background():
    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (
            WIDTH_OFFSET + BLOCK_DIMENSION * COLUMNS + BLOCK_DIMENSION,
            HEIGHT_OFFSET,
            BLOCK_DIMENSION * 6,
            BLOCK_DIMENSION * 6,
        ),
    )


# to make a info background and write text on it
def info_bar():
    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (
            WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION,
            HEIGHT_OFFSET + BLOCK_DIMENSION * 3.5,
            BLOCK_DIMENSION * 5,
            BLOCK_DIMENSION * ROWS - BLOCK_DIMENSION * 4,
        ),
    )

    create_text(
        "Arial",
        15,
        "Seconds Spent: " + str(int(current_time)),
        "green",
        (WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION + 10, HEIGHT_OFFSET * 4),
    )

    create_text(
        "Arial",
        15,
        "Current Score: " + str(int(current_score)),
        "white",
        (WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION + 10, HEIGHT_OFFSET * 5),
    )

    create_text(
        "Arial",
        15,
        "FPS counter: " + str(int(clock.get_fps())),
        "white",
        (WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION + 10, HEIGHT_OFFSET * 6),
    )


# to draw a single block
def draw_block(x, y, color=(255, 0, 0)):
    pygame.draw.rect(
        screen,
        color,
        (
            WIDTH_OFFSET + x * BLOCK_DIMENSION,
            HEIGHT_OFFSET + y * BLOCK_DIMENSION,
            BLOCK_DIMENSION,
            BLOCK_DIMENSION,
        ),
    )


# to get the shape and variant
def random_shape_varient():
    shape_index = random.randint(0, len(SHAPES) - 1)
    number_of_varinats = len(SHAPES[shape_index])
    variant_index = random.randint(0, number_of_varinats - 1)
    current_shape = SHAPES[shape_index][variant_index]
    return shape_index, variant_index, current_shape


# to chose a random color for the shape
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


current_shape_index, current_shape_variant, current_shape = random_shape_varient()
next_shape_index, next_shape_variant, next_shape = random_shape_varient()
current_color = random_color()
next_color = random_color()


# to draw the shape
def draw_shape(shape, x, y):
    sh = shape
    for i in range(4):
        for j in range(4):
            if i + y < 0:
                continue
            if sh[i][j] == 0:
                continue
            draw_block(x + j, y + i, current_color)


# to draw the oncoming shape
def draw_next_shape(shape):
    sh = shape
    next_shape_background()
    for i in range(4):
        for j in range(4):
            if sh[j][i] == 0:
                continue
            draw_block(i + COLUMNS + 2, j + 1, next_color)


# to draw the shape in its final position
def draw_final_shape():
    for i in range(ROWS):
        for j in range(COLUMNS):
            if GRID[i][j] == 1 and GRID[i][j] is not None:
                draw_block(j, i, GRID_COLOR[i][j])


# to set the shape in its final position
def game_state(shape):
    global current_shape_index, current_shape_variant, current_shape
    global next_shape_index, next_shape_variant, next_shape
    global current_pos
    global current_color, next_color
    x = current_pos[0]
    y = current_pos[1]
    for i in range(4):
        for j in range(4):
            if shape[i][j] == 0:
                continue
            abs_x = x + j
            abs_y = y + i
            if abs_y < 0:
                continue
            GRID[abs_y][abs_x] = 1
            GRID_COLOR[abs_y][abs_x] = current_color
    current_shape_index, current_shape_variant, current_shape = (
        next_shape_index,
        next_shape_variant,
        next_shape,
    )
    next_shape_index, next_shape_variant, next_shape = random_shape_varient()
    current_color = next_color
    next_color = random_color()
    current_pos = [COLUMNS // 2 - 2, -3]


# to check the if the next position of the shape is possible or not
def check_pos(shape, coordinate):
    for i in range(4):
        for j in range(4):
            if shape[i][j] == 0:
                continue
            abs_x = coordinate[0] + j
            abs_y = coordinate[1] + i
            if abs_x < 0 or abs_x >= COLUMNS:
                return False
            if abs_y >= ROWS:
                return False
            if abs_y > 0 and 1 == GRID[abs_y][abs_x]:
                return False

    return True


# to move the shape with some velocity
def movement(shape):
    global NEXT_MOVE_TIME
    global REFRESH_MOVE_TIME
    global current_time
    if current_time < NEXT_MOVE_TIME:
        return

    global current_pos
    temp_pos = current_pos.copy()
    was_button_pressed = False
    if pygame.key.get_pressed()[pygame.K_s]:
        temp_pos[1] += 1
        was_button_pressed = True
    if pygame.key.get_pressed()[pygame.K_a]:
        temp_pos[0] -= 1
        was_button_pressed = True
    if pygame.key.get_pressed()[pygame.K_d]:
        temp_pos[0] += 1
        was_button_pressed = True
    if check_pos(shape, temp_pos):
        current_pos = temp_pos
    if was_button_pressed:
        NEXT_MOVE_TIME = current_time + REFRESH_MOVE_TIME


# to rotate the shape with some velocity
def rotate():
    global NEXT_ROTATE_TIME
    global REFRESH_ROTATE_TIME
    global current_shape_variant, current_shape
    if current_time < NEXT_ROTATE_TIME:
        return
    was_button_pressed = False
    if pygame.key.get_pressed()[pygame.K_e]:
        new_variant = (current_shape_variant + 1) % len(SHAPES[current_shape_index])
        new_shape = SHAPES[current_shape_index][new_variant]
        if check_pos(new_shape, current_pos):
            current_shape_variant = new_variant
            current_shape = new_shape
            was_button_pressed = True
    if pygame.key.get_pressed()[pygame.K_q]:
        new_variant = (current_shape_variant - 1) % len(SHAPES[current_shape_index])
        new_shape = SHAPES[current_shape_index][new_variant]
        if check_pos(new_shape, current_pos):
            current_shape_variant = new_variant
            current_shape = new_shape
            was_button_pressed = True
    if was_button_pressed:
        NEXT_ROTATE_TIME = current_time + REFRESH_ROTATE_TIME


# to drop the shape with some velocity
def drop_shape(shape):
    global NEXT_DROP_TIME
    global REFRESH_DROP_TIME
    global current_time
    if current_time < NEXT_DROP_TIME:
        return
    global current_pos
    temp_pos = current_pos.copy()
    temp_pos[1] += 1
    if check_pos(shape, temp_pos):
        current_pos = temp_pos
    else:
        game_state(shape)
    NEXT_DROP_TIME = current_time + REFRESH_DROP_TIME


# to remove the rows of 1s after it fully filled
def remove_rows():
    global current_score
    for i in range(ROWS):
        if GRID[i] == [1 for _ in range(COLUMNS)]:
            GRID.remove(GRID[i])
            GRID.insert(0, [0 for _ in range(COLUMNS)])
            current_score += 10


# to create a grid lines
def column(COLUMNS):
    gap = 0
    for line in range(COLUMNS + 1):
        pygame.draw.line(
            screen,
            "grey",
            (WIDTH_OFFSET + gap, HEIGHT_OFFSET),
            (WIDTH_OFFSET + gap, SCREEN_HEIGHT - HEIGHT_OFFSET),
        )
        gap += BLOCK_DIMENSION


def row(ROWS):
    gap = 0
    for line in range(ROWS + 1):
        pygame.draw.line(
            screen,
            "grey",
            (WIDTH_OFFSET, HEIGHT_OFFSET + gap),
            (SCREEN_WIDTH - WIDTH_OFFSET, HEIGHT_OFFSET + gap),
        )
        gap += BLOCK_DIMENSION


while True:
    menu()
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         if start_button.click(pygame.mouse.get_pos()) == True:
    #             print("Start button clicked")

    #             game_screen()

    #             tetris_logo = pygame.image.load("tetris_logo.png").convert_alpha()
    #             tetris_logo = pygame.transform.scale(
    #                 tetris_logo, (BLOCK_DIMENSION * 5, BLOCK_DIMENSION * 4)
    #             )

    #             screen.blit(
    #                 tetris_logo,
    #                 (
    #                     WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION,
    #                     HEIGHT_OFFSET,
    #                 ),
    #             )

    #             while True:
    #                 for i in GRID[0]:
    #                     if i == 1:
    #                         print("Game Over")
    #                         game_over()

    #                 current_time = pygame.time.get_ticks() / 1000
    #                 for event in pygame.event.get():
    #                     if event.type == pygame.QUIT:
    #                         pygame.quit()

    #                 screen.blit(GRID_BACKGROUND, (WIDTH_OFFSET, HEIGHT_OFFSET))
    #                 draw_shape(current_shape, current_pos[0], current_pos[1])
    #                 draw_next_shape(next_shape)
    #                 movement(current_shape)
    #                 drop_shape(current_shape)
    #                 draw_final_shape()
    #                 remove_rows()
    #                 info_bar()

    #                 column(COLUMNS)
    #                 row(ROWS)
    #                 rotate()
    #                 pygame.display.update()
    #                 clock.tick(120)

    #         if settings_button.click(pygame.mouse.get_pos()) == True:
    #             print("Settings button clicked")
    #         if quit_button.click(pygame.mouse.get_pos()) == True:
    #             pygame.quit()

    # screen.blit(menu_background_surface, (0, 0))

    # start_button.update()
    # settings_button.update()
    # quit_button.update()

    # start_button.change_color(pygame.mouse.get_pos())
    # settings_button.change_color(pygame.mouse.get_pos())
    # quit_button.change_color(pygame.mouse.get_pos())

    # pygame.display.update()
pygame.quit()
