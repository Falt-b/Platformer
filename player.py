import pygame
from animator import Animator


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        position: pygame.Vector2,
        player_size: tuple,
        img_size: tuple,
        scale: int,
        animator: Animator,
        start_state: str,
        *groups
    ):
        self.scale = scale
        self.player_size = (player_size[0] * self.scale, player_size[1] * self.scale)
        self.img_size = (img_size[0] * self.scale, img_size[1] * self.scale)
        self.img = animator.animation_index[start_state][0]
        self.rect = pygame.Rect(position, self.player_size)
        self.scale = scale

        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()
        self.acceleration = 0
        self.direction = pygame.Vector2()
        self.last_input = pygame.Vector2()

        self.max_speed = 62.5 * self.scale
        self.max_fall = 250 * self.scale
        self.jump_force = -100 * self.scale  # -87.5 * self.scale
        self.jump_released = True
        self.gravity_mul = 1

        self.air_time = 0
        self.on_ground = False
        self.has_jump = False

        self.animator = animator
        self.flipped = False
        self.last_state = None
        self.desired_state = ["Idle", False, 0, [], 0]

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
            self.acceleration = 0
        if self.last_input.x == -self.direction.x:
            self.acceleration = 0
        self.acceleration += abs(self.direction.x) * 10 * dt
        self.acceleration = max(min(self.acceleration, 1), 0)
        self.velocity.x = self.acceleration * self.max_speed * self.direction.x

    def y_movement(self, dt: float, gravity: float):
        if self.direction.y == -1 and self.has_jump and self.jump_released:
            self.velocity.y = self.jump_force
            self.has_jump = False
            self.on_ground = False
            self.jump_released = False
            self.gravity_mul = 0.25 * self.scale
        if not self.jump_released and self.direction.y != -1:
            self.gravity_mul = 0.75 * self.scale
            self.jump_released = True
        if self.velocity.y > 0:
            self.gravity_mul = 1.75 * self.scale
        self.velocity.y += gravity * self.gravity_mul * dt
        self.velocity.y = min(self.velocity.y, self.max_fall)

    def get_collisions(self, colliders: list[pygame.sprite.Sprite]):
        return [
            collider for collider in colliders if self.rect.colliderect(collider.rect)
        ]

    def check_collisions(self, dt: float, colliders: list[pygame.sprite.Sprite]):
        collision_types = [False, False, False, False]
        # top, bottom, left, right
        self.position.x += self.velocity.x * dt
        self.rect.x = round(self.position.x)
        for collider in self.get_collisions(colliders):
            if self.velocity.x > 0:
                self.rect.right = collider.rect.left
                collision_types[3] = True
            elif self.velocity.x < 0:
                self.rect.left = collider.rect.right
                collision_types[2] = True
        self.position.y += self.velocity.y * dt
        self.rect.y = round(self.position.y)
        for collider in self.get_collisions(colliders):
            if self.velocity.y > 0:
                self.rect.bottom = collider.rect.top
                collision_types[1] = True
            elif self.velocity.y < 0:
                self.rect.top = collider.rect.bottom
                collision_types[0] = True
        return tuple(collision_types)

    def handle_collisions(self, dt: float, colliders: list[pygame.sprite.Sprite]):
        collision_types = self.check_collisions(dt, colliders)
        if collision_types[1]:
            self.on_ground = True
            self.has_jump = True
            self.velocity.y = 0
            self.position.y = self.rect.y + 1
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
            self.velocity.x = 10 * self.direction.x
            self.position.x = self.rect.x

    def fall_frame(self, max_frames: int):
        return min(
            round(
                (self.velocity.y - self.jump_force)
                / (self.max_fall - self.jump_force)
                * max_frames
            ),
            max_frames - 1,
        )

    def set_animation(self):
        if self.velocity.x == 0 and self.on_ground:
            self.animator.request_state("Idle", False, 0, 0, [])
        if self.velocity.x != 0 and self.on_ground:
            self.animator.request_state("Run", False, 0, 0, [])
        if not self.on_ground:
            self.animator.request_state("Jump", True, self.fall_frame(3), 1, [])
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
        self.y_movement(dt, gravity)
        self.handle_collisions(dt, colliders)
        self.set_animation()
        self.last_state = self.animator.update_frame()
        self.img = self.animator.get_frame()

    def draw(self, surface: pygame.Surface, offset: pygame.Vector2):
        self.img = pygame.transform.flip(self.img, self.flipped, False)
        img_pos = pygame.Vector2(
            self.position[0] - (self.img_size[0] - self.player_size[0]) / 2,
            self.position[1] - (self.img_size[1] - self.player_size[1]),
        )
        surface.blit(self.img, img_pos - offset)
