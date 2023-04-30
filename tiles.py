import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        position: pygame.Vector2,
        img: pygame.Surface,
        width: int,
        height: int,
        scale: int,
        movable: bool = False,
        *groups
    ):
        super().__init__(*groups)
        self.scale = scale
        self.rect = pygame.Rect(position, (width * self.scale, height * self.scale))
        self.image = img
        self.position = position

    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.topleft - offset)
