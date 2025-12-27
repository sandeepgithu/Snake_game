import pygame
import sys
import random
import math
from pygame.math import Vector2

class Particle:
	def __init__(self):
		self.x = random.randint(0, cell_number * cell_size)
		self.y = random.randint(0, cell_number * cell_size)
		self.speed = random.uniform(0.5, 2)
		self.size = random.randint(2, 5)
		self.color = random.choice([
			(200, 230, 100),
			(180, 220, 90),
			(160, 210, 80),
			(140, 200, 70)
		])
		
	def move(self):
		self.y += self.speed
		if self.y > cell_number * cell_size:
			self.y = 0
			self.x = random.randint(0, cell_number * cell_size)
	
	def draw(self, surface):
		pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class SNAKE:
	def __init__(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(1,0)  # Start moving right
		self.new_block = False

		try:
			self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
			self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
			self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
			self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
			
			self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
			self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
			self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
			self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

			self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
			self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

			self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
			self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
			self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
			self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
			
			self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
		except:
			print("Warning: Could not load snake graphics/sounds")
			self.crunch_sound = None

	def draw_snake(self):
		self.update_head_graphics()
		self.update_tail_graphics()

		for index,block in enumerate(self.body):
			x_pos = int(block.x * cell_size)
			y_pos = int(block.y * cell_size)
			block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

			if index == 0:
				screen.blit(self.head,block_rect)
			elif index == len(self.body) - 1:
				screen.blit(self.tail,block_rect)
			else:
				previous_block = self.body[index + 1] - block
				next_block = self.body[index - 1] - block
				if previous_block.x == next_block.x:
					screen.blit(self.body_vertical,block_rect)
				elif previous_block.y == next_block.y:
					screen.blit(self.body_horizontal,block_rect)
				else:
					if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
						screen.blit(self.body_tl,block_rect)
					elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
						screen.blit(self.body_bl,block_rect)
					elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
						screen.blit(self.body_tr,block_rect)
					elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
						screen.blit(self.body_br,block_rect)

	def update_head_graphics(self):
		head_relation = self.body[1] - self.body[0]
		if head_relation == Vector2(1,0): self.head = self.head_left
		elif head_relation == Vector2(-1,0): self.head = self.head_right
		elif head_relation == Vector2(0,1): self.head = self.head_up
		elif head_relation == Vector2(0,-1): self.head = self.head_down

	def update_tail_graphics(self):
		tail_relation = self.body[-2] - self.body[-1]
		if tail_relation == Vector2(1,0): self.tail = self.tail_left
		elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
		elif tail_relation == Vector2(0,1): self.tail = self.tail_up
		elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

	def move_snake(self):
		if self.new_block == True:
			body_copy = self.body[:]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]
			self.new_block = False
		else:
			body_copy = self.body[:-1]
			body_copy.insert(0,body_copy[0] + self.direction)
			self.body = body_copy[:]

	def add_block(self):
		self.new_block = True

	def play_crunch_sound(self):
		if self.crunch_sound:
			self.crunch_sound.play()

	def reset(self):
		self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
		self.direction = Vector2(1,0)  # Start moving right


class FRUIT:
	def __init__(self):
		self.randomize()
		self.pulse_offset = 0

	def draw_fruit(self):
		# Add pulsing animation
		self.pulse_offset += 0.15
		scale = 1 + math.sin(self.pulse_offset) * 0.08
		
		fruit_size = int(cell_size * scale)
		offset = (cell_size - fruit_size) // 2
		
		fruit_rect = pygame.Rect(
			int(self.pos.x * cell_size) + offset,
			int(self.pos.y * cell_size) + offset,
			fruit_size,
			fruit_size
		)
		
		# Scale the apple image
		if apple:
			scaled_apple = pygame.transform.scale(apple, (fruit_size, fruit_size))
			screen.blit(scaled_apple, fruit_rect)
		else:
			# Fallback if apple image not loaded
			pygame.draw.circle(screen, (255, 0, 0), fruit_rect.center, fruit_size // 2)

	def randomize(self):
		self.x = random.randint(0,cell_number - 1)
		self.y = random.randint(0,cell_number - 1)
		self.pos = Vector2(self.x,self.y)


class Button:
	def __init__(self, x, y, width, height, text, color, hover_color, text_color):
		self.rect = pygame.Rect(x, y, width, height)
		self.text = text
		self.color = color
		self.hover_color = hover_color
		self.text_color = text_color
		self.is_hovered = False
		
	def draw(self, surface, font):
		# Shadow
		shadow_rect = self.rect.copy()
		shadow_rect.x += 4
		shadow_rect.y += 4
		pygame.draw.rect(surface, (40, 50, 10), shadow_rect, border_radius=10)
		
		# Button
		color = self.hover_color if self.is_hovered else self.color
		pygame.draw.rect(surface, color, self.rect, border_radius=10)
		pygame.draw.rect(surface, (56, 74, 12), self.rect, 3, border_radius=10)
		
		# Text
		text_surface = font.render(self.text, True, self.text_color)
		text_rect = text_surface.get_rect(center=self.rect.center)
		surface.blit(text_surface, text_rect)
		
	def check_hover(self, pos):
		self.is_hovered = self.rect.collidepoint(pos)
		return self.is_hovered
		
	def is_clicked(self, pos):
		return self.rect.collidepoint(pos)


class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.fruit = FRUIT()
		self.game_state = "start"  # start, playing, paused, game_over
		self.high_score = 0
		self.difficulty = "medium"
		self.speed_settings = {"easy": 200, "medium": 150, "hard": 100}
		self.animation_offset = 0
		self.score_animation = 0
		self.particles = [Particle() for _ in range(30)]
		self.wave_offset = 0
		self.create_buttons()

	def create_buttons(self):
		center_x = cell_number * cell_size // 2
		
		# Start screen buttons
		self.start_button = Button(center_x - 100, 320, 200, 50, "START GAME", (120, 180, 40), (140, 200, 60), (255, 255, 255))
		self.easy_button = Button(center_x - 220, 420, 130, 45, "EASY", (100, 160, 30), (120, 180, 50), (255, 255, 255))
		self.medium_button = Button(center_x - 65, 420, 130, 45, "MEDIUM", (100, 160, 30), (120, 180, 50), (255, 255, 255))
		self.hard_button = Button(center_x + 90, 420, 130, 45, "HARD", (100, 160, 30), (120, 180, 50), (255, 255, 255))
		
		# Game over buttons
		self.restart_button = Button(center_x - 100, 500, 200, 50, "PLAY AGAIN", (120, 180, 40), (140, 200, 60), (255, 255, 255))
		self.menu_button = Button(center_x - 100, 570, 200, 50, "MAIN MENU", (100, 160, 30), (120, 180, 50), (255, 255, 255))

	def update(self):
		# Update animations
		self.animation_offset += 0.05
		self.wave_offset += 0.02
		
		# Update particles
		for particle in self.particles:
			particle.move()
		
		if self.game_state == "playing":
			self.snake.move_snake()
			self.check_collision()
			self.check_fail()

	def draw_elements(self):
		# Draw animated background
		self.draw_animated_background()
		
		if self.game_state == "start":
			self.draw_start_screen()
		elif self.game_state == "playing":
			self.draw_grass()
			self.fruit.draw_fruit()
			self.snake.draw_snake()
			self.draw_score()
		elif self.game_state == "paused":
			self.draw_grass()
			self.fruit.draw_fruit()
			self.snake.draw_snake()
			self.draw_score()
			self.draw_pause_screen()
		elif self.game_state == "game_over":
			self.draw_grass()
			self.draw_game_over_screen()

	def draw_animated_background(self):
		"""Draw animated gradient background with moving waves"""
		# Create gradient background
		for y in range(cell_number):
			# Animated wave pattern
			wave = math.sin(y * 0.3 + self.wave_offset) * 10
			
			# Calculate color based on position and wave
			r = int(160 + wave + math.sin(self.animation_offset + y * 0.1) * 15)
			g = int(200 + wave + math.cos(self.animation_offset + y * 0.15) * 15)
			b = int(60 + wave + math.sin(self.animation_offset * 0.5) * 10)
			
			# Clamp colors
			r = max(140, min(180, r))
			g = max(180, min(220, g))
			b = max(50, min(80, b))
			
			color = (r, g, b)
			rect = pygame.Rect(0, y * cell_size, cell_number * cell_size, cell_size)
			pygame.draw.rect(screen, color, rect)
		
		# Draw floating particles
		for particle in self.particles:
			particle.draw(screen)

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize()
			self.snake.add_block()
			self.snake.play_crunch_sound()
			self.score_animation = 10

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize()

	def check_fail(self):
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			self.game_over()

		for block in self.snake.body[1:]:
			if block == self.snake.body[0]:
				self.game_over()
		
	def game_over(self):
		current_score = len(self.snake.body) - 3
		if current_score > self.high_score:
			self.high_score = current_score
		self.game_state = "game_over"

	def restart_game(self):
		self.snake.reset()
		self.fruit.randomize()
		self.game_state = "playing"
		self.update_speed()
		self.animation_offset = 0

	def update_speed(self):
		pygame.time.set_timer(SCREEN_UPDATE, self.speed_settings[self.difficulty])

	def draw_grass(self):
		grass_color = (167, 209, 61)
		
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
						pygame.draw.rect(screen, grass_color, grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
						pygame.draw.rect(screen, grass_color, grass_rect)
		
		# Draw border
		border_width = 8
		pygame.draw.rect(screen, (56, 74, 12), (0, 0, cell_number * cell_size, cell_number * cell_size), border_width)

	def draw_score(self):
		score_text = str(len(self.snake.body) - 3)
		
		# Animate score when eating
		scale = 1.0
		if self.score_animation > 0:
			scale = 1.0 + (self.score_animation / 20)
			self.score_animation -= 0.5
		
		font_size = int(28 * scale)
		font_size = max(20, min(font_size, 40))  # Clamp size
		scaled_font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)
		score_surface = scaled_font.render(score_text, True, (56, 74, 12))
		
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center=(score_x, score_y))
		
		if apple:
			apple_size = int(40 * scale)
			apple_size = max(30, min(apple_size, 50))  # Clamp size
			scaled_apple = pygame.transform.scale(apple, (apple_size, apple_size))
			apple_rect = scaled_apple.get_rect(midright=(score_rect.left - 5, score_rect.centery))
		else:
			apple_rect = pygame.Rect(score_rect.left - 45, score_rect.centery - 20, 40, 40)
		
		bg_rect = pygame.Rect(
			apple_rect.left - 8,
			apple_rect.top - 5,
			apple_rect.width + score_rect.width + 20,
			apple_rect.height + 10
		)
		
		# Shadow
		shadow_rect = bg_rect.copy()
		shadow_rect.x += 3
		shadow_rect.y += 3
		pygame.draw.rect(screen, (40, 50, 10), shadow_rect, border_radius=10)
		
		# Background
		pygame.draw.rect(screen, (167, 209, 61), bg_rect, border_radius=10)
		screen.blit(score_surface, score_rect)
		if apple:
			screen.blit(scaled_apple, apple_rect)
		else:
			pygame.draw.circle(screen, (255, 0, 0), apple_rect.center, 15)
		pygame.draw.rect(screen, (56, 74, 12), bg_rect, 3, border_radius=10)

	def draw_start_screen(self):
		# Semi-transparent overlay
		overlay = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
		overlay.set_alpha(200)
		overlay.fill((175, 215, 70))
		screen.blit(overlay, (0, 0))
		
		# Animated title with bounce effect
		bounce = math.sin(self.animation_offset * 2) * 8
		title_font_size = 70
		title_font = pygame.font.Font(font_path, title_font_size) if font_path else pygame.font.Font(None, title_font_size)
		
		# Title shadow
		title_shadow = title_font.render('SNAKE GAME', True, (40, 50, 10))
		shadow_rect = title_shadow.get_rect(center=(cell_number * cell_size // 2 + 4, 120 + bounce + 4))
		screen.blit(title_shadow, shadow_rect)
		
		# Title
		title_surface = title_font.render('SNAKE GAME', True, (56, 74, 12))
		title_rect = title_surface.get_rect(center=(cell_number * cell_size // 2, 120 + bounce))
		screen.blit(title_surface, title_rect)
		
		# Decorative apples around title
		if apple:
			for i, angle in enumerate([0, 90, 180, 270]):
				offset_x = math.cos(math.radians(angle + self.animation_offset * 50)) * 150
				offset_y = math.sin(math.radians(angle + self.animation_offset * 50)) * 60
				apple_pos = (int(cell_number * cell_size // 2 + offset_x - 20), int(150 + offset_y))
				screen.blit(apple, apple_pos)
		
		# Start button
		self.start_button.draw(screen, game_font)
		
		# Difficulty label
		diff_label = game_font.render('SELECT DIFFICULTY:', True, (56, 74, 12))
		diff_rect = diff_label.get_rect(center=(cell_number * cell_size // 2, 390))
		screen.blit(diff_label, diff_rect)
		
		# Difficulty buttons with selection indicator
		for button, diff in [(self.easy_button, "easy"), (self.medium_button, "medium"), (self.hard_button, "hard")]:
			if self.difficulty == diff:
				# Highlight selected difficulty
				highlight = pygame.Rect(button.rect.x - 5, button.rect.y - 5, button.rect.width + 10, button.rect.height + 10)
				pygame.draw.rect(screen, (255, 200, 0), highlight, 4, border_radius=12)
			button.draw(screen, game_font_small)
		
		# High score display
		if self.high_score > 0:
			hs_bg = pygame.Rect(cell_number * cell_size // 2 - 120, 540, 240, 50)
			pygame.draw.rect(screen, (120, 180, 40), hs_bg, border_radius=10)
			pygame.draw.rect(screen, (56, 74, 12), hs_bg, 3, border_radius=10)
			
			high_score_surface = game_font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
			high_score_rect = high_score_surface.get_rect(center=(cell_number * cell_size // 2, 565))
			screen.blit(high_score_surface, high_score_rect)
		
		# Controls info
		controls_y = 630
		controls = [
			'Arrow Keys - Move | P - Pause',
			'Click buttons or press SPACE to start'
		]
		for i, control in enumerate(controls):
			ctrl_surface = game_font_small.render(control, True, (80, 110, 20))
			ctrl_rect = ctrl_surface.get_rect(center=(cell_number * cell_size // 2, controls_y + i * 25))
			screen.blit(ctrl_surface, ctrl_rect)

	def draw_game_over_screen(self):
		# Animated overlay
		overlay = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
		alpha = min(240, int(200 + abs(math.sin(self.animation_offset * 3) * 40)))
		overlay.set_alpha(alpha)
		overlay.fill((175, 215, 70))
		screen.blit(overlay, (0, 0))
		
		# Game Over title
		title_font_size = 75
		title_font = pygame.font.Font(font_path, title_font_size) if font_path else pygame.font.Font(None, title_font_size)
		
		# Title shadow
		title_shadow = title_font.render('GAME OVER', True, (150, 30, 30))
		shadow_rect = title_shadow.get_rect(center=(cell_number * cell_size // 2 + 5, 165))
		screen.blit(title_shadow, shadow_rect)
		
		# Title
		title_surface = title_font.render('GAME OVER', True, (220, 50, 50))
		title_rect = title_surface.get_rect(center=(cell_number * cell_size // 2, 160))
		screen.blit(title_surface, title_rect)
		
		# Score panel
		current_score = len(self.snake.body) - 3
		panel_rect = pygame.Rect(cell_number * cell_size // 2 - 150, 260, 300, 120)
		
		# Panel shadow
		shadow_panel = panel_rect.copy()
		shadow_panel.x += 5
		shadow_panel.y += 5
		pygame.draw.rect(screen, (40, 50, 10), shadow_panel, border_radius=15)
		
		# Panel background
		pygame.draw.rect(screen, (140, 190, 50), panel_rect, border_radius=15)
		pygame.draw.rect(screen, (56, 74, 12), panel_rect, 4, border_radius=15)
		
		# Score text
		score_font_size = 45
		score_font = pygame.font.Font(font_path, score_font_size) if font_path else pygame.font.Font(None, score_font_size)
		score_surface = score_font.render(f'Score: {current_score}', True, (255, 255, 255))
		score_rect = score_surface.get_rect(center=(cell_number * cell_size // 2, 295))
		screen.blit(score_surface, score_rect)
		
		# High score
		high_score_surface = game_font.render(f'Best: {self.high_score}', True, (255, 255, 200))
		high_score_rect = high_score_surface.get_rect(center=(cell_number * cell_size // 2, 345))
		screen.blit(high_score_surface, high_score_rect)
		
		# New high score badge
		if current_score == self.high_score and current_score > 0:
			badge_scale = 1 + math.sin(self.animation_offset * 4) * 0.1
			badge_font_size = int(35 * badge_scale)
			badge_font_size = max(30, min(badge_font_size, 45))  # Clamp size
			new_high_font = pygame.font.Font(font_path, badge_font_size) if font_path else pygame.font.Font(None, badge_font_size)
			new_high_surface = new_high_font.render('★ NEW RECORD! ★', True, (255, 215, 0))
			new_high_rect = new_high_surface.get_rect(center=(cell_number * cell_size // 2, 420))
			
			# Badge glow effect
			glow_rect = pygame.Rect(new_high_rect.x - 10, new_high_rect.y - 5, new_high_rect.width + 20, new_high_rect.height + 10)
			pygame.draw.rect(screen, (255, 200, 100), glow_rect, border_radius=10)
			screen.blit(new_high_surface, new_high_rect)
		
		# Buttons
		button_y_offset = 30 if current_score == self.high_score and current_score > 0 else -20
		self.restart_button.rect.y = 500 + button_y_offset
		self.menu_button.rect.y = 570 + button_y_offset
		
		self.restart_button.draw(screen, game_font)
		self.menu_button.draw(screen, game_font)

	def draw_pause_screen(self):
		# Semi-transparent overlay with pulse
		overlay = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
		alpha = int(150 + abs(math.sin(self.animation_offset * 2) * 30))
		overlay.set_alpha(alpha)
		overlay.fill((175, 215, 70))
		screen.blit(overlay, (0, 0))
		
		# Pause panel
		panel_width = 400
		panel_height = 200
		panel_rect = pygame.Rect(
			cell_number * cell_size // 2 - panel_width // 2,
			cell_number * cell_size // 2 - panel_height // 2,
			panel_width,
			panel_height
		)
		
		# Panel shadow
		shadow_panel = panel_rect.copy()
		shadow_panel.x += 6
		shadow_panel.y += 6
		pygame.draw.rect(screen, (40, 50, 10), shadow_panel, border_radius=20)
		
		# Panel background
		pygame.draw.rect(screen, (140, 190, 50), panel_rect, border_radius=20)
		pygame.draw.rect(screen, (56, 74, 12), panel_rect, 5, border_radius=20)
		
		# Pause icon (two bars)
		bar_width = 15
		bar_height = 50
		bar_spacing = 20
		bar_y = cell_number * cell_size // 2 - bar_height // 2 - 30
		
		for i in range(2):
			bar_x = cell_number * cell_size // 2 - bar_width - bar_spacing // 2 + i * (bar_width + bar_spacing)
			bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
			pygame.draw.rect(screen, (56, 74, 12), bar_rect, border_radius=5)
		
		# Paused text
		pause_font_size = 55
		pause_font = pygame.font.Font(font_path, pause_font_size) if font_path else pygame.font.Font(None, pause_font_size)
		pause_surface = pause_font.render('PAUSED', True, (56, 74, 12))
		pause_rect = pause_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 20))
		screen.blit(pause_surface, pause_rect)
		
		# Resume instruction with animation
		bounce = math.sin(self.animation_offset * 3) * 3
		resume_surface = game_font.render('Press P to Resume', True, (255, 255, 255))
		resume_rect = resume_surface.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2 + 70 + bounce))
		screen.blit(resume_surface, resume_rect)

	def handle_mouse_click(self, pos):
		if self.game_state == "start":
			if self.start_button.is_clicked(pos):
				self.restart_game()
			elif self.easy_button.is_clicked(pos):
				self.difficulty = "easy"
			elif self.medium_button.is_clicked(pos):
				self.difficulty = "medium"
			elif self.hard_button.is_clicked(pos):
				self.difficulty = "hard"
		
		elif self.game_state == "game_over":
			if self.restart_button.is_clicked(pos):
				self.restart_game()
			elif self.menu_button.is_clicked(pos):
				self.game_state = "start"

	def handle_mouse_motion(self, pos):
		if self.game_state == "start":
			self.start_button.check_hover(pos)
			self.easy_button.check_hover(pos)
			self.medium_button.check_hover(pos)
			self.hard_button.check_hover(pos)
		
		elif self.game_state == "game_over":
			self.restart_button.check_hover(pos)
			self.menu_button.check_hover(pos)


# Initialize Pygame
try:
	pygame.mixer.pre_init(44100, -16, 2, 512)
	pygame.init()
except:
	pygame.init()

# Game settings
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Snake Game - Enhanced Edition')
clock = pygame.time.Clock()

# Load assets with error handling
apple = None
font_path = None

try:
	apple = pygame.image.load('Graphics/apple.png').convert_alpha()
except:
	print("Warning: Could not load apple.png, using fallback graphics")

try:
	font_path = 'Font/PoetsenOne-Regular.ttf'
	game_font = pygame.font.Font(font_path, 28)
	game_font_small = pygame.font.Font(font_path, 22)
except:
	print("Warning: Could not load font, using default font")
	font_path = None
	game_font = pygame.font.Font(None, 28)
	game_font_small = pygame.font.Font(None, 22)

# Create custom event for screen update
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Create main game object
main_game = MAIN()

print("Snake Game Started!")
print("Controls: Arrow Keys to move, P to pause, SPACE to start")
print("Click buttons with mouse or use keyboard")

# Main game loop
running = True
while running:
	try:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				
			if event.type == SCREEN_UPDATE:
				main_game.update()
			
			if event.type == pygame.MOUSEMOTION:
				main_game.handle_mouse_motion(event.pos)
			
			if event.type == pygame.MOUSEBUTTONDOWN:
				main_game.handle_mouse_click(event.pos)
				
			if event.type == pygame.KEYDOWN:
				# Start screen controls
				if main_game.game_state == "start":
					if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
						main_game.restart_game()
					elif event.key == pygame.K_1:
						main_game.difficulty = "easy"
					elif event.key == pygame.K_2:
						main_game.difficulty = "medium"
					elif event.key == pygame.K_3:
						main_game.difficulty = "hard"
				
				# Game over screen controls
				elif main_game.game_state == "game_over":
					if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
						main_game.restart_game()
					elif event.key == pygame.K_ESCAPE:
						main_game.game_state = "start"
				
				# Playing state controls
				elif main_game.game_state == "playing":
					if event.key == pygame.K_UP or event.key == pygame.K_w:
						if main_game.snake.direction.y != 1:
							main_game.snake.direction = Vector2(0, -1)
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
						if main_game.snake.direction.x != -1:
							main_game.snake.direction = Vector2(1, 0)
					elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
						if main_game.snake.direction.y != -1:
							main_game.snake.direction = Vector2(0, 1)
					elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
						if main_game.snake.direction.x != 1:
							main_game.snake.direction = Vector2(-1, 0)
					elif event.key == pygame.K_p or event.key == pygame.K_SPACE:
						main_game.game_state = "paused"
					elif event.key == pygame.K_ESCAPE:
						main_game.game_state = "start"
				
				# Paused state controls
				elif main_game.game_state == "paused":
					if event.key == pygame.K_p or event.key == pygame.K_SPACE:
						main_game.game_state = "playing"
					elif event.key == pygame.K_ESCAPE:
						main_game.game_state = "start"

		# Always update animations
		main_game.animation_offset += 0.05
		main_game.wave_offset += 0.02
		for particle in main_game.particles:
			particle.move()

		screen.fill((175, 215, 70))
		main_game.draw_elements()
		pygame.display.update()
		clock.tick(60)
		
	except Exception as e:
		print(f"Error in game loop: {e}")
		import traceback
		traceback.print_exc()
		running = False

pygame.quit()
sys.exit()