import pygame
from pygame import mixer

import random
import math

FPS = 60
WIDTH = 800
HEIGHT = 600

# Player

class Player(object):
	def __init__(self):
		self.img = pygame.image.load("player.png")
		self.x = 370
		self.y = 480
		self.x_change = 0
		self.y_change = 0
		self.lives = 3

# Enemy
class Alien(object):
	def __init__(self):
		self.img = pygame.image.load("alien.png")
		self.x = 0
		self.y = 50
		self.x_change = 5
		self.y_change = 10


# Bullet
class Bullet(object):
	def __init__(self):
		self.img = pygame.image.load("bullet.png")
		self.x = 0
		self.y = 496
		self.x_change = 0
		self.y_change = 20
		self.state = "ready"


def show_score(x, y, score_value):
	score = font.render("Score : " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

def show_lives(x, y, lives_value):
	live = lives_font.render("Lives : " + str(lives_value), True, (255, 255, 255))
	screen.blit(live, (x, y))

def game_over():
	text = over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(text, (200, 200))


def draw_player(img, x, y):
	screen.blit(img, (x, y))

 
def draw_alien(img, x, y):
	screen.blit(img, (x, y))


def draw_bullet(img, x, y):
	screen.blit(img, (x, y))


def is_collision(a, b):
	distance = math.sqrt((math.pow(a.x - b.x, 2)) + (math.pow(a.y - b.y, 2)))
	if (distance < 27):
		return True
	else:
		return False


def main_loop():

	score_value = 0
	# Game loop
	running = True
	while running:

		# RGB: Red, Green, Blue
		screen.fill((0, 0, 0))
		screen.blit(background, (0, 0))

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				running = False
			# if a keystroke is pressed check whether it's right or left
			if (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					running = False
				if (event.key == pygame.K_LEFT):
					player.x_change = -5
				if (event.key == pygame.K_RIGHT):
					player.x_change = 5
				if (event.key == pygame.K_UP):
					player.y_change = -5
				if (event.key == pygame.K_DOWN):
					player.y_change = 5
				if (event.key == pygame.K_SPACE):
					if bullet.state == "ready":
						bullet_sound.play()
						bullet.x = player.x + 16
						bullet.y = player.y - 32
						draw_bullet(bullet.img, bullet.x, bullet.y)
						bullet.state = "fire"
			if event.type == pygame.KEYUP:
				if ((event.key == pygame.K_LEFT) or 
					(event.key == pygame.K_RIGHT)):
					player.x_change = 0
				if ((event.key == pygame.K_UP) or
					(event.key == pygame.K_DOWN)):
					player.y_change = 0
				if (event.key == pygame.K_SPACE):
					pass
					
		if (player.lives == 0):
			bullet.state = "off"
			player.y = 2000
			for enemy in enemies:
				enemy.y = 2000
			game_over()

	   	# Player movement
		if player.x <= 0:
			player.x = 0
		if player.x >= 736:
			player.x = 736

		if player.y <= 0:
			player.y = 0
		if player.y >= 536:
			player.y = 536

		player.x += player.x_change
		player.y += player.y_change
		
		# Alien movement
		for enemy in enemies:
			# Game over
			if (enemy.y > 370):
				player.y = 2000
				bullet.state = "off"
				for enemy in enemies: enemy.y = 2000
				game_over()
				break

			if enemy.x <= 0:
				enemy.x_change = 5
				enemy.y += enemy.y_change
			elif enemy.x >= 736:
				enemy.x_change = -5
				enemy.y += enemy.y_change
			
			enemy.x += enemy.x_change

			# Enemy hit by bullet
			hit = is_collision(enemy, bullet)
			crashed = is_collision(enemy, player)
			if hit:
				collision_sound.play()
				bullet.y = 496
				bullet.state = "ready"
				score_value += 1
				enemy.x = random.randint(0, 736)
				enemy.y = random.randint(50, 250)
			elif crashed:
				player.x = 370
				player.y = 480
				player.lives -= 1
			
			draw_alien(enemy.img, enemy.x, enemy.y)

		# Bullet movement
		if bullet.y <= 0:
			bullet.y = 496
			bullet.state = "ready"
		if (bullet.state == "fire"):
			bullet.y -= bullet.y_change
			draw_bullet(bullet.img, bullet.x, bullet.y)

		draw_player(player.img, player.x, player.y)
		show_score(10, 10, score_value)
		show_lives(700, 10, player.lives)
			

		pygame.display.update()
		clock.tick(FPS)


if __name__ == "__main__":
	# Initialize the pygame
	pygame.init()
	
	# Create the screen
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Space Invaders")
	icon = pygame.image.load("ufo.png")
	pygame.display.set_icon(icon)

	# Score Text
	font = pygame.font.Font('freesansbold.ttf', 32)

	lives_font = pygame.font.Font('freesansbold.ttf', 16)
	
	# Background
	background = pygame.image.load("background.png")

	# Background music
	mixer.music.load("background.wav")
	mixer.music.play(-1)

	# Collision Sound
	collision_sound = mixer.Sound("explosion.wav")

	# Bullet Sound
	bullet_sound = mixer.Sound("laser.wav")

	# Game Over Text
	over_font = pygame.font.Font('freesansbold.ttf', 64)

	player = Player()
	bullet = Bullet()

	enemies = []

	clock = pygame.time.Clock()

	num_of_enemies = 6

	for i in range(num_of_enemies):
		enemy = Alien()
		enemy.x = random.randint(0, 735)
		enemy.y = random.randint(50, 250)
		enemies.append(enemy)
	
	main_loop()
	
