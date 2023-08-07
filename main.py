import pygame
import time
import os
from sys import exit
from player import Player
from animator import Animator
from level import Level
from fx import create_shadow
from hash_map import Hash_Map
from camera import Camera

WIDTH = 1280
HEIGHT = 720

PALLETTE = {
    "black": (0, 0, 0),
    "dark-blue": (29, 43, 83),
    "dark-purple": (126, 37, 83),
    "dark-green": (0, 135, 81),
    "brown": (171, 82, 54),
    "dark-grey": (95, 87, 79),
    "light-grey": (194, 195, 199),
    "white": (255, 241, 232),
    "red": (255, 0, 77),
    "orange": (255, 163, 0),
    "yellow": (255, 236, 39),
    "green": (0, 22, 54),
    "blue": (41, 173, 255),
    "lavender": (131, 118, 156),
    "pink": (255, 119, 168),
    "light-peach": (255, 204, 170),
}

"""------------- Main -------------"""


def main():
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Platformer Test")
    clock = pygame.time.Clock()

    test_surface = pygame.Surface((320, 180))

    player_scale = 1
    player_animator = Animator(100)
    player_animator.init_state("Idle", "Triangle_Man_Sprites.png", 0, 8, 18, 16, 17)
    player_animator.init_state("Run", "Triangle_Man_Sprites.png", 0, 0, 8, 16, 17)
    player_animator.init_state(
        "Transition", "Triangle_Man_Sprites.png", 0, 22, 23, 16, 17
    )
    player_animator.init_state("Jump", "Triangle_Man_Sprites.png", 0, 18, 21, 16, 17)
    player_animator.init_state("Land", "Triangle_Man_Sprites.png", 0, 21, 22, 16, 17)
    p1 = Player((0, 0), 12, 14, player_animator, "Idle")
    p1.animator.current_state = "Idle"
    p1.animator.last_state = "Idle"
    p1.animator.requested_state = ["Idle", False, 0, 0, []]

    test_map = Hash_Map(32, 1920)
    test_level = Level(test_map)
    test_level.load_level("Level_Files/testing_room.tmj")
    camera = Camera(320, 180)

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

        p1.update(dt, 400, test_level.get_nearest_colliders(camera.view_box))
        camera.draw(display, p1.position, test_level, p1, 3)

        pygame.display.update()


"""------------- Main -------------"""

if __name__ == "__main__":
    main()
    pygame.quit()
    exit()
