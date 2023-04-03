import pygame
import time
from sys import exit
from player import Player
from animator import Animation_Clock, Animator

WIDTH = 800
HEIGHT = 800



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


"""------------- Main -------------"""

def main():
	pygame.init()
	display = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Platformer Test")
	clock = pygame.time.Clock()
	ac = Animation_Clock(100)

	p_group = pygame.sprite.Group()
	t_group = pygame.sprite.Group()
	t1 = Tile(pygame.Vector2(0, 700), 800, 5000, (0, 0, 0), t_group)
	
	player_animator = Animator(100)
	player_animator.init_state(
		"Idle",
		"Triangle_Man_Sprites.png",
		0, 8, 18, 17, 17, 8
	)
	player_animator.init_state(
		"Run",
		"Triangle_Man_Sprites.png",
		0, 0, 8, 17, 17, 8
	)
	player_animator.init_state(
		"Transition",
		"Triangle_Man_Sprites.png",
		0, 18, 19, 17, 17, 8
	)
	p1 = Player(
		(0, 0),
		17,
		17,
		8,
		player_animator,
		p_group
	)

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

		display.fill((0, 135, 81))

		p1.update(2.5, [t1], dt)
		p1.draw(display)
		t_group.draw(display)

		pygame.display.update()

"""------------- Main -------------"""

if __name__ == '__main__':
	main()
	pygame.quit()
	exit()