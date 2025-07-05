import random
import pygame

# To start
pygame.init()

clock = pygame.time.Clock()
# Shapes
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

REFRESH_ROTATE_TIME = 0.1
NEXT_ROTATE_TIME = 0

# To create a grid
GRID = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
GRID_COLOR = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]

GRID_BACKGROUND = pygame.Surface(
    (SCREEN_WIDTH - WIDTH_OFFSET * 2, SCREEN_HEIGHT - HEIGHT_OFFSET * 2)
)

current_pos = [COLUMNS // 2 - 2, -4]
current_time = pygame.time.get_ticks() / 1000
current_score = 0
previous_frame_time = 0

# Name of application
pygame.display.set_caption("Tetris")

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Initialize font
def create_text(font_name, font_size, text, color, surface_size):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, surface_size)


# Game UI
def game_screen():
    background = pygame.image.load("map1.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))


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

def info_bar():
    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (
            WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION,
            HEIGHT_OFFSET + BLOCK_DIMENSION * 3.5,
            BLOCK_DIMENSION * 5,
            BLOCK_DIMENSION * ROWS - BLOCK_DIMENSION * 4 ,
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


def random_shape_varient():
    shape_index = random.randint(0, len(SHAPES) - 1)
    number_of_varinats = len(SHAPES[shape_index])
    variant_index = random.randint(0, number_of_varinats - 1)
    current_shape = SHAPES[shape_index][variant_index]
    return shape_index, variant_index, current_shape


def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


current_shape_index, current_shape_variant, current_shape = random_shape_varient()
next_shape_index, next_shape_variant, next_shape = random_shape_varient()
current_color = random_color()
next_color = random_color()


def draw_shape(shape, x, y):
    sh = shape
    for i in range(4):
        for j in range(4):
            if i + y < 0:
                continue
            if sh[i][j] == 0:
                continue
            draw_block(x + j, y + i, current_color)


def draw_next_shape(shape):
    sh = shape
    next_shape_background()
    for i in range(4):
        for j in range(4):
            if sh[j][i] == 0:
                continue
            draw_block(i + COLUMNS + 2, j + 1, next_color)


def draw_final_shape():
    for i in range(ROWS):
        for j in range(COLUMNS):
            if GRID[i][j] == 1 and GRID[i][j] != None:
                draw_block(j, i, GRID_COLOR[i][j])


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


def remove_rows():
    global current_score
    for i in range(ROWS):
        if GRID[i] == [1 for _ in range(COLUMNS)]:
            GRID.remove(GRID[i])
            GRID.insert(0, [0 for _ in range(COLUMNS)])
            current_score += 10


# To create a grid lines
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


game_screen()

tetris_logo = pygame.image.load("tetris_logo.png").convert_alpha()
tetris_logo = pygame.transform.scale(
    tetris_logo, (BLOCK_DIMENSION * 5, BLOCK_DIMENSION * 4)
)

screen.blit(
    tetris_logo,
    (WIDTH_OFFSET - BLOCK_DIMENSION * 5 - BLOCK_DIMENSION, HEIGHT_OFFSET),

)
while True:
    if GRID[0] == [1 for _ in range(COLUMNS)]:
        pass


    current_time = pygame.time.get_ticks() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

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
