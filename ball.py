import pygame
import random


class Ball(pygame.sprite.Sprite):
    def __init__(
        self,
        parent_surface: pygame.Surface,
        group: pygame.sprite.Group,
        radius: int,
        max_ball_height: int,
    ) -> None:
        super().__init__(group)
        self.display_surface = parent_surface
        self.display_surface_rect = self.display_surface.get_rect()

        self.color = (255, 255, 255)
        self.image = self.generate_ball(radius)
        self.rect = self.image.get_rect(
            top=random.randint(
                max_ball_height + 10,
                (self.display_surface_rect.h - 40) - 150,
            ),
            left=random.randint(
                10,
                self.display_surface_rect.w - (2 * radius) - 10,
            ),
        )

        self.direction = pygame.Vector2(-1, +1)
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 160

    def generate_ball(self, radius: int):
        surface = pygame.Surface(
            (2 * radius, 2 * radius),
            pygame.SRCALPHA,
            32,
        ).convert_alpha()
        pygame.draw.circle(surface, self.color, surface.get_rect().center, radius)
        return surface

    def reset(self, max_ball_height: int):
        self.rect.top = random.randint(
            max_ball_height + 10,
            (self.display_surface_rect.h - 40) - 150,
        )
        self.rect.left = random.randint(
            10,
            self.display_surface_rect.w - self.rect.w - 10,
        )
        self.pos = pygame.Vector2(self.rect.center)

    def collision(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction.x = +1

        elif self.rect.right > self.display_surface_rect.w:
            self.rect.right = self.display_surface_rect.w
            self.direction.x = -1

        if self.rect.top < 0:
            self.rect.top = 0
            self.direction.y = +1

    def move(self, dt: float):
        # normlizing a vector
        if self.direction.magnitude():
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)

        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = round(self.pos.y)

        self.collision()

    def update(self, dt: float) -> None:
        self.move(dt)
