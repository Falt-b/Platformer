import pygame
from sys import exit
# Triangle Sprites are 17 x 17

WIDTH = 800
HEIGHT = 800

"""------------- Image Loading -------------"""

def get_image(
	original_image: pygame.Surface, 
	row: int, 
	col: int, 
	width: int, 
	height: int,
	color_key: tuple = (0, 0, 0)
):
	new_img = pygame.Surface((width, height))
	new_img.set_colorkey(color_key)
	new_img.blit(
		original_image, 
		(0, 0), 
		(
			col * width, row * height, 
			(col * width) + width, (row * height) + height
		)
	)
	return new_img

def load_animation(
	sprite_sheet: str, 
	row: int, 
	col: int, 
	start: int, 
	stop: int, 
	width: int, 
	height: int, 
	scale: int, 
	color_key: tuple = (0, 0, 0)
):
	img_array = []
	image = pygame.image.load(sprite_sheet)
	image = pygame.transform.scale(
		image, (image.get_width() * scale, image.get_height() * scale)
	)
	return [
		get_image(
			image, row, col + i[1], width * scale, height * scale, color_key
		) for i in enumerate(range(stop - start))
	]

"""------------- Image Loading -------------"""



"""------------- Probably pointless -------------"""

class Animation_Clock:
	def __init__(self, cooldown):
		self.cooldown = cooldown
		self.last_update = 0

	def update_frame(self):
		ct = pygame.time.get_ticks()
		if ct - self.last_update >= self.cooldown:
			self.last_update = ct
			return 1
		return 0

"""------------- Probably pointless -------------"""



"""------------- Tile Class -------------"""

class Tile(pygame.sprite.Sprite):
	def __init__(
		self, 
		position: pygame.Vector2, 
		width: int, 
		height: int, 
		color: tuple,
		*groups
	):
		super().__init__(*groups)
		self.position = position
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.topleft = self.position

"""------------- Tile Class -------------"""



"""------------- Player Class -------------"""

class Player(pygame.sprite.Sprite):
	def __init__(
		self, 
		position: tuple, 
		width: int, 
		height: int, 
		color: tuple, 
		*groups
	):
		super().__init__(*groups)
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.topleft = position

		# Player input
		self.direction = pygame.Vector2()
		self.last_input = pygame.Vector2()
		self.velocity = pygame.Vector2()
		self.acceleration = 0
		self.accel_speed = .38
		self.friction_force = .45
		self.speed = 20
		self.jump_speed = -16
		self.has_jump = True
		self.on_ground = True
		self.max_fall_speed = 20

		# Player Animation
		self.frame = 0
		self.current_state = "Idle"
		self.last_state = self.current_state
		self.animation_index = {
			"Idle": [], "Run": [], "Jump": [], "Attack": []
		}

	def init_animation(
		self, 
		state: str,
		sprite_sheet: str, 
		row: int, 
		col: int, 
		start: int, 
		stop: int, 
		width: int, 
		height: int, 
		scale: int, 
		color_key: tuple = (0, 0, 0)
	):
		self.animations[state] = load_animation(
			sprite_sheet,
			row,
			col,
			start,
			stop,
			width,
			height,
			scale,
			color_key
		)

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

	def update(self, other: pygame.sprite.Sprite):

		# --- Input, Movement, and Collisions --- #
		self.get_input()
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
		self.rect.topleft = (
			self.rect.topleft[0] + self.velocity.x, self.rect.topleft[1]
		)
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
		self.rect.topleft = (
			self.rect.topleft[0], self.rect.topleft[1] + self.velocity.y
		)
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
		# --- Input, Movement, and Collisions --- #

"""------------- Player Class -------------"""



"""------------- Main -------------"""

def main():
	pygame.init()
	display = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Platformer Test")
	clock = pygame.time.Clock()
	ac = Animation_Clock(100)

	p_group = pygame.sprite.Group()
	t_group = pygame.sprite.Group()
	p1 = Player(pygame.Vector2(), 17, 17, (255, 241, 232), p_group)
	t1 = Tile(pygame.Vector2(0, 700), 800, 5000, (0, 0, 0), t_group)

	while True:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					return False

		display.fill((29, 43, 83))

		p_group.update(t1)
		p_group.draw(display)
		t_group.draw(display)

		pygame.display.update()

"""------------- Main -------------"""

if __name__ == '__main__':
	main()