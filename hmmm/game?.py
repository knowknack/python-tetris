import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.player_velocity = pygame.math.Vector2(0, 0)

        self.player_speed = 250
        self.gravity_strength = 1500
        self.jump_strength = 400

    def possible_move(self):
        pass

    def movement(self, dt):

        # left-right movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_velocity.x = -self.player_speed
        if keys[pygame.K_d]:
            self.player_velocity.x = self.player_speed

        # # jump
        if keys[pygame.K_SPACE]:
            self.player_velocity.y = self.jump_strength

        # gravity
        self.player_velocity.y -= self.gravity_strength * dt

        move_dist_x = self.player_velocity.x * dt
        move_dist_y = self.player_velocity.y * dt

        self.rect.y -= move_dist_y
        self.rect.x += move_dist_x

        self.player_velocity.x = 0


    def update(self, dt):
        self.movement(dt)


class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.border_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = Player(self.all_sprites)
        self.game_running = True

    def background(self):
        self.game_bg = pygame.image.load("background.png").convert()
        self.game_bg = pygame.transform.scale(
            self.game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.screen.blit(self.game_bg, (0, 0))

    # def sprites(self):

    def run(self):
        while self.game_running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

            self.background()
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Game")

    game = Game()
    game.run()
