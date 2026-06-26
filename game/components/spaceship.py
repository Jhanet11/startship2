import pygame
from game.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game.components.bullet import Bullet

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("game/assets/Spaceship/spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        
        self.rect.centerx = SCREEN_WIDTH // 3
        self.rect.bottom = SCREEN_HEIGHT - 21
        
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

        if keys[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False
        if not keys[pygame.K_SPACE]:
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