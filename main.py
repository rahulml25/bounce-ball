import pygame
import sys
from utils import resource_path

from bouncer import Bouncer
from ball import Ball
from cube import Cube


class Game:
    def __init__(self, title, size: tuple[int, int] = (800, 500)) -> None:
        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_icon(pygame.image.load(resource_path("image/icon.ico")))
        self.surface = pygame.display.set_mode(size)
        self.surface_rect = self.surface.get_rect()

        self.gap = 3
        self.score = 0
        self.gameover = False

        self.score_surface = pygame.Surface((self.surface_rect.w, 60 - self.gap))
        self.score_surface_rect = self.score_surface.get_rect()

        self.game_surface = pygame.Surface(
            (
                self.surface_rect.w,
                self.surface_rect.h - self.score_surface_rect.h + self.gap,
            )
        )
        self.game_surface_rect = self.game_surface.get_rect()

        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()

        self.bouncer = Bouncer(self.game_surface, self.all_sprites, (120, 16))

        self.cubes = pygame.sprite.Group()
        max_ball_height = self.generate_cubes(50)

        self.ball = Ball(self.game_surface, self.all_sprites, 10, max_ball_height)

    def generate_cubes(self, count: int):
        cube_side = 40
        limit = self.surface_rect.w / cube_side

        done = 0
        phase = 0
        item = 0

        while done < count:
            if item > limit:
                item = 0
                phase += 1

            cube = Cube(self.game_surface, [self.all_sprites, self.cubes], cube_side)
            cube.rect.left = item * cube_side
            cube.rect.top = phase * cube_side

            done += 1
            item += 1

        return (phase + 1) * cube_side

    def ball_collisions(self):
        # bouncer_collision
        if pygame.sprite.collide_rect(self.ball, self.bouncer):
            self.ball.direction.y = -1
        elif self.ball.rect.top == self.game_surface_rect.h:
            self.gameover = True

        # cubes_collision
        for cube in self.cubes.sprites():
            cube: Cube = cube
            if not cube.alive():
                continue
            if pygame.sprite.collide_rect(self.ball, cube):
                cube.kill()
                self.score += 1

                mod = lambda x: x if x > 0 else x * -1
                sides = {
                    "top": self.ball.rect.top - cube.rect.bottom,
                    "buttom": self.ball.rect.bottom - cube.rect.top,
                    "left": self.ball.rect.left - cube.rect.right,
                    "right": self.ball.rect.right - cube.rect.left,
                }

                lowest = {"side": "top", "dist": mod(sides["top"])}

                for side, dist in sides.items():
                    if lowest["dist"] > mod(dist):
                        lowest["side"] = side
                        lowest["dist"] = mod(dist)

                match lowest["side"]:
                    case "top":
                        self.ball.direction.y = +1
                    case "buttom":
                        self.ball.direction.y = -1
                    case "left":
                        self.ball.direction.x = +1
                    case "right":
                        self.ball.direction.x = -1

    def reset(self):
        self.score = 0
        self.bouncer.rect.centerx = self.surface_rect.centerx

        for sprite in self.cubes.sprites():
            sprite.kill()
        max_ball_height = self.generate_cubes(50)

        self.ball.reset(max_ball_height)

    def show_scores(self):
        font = pygame.font.Font(resource_path("font/LycheeSoda.ttf"), 47)
        score_surface = font.render(f"Score: {self.score}", True, "white")
        self.score_surface.blit(
            score_surface,
            score_surface.get_rect(center=self.score_surface_rect.center),
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            if not self.gameover:
                self.play(dt)
            else:
                self.game_over()

            pygame.display.update()

    def game_over(self):
        gameover_surface = pygame.Surface((400, 240), pygame.SRCALPHA, 32)
        gameover_surface_rect = gameover_surface.get_rect(
            center=self.surface_rect.center
        )

        pygame.draw.rect(
            gameover_surface,
            "yellow",
            (0, 0, *gameover_surface_rect.size),
            border_radius=15,
        )

        pygame.draw.rect(
            gameover_surface,
            "#f5a802",
            (0, 0, *gameover_surface_rect.size),
            width=4,
            border_radius=15,
        )

        font = pygame.font.Font(resource_path("font/LycheeSoda.ttf"), 56)
        title_surface = font.render("GAME OVER", True, "#07b007")
        gameover_surface.blit(
            title_surface,
            title_surface.get_rect(
                centerx=gameover_surface_rect.w // 2,
                centery=(gameover_surface_rect.h // 2) - 25,
            ),
        )

        font = pygame.font.Font(resource_path("font/LycheeSoda.ttf"), 47)
        score_surface = font.render(f"Score: {self.score}", True, "blue")
        gameover_surface.blit(
            score_surface,
            score_surface.get_rect(
                centerx=gameover_surface_rect.w // 2,
                centery=(gameover_surface_rect.h // 2) + 25,
            ),
        )

        self.surface.blit(gameover_surface, gameover_surface_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.gameover = False
            self.reset()

    def play(self, dt: float):
        self.surface.fill("white")

        self.surface.blits(
            [
                (self.score_surface, (0, 0)),
                (self.game_surface, (0, self.score_surface_rect.h + self.gap)),
            ]
        )

        self.score_surface.fill("#0b9104")
        self.show_scores()

        self.game_surface.fill("black")
        self.all_sprites.draw(self.game_surface)
        self.all_sprites.update(dt)
        self.ball_collisions()


if __name__ == "__main__":
    game = Game("Bounce Ball")
    game.run()
