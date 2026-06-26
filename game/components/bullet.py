import pygame
from game.utils.constants import SCREEN_HEIGHT

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
        self.rect.y -= self.speed  # Sube hacia arriba
        # Si sale de la pantalla, se elimina
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)