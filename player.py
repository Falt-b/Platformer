import pygame
from animator import Animator

class Player(pygame.sprite.Sprite):
	def __init__(
		self, 
		position: tuple, 
		width: int, 
		height: int, 
		color: tuple, 
		animator: Animator
		*groups
	):
		super().__init__(*groups)
		self.player_image = pygame.Surface((width, height))
		self.rect = pygame.Rect(position, (width, height))
		self.rect.topleft = position

		self.animator = animator
		self.player_flipped = False

		# Player Settings
		self.direction = pygame.Vector2()
		self.last_input = pygame.Vector2()
		self.velocity = pygame.Vector2()
		self.acceleration = 0
		self.accel_speed = .38
		self.friction_force = .45
		self.speed = 5
		self.jump_speed = -16
		self.has_jump = True
		self.on_ground = True
		self.max_fall_speed = 20

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

	def x_movement(self):
		if (
			self.last_input.x == self.direction.x * -1 and 
			self.last_input.x != 0
		):
			self.acceleration = 0
		self.acceleration += abs(self.direction.x) * self.accel_speed
		if self.direction.x == 0:
			self.acceleration -= self.friction_force
		self.acceleration = max(min(self.acceleration, 1), 0)
		self.velocity.x = self.acceleration * self.direction.x * self.speed

	def y_movement(self):
		self.velocity.y += 1 
		if self.has_jump and self.direction.y == -1:
			self.velocity.y = self.jump_speed
			self.has_jump = False
			self.state = "Jump"
		self.velocity.y = max(
			min(self.velocity.y, self.max_fall_speed), -self.max_fall_speed
		)
		self.last_input = self.direction
		self.on_ground = False

	def x_collisions(self, collided_rects: list[pygame.Rect]):
		self.rect.topleft = (
			self.rect.topleft[0] + self.velocity.x, self.rect.topleft[1]
		)
		for rect in collided_rects:
			if self.rect.colliderect(other.rect):
				if (
					self.rect.right > other.rect.left and
					self.rect.right < other.rect.right
				):
					self.rect.right = other.rect.left
				if (
					self.rect.left < other.rect.right and
					self.rect.left > other.rect.left
				):
					self.rect.left = other.rect.right
				self.velocity.x = 0
				self.acceleration = 0

	def y_collisions(self, collided_rects: list[pygame.Rect]):
		self.rect.topleft = (
			self.rect.topleft[0], self.rect.topleft[1] + self.velocity.y
		)
		for rect in collided_rects:
			if self.rect.colliderect(other.rect):
				if (
					self.rect.bottom > other.rect.top and
					self.rect.bottom < other.rect.bottom
				):
					self.rect.bottom = other.rect.top
					self.has_jump = True
					self.on_ground = True
				if (
					self.rect.top < other.rect.bottom and
					self.rect.top > other.rect.top
				):
					self.rect.top = other.rect.bottom
				self.velocity.y = 0

	def set_state(self):
		if self.velocity.x == 0 and self.on_ground:
			self.animator.current_state = "Idle"
		if self.velocity.x != 0 and self.on_ground:
			self.animator.current_state = "Run"

		if self.velocity.x < 0:
			self.player_flipped = True
		if self.velocity.x > 0:
			self.player_flipped = False

	def update(self, all_rects: list[pygame.Rect]):
		self.get_input()
		self.x_movement()
		self.y_movement()
		self.x_collisions(all_rects)
		self.y_collisions(all_rects)
		self.set_state()
		self.player_image = self.amimator.animate()


	def draw(self, surface: pygame.Surface):
		self.player_image = pygame.transform.flip(
			self.player_image, self.player_flipped, False
		)
		surface.blit(self.player_image, self.rect.topleft)
