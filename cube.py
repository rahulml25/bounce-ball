import pygame
import random


class Cube(pygame.sprite.Sprite):
    def __init__(
        self,
        parent_surface: pygame.Surface,
        groups: list[pygame.sprite.Group],
        side: int,
    ) -> None:
        super().__init__(*groups)
        self.display_surface = parent_surface
        self.display_surface_rect = self.display_surface.get_rect()

        self.color = self.random_color()
        self.image = self.generate_cube(side)
        self.rect = self.image.get_rect()

    def random_color(self):
        colors = ["#32a852", "#333fc4", "#de2723", "#d5de23"]
        return random.choice(colors)

    def generate_cube(self, side: int):
        size = (side, side)
        surface = pygame.Surface(size)
        surface.fill(self.color)
        pygame.draw.rect(surface, "black", pygame.Rect(0, 0, *size), 1)
        return surface
