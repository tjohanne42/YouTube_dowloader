import pygame as pg
import time

pg.font.init()

FT_BUTTON_BG = (80, 90, 110)
FT_BUTTON_BG_FO = (40, 50, 70)
FT_WHITE_TXT = (200, 200, 200)
FT_INPUT_TEXTBAR_BG = (80, 90, 110)
FT_INPUT_TEXTBAR_BG_FO = (40, 50, 70)
FT_BORDER_COLOR = (0, 0, 0)
FT_CURSOR_COLOR = (255, 255, 255)
FT_AUTO_FONT = pg.font.Font(pg.font.get_default_font(), 30)

class FtPgInteractive(object):

	def __init__(self, screen):

		self.screen = screen
		self.buttons = {}
		self.input_textbar = {}
		self.cursor_is_ibeam = False
		self.user_typing = "noone"
		self.cursor_position = 0

	def add_button	(
					self,
					index,
					flyover=True,
					pos=(0, 0),
					size=(100, 40),
					bg=FT_BUTTON_BG,
					bg_fo=FT_BUTTON_BG_FO,
					border=True,
					border_width=2,
					border_radius=1,
					border_color=FT_BORDER_COLOR,
					text=False,
					text_font=FT_AUTO_FONT,
					text_color=FT_WHITE_TXT,
					text_antialias=True
					):
		pass

	def add_input_textbar	(
							self,
							index,
							flyover=True,
							pos=(0, 0),
							size=(100, 40),
							bg=FT_INPUT_TEXTBAR_BG,
							bg_fo=FT_INPUT_TEXTBAR_BG_FO,
							border=True,
							border_width=2,
							border_radius=6,
							border_color=FT_BORDER_COLOR,
							initial_text="",
							font=FT_AUTO_FONT,
							text_color=FT_WHITE_TXT,
							text_antialias=True,
							cursor_ms_visible=500,
							cursor_color=FT_CURSOR_COLOR,
							repeat_keys_initial_ms=400,
							repeat_keys_interval_ms=35,
							display_on=True
							):

		# save usefull params of this input_textbar in a dict
		self.input_textbar[index] = 	{
												"flyover" : flyover,
												"pos_rect" : pg.Rect(pos[0], pos[1], size[0], size[1]),
												"font" : font,
												"text" : initial_text,
												"text_color" : text_color,
												"text_antialias" : text_antialias,
												"cursor_ms_visible" : cursor_ms_visible,
												"repeat_keys_initial_ms" : repeat_keys_initial_ms,
												"repeat_keys_interval_ms" : repeat_keys_interval_ms,
												"display_on" : display_on
											}

		
		# create rounded rectangle
		surface = pg.Surface(size)
		surface.fill(bg)
		rounded_surface = pg.Surface(size, pg.SRCALPHA)
		pg.draw.rect(rounded_surface, (255, 255, 255), (0, 0, *size), border_radius=border_radius)
		surface = surface.convert_alpha()
		surface.blit(rounded_surface, (0, 0), None, pg.BLEND_RGBA_MIN)

		# create rounded rectangle for flyover
		surface_fo = pg.Surface(size)
		surface_fo.fill(bg_fo)
		surface_fo = surface_fo.convert_alpha()
		surface_fo.blit(rounded_surface, (0, 0), None, pg.BLEND_RGBA_MIN)


		# save initial_surface (without text) so we don't have to load at every frame
		self.input_textbar[index]["initial_surface"] = surface.copy()
		if border:
			# draw border if param border == True
			pg.draw.rect(self.input_textbar[index]["initial_surface"], border_color, pg.Rect(0, 0, *size),
				width=border_width, border_radius=border_radius)

		# save initial_surface if param flyover == True
		if flyover:
			self.input_textbar[index]["initial_surface_fo"] = surface_fo.copy()
			if border:
				pg.draw.rect(self.input_textbar[index]["initial_surface_fo"], border_color, pg.Rect(0, 0, *size),
					width=border_width, border_radius=border_radius)

		# save cursor_surface
		surface = pg.Surface((1, font.size("|")[1]))
		surface.fill(cursor_color)
		self.input_textbar[index]["cursor_surface"] = surface

		# save actual_surface (with text)
		self.input_textbar_actual_surface(index)
		

	def input_textbar_actual_surface(self, index):
		# create text_surface
		text_surface = self.input_textbar[index]["font"].render(self.input_textbar[index]["text"], self.input_textbar[index]["text_antialias"],
			self.input_textbar[index]["text_color"])

		# copy initial surface into actual_surface
		self.input_textbar[index]["actual_surface"] = self.input_textbar[index]["initial_surface"].copy()
		
		# calculate distance between the left start position of the input_textbar
		# and the actual left start position of the text
		self.input_textbar[index]["distance_left_text"] = self.input_textbar[index]["initial_surface"].get_size()[0] / 2 - text_surface.get_size()[0] / 2
		# same for the top start position
		self.input_textbar[index]["distance_top_text"] = self.input_textbar[index]["initial_surface"].get_size()[1] / 2 - text_surface.get_size()[1] / 2

		# blit text on actual_surface
		self.input_textbar[index]["actual_surface"].blit(text_surface,
			(self.input_textbar[index]["initial_surface"].get_size()[0] / 2 - text_surface.get_size()[0] / 2,
			self.input_textbar[index]["initial_surface"].get_size()[1] / 2 - text_surface.get_size()[1] / 2))

		# blit text on actuel_surface_fo
		if self.input_textbar[index]["flyover"]:
			self.input_textbar[index]["actual_surface_fo"] = self.input_textbar[index]["initial_surface_fo"].copy()
			self.input_textbar[index]["actual_surface_fo"].blit(text_surface,
				(self.input_textbar[index]["distance_left_text"],
				self.input_textbar[index]["distance_top_text"]))



	def event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
			mx, my = pg.mouse.get_pos()
			for key, value in self.input_textbar.items():
				if value["display_on"]:
					if value["pos_rect"].collidepoint((mx, my)):
						# if user clicks on input_textbar, we register on wich input_textbar he did it
						# and we set the cursor position at the len(str)
						self.user_typing = key
						self.cursor_position = len(self.input_textbar[self.user_typing]["text"])

		elif event.type == pg.KEYDOWN and self.user_typing != "noone":
			if event.key == pg.K_BACKSPACE:
				self.input_textbar[self.user_typing]["text"] = (
					self.input_textbar[self.user_typing]["text"][:max(self.cursor_position - 1, 0)]
					+ self.input_textbar[self.user_typing]["text"][self.cursor_position:]
				)
				# Subtract one from cursor_pos, but do not go below zero:
				self.cursor_position = max(self.cursor_position - 1, 0)
				# save actual_surface (with text)
				self.input_textbar_actual_surface(self.user_typing)
			elif event.key == pg.K_DELETE:
				self.input_textbar[self.user_typing]["text"] = (
					self.input_textbar[self.user_typing]["text"][:self.cursor_position]
					+ self.input_textbar[self.user_typing]["text"][self.cursor_position + 1:]
				)
				self.input_textbar_actual_surface(self.user_typing)
			elif event.key == pg.K_RETURN:
				print(self.input_textbar[self.user_typing]["text"])
				self.user_typing = "noone"
			elif event.key == pg.K_RIGHT:
				# Add one to cursor_pos, but do not exceed len(input_string)
				self.cursor_position = min(self.cursor_position + 1, len(self.input_textbar[self.user_typing]["text"]))
			elif event.key == pg.K_LEFT:
				# Subtract one from cursor_pos, but do not go below zero:
				self.cursor_position = max(self.cursor_position - 1, 0)
			elif event.key == pg.K_END:
				self.cursor_position = len(self.input_textbar[self.user_typing]["text"])
			elif event.key == pg.K_HOME:
				self.cursor_position = 0
			else:
				self.input_textbar[self.user_typing]["text"] = (
					self.input_textbar[self.user_typing]["text"][:self.cursor_position]
					+ event.unicode
					+ self.input_textbar[self.user_typing]["text"][self.cursor_position:]
				)
				self.cursor_position += len(event.unicode)
				self.input_textbar_actual_surface(self.user_typing)

		elif event.type == pg.MOUSEMOTION:
			mx, my = pg.mouse.get_pos()
			set_cursor_ibeam = False
			for key, value in self.input_textbar.items():
				if value["display_on"]:
					if value["pos_rect"].collidepoint((mx, my)):
						set_cursor_ibeam = True
			if set_cursor_ibeam and not self.cursor_is_ibeam:
				# if user moves on input_textbar, set the mouse cursor as ibeam
				pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_IBEAM)
				self.cursor_is_ibeam = True
			elif not set_cursor_ibeam and self.cursor_is_ibeam:
				# if user was on input_textbar and move away, set the mouse cursor as arrow
				pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
				self.cursor_is_ibeam = False

	def display(self):
		mx, my = pg.mouse.get_pos()

		# display all input_textbar
		for key, value in self.input_textbar.items():
			if value["display_on"]:
				if value["flyover"] and value["pos_rect"].collidepoint((mx, my)):
					self.screen.blit(value["actual_surface_fo"], (value["pos_rect"].x, value["pos_rect"].y))
				else:
					self.screen.blit(value["actual_surface"], (value["pos_rect"].x, value["pos_rect"].y))

		# if user is typing on input_textbar, display cursor
		if self.user_typing != "noone":
			cursor_y_pos = self.input_textbar[self.user_typing]["font"].size(
				self.input_textbar[self.user_typing]["text"][:self.cursor_position])[0]
			# Without this, the cursor is invisible when self.cursor_position > 0:
			if self.cursor_position > 0:
				cursor_y_pos -= self.input_textbar[self.user_typing]["cursor_surface"].get_width()
			self.screen.blit(self.input_textbar[self.user_typing]["cursor_surface"],
				(self.input_textbar[self.user_typing]["pos_rect"].x + cursor_y_pos + self.input_textbar[self.user_typing]["distance_left_text"]
				, self.input_textbar[self.user_typing]["pos_rect"].y + self.input_textbar[self.user_typing]["distance_top_text"]))
