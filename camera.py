import pygame
from level import Level
from general_funcs import *


class Camera(object):
    def __init__(self, view_width: int, view_height: int, up_scale_level: int = 1):
        self.view_box = pygame.Rect((0, 0), (view_width, view_height))
        self.target_box = pygame.Rect(75, 90, 140, 30)
        self.offset = pygame.Vector2()

    def find_active(self, target: tuple, level: Level):
        self.view_box.center = (
            limit_range(
                target[0],
                level.width - (self.view_box.width * 0.5),
                self.view_box.width * 0.5,
            ),
            limit_range(
                target[1],
                level.height - (self.view_box.height * 0.5),
                self.view_box.height * 0.5,
            ),
        )
        return level.get_active_tiles(self.view_box)

    def draw_level(self, target: tuple, level: Level):
        level_surf = pygame.Surface((level.width, level.height))
        level_surf.set_colorkey((0, 0, 0))
        for tile in self.find_active(target, level)[0]:
            level_surf.blit(tile.image, tile.rect.topleft)
        return level_surf


    def draw_upscaled(
        self,
        surface: pygame.Surface,
        image: pygame.Surface,
        original_position: pygame.Vector2,
        up_scale_level: int,
    ):
        surface.blit(
            pygame.transform.scale(
                image,
                (
                    image.get_width() * up_scale_level,
                    image.get_height() * up_scale_level,
                ),
            ),
            (original_position - self.offset) * up_scale_level,
        )



