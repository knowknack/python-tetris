import random
from typing import List
import pygame


# To start
pygame.init()

# Name of application
pygame.display.set_caption("Tetris")

screen_width = 1280
screen_height = 720
block_dimention = 40
COLUMNS = 16
ROWS = 8
width_offset = (screen_width - (8 * block_dimention)) // 2
height_offset = (screen_height - (16 * block_dimention)) // 2
shape_speed = 10

# Initialize screen
screen = pygame.display.set_mode((screen_width, screen_height))


# Initialize font
def create_title(font_name, font_size):
    return pygame.font.SysFont(font_name, font_size)


menu_font = create_title("arial", 60)
button_font = create_title("cambridge", 30)
character_font = create_title("arial", 10)


# Game UI
def game_screen():
    background = pygame.image.load("map1.jpg").convert()
    background = pygame.transform.scale(background, (screen_width, screen_height + 30))
    screen.blit(background, (0, 0))


# Block color
r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)

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
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
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
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
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
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 0],
    ],
]
Z_MIRROR_SHAPE = [
    [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [1, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
]
SQR_SHAPE = [
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
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ],
    [
        [0, 1, 0, 0],
        [1, 1, 1, 0],
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

# Grid
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


def draw_block(x, y, color=(255, 0, 0)):
    pygame.draw.rect(
        screen,
        color,
        (
            width_offset + x * block_dimention,
            height_offset + y * block_dimention,
            block_dimention,
            block_dimention,
        ),
    )


def draw_shape(shape: List[List[List[int]]], variant: int, x: int, y: int):
    # def draw_shape(shape):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    sh = shape[variant]

    for i in range(4):
        for j in range(4):
            if sh[i][j] == 0:
                continue

            draw_block(x + j, y + i, (r, g, b))


def possible_move(shape_variant, x, y):
    for i in range(4):
        for j in range(4):
            if shape_variant[i][j] == 0:
                continue
            if x + j < 0 or x + j >= ROWS or y + i >= COLUMNS:
                return False
    return True


current_pos = [0, 0]
test = possible_move(T_SHAPE, current_pos[0], current_pos[1])


def shapeFirstColumnContain(shape):
    print(shape)
    for line in shape:
        if line[0] == 1:
            print("ok true")
            return True
    return False


def shapeLastColumnContain(shape):
    print(shape)

    for line in shape:
        if line[3] == 1:
            print("ok true")
            return True
    return False


def shapeLastRowContain(shape):
    for block in shape[3]:
        if block == 1:
            return True
    return False


def is_movement_possible(shape: List[List[int]], position: List[int]) -> bool:
    for i in range(4):
        for j in range(4):
            if shape[i][j] == 0:
                continue

            if j + position[0] < 0 or j + position[0] > 7:
                return False

            if i + position[1] < 0 or i + position[1] > 15:
                return False

    return True


def movement(shape):
    # print(str(current_pos))
    global current_pos
    temp_pos = [current_pos[0], current_pos[1]]
    if pygame.key.get_pressed()[pygame.K_a]:
        temp_pos[0] -= 1
    if pygame.key.get_pressed()[pygame.K_d]:
        temp_pos[0] += 1
    if pygame.key.get_pressed()[pygame.K_w]:
        temp_pos[1] -= 1
    if pygame.key.get_pressed()[pygame.K_s]:
        temp_pos[1] += 1

    if is_movement_possible(shape, temp_pos):
        current_pos = [temp_pos[0], temp_pos[1]]


# To create a grid
def column(lines):
    gap = 0
    for line in range(lines):
        pygame.draw.line(
            screen,
            "grey",
            (width_offset + gap, height_offset),
            (width_offset + gap, screen_height - height_offset),
        )
        gap += block_dimention


grid_background = pygame.Surface(
    (screen_width - width_offset * 2, screen_height - height_offset * 2)
)


def row(lines):
    gap = 0
    for line in range(lines):
        pygame.draw.line(
            screen,
            "grey",
            (width_offset, height_offset + gap),
            (screen_width - width_offset, height_offset + gap),
        )
        gap += block_dimention


x = 0
y = 0
game_screen()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                continue
            pygame.draw.rect(
                screen,
                (r, g, b),
                (
                    width_offset + j * block_dimention,
                    height_offset + i * block_dimention,
                    block_dimention,
                    block_dimention,
                ),
            )
    screen.blit(grid_background, (width_offset, height_offset))

    draw_shape(T_SHAPE, 1, current_pos[0], current_pos[1])
    movement(T_SHAPE[1])
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (width_offset + block_dimention * ROWS, height_offset, 200, 200),
    )

    column(lines=ROWS + 1)
    row(lines=COLUMNS + 1)
    pygame.display.update()
    pygame.time.Clock().tick(120)
