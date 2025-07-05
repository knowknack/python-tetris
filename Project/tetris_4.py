import random
import math
from typing import List
import pygame
import time
from pygame.locals import DOUBLEBUF, QUIT, KEYDOWN, KEYUP

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

SHAPES = [
    L_SHAPE,
    L_MIRROR_SHAPE,
    Z_SHAPE,
    Z_MIRROR_SHAPE,
    SQR_SHAPE,
    T_SHAPE,
    STRAIGHT_SHAPE,
]
SHAPE_NAMES = [
    "L_SHAPE",
    "L_MIRROR_SHAPE",
    "Z_SHAPE",
    "Z_MIRROR_SHAPE",
    "SQR_SHAPE",
    "T_SHAPE",
    "STRAIGHT_SHAPE",
]
NUMBER_OF_SHAPES = len(SHAPES)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS_LIMIT = 120

CELL_SIZE = 40

GRID_LINE_WIDTH = 1
GRID_LINE_COLOR = WHITE
GRID_BG_COLOR = (32, 32, 32)

PADDING = 20
INFO_SCREEN_WIDTH = CELL_SIZE * 4 + (20 * 2)
INFO_SCREEN_BG_COLOR = (32, 32, 32)
INFO_SCREEN_NEXT_SHAPE_BG_COLOR = WHITE
NUMBER_OF_COLS = 8
NUMBER_OF_ROWS = 16

TEXT_REFRESH_PER_SECOND = 3.0
TARGET_FPS = 120.0

DEFAULT_BLOCK_DROP_CELL_PER_SECOND = 2.0
DEFAULT_REFRESH_BLOCK_MOVE_TIME = 0.2


def calculate_offsets():
    total_width = (NUMBER_OF_COLS * CELL_SIZE) + INFO_SCREEN_WIDTH + PADDING
    horizontal_offset1 = (WINDOW_WIDTH - total_width) // 2
    horizontal_offset2 = horizontal_offset1 + (NUMBER_OF_COLS * CELL_SIZE) + PADDING

    total_hight = NUMBER_OF_ROWS * CELL_SIZE
    vertical_offset = (WINDOW_HEIGHT - total_hight) // 2

    return horizontal_offset1, horizontal_offset2, vertical_offset


def get_random_shape():
    shape_index = random.randint(0, NUMBER_OF_SHAPES - 1)
    variant_index = random.randint(0, len(SHAPES[shape_index]) - 1)
    return shape_index, variant_index, SHAPES[shape_index][variant_index]


def get_shape(shape_index: int, variant_index=0):
    return SHAPES[shape_index][variant_index]


class Game:
    def __init__(self) -> None:
        pygame.init()

        ## OPTIMIZATION: Only tracking those events that are required
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

        flags = DOUBLEBUF  # FULLSCREEN
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags)
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        self.events = pygame.event.get()
        self.game_running = True
        self.horizontal_offset1, self.horizontal_offset2, self.vertical_offset = (
            calculate_offsets()
        )
        self.last_frame_time = 0.0
        # dont set to 0 as it might lead to divide by zero error
        self.current_frame_time = 1.0

        self.fps_text = pygame.font.Font(None, 32)
        self.next_text_refresh_time = 0.0
        self.current_fps = "0.0"
        self.next_tick_block_move_time = 0.0
        self.refresh_block_move_time = DEFAULT_REFRESH_BLOCK_MOVE_TIME
        self.block_start_cord = [
            math.floor(NUMBER_OF_COLS / 2) - 1,
            -4,  ## Start from off screen from above
        ]

        self.next_tick_block_move_down_time = 0.0
        self.block_speed = DEFAULT_BLOCK_DROP_CELL_PER_SECOND

        background_image = pygame.image.load("map1.jpg").convert()
        self.BACKGROUND_IMAGE = pygame.transform.scale(
            background_image, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )

        self.current_block_index, self.current_block_variant, self.current_block = (
            get_random_shape()
        )
        self.next_block_index, self.next_block_variant, self.next_block = (
            get_random_shape()
        )

        self.current_block_cord = [self.block_start_cord[0], self.block_start_cord[1]]

        self.game_state = [
            [0 for _ in range(NUMBER_OF_COLS)] for _ in range(NUMBER_OF_ROWS)
        ]

    def get_nth_variant(self, nth: int):
        number_of_variants = len(SHAPES[self.current_block_index])

        while nth < 0:
            nth += number_of_variants

        nth_block_vairant = (self.current_block_variant + nth) % number_of_variants
        current_block = SHAPES[self.current_block_index][nth_block_vairant]
        return nth_block_vairant, current_block

    def render_background_img(self):
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

    def draw_grid(self):
        grid_background = pygame.Surface(
            (NUMBER_OF_COLS * CELL_SIZE, NUMBER_OF_ROWS * CELL_SIZE)
        )
        grid_background.fill(GRID_BG_COLOR)

        self.screen.blit(
            grid_background, (self.horizontal_offset1, self.vertical_offset)
        )

        ## Drawing Columns
        for i in range(NUMBER_OF_COLS + 1):
            pygame.draw.line(
                self.screen,
                GRID_LINE_COLOR,
                (self.horizontal_offset1 + (i * CELL_SIZE), self.vertical_offset),
                (
                    self.horizontal_offset1 + (i * CELL_SIZE),
                    self.vertical_offset + (NUMBER_OF_ROWS * CELL_SIZE),
                ),
            )

        ## Drawing rows
        for i in range(NUMBER_OF_ROWS + 1):
            pygame.draw.line(
                self.screen,
                GRID_LINE_COLOR,
                (self.horizontal_offset1, self.vertical_offset + (i * CELL_SIZE)),
                (
                    self.horizontal_offset1 + (NUMBER_OF_COLS * CELL_SIZE),
                    self.vertical_offset + (i * CELL_SIZE),
                ),
            )

    def draw_info_screen(self):
        info_background = pygame.Surface(
            (INFO_SCREEN_WIDTH, NUMBER_OF_ROWS * CELL_SIZE)
        )
        info_background.fill(INFO_SCREEN_BG_COLOR)

        self.screen.blit(
            info_background, (self.horizontal_offset2, self.vertical_offset)
        )

    def draw_fps(self):
        text = self.fps_text.render(self.current_fps, True, WHITE, BLACK)
        self.screen.blit(text, (30, 30))

        if self.current_frame_time < self.next_text_refresh_time:
            return

        self.current_fps = str(round(1 / self.delta_time, 1))

        self.next_text_refresh_time = self.current_frame_time + (
            1 / (TEXT_REFRESH_PER_SECOND)
        )

    def set_next_block(self):
        self.current_block_index = self.next_block_index
        self.current_block_variant = self.next_block_variant
        self.current_block = self.next_block
        self.current_block_cord = [self.block_start_cord[0], self.block_start_cord[1]]

        self.next_block_index, self.next_block_variant, self.next_block = (
            get_random_shape()
        )

    def draw_cell(self, coordinate: List[int], color=RED):
        pygame.draw.rect(
            self.screen,
            color,
            (
                coordinate[0],
                coordinate[1],
                CELL_SIZE,
                CELL_SIZE,
            ),
        )

    def draw_cell_in_grid(self, coordinate: List[int], color=RED) -> bool:
        if coordinate[0] < 0:
            return False
        if coordinate[0] >= NUMBER_OF_COLS:
            return False

        if coordinate[1] < 0:
            return False
        if coordinate[1] >= NUMBER_OF_ROWS:
            return False

        draw_cord = [
            self.horizontal_offset1 + coordinate[0] * CELL_SIZE,
            self.vertical_offset + coordinate[1] * CELL_SIZE,
        ]
        self.draw_cell(draw_cord, color)
        return True

    def render_current_block(self):
        for i in range(4):
            for j in range(4):
                if self.current_block[i][j] == 0:
                    continue

                absolute_cord = [
                    self.current_block_cord[0] + j,
                    self.current_block_cord[1] + i,
                ]

                self.draw_cell_in_grid(absolute_cord)

    def render_next_block(self):
        text = self.fps_text.render(
            SHAPE_NAMES[self.current_block_index], True, WHITE, BLACK
        )
        self.screen.blit(text, (30, 60))

        text = self.fps_text.render(
            "shape variant: " + str(self.current_block_index), True, WHITE, BLACK
        )
        self.screen.blit(text, (30, 90))

        text = self.fps_text.render(
            "shape index: " + str(self.current_block_variant), True, WHITE, BLACK
        )
        self.screen.blit(text, (30, 120))

        text = self.fps_text.render(
            SHAPE_NAMES[self.next_block_index], True, WHITE, BLACK
        )
        self.screen.blit(text, (30, 150))

        text = self.fps_text.render(
            "shape variant: " + str(self.next_block_index), True, WHITE, BLACK
        )
        self.screen.blit(text, (30, 180))

        text = self.fps_text.render(
            "shape index: " + str(self.next_block_variant), True, WHITE, BLACK
        )
        self.screen.blit(text, (30, 210))

        ## ====
        info_next_shape_background = pygame.Surface((INFO_SCREEN_WIDTH - 20, 190))
        info_next_shape_background.fill(INFO_SCREEN_NEXT_SHAPE_BG_COLOR)

        # info_next_shape
        self.screen.blit(
            info_next_shape_background,
            (self.horizontal_offset2 + 10, self.vertical_offset + 10),
        )

        for i in range(4):
            for j in range(4):
                if self.next_block[i][j] == 0:
                    continue

                cord = [
                    (self.horizontal_offset2 + 20) + (j * CELL_SIZE),
                    (self.vertical_offset + 20) + (i * CELL_SIZE),
                ]

                self.draw_cell(cord)

    def is_movement_possible(
        self, block: List[List[int]], coordinate: List[int]
    ) -> bool:
        for i in range(4):
            for j in range(4):
                if block[i][j] == 0:
                    continue

                if j + coordinate[0] < 0 or j + coordinate[0] > 7:
                    return False

                # allow negitive movement in y axis, although this movement
                # cannot be possible in move() function
                # i + coordinate[1] < 0 or
                if i + coordinate[1] > 15:
                    return False

                abs_x = j + coordinate[0]
                abs_y = i + coordinate[1]

                # Check if block already exist on that coordinate
                if self.game_state[abs_y][abs_x] == 1 and abs_x >= 0 and abs_y >= 0:
                    return False

        return True

    def move(self):
        if self.current_frame_time < self.next_tick_block_move_time:
            return

        was_key_pressed = False
        pressed_keys = pygame.key.get_pressed()
        temp_cord = self.current_block_cord.copy()
        temp_block = self.current_block
        temp_block_variant = self.current_block_variant
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            was_key_pressed = True
            temp_cord[0] -= 1
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            was_key_pressed = True
            temp_cord[0] += 1
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            was_key_pressed = True
            temp_cord[1] -= 1
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            was_key_pressed = True
            temp_cord[1] += 1

        # rotate left
        if pressed_keys[pygame.K_q]:
            was_key_pressed = True
            temp_block_variant, temp_block = self.get_nth_variant(-1)
        if pressed_keys[pygame.K_e]:
            was_key_pressed = True
            temp_block_variant, temp_block = self.get_nth_variant(1)

        if not was_key_pressed:
            return

        if not self.is_movement_possible(temp_block, temp_cord):
            return

        self.next_tick_block_move_time = (
            self.current_frame_time + self.refresh_block_move_time
        )
        self.current_block_cord = temp_cord
        self.current_block_variant = temp_block_variant
        self.current_block = temp_block

    def print_game_state(self):
        for i in range(NUMBER_OF_ROWS):
            print(self.game_state[i])

    def set_game_state(self):
        for i in range(4):
            for j in range(4):
                if self.current_block[i][j] == 0:
                    continue

                abs_x = j + self.current_block_cord[0]
                abs_y = i + self.current_block_cord[1]
                self.game_state[abs_y][abs_x] = 1

        flag = True
        rows_to_delete = 0
        for row in self.game_state[::-1]:
            for val in row:
                if val == 0:
                    flag = False
            if flag:
                rows_to_delete += 1

            flag = True

        for _ in range(rows_to_delete):
            self.game_state.pop()
            self.game_state.insert(0, [0 for _ in range(NUMBER_OF_COLS)])

        self.set_next_block()

    def draw_game_state(self):
        for i in range(NUMBER_OF_ROWS):
            for j in range(NUMBER_OF_COLS):
                if self.game_state[i][j] == 0:
                    continue

                self.draw_cell_in_grid([j, i], WHITE)

    def down_movement(self):
        if self.current_frame_time < self.next_tick_block_move_down_time:
            return

        temp_cord = self.current_block_cord.copy()
        temp_cord[1] += 1

        if not self.is_movement_possible(self.current_block, temp_cord):
            self.set_game_state()
            return

        self.next_tick_block_move_down_time = self.current_frame_time + (
            1 / self.block_speed
        )
        self.current_block_cord = temp_cord

    def game_loop(self):
        self.render_background_img()
        self.draw_info_screen()

        while self.game_running:
            self.current_frame_time = time.time()
            self.delta_time = self.current_frame_time - self.last_frame_time
            #
            # Set game events
            self.events = pygame.event.get()

            # check exit event
            if self._check_exit():
                break

            self.draw_grid()
            self.draw_fps()
            self.render_current_block()
            self.render_next_block()

            self.move()
            self.down_movement()
            self.draw_game_state()

            pygame.display.update()
            self.last_frame_time = self.current_frame_time
            pygame.time.Clock().tick(FPS_LIMIT)

    def _check_exit(self) -> bool:
        for event in self.events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False


def main():
    game = Game()

    game.game_loop()

    print("Game ended")


if __name__ == "__main__":
    main()
