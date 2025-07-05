from pygame.surface import Surface
from typing import List
import pygame
import random
from shapes import SHAPES, NUMBER_OF_SHAPES

GAME_STATE_RUNNING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_MAIN_MENU = 3
GAME_STATE_SETTINGS = 4
GAME_STATE_QUIT = 0

## COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


DEFAULT_BLOCK_DIMENSION = 35
DEFAULT_ROWS = 18
DEFAULT_COLUMNS = 9
DEFAULT_REFRESH_MOVE_TIME = 0.1
DEFAULT_REFRESH_DROP_TIME = 0.5
DEFAULT_REFRESH_ROTATE_TIME = 0.15

GRID = [[0 for _ in range(DEFAULT_COLUMNS)] for _ in range(DEFAULT_ROWS)]


class Time:
    current_time = 0.0

    def __init__(self, refresh_time: float):
        self.refresh_time = refresh_time
        self.next_available_time = 0

    @staticmethod
    def update():
        Time.current_time = pygame.time.get_ticks() / 1000

    def consume_time(self):
        self.next_available_time = Time.current_time + self.refresh_time

    def is_possible(self):
        return Time.current_time >= self.next_available_time


class Screen:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Mouse:
    mouse_position = [0, 0]
    was_clicked = False

    @staticmethod
    def update():
        Mouse.mouse_position = pygame.mouse.get_pos()
        Mouse.was_clicked = pygame.mouse.get_pressed()[0]


class Button:
    def __init__(self, image, x, y, text_input):
        Mouse.update()
        self.active = True
        self.button_font = pygame.font.SysFont("Arial", 30)
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        self.text = self.button_font.render(text_input, True, "grey")
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def update(self):
        if not self.active:
            return

        Screen.screen.blit(self.image, self.rect)
        Screen.screen.blit(self.text, self.text_rect)

        if self.is_mouse_inside_button():
            self.text = self.button_font.render(self.text_input, True, (75, 230, 75))
        else:
            self.text = self.button_font.render(self.text_input, True, "white")

    def was_click(self) -> bool:
        if not self.active:
            return False

        if not self.rect.collidepoint(Mouse.mouse_position):
            return False

        return Mouse.was_clicked

    def is_mouse_inside_button(self) -> bool:
        return self.rect.collidepoint(Mouse.mouse_position)

    def disable(self):
        self.active = False

    def enable(self):
        self.active = True


class Game:
    def __init__(self):
        image = pygame.image.load("map1.jpg").convert()
        self.background = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        image = pygame.image.load("menu_background.jpeg").convert()
        self.menu_background = pygame.transform.scale(
            image, (SCREEN_WIDTH, SCREEN_HEIGHT + 30)
        )

        image = pygame.image.load("button.png").convert_alpha()
        button_size = pygame.transform.scale(image, (300, 75))
        self.start_button = Button(button_size, SCREEN_WIDTH // 2, 300, "Start")
        self.settings_button = Button(
            button_size, SCREEN_WIDTH // 2, 400, "Settings"
        )
        self.quit_button = Button(button_size, SCREEN_WIDTH // 2, 500, "Quit")

        self.actual_game = ActualGame(self.background)

        self.game_state = GAME_STATE_MAIN_MENU
        self.events = pygame.event.get()

    def check_exit(self) -> bool:
        for event in self.events:
            if event.type == pygame.QUIT:
                return True
        return False

    def game_loop(self):
        while True:
            self.events = pygame.event.get()
            Time.update()
            Mouse.update()

            if GAME_STATE_MAIN_MENU == self.game_state:
                self.main_menu_handler()
            elif GAME_STATE_RUNNING == self.game_state:
                self.actual_game.update()
                pass
            elif GAME_STATE_QUIT == self.game_state:
                break
            else:
                print("Game state", self.game_state)
                raise Exception("Invalid game state")

            if self.check_exit():
                break

            pygame.display.update()

    def main_menu_handler(self):
        Screen.screen.blit(self.menu_background, (0, 0))
        self.start_button.update()
        self.settings_button.update()
        self.quit_button.update()

        if self.start_button.was_click():
            print("Start button clicked")
            self.setup_game_start()
        elif self.settings_button.was_click():
            print("Settings button clicked")
        elif self.quit_button.was_click():
            self.game_state = GAME_STATE_QUIT

    def setup_main_menu(self):
        self.game_state = GAME_STATE_MAIN_MENU

    def setup_game_start(self):
        self.start_button.disable()
        self.settings_button.disable()
        self.quit_button.disable()
        self.actual_game.setup()
        self.game_state = GAME_STATE_RUNNING


class ActualGame:
    def __init__(
        self,
        background: Surface,
        rows=DEFAULT_ROWS,
        columns=DEFAULT_COLUMNS,
        block_dimension=DEFAULT_BLOCK_DIMENSION,
    ) -> None:
        self.background = background
        self.columns = columns
        self.rows = rows
        self.block_dimension = block_dimension

        image = pygame.image.load("tetris_logo.png").convert_alpha()
        self.tetris_logo = pygame.transform.scale(
            image, (self.block_dimension * 5, self.block_dimension * 4)
        )

        self.width_offset = (SCREEN_WIDTH - (self.columns * self.block_dimension)) // 2
        self.height_offset = (SCREEN_HEIGHT - (self.rows * self.block_dimension)) // 2

        self.info_1_x_offset = self.width_offset - (6 * self.block_dimension)
        self.info_2_x_offset = (
            self.width_offset + (self.columns + 1) * self.block_dimension
        )

        self.GRID_BACKGROUND = pygame.Surface(
            (
                SCREEN_WIDTH - self.width_offset * 2,
                SCREEN_HEIGHT - self.height_offset * 2,
            )
        )

        self.block_start_cord = [
            self.columns // 2 - 1,
            -4,  ## Start from off screen from above
        ]

        self.current_block_index, self.current_block_variant, self.current_block = (
            get_random_shape()
        )
        self.next_block_index, self.next_block_variant, self.next_block = (
            get_random_shape()
        )

        self.current_block_cord = self.block_start_cord.copy()
        self.down_movement_time = Time(DEFAULT_REFRESH_DROP_TIME)

    def setup(self):
        self.reset()
        Screen.screen.blit(self.background, (0, 0))

    def reset(self):
        pass

    def draw_grid(self):
        Screen.screen.blit(
            self.GRID_BACKGROUND, (self.width_offset, self.height_offset)
        )

        gap = 0
        for _ in range(self.columns + 1):
            pygame.draw.line(
                Screen.screen,
                "grey",
                (self.width_offset + gap, self.height_offset),
                (self.width_offset + gap, SCREEN_HEIGHT - self.height_offset),
            )
            gap += self.block_dimension

        gap = 0
        for _ in range(self.rows + 1):
            pygame.draw.line(
                Screen.screen,
                "grey",
                (self.width_offset, self.height_offset + gap),
                (SCREEN_WIDTH - self.width_offset, self.height_offset + gap),
            )
            gap += self.block_dimension

    def draw_next_shape(self):
        pygame.draw.rect(
            Screen.screen,
            (25, 25, 25),
            (
                self.info_2_x_offset,
                self.height_offset,
                self.block_dimension * 6,
                self.block_dimension * 6,
            ),
        )

    def draw_info(self):
        Screen.screen.blit(
            self.tetris_logo,
            (
                self.info_1_x_offset,
                self.height_offset,
            ),
        )

        pygame.draw.rect(
            Screen.screen,
            (25, 25, 25),
            (
                self.info_1_x_offset,
                self.height_offset + self.block_dimension * 3.5,
                self.block_dimension * 5,
                self.block_dimension * self.rows - self.block_dimension * 4,
            ),
        )

        current_time = 0
        create_text(
            "Arial",
            15,
            "Seconds Spent: " + str(int(current_time)),
            "green",
            (
                self.info_1_x_offset + 10,
                self.height_offset * 4,
            ),
        )

        current_score = 0
        create_text(
            "Arial",
            15,
            "Current Score: " + str(int(current_score)),
            "white",
            (
                self.info_1_x_offset + 10,
                self.height_offset * 5,
            ),
        )

        clock = pygame.time.Clock()
        create_text(
            "Arial",
            15,
            "FPS counter: " + str(int(clock.get_fps())),
            # "FPS counter: " + str(fps),
            "white",
            (
                self.info_1_x_offset + 10,
                self.height_offset * 6,
            ),
        )

    def set_next_block(self):
        self.current_block_index = self.next_block_index
        self.current_block_variant = self.next_block_variant
        self.current_block = self.next_block
        self.current_block_cord = self.block_start_cord.copy()

        self.next_block_index, self.next_block_variant, self.next_block = (
            get_random_shape()
        )

    def draw_cell(self, coordinate: List[int], color=RED):
        pygame.draw.rect(
            Screen.screen,
            color,
            (
                coordinate[0],
                coordinate[1],
                self.block_dimension,
                self.block_dimension,
            ),
        )

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

    def draw_cell_in_grid(self, coordinate: List[int], color=RED) -> bool:
        if coordinate[0] < 0:
            return False
        if coordinate[0] >= self.columns:
            return False

        if coordinate[1] < 0:
            return False
        if coordinate[1] >= self.rows:
            return False

        draw_cord = [
            self.width_offset + coordinate[0] * self.block_dimension,
            self.height_offset + coordinate[1] * self.block_dimension,
        ]
        self.draw_cell(draw_cord, color)
        return True

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
                if i + coordinate[1] > self.rows:
                    return False

                # abs_x = j + coordinate[0]
                # abs_y = i + coordinate[1]

                # # Check if block already exist on that coordinate
                # if self.game_state[abs_y][abs_x] == 1 and abs_x >= 0 and abs_y >= 0:
                #     return False

        return True

    def check_pos(self,shape, coordinate):
        for i in range(4):
            for j in range(4):
                if shape[i][j] == 0:
                    continue
                abs_x = coordinate[0] + j
                abs_y = coordinate[1] + i
                if abs_x < 0 or abs_x >= DEFAULT_COLUMNS:
                    return False
                if abs_y >= DEFAULT_ROWS:
                    return False
                if abs_y > 0 and 1 == GRID[abs_y][abs_x]:
                    return False

        return True

    def movement(self):
        temp_cord = self.current_block_cord.copy()
        if pygame.key.get_pressed()[pygame.K_s]:
            temp_cord[1] += 1
            was_button_pressed = True
        if pygame.key.get_pressed()[pygame.K_a]:
            temp_cord[0] -= 1
            was_button_pressed = True
        if pygame.key.get_pressed()[pygame.K_d]:
            temp_cord[0] += 1
            was_button_pressed = True

    def down_movement(self):
        if not self.down_movement_time.is_possible():
            return

        temp_cord = self.current_block_cord.copy()
        temp_cord[1] += 1

        if not self.is_movement_possible(self.current_block, temp_cord):
            # self.set_game_state()
            return

        self.down_movement_time.consume_time()
        self.current_block_cord = temp_cord

    def update(self):
        self.draw_grid()
        self.draw_info()
        self.draw_next_shape()
        self.draw_info()

        self.down_movement()

        self.render_current_block()


def create_text(font_name, font_size, text, color, surface_size):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, color)
    Screen.screen.blit(text_surface, surface_size)


def get_random_shape():
    shape_index = random.randint(0, NUMBER_OF_SHAPES - 1)
    variant_index = random.randint(0, len(SHAPES[shape_index]) - 1)
    return shape_index, variant_index, SHAPES[shape_index][variant_index]


if __name__ == "__main__":
    pygame.init()
    Game().game_loop()
    pygame.quit()
