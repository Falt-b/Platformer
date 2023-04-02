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
		if ct - self.last_update > self.cooldown:
			self.last_update = ct
			return 1, True
		return 0, False

class Animator(Animation_Clock):
	def __init__(self, cooldown: int):
		super().__init__(cooldown)
		self.frame = 0
		self.frame_complete = False
		self.current_state = "Idle"
		self.last_state = self.current_state
		self.hold = False
		self.held_frame = 0
		self.held_state = "Idle"
		self.next_state = "Idle"
		self.hold_timer = 2
		self.held_time = 0
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

	def set_state(self, state: str):
		self.current_state = state

	def hold_frame(self, state: str, next_state: str, frame: int, time: int):
		self.current_state = state
		self.held_state = state
		self.next_state = next_state
		self.held_frame = frame
		self.hold = True
		self.hold_timer = time
		self.held_time = 0

	def animate(self):
		if self.hold and self.held_time > self.hold_timer and self.frame_complete:
			self.hold = False
		if (
			self.hold and 
			self.current_state == self.next_state and 
			self.held_time < self.hold_timer
		):
			self.current_state = self.held_state

		if self.current_state != self.last_state:
			if (
				self.frame_complete
			):
				self.current_state == self.last_state
			else:
				self.frame = 0

		frame_update = self.update_frame()
		self.frame += frame_update[0]
		self.held_time += frame_update[0]
		self.frame_complete = frame_update[1]

		if self.hold and self.frame != self.held_frame:
			self.frame = self.held_frame

		if self.frame > len(self.animation_index[self.current_state]) - 1:
			self.frame = 0
		self.last_state = self.current_state
		return self.animation_index[self.current_state][self.frame]

