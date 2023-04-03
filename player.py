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

		self.rect = pygame.Rect(
			position, 
			(width * scale, height * scale)
		)
		self.img = animator.animation_index["Idle"][0]
		self.position = pygame.Vector2(position)
		self.velocity = pygame.Vector2()
		self.acceleration = 0
		self.direction = pygame.Vector2()
		self.last_input = pygame.Vector2()
		self.on_ground = False
		self.has_jump = False
		self.last_jump = 0
		self.jump_time = 500
		
		self.animator = animator
		self.flipped = False

		self.accel_speed = .1
		self.friction = .25
		self.max_speed = 400
		self.max_fall = 50
		self.jump_force = -500

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

	def y_movement(self, gravity: float, dt: float):
		if (
			self.last_input.y == -1 and 
			self.direction.y == -1 and 
			pygame.time.get_ticks() - self.last_jump < self.jump_time
		):
			self.velocity.y += gravity * .85 * dt
		else:
			self.velocity.y += gravity * dt
		if (
			self.has_jump and
			self.direction.y == -1 and
			self.on_ground
		):
			self.velocity.y = self.jump_force * dt
			self.last_jump = pygame.time.get_ticks()
		self.velocity.y = min(self.velocity.y, self.max_fall)

	def x_collisions(self, collide_objects: list[pygame.sprite.Sprite]):
		self.position.x += self.velocity.x
		self.rect.topleft = (round(self.position.x), self.rect.topleft[1])
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
		self.rect.topleft = (self.rect.topleft[0], round(self.position.y))
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

		if self.on_ground and self.velocity.y != 0:
			self.on_ground = False
		if self.on_ground:
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

	def update(self, gravity: float, all_objects: list[pygame.sprite.Sprite], dt: float):
		self.get_input()
		self.x_movement(dt)
		self.y_movement(gravity, dt)
		self.x_collisions(all_objects)
		self.y_collisions(all_objects)
		self.last_input = self.direction
		self.set_animation()
		self.player_image = self.animator.animate()

	def draw(self, surface: pygame.Surface):
		self.player_image = pygame.transform.flip(
			self.player_image, self.flipped, False
		)
		surface.blit(self.player_image, self.position)