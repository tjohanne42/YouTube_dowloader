import pygame as pg

# my modules
from ft_pg_input_textbar import *


class FtPgGui(object):

	def __init__(self, screen):

		self.screen = screen
		#self.buttons = []
		self.input_textbar = []
		pg.key.set_repeat(400, 35)


	def add_input_textbar(self, **kwargs):
		args = (self.screen)
		for key, value in kwargs.items():
			args = (*args, {key:value})
		print(args)
		self.input_textbar.append(FtPgInputTextbar(args))
		return self.input_textbar[-1]


	def event(self, event):
		for textbar in self.input_textbar:
			ret = textbar.event(event)


	def display(self):
		for textbar in self.input_textbar:
			textbar.display()
