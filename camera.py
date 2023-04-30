import pygame
from level import Level


class Camera(object):
    def __init__(self, width: int, height: int, topleft: tuple):
        self.view_box = pygame.Rect(topleft, (width, height))
        self.offset = pygame.Vector2()
        self.min_offset = (1, 1)
        self.max_offset = (0, 0)
        self.screenwidth = 0
        self.screenheight = 0
        self.out_timer = 0

    def set_bounds(
        self, display_surf: pygame.Surface, level: Level, left: int = 0, top: int = 0
    ):
        self.max_offset = (
            level.width - display_surf.get_width() - 1,
            level.height - display_surf.get_height() - 1,
        )
        self.min_offset = (left, top)

    def restrict_cam(self):
        return pygame.Vector2(
            max(min(self.offset.x, self.max_offset[0]), self.min_offset[0]),
            max(min(self.offset.y, self.max_offset[1]), self.min_offset[1]),
        )

    def center_diff(self, follow: pygame.sprite.Sprite):
        return (
            pygame.Vector2(
                follow.rect.centerx - self.view_box.centerx,
                follow.rect.centery - self.view_box.centery,
            )
            - self.offset
        )

    def get_direction(self, follow: pygame.sprite.Sprite):
        side = [1, 1]
        if follow.rect.centerx < self.view_box.centerx:
            side[0] = -1
        if follow.rect.centery < self.view_box.centery:
            side[1] = -1
        return tuple(side)

    def shift_speed(
        self,
        pos_diff: pygame.Vector2,
        rel_position: tuple,
        x_margin: float,
        y_margin: float,
    ):
        return pygame.Vector2(
            max(abs(pos_diff.x) - (self.view_box.width * 0.5) + x_margin, 0)
            * rel_position[0]
            / self.view_box.topleft[0],
            max(abs(pos_diff.y) - (self.view_box.height * 0.5) + y_margin, 0)
            * rel_position[1]
            / self.view_box.topleft[1],
        )

    def update(
        self,
        follow: pygame.sprite.Sprite,
        max_x: float,
        max_y: float,
        x_margin: float,
        y_margin: float,
        dt: float,
    ):
        if self.view_box.collidepoint(pygame.Vector2(follow.rect.center) - self.offset):
            return
        cam_speed = self.shift_speed(
            self.center_diff(follow), self.get_direction(follow), x_margin, y_margin
        )
        self.offset += pygame.Vector2(
            cam_speed.x * max_x * dt, cam_speed.y * max_y * dt
        )
        self.offset = self.restrict_cam()

    def draw(self, surface: pygame.Surface, level: Level):
        for sprite in level.tiles.sprites():
            sprite.draw(surface, self.offset)
