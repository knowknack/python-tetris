import pygame
pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pause_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# importing a pause menu screen image
pause_menu_screen = pygame.image.load('paused.png').convert_alpha()
pause_menu_screen = pygame.transform.scale(pause_menu_screen, (SCREEN_WIDTH // 2, SCREEN_WIDTH // 2))

# takes the size of the pause menu screen
bg_width, bg_height = pause_menu_screen.get_size()

# getting the x and y coordinates for the pause menu screen
bg_x = (SCREEN_WIDTH - bg_width) // 2
bg_y = (SCREEN_HEIGHT - bg_height) // 2

# creating a transparent background
transparent_background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
transparent_background.fill((32, 32, 32, 128))

# transferring the transparent background and pause menu screen onto the pause screen
pause_screen.blit(transparent_background, (0, 0))
pause_screen.blit(pause_menu_screen, (bg_x, bg_y))

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
        pause_screen.blit(self.image, self.rect)
        pause_screen.blit(self.text, self.text_rect)

    def click(self, position):
        action = False
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0]:
                action = True
        return action


home_button_bg = pygame.draw.rect(pause_screen, (0,0,0), (0, SCREEN_HEIGHT - 70, 70, 70))
resume_button_bg = pygame.draw.rect(pause_screen, (0,0,0), (0, 0, 70, 70))
restart_button_bg = pygame.draw.rect(pause_screen, (0,0,0), (SCREEN_WIDTH - 70, 0, 70, 70))
settings_button_bg = pygame.draw.rect(pause_screen, (0,0,0), (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 70, 70 ,70))


home_button_surf = pygame.image.load("home_button.png").convert_alpha()
home_button_surf = pygame.transform.scale(home_button_surf, (75, 75))

resume_button_surf = pygame.image.load("resume_button.png").convert_alpha()
resume_button_surf = pygame.transform.scale(resume_button_surf, (75, 75))

restart_button_surf = pygame.image.load("restart_button.png").convert_alpha()
restart_button_surf = pygame.transform.scale(restart_button_surf, (75, 75))

settings_button_surf = pygame.image.load("settings_button.png").convert_alpha()
settings_button_surf = pygame.transform.scale(settings_button_surf, (75, 75))


p_home_button = Button(home_button_surf, 75/2, SCREEN_HEIGHT - 75/2, "")
p_resume_button = Button(resume_button_surf, 75/2, 75/2, "")
p_restart_button = Button(restart_button_surf, SCREEN_WIDTH - 75/2, 75/2, "")
p_settings_button = Button(settings_button_surf, SCREEN_WIDTH - 75/2, SCREEN_HEIGHT - 75/2, "")


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
