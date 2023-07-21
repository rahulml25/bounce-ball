import pygame


class Bouncer(pygame.sprite.Sprite):
    def __init__(
        self,
        parent_surface: pygame.Surface,
        group: pygame.sprite.Group,
        size: tuple[int, int],
    ) -> None:
        super().__init__(group)
        self.display_surface = parent_surface
        self.display_surface_rect = self.display_surface.get_rect()

        self.color = (255, 255, 255)
        self.image = self.generate_bouncer(size)
        self.rect = self.image.get_rect(
            bottom=self.display_surface_rect.h,
            centerx=int(self.display_surface_rect.w / 2),
        )

        self.direction = pygame.Vector2()
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 200

    def generate_bouncer(self, size: tuple[int, int]):
        surface = pygame.Surface(size)
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(0, 0, *size),
            border_radius=2,
        )
        return surface

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            self.direction.x = 0

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1

        elif keys[pygame.K_RIGHT]:
            self.direction.x = +1

        else:
            self.direction.x = 0

    def collision(self):
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos = pygame.Vector2(self.rect.center)

        elif self.rect.right > self.display_surface_rect.w:
            self.rect.right = self.display_surface_rect.w
            self.pos = pygame.Vector2(self.rect.center)

    def move(self, dt: float):
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        self.collision()

    def update(self, dt: float) -> None:
        self.input()
        self.move(dt)
