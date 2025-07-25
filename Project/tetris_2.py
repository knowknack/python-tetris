import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GRID_BLOCK_SIZE = 40


# pygame setup
pygame.init()
screen = pygame.display.set_mode((480, 360))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # # poll for events
    # # pygame.QUIT event means the user clicked X to close your window

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    events = pygame.event.get()

    # # fill the screen with a color to wipe away anything from last frame
    # screen.fill("purple")

    # pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        print("hello")
        # print(keys[pygame.K_w])

    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    # dt = clock.tick(60) / 1000
    dt = clock.tick(0.3) / 1000

pygame.quit()
