import pygame
import time
import os
from sys import exit
from player import Player
from animator import Animator
from level import Level
from camera import Camera

WIDTH = 1920
HEIGHT = 768


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, position: pygame.Vector2, width: int, height: int, color: tuple, *groups
    ):
        super().__init__(*groups)
        self.position = position
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position


"""------------- Main -------------"""


def main():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Test")
    clock = pygame.time.Clock()

    player_scale = 4.5
    player_animator = Animator(100)
    player_animator.init_state(
        "Idle", "Triangle_Man_Sprites.png", 0, 8, 18, 16, 17, player_scale
    )
    player_animator.init_state(
        "Run", "Triangle_Man_Sprites.png", 0, 0, 8, 16, 17, player_scale
    )
    player_animator.init_state(
        "Transition", "Triangle_Man_Sprites.png", 0, 22, 23, 16, 17, player_scale
    )
    player_animator.init_state(
        "Jump", "Triangle_Man_Sprites.png", 0, 18, 21, 16, 17, player_scale
    )
    player_animator.init_state(
        "Land", "Triangle_Man_Sprites.png", 0, 21, 22, 16, 17, player_scale
    )
    p1 = Player((300, 150), (12, 13), (16, 17), player_scale, player_animator, "Idle")
    p1.animator.current_state = "Idle"
    p1.animator.last_state = "Idle"
    p1.animator.requested_state = ["Idle", False, 0, 0, []]

    test_level = Level()
    test_level.load_level("Level_Files/testing_room.tmj", 4.5)
    tc = Camera(800, 400, (560, 184))
    tc.set_bounds(display, test_level)

    last_time = time.time()

    while True:
        dt = time.time() - last_time
        last_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        display.fill((255, 241, 232))

        p1.update(dt, 400, test_level.colliders)
        p1.draw(display, tc.offset)
        tc.update(p1, p1.max_speed, p1.max_fall, 300, 30, dt)
        tc.draw(display, test_level)
        pygame.draw.rect(display, (255, 0, 0), tc.view_box, 3)

        pygame.display.update()


"""------------- Main -------------"""

if __name__ == "__main__":
    main()
    pygame.quit()
    exit()
    # print(os.path.relpath("Level_Files/testing_room.tmj", start=os.curdir))
