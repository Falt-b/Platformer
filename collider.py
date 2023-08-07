import pygame


class Collider(pygame.sprite.Sprite):
    def __init__(self, position: pygame.Vector2, width: int, height: int):
        self.image = pygame.Surface((width, height))
        self.rect = pygame.Rect(position, (width, height))
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2()

    def apply_gravity(self, dt: float, gravity: float, max_fall: float):
        self.velocity.y += gravity * dt
        self.velocity.y = min(self.velocity.y, max_fall)

    def get_collisions(self, colliders: list[pygame.sprite.Sprite]):
        return [
            collider for collider in colliders if self.rect.colliderect(collider.rect)
        ]

    def check_collisions(
        self,
        dt: float,
        colliders: list[pygame.sprite.Sprite],
        special_colliders: list[pygame.sprite.Sprite] = [],
    ):
        collision_types = [False, False, False, False]
        # top, bottom, left, right

        # find collisions on x-axis
        self.position.x += self.velocity.x * dt
        self.rect.x = round(self.position.x)
        for collider in self.get_collisions(colliders):
            if self.velocity.x > 0:
                self.rect.right = collider.rect.left
                collision_types[3] = True
            elif self.velocity.x < 0:
                self.rect.left = collider.rect.right
                collision_types[2] = True

        # get collisions on y-axis
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

    def draw(
        self,
        surface: pygame.Surface,
        image_size: tuple,
        offset: pygame.Vector2,
        flip_x: bool = False,
        flip_y: bool = False,
    ):
        surface.blit(
            pygame.transform.flip(self.image, flip_x, flip_y),
            pygame.Vector2(
                self.position.x - (image_size[0] - self.rect.width) * 0.5,
                self.position.y - (image_size[1] - self.rect.height) * 0.5,
            )
            - offset,
        )
