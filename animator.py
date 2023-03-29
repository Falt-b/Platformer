import pygame

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
		) for i in enumerate(range(stop - col))
	]

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

class Animator():
	def __init__(self, clock: Animation_Clock, states: list[str]):
		self.clock = clock
		self.frame = 0
		self.current_state = "Idle"
		self.last_state = self.current_state
		self.transition_frame = 0
		self.transition_frames = 4
		self.animation_index = {
			"Idle": [], "Transition": [], "Run": [], "Jump": []
		}

	def init_state(
		self, 
		state: str,
		sprite_sheet: str, 
		row: int, 
		col: int, 
		stop: int, 
		width: int, 
		height: int, 
		scale: int, 
		color_key: tuple = (0, 0, 0)
	):
		self.animation_index[state] = load_animation(
			sprite_sheet,
			row,
			col,
			stop,
			width,
			height,
			scale,
			color_key
		)

	def animate(self):
		if self.last_state != "Idle" and self.current_state == "Idle":
			self.state = "Transition"
		if self.current_state == "Idle" and self.transition_frame < self.transition_frames:
			self.current_state = "Transition"
			self.transition_frame = 0
		if self.current_state != self.last_state:
			if (
				pygame.time.get_ticks() - self.clock.last_update < self.clock.cooldown
			):
				self.current_state == self.last_state
			else:
				self.frame = 0

		frame_update = self.animation_clock.update_frame()
		self.frame += frame_update
		self.transition_frame += frame_update
		if self.frame > len(self.animation_index[self.current_state]) - 1:
			self.frame = 0
		self.last_state = self.current_state
		return self.animation_index[self.current_state][self.frame]

