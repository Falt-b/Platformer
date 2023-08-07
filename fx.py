import pygame
from general_funcs import *


def create_shadow(surface: pygame.Surface, shadow_color: tuple, shadow_scale: float):
    shadow_surf = pygame.mask.from_surface(surface).to_surface(setcolor=shadow_color)
    shadow_surf = pygame.transform.scale(
        shadow_surf,
        (
            int(surface.get_width() * shadow_scale),
            int(surface.get_height() * shadow_scale),
        ),
    )
    shadow_surf.set_colorkey((0, 0, 0))
    return shadow_surf


def create_outline(surface: pygame.Surface, outline_color: tuple, thickness: int):
    pass
