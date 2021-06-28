import pygame
from pygame import mixer

import random
import math

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Score Text
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 10
texty = 10

def show_score(x, y):
	score = font.render("Score : " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over():
	text = over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(text, (200, 200))

# Player
player_img = pygame.image.load("player.png")
player_x = 370
player_y = 480
playerx_change = 0
playery_change = 0

# Enemy
num_of_enemies = 6
alien_img = []
alien_x = []
alien_y = []
alienx_change = []
alieny_change = []

for i in range(num_of_enemies):
	alien_img.append(pygame.image.load("alien.png"))
	alien_x.append(random.randint(0, 736))
	alien_y.append(random.randint(50, 250))
	alienx_change.append(0.5)
	alieny_change.append(30)

# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_x = 0
bullet_y = 496
bulletx_change = 0
bullety_change = 2.5
bullet_state = "ready"

# Background
background = pygame.image.load("background.png")

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Collision Sound
collision_sound = mixer.Sound("explosion.wav")

# Bullet Sound
bullet_sound = mixer.Sound("laser.wav")

def player(x, y):
	screen.blit(player_img, (x, y))

 
def alien(x, y, i):
	screen.blit(alien_img[i], (x, y))


def bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bullet_img, (x, y))


def is_collision(alienx, alieny, bulletx, bullety):
	distance = math.sqrt((math.pow(alienx - bulletx, 2)) + (math.pow(alieny - bullety, 2)))
	if (distance < 27):
		return True
	else:
		return False


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
			if (event.key == pygame.K_LEFT):
				playerx_change = -1
			if (event.key == pygame.K_RIGHT):
				playerx_change = 1
			#if (event.key == pygame.K_UP):
			#	playery_change = -1
			#if (event.key == pygame.K_DOWN):
			#	playery_change = -1
			if (event.key == pygame.K_SPACE):
				if bullet_state == "ready":
					bullet_sound.play()
					bullet_x = player_x + 16
					bullet(bullet_x, bullet_y)
					bullet_state = "fire"
		if event.type == pygame.KEYUP:
			if ((event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT)):
				playerx_change = 0
			if (event.key == pygame.K_SPACE):
				pass
				
   	# Player movement
	if player_x <= 0:
		player_x = 0
	if player_x >= 736:
		player_x = 736

	player_x += playerx_change
	
	# Alien movement
	for i in range(num_of_enemies):
		# Game over
		if alien_y[i] > 380:
			for i in range(num_of_enemies):
				alien_y[i] = 2000
				player_y = 2000
			game_over()
			break


		if alien_x[i] <= 0:
			alienx_change[i] = 0.5
			alien_y[i] += alieny_change[i]
		elif alien_x[i] >= 736:
			alienx_change[i] = -0.5
			alien_y[i] += alieny_change[i]
		
		alien_x[i] += alienx_change[i]

		# Collision
		collision = is_collision(alien_x[i], alien_y[i], bullet_x, bullet_y)
		if collision:
			collision_sound.play()
			bullet_y = 496
			bullet_state = "ready"
			score_value += 1
			alien_x[i] = random.randint(0, 736)
			alien_y[i] = random.randint(50, 250)
		

		alien(alien_x[i], alien_y[i], i)

	#Bullet movement
	if bullet_y <= 0:
		bullet_y = 496
		bullet_state = "ready"

	if (bullet_state == "fire"):
		bullet_y -= bullety_change
		bullet(bullet_x, bullet_y)

	player(player_x, player_y)
	show_score(textx, texty)
		

	pygame.display.update()