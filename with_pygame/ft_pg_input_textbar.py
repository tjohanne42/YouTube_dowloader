import pygame as pg
import pyperclip

pg.font.init()

FT_WTHEME_TXT = (3, 3, 3)
FT_WTHEME_BG_COLOR = (249, 249, 249)
FT_WTHEME_BORDER_COLOR = (0, 0, 0)
FT_WTHEME_CURSOR_COLOR = (3, 3, 3)
FT_WTHEME_PLACECHOLDER_COLOR = (96, 96, 96)

# todo: 
#		- create some THEMES (black, white, blue, etc...)
#		- limiter la taille du texte pour pas qu'il depasse
#		- clignotement du curseur
#		- selection du texte (pour copier coller, supprimer, couper)
#		- selectionner une font auto avec une taille adaptée
#		- historique pour ctrl + z et ctrl + shift + z
#		- menu clique droit
#		- gestion des caracs chelous genre TAB qui affichent des carrés en mode caractère pas pris en compte
#		- ajout d'une FONCTION qui permet de changer les parametres (couleur, texte, etc...) depuis le main
#		- ajout argument fonction pour lancer une fonction lorsque l'utilisateur tape entree
#		- ajout argument bg transparent
#		- ajout argument croix sur le coté droit pour supprimer toute la recherche
#		- ajout argument bouton search
#		- ajout argument bouton reconnaissance vocale
#		- ajout argument historique des recherches qui s'affichent quand on clique sur la barre
#		- ajout argument changement de la couleur de la bordure quand active = True

FT_AUTO_FONT = pg.font.Font(pg.font.get_default_font(), 30)

class FtPgInputTextbar(object):
	def __init__(
				self,
				screen,
				pos=(0, 0),
				size=(200, 50),
				bg_color=FT_WTHEME_BG_COLOR,
				rounded=6,
				border=True,
				border_width=2,
				border_color=FT_WTHEME_BORDER_COLOR,
				initial_text="",
				placeholder=False,
				placeholder_color=FT_WTHEME_PLACECHOLDER_COLOR,
				font=FT_AUTO_FONT,
				text_color=FT_WTHEME_TXT,
				text_antialias=True,
				text_centered=False,
				text_max_width=-1,
				cursor_ms_visible=500,
				cursor_color=FT_WTHEME_CURSOR_COLOR,
				display_on=True
				):

		self.screen = screen
		self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
		self.bg_color = bg_color
		self.rounded = rounded
		self.border = border
		self.border_width = border_width
		self.border_color = border_color
		self.font = font
		self.text_color = text_color
		self.text_antialias = text_antialias
		self.text_centered=text_centered
		if text_max_width < 0:
			self.text_max_width = self.rect.w - 30 - rounded / 2
		else:
			self.text_max_width = text_max_width
		self.cursor_color = cursor_color
		self.display_on = display_on
		if placeholder:
			self.placeholder = font.render(placeholder, text_antialias, placeholder_color)
		else:
			self.placeholder = placeholder
		self.active = False
		self.ctrl_pressed = False
		self.cursor_ibeam = False
		self.text = initial_text
		self.distance_top_text = self.rect.h / 2 - self.font.size("|")[1] / 2
		self.init_bg_surface_and_cursor()


	def init_bg_surface_and_cursor(self):
		# save bg_surface
		self.bg_surface = pg.Surface((self.rect.w, self.rect.h))
		self.bg_surface.fill(self.bg_color)
		rounded_surface = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)
		pg.draw.rect(rounded_surface, (255, 255, 255), (0, 0, self.rect.w, self.rect.h), border_radius=self.rounded)
		self.bg_surface = self.bg_surface.convert_alpha()
		self.bg_surface.blit(rounded_surface, (0, 0), None, pg.BLEND_RGBA_MIN)

		if self.border:
			# draw border if param border == True
			pg.draw.rect(self.bg_surface, self.border_color, pg.Rect(0, 0, self.rect.w, self.rect.h),
				width=self.border_width, border_radius=self.rounded)

		# save cursor_surface
		self.cursor_surface = pg.Surface((1, self.font.size("|")[1]))
		self.cursor_surface.fill(self.cursor_color)

		# save actual_surface
		self.get_actual_surface()


	def get_actual_surface(self):
		# copy bg surface into actual_surface
		self.actual_surface = self.bg_surface.copy()
		
		blit_text = True

		if self.text != "":
			text_surface = self.font.render(self.text, self.text_antialias, self.text_color)
		elif not self.active and self.placeholder:
			text_surface = self.placeholder.copy()
		else:
			blit_text = False
			if self.text_centered:
				self.distance_left_text = self.rect.w / 2 
			else:
				self.distance_left_text = (self.rect.w - self.text_max_width) / 2

		if blit_text:
			if self.text_centered:
				self.distance_left_text = self.rect.w / 2 - text_surface.get_size()[0] / 2
			else:
				self.distance_left_text = (self.rect.w - self.text_max_width) / 2

			# blit text on actual_surface
			self.actual_surface.blit(text_surface, (self.distance_left_text, self.distance_top_text))


	def event(self, event):
		if self.display_on:
			if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
				mx, my = pg.mouse.get_pos()
				if self.rect.collidepoint((mx, my)):
					if not self.active:
						self.active = True
						self.cursor_position = len(self.text)
						self.ctrl_pressed = False
						self.get_actual_surface()
				else:
					self.active = False
					self.get_actual_surface()

			elif self.active and event.type == pg.KEYDOWN:
				if event.key == 1073742048:
					self.ctrl_pressed = True
				elif event.key == pg.K_BACKSPACE:
					self.text = (self.text[:max(self.cursor_position - 1, 0)] + self.text[self.cursor_position:])
					# Subtract one from cursor_pos, but do not go below zero:
					self.cursor_position = max(self.cursor_position - 1, 0)
					# save actual_surface (with text)
					self.get_actual_surface()
				elif event.key == pg.K_DELETE:
					self.text = (self.text[:self.cursor_position] + self.text[self.cursor_position + 1:])
					self.get_actual_surface()
				elif event.key == pg.K_RETURN:
					self.active = False
					self.get_actual_surface()
					return self.text

				elif event.key == pg.K_RIGHT:
					# Add one to cursor_pos, but do not exceed len(input_string)
					self.cursor_position = min(self.cursor_position + 1, len(self.text))
				elif event.key == pg.K_LEFT:
					# Subtract one from cursor_pos, but do not go below zero:
					self.cursor_position = max(self.cursor_position - 1, 0)
				elif event.key == pg.K_END:
					self.cursor_position = len(self.text)
				elif event.key == pg.K_HOME:
					self.cursor_position = 0

				elif self.ctrl_pressed:
					if event.key == ord("v"):
						string = pyperclip.paste()
						self.text = (self.text[:self.cursor_position] + string + self.text[self.cursor_position:])
						self.cursor_position += len(string)
						self.get_actual_surface()
					elif event.key == ord("c"):
						pyperclip.copy(self.text)
					elif event.key == ord("x"):
						pyperclip.copy(self.text)
						self.text = ""
						self.cursor_position = 0
						self.get_actual_surface()
				else:
					self.text = (self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:])
					self.cursor_position += len(event.unicode)
					self.get_actual_surface()

			elif event.type == pg.KEYUP and event.key == 1073742048:
				self.ctrl_pressed = False

		# if active is False or True
		if event.type == pg.MOUSEMOTION:
			mx, my = pg.mouse.get_pos()
			if self.rect.collidepoint((mx, my)):
				if not self.cursor_ibeam:
					pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_IBEAM)
					self.cursor_ibeam = True
			elif self.cursor_ibeam:
				pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_ARROW)
				self.cursor_ibeam = False

		return False

	def display(self):
		if self.display_on:
			self.screen.blit(self.actual_surface, (self.rect.x, self.rect.y))
			if self.active:
				# display cursor
				cursor_y_pos = self.font.size(self.text[:self.cursor_position])[0]
				if self.cursor_position > 0:
					cursor_y_pos -= self.cursor_surface.get_width()
				self.screen.blit(self.cursor_surface,
					(self.rect.x + cursor_y_pos + self.distance_left_text, self.rect.y + self.distance_top_text))
