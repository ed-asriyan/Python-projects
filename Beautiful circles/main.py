import pygame
import time
from circleContainer import *
from random import randint, random

# --- Constants ----------------------------------------------------

SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 650
FPS = 120
BACKGROUND = [ 0 ] * 3

# --- Generator ----------------------------------------------------

def get_rand_color():
	return ( randint(1, 255), randint(1, 255), randint(1, 255) )

def generate(diameter, count):
	VELOCITY = 8e-2
	BACKGROUND_COL = (0, 0, 0, 0)

	# I think its more readble
	fill_colors   = [ get_rand_color() for i in range(count) ]
	border_colors = [ get_rand_color() for i in range(count) ]
	diameters     = [ diameter // 2 ** (count - i - 1) for i in range(count) ]
	velocities    = [ VELOCITY * (random() + 0.4) / (i + 1) ** 0.8 for i in range(count) ]
	angles        = [ 2 * 3.14 * random() for i in range(count) ]
	b_thicknesses = [ 2 for i in range(count) ]


	result = [ ]

	for i in range(count):
		if not i:
			child = Surface((1, 1))
		else:
			child = result[i - 1][0]

		circle = CircleContainer(child, diameters[i], fill_colors[i], border_colors[i], b_thicknesses[i], True, angles[i])
		obj = [ circle, velocities[i] ]

		print(i, ':',child, diameters[i], fill_colors[i], border_colors[i], b_thicknesses[i], i != count , angles[i])

		result.append(obj)

		diameter *= 2

	return result

# --- Drawing ways -------------------------------------------------

def blit(screen, objs, pos):
	screen.blit(objs[-1][0], pos)

def clear(screen):
	screen.fill(BACKGROUND)

def foreach(objs, func):
	for obj in objs:
		func(obj)


def redraw(screen, objs, pos):
	clear(screen)

	for obj in objs:
		obj[0].redraw(obj[1])

	blit(screen, objs, pos)

def draw_points(screen, objs, pos):
	objs[0][0].draw_point((255, 255, 255))
	for obj in objs:
		obj[0].draw_point(obj[0].get_fill_color())
		obj[0].draw_child(obj[1])
		# x, y = obj[0].calc_child_center()
		# x += SCREEN_WIDTH // 2
		# pygame.draw.circle(animation_screen, obj[0].get_fill_color(), (int(x), int(y)), int(obj[0].get_border_thickness()))

	blit(screen, objs, pos)

# --- Main program -------------------------------------------------

pygame.init()

animation_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
animation_screen.set_alpha(255)

objects1 = generate(min(SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)
objects2 = generate(min(SCREEN_WIDTH // 2, SCREEN_HEIGHT), 5)

done = False
while not done:
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

	redraw(animation_screen, objects1, (0, 0))
	draw_points(animation_screen, objects2, (SCREEN_WIDTH // 2, 0))

	# draw_points(animation_screen, objects[:2])
	# redraw(animation_screen, objects[2:])

	display.flip()
	time.wait(1000 // FPS)

pygame.quit()
