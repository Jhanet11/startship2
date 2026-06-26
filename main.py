import pygame
import random
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("game/assets/Bullet/bullet_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game/assets/Enemy/enemy_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 3
        self.health = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, screen):
        bar_width = self.rect.width
        bar_height = 6
        fill = (self.health / 5) * bar_width
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.rect.x, self.rect.y - 10, fill, bar_height))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game/assets/Spaceship/spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.can_shoot = True

    def update(self):
        self.handle_input()
        self.clamp()
        self.bullets.update()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed

        click = pygame.mouse.get_pressed()
        if click[0] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
        if not click[0]:
            self.can_shoot = True

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        self.bullets.add(bullet)

    def clamp(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 60, bold=True)
        self.font_btn = pygame.font.SysFont("Arial", 36)
        self.bg = pygame.transform.scale(
            pygame.image.load("game/assets/Other/GameOver.png").convert(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        # Botones
        self.btn_play = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 55)
        self.btn_quit = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 55)

    def draw(self):
        # Fondo
        self.screen.blit(self.bg, (0, 0))

        # Título
        title = self.font_title.render("STARSHIP", True, (255, 255, 255))
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))

        # Botón Jugar
        pygame.draw.rect(self.screen, (0, 180, 0), self.btn_play, border_radius=10)
        txt_play = self.font_btn.render("JUGAR", True, (255, 255, 255))
        self.screen.blit(txt_play, (self.btn_play.centerx - txt_play.get_width() // 2,
                                    self.btn_play.centery - txt_play.get_height() // 2))

        # Botón Salir
        pygame.draw.rect(self.screen, (180, 0, 0), self.btn_quit, border_radius=10)
        txt_quit = self.font_btn.render("SALIR", True, (255, 255, 255))
        self.screen.blit(txt_quit, (self.btn_quit.centerx - txt_quit.get_width() // 2,
                                    self.btn_quit.centery - txt_quit.get_height() // 2))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_play.collidepoint(event.pos):
                    return "play"
                if self.btn_quit.collidepoint(event.pos):
                    return "quit"
        return None

    def run(self):
        while True:
            self.draw()
            action = self.handle_events()
            if action == "play":
                return True   # Iniciar juego
            if action == "quit":
                return False  # Salir


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.spaceship = Spaceship()
        self.enemies = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_delay = 90

    def reset(self):
        # Reinicia el estado del juego
        self.spaceship = Spaceship()
        self.enemies.empty()
        self.spawn_timer = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 0

    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.display.quit()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.spaceship.update()
        self.enemies.update()
        self.spawn_enemy()
        self.check_collisions()

    def spawn_enemy(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            enemy = Enemy()
            self.enemies.add(enemy)
            self.spawn_timer = 0

    def check_collisions(self):
        for enemy in self.enemies:
            hits = pygame.sprite.spritecollide(enemy, self.spaceship.bullets, True)
            for _ in hits:
                enemy.hit()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.spaceship.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)

    while True:
        # Mostrar menú
        menu = Menu(screen)
        if not menu.run():
            break  # Salir si eligió "SALIR"

        # Iniciar juego
        game = Game()
        game.reset()
        game.run()

    pygame.quit()