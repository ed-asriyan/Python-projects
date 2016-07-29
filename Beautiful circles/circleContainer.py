from pygame import *
from math import sin, cos
from random import randint

class Movement:
	def __init__(self, screen, surface, x_pos, y_pos):
		self._screen     = screen
		self._surface    = surface
		self._curr_angle = 0
		self._x_pos      = x_pos
		self._y_pos      = y_pos

	def _rot_center(self, angle):
		"""rotate an image while keeping its center and size"""
		image = self._surface

		orig_rect = image.get_rect()
		rot_image = transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		
		rot_image.set_alpha(255)
		return rot_image

	def angle(self, val=None):
		if not val is None:
			self._curr_angle = int(val)
		return self._curr_angle

	def surface(self, val=None):
		if not val is None:
			self._surface = val
		return self._surface

	def x_pos(self, val=None):
		if not val is None:
			self._x_pos = int(val)
		return self._x_pos

	def y_pos(self, val=None):
		if not val is None:
			self._y_pos = int(val)
		return self._y_pos

	def move(self, dx, dy, with_rotation=True, forward_direction=True):
		self._curr_angle += (180 * (dx ** 2 + dy ** 2) ** 0.5 / max(self._surface.get_width(), self._surface.get_height())) * (1 if forward_direction else -1)
		self._x_pos      += dx
		self._y_pos      += dy

		new_ball = self._rot_center(self._curr_angle) if with_rotation else self._surface

		self._screen.blit(new_ball, (self._x_pos, self._y_pos))

class CircleMovement(Movement):
	def __init__(self, screen, surface, x_center, y_center, radius, angle=0):
		Movement.__init__(self, screen, surface, x_center - radius, y_center)

		self._curr_circle_angle = angle
		self._center_x = x_center
		self._center_y = y_center
		self._radius   = radius

	def move(self, angle, with_rotation=True, forward_direction=True):
		self._curr_circle_angle += angle

		width, height = self._surface.get_size()

		new_x = self._center_x + self._radius * cos(self._curr_circle_angle) - width // 2
		new_y = self._center_y - self._radius * sin(self._curr_circle_angle) - height // 2

		Movement.move(self, new_x - self._x_pos, new_y - self._y_pos, with_rotation, forward_direction)

	def center(self, x_pos=None, y_pos=None):
		if not (x_pos is None) and not (y_pos is None):
			self._center_x = self._x_pos
			self._center_y = self._y_pos
		return self._center_x, self._center_y

	def angle(self, val=None):
		if not val is None:
			self._curr_circle_angle = float(val)

		return self._curr_circle_angle

class CircleContainer(Surface):
	def __init__(self, child_surface, size, \
		fill_color=(0, 0, 0, 0), border_color=(0, 0, 0), border_thickness=3, is_inside=True, angle=0,\
		**kwargs):
		
		# child info
		self._child_size = max(child_surface.get_size())

		# main info
		self._is_inside = bool(is_inside)
		self._size = size
		self._fill_color = fill_color
		self._border_color = border_color
		self._border_thickness = int(border_thickness)
		self._center = int(self._size // 2)
		self._radius = int(self._size - (not self._is_inside) * self._child_size * 2) // 2

		# init
		Surface.__init__(self, (self._size, self._size), SRCALPHA)
		self.set_alpha(255)
		
		movement_radius = self._radius + (self._child_size // 2 + self._border_thickness) * (-1 if self._is_inside else 1) - 1.5
		self._child_movement = CircleMovement(self, child_surface, self._center, self._center, movement_radius, angle)



	# --- Getters --------------------------------------------------

	def is_inside(self):
		return self._is_inside

	def size(self):
		return self._size

	def get_fill_color(self):
		return self._fill_color

	def get_border_color(self):
		return self._border_color

	def get_border_thickness(self):
		return self._border_thickness

	# --- Drawing --------------------------------------------------

	def draw_border(self):
		draw.circle(self, self._border_color, (self._center, self._center), self._radius)
		draw.circle(self, self._fill_color, (self._center, self._center), self._radius - self._border_thickness)
	
	def draw_point(self, color=(0, 0, 0)):
		draw.circle(self, color, [ self._center - self._border_thickness // 2, self._border_thickness // 2 ], self._border_thickness // 2)

	def draw_child(self, angle):
		self._child_movement.move(angle, True, not self._is_inside)

	def clear(self):
		self.fill((0, 0, 0, 0))

	def draw_all(self, angle):
		self.draw_border()
		self.draw_point()
		self.draw_child(angle)

	def redraw(self, angle):
		self.clear()
		self.draw_all(angle)

	# --- Other ----------------------------------------------------

	def calc_child_center(self):
		return (self._child_movement.x_pos(), self._child_movement.y_pos())