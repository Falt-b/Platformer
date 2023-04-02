import pygame
from animator import Animator

class Player(pygame.sprite.Sprite):
	def __init__(
		self,
		position: pygame.Vector2,
		width: int,
		height: int,
		scale: int,
		animator: Animator,
		*groups
	):
		super().__init__(*groups)
		self.player_image = animator.animation_index["Idle"][0]

		self.rect = pygame.Rect(position, (width * scale, height * scale))
		self.position = pygame.Vector2(position)
		self.velocity = pygame.Vector2()
		self.acceleration = 0

		self.animator = animator
		self.flipped = False

		self.direction = pygame.Vector2()
		self.last_input = pygame.Vector2()

		self.has_jump = False
		self.on_ground = False

		self.accel_speed = .1
		self.friction = .25
		self.max_speed = 10
		self.max_fall_speed = 100
		self.jump_force = -100

	def get_input(self):
		keys = pygame.key.get_pressed()
		self.direction = pygame.Vector2()
		if keys[pygame.K_a]:
			self.direction.x = -1
		if keys[pygame.K_d]:
			self.direction.x = 1
		if keys[pygame.K_w]:
			self.direction.y = -1
		if keys[pygame.K_s]:
			self.direction.y = 1

	def x_movement(self, dt: float):
		if (
			self.last_input.x == self.direction.x * -1 and
			self.last_input.x != 0
		):
			self.acceleration = 0
		self.acceleration += abs(self.direction.x) * self.accel_speed
		if self.direction.x == 0:
			self.acceleration -= self.friction
		self.acceleration = max(min(self.acceleration, 1), 0)
		self.velocity.x = (
			self.acceleration * self.direction.x * self.max_speed
		) * dt

	def y_movement(self, dt: float):
		self.velocity.y += 10 * dt
		if self.has_jump and self.direction.y == -1:
			self.velocity.y = self.jump_force * dt
			self.has_jump = False
			self.state = "Jump"
		self.velocity.y = max(
			min(self.velocity.y, self.max_fall_speed), -self.max_fall_speed
		) * dt

	def x_collisions(self, collide_objects: list[pygame.sprite.Sprite]):
		self.position.x += self.velocity.x
		self.rect.topleft = (self.position.x, self.rect.topleft[1])
		for game_object in collide_objects:
			if self.rect.colliderect(game_object.rect):
				if (
					self.rect.right > game_object.rect.left and
					self.rect.right < game_object.rect.right
				):
					self.rect.right = game_object.rect.left
				if (
					self.rect.left < game_object.rect.right and
					self.rect.left > game_object.rect.left
				):
					self.rect.left = game_object.rect.right
				self.position.x = self.rect.topleft[0]
				self.velocity.x = 0
				self.acceleration = 0

	def y_collisions(self, collide_objects: list[pygame.sprite.Sprite]):
		self.position.y += self.velocity.y
		self.rect.topleft = (self.rect.topleft[0], self.position.y)
		for game_object in collide_objects:
			if self.rect.colliderect(game_object.rect):
				if (
					self.rect.bottom > game_object.rect.top and
					self.rect.bottom < game_object.rect.bottom
				):
					self.rect.bottom = game_object.rect.top
					self.has_jump = True
					self.on_ground = True
				if (
					self.rect.top < game_object.rect.bottom and
					self.rect.top > game_object.rect.top
				):
					self.rect.top = game_object.rect.bottom
				self.position.y = self.rect.topleft[1]
				self.velocity.y = 0

	def set_animation(self):
		if self.velocity.x == 0 and self.on_ground:
			self.animator.set_state("Idle")
		if self.velocity.x != 0 and self.on_ground:
			self.animator.set_state("Run")
		if (
			self.animator.last_state != "Idle" and
			self.animator.last_state != "Transition" and
			self.animator.current_state == "Idle"
		):
			self.animator.hold_frame("Transition", "Idle", 0, 4)

		if self.velocity.x < 0:
			self.flipped = True
		if self.velocity.x > 0:
			self.flipped = False

	def update(self, all_objects: list[pygame.sprite.Sprite], dt: float):
		self.get_input()
		self.x_movement(dt)
		self.y_movement(dt)
		self.last_input = self.direction
		self.on_ground = False
		self.x_collisions(all_objects)
		self.y_collisions(all_objects)
		self.set_animation()
		self.player_image = self.animator.animate()

	def draw(self, surface: pygame.Surface):
		self.player_image = pygame.transform.flip(
			self.player_image, self.flipped, False
		)
		surface.blit(self.player_image, self.position)