import pygame
from animator import Animator
from collider import Collider
from general_funcs import limit_range, map_range
from fx import create_shadow


class Player(Collider):
    def __init__(
        self,
        position: pygame.Vector2,
        width: int,
        height: int,
        animator: Animator,
        start_state: str,
        *groups
    ):
        super().__init__(position, width, height, *groups)
        self.image = animator.animation_index[start_state][0]
        self.rect = pygame.Rect(position, (width, height))
        self.shadow_offset = pygame.Vector2(4, -2)

        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()
        self.accel = 0
        self.direction = pygame.Vector2()
        self.last_input = pygame.Vector2()
        self.jump_released = True

        self.max_speed = 62.5
        self.max_fall = 250
        self.jump_force = -100
        self.gravity_mul = 1

        self.air_time = 0
        self.on_ground = False
        self.has_jump = False

        self.animator = animator
        self.flipped = False
        self.last_state = None

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1

    def x_movement(self, dt: float):
        if self.direction.x == 0:
            self.accel = 0
        if self.last_input.x == -self.direction.x:
            self.accel = 0
        self.accel += abs(self.direction.x) * 10 * dt
        self.accel = limit_range(self.accel, 1, 0)
        self.velocity.x = self.accel * self.max_speed * self.direction.x

    def apply_gravity(
        self, dt: float, gravity: float, max_fall: float, gravity_mul: float
    ):
        self.velocity.y += gravity * gravity_mul * dt
        self.velocity.y = min(self.velocity.y, max_fall)

    def y_movement(self, dt: float):
        if self.direction.y == -1 and self.has_jump and self.jump_released:
            self.velocity.y = self.jump_force
            self.has_jump = False
            self.on_ground = False
            self.jump_released = False
            self.gravity_mul = 0.25
        if not self.jump_released and self.direction.y != -1:
            self.gravity_mul = 0.75
            self.jump_released = True
        if self.velocity.y > 0:
            self.gravity_mul = 1.75

    def handle_collisions(
        self, dt: float, colliders: list[pygame.sprite.Sprite], tolerance: float
    ):
        collision_types = self.check_collisions(dt, colliders)
        if collision_types[1]:
            self.on_ground = True
            self.has_jump = True
            self.velocity.y = 0
            self.position.y = self.rect.y + tolerance
            self.air_time = 0
        else:
            self.air_time += 1
        if self.air_time > 6:
            self.on_ground = False
            self.has_jump = False
        if collision_types[0]:
            self.velocity.y = 0
            self.position.y = self.rect.y
        if collision_types[2] or collision_types[3]:
            self.position.x = self.rect.x + (tolerance * self.direction.x)

    def set_animation(self):
        if self.velocity.x == 0 and self.on_ground:
            self.animator.request_state("Idle", False, 0, 0, [])
        if self.velocity.x != 0 and self.on_ground:
            self.animator.request_state("Run", False, 0, 0, [])
        if not self.on_ground:
            self.animator.request_state(
                "Jump",
                True,
                min(
                    round(
                        map_range(self.velocity.y, self.max_fall, self.jump_force, 3)
                    ),
                    2,
                ),
                1,
                [],
            )
        if self.last_state == "Jump" and self.animator.requested_state[0] != "Jump":
            self.animator.request_state("Land", True, 0, 1, ["Idle", "Transition"])
        if (
            self.last_state != "Transition"
            and self.last_state != "Idle"
            and self.animator.requested_state[0] == "Idle"
        ):
            self.animator.request_state("Transition", True, 0, 3, ["Idle"])
        if self.velocity.x < 0:
            self.flipped = True
        if self.velocity.x > 0:
            self.flipped = False

    def update(self, dt: float, gravity: float, colliders: list[pygame.sprite.Sprite]):
        self.get_input()
        self.x_movement(dt)
        self.apply_gravity(dt, gravity, self.max_fall, self.gravity_mul)
        self.y_movement(dt)
        self.handle_collisions(dt, colliders, 0.25)
        self.set_animation()
        self.last_state = self.animator.update_frame()
        self.image = self.animator.get_frame()

    def draw(
        self,
        surface: pygame.Surface,
        offset: pygame.Vector2,
        shadow_color: tuple = (1, 1, 1),
        shadow: bool = False,
    ):
        p_img = pygame.transform.flip(self.image, self.flipped, False)
        img_pos = (
            pygame.Vector2(
                self.position.x - (p_img.get_width() - self.rect.width) * 0.5,
                self.position.y - (p_img.get_height() - self.rect.height),
            )
            - offset
        )
        if shadow:
            surface.blit(
                create_shadow(p_img, shadow_color, 1),
                (
                    round(img_pos.x - self.shadow_offset.x),
                    round(img_pos.y - self.shadow_offset.y),
                ),
            )
        surface.blit(p_img, (round(img_pos.x), round(img_pos.y)))
