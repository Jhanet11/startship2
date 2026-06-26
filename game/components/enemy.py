import pygame
import random
from game.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game/assets/Enemy/enemy_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        
        # Aparece en posición X aleatoria en la parte superior
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        
        self.speed = 3
        self.health = 5  # 5 disparos para morir

    def update(self):
        self.rect.y += self.speed
        # Si sale por abajo de la pantalla, se elimina
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True  # Murió
        return False  # Sigue vivo

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        # Barra de vida encima del enemigo
        bar_width = self.rect.width
        bar_height = 6
        fill = (self.health / 5) * bar_width
        
        # Fondo rojo
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        # Vida restante en verde
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.rect.x, self.rect.y - 10, fill, bar_height))