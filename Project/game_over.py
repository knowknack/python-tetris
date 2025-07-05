import pygame
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

game_over_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_over_screen_bg = pygame.image.load("game_over.png").convert()
game_over_screen.blit(game_over_screen_bg, (0, 0))

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
        game_over_screen.blit(self.image, self.rect)
        game_over_screen.blit(self.text, self.text_rect)

    def click(self, position):
        action = False
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0]:
                action = True
                print("button clicked")
        return action

home_button_bg = pygame.draw.rect(game_over_screen, (0,0,0), (SCREEN_WIDTH // 2 + 35, SCREEN_HEIGHT //2 + 200, 70, 70))
restart_button_bg = pygame.draw.rect(game_over_screen, (0,0,0), (SCREEN_WIDTH // 2 - 105, SCREEN_HEIGHT // 2 + 200, 70, 70))

home_button_surf = pygame.image.load("home_button.png").convert_alpha()
home_button_surf = pygame.transform.scale(home_button_surf, (75, 75))

restart_button_surf = pygame.image.load("restart_button.png").convert_alpha()
restart_button_surf = pygame.transform.scale(restart_button_surf, (75, 75))

g_home_button = Button(home_button_surf, SCREEN_WIDTH // 2 + 70, SCREEN_HEIGHT //2 + 235, "")
g_restart_button = Button(restart_button_surf, SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 + 235, "")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if g_home_button.click(pygame.mouse.get_pos()) == True:
                print("Home button clicked")
            if g_restart_button.click(pygame.mouse.get_pos()) == True:
                print("Restart button clicked")

    g_home_button.update()
    g_restart_button.update()

    pygame.display.update()
