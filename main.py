import pygame as pg
import time
import os

# for loading https images
import requests
import io

# for downloading YouTube video
from pytube import YouTube

# for YouTube search
from youtubesearchpython import VideosSearch

# my modules
from ft_pg_init import *
from ft_pg_interactive import *

BG = (60, 70, 90)
WHITE_TXT = (200, 200, 200)


class MyApp(object):

	def __init__(self):

		self.screen, self.window_width, self.window_height, self.clock, self.fonts = ft_pg_init()
		self.fps = 60
		self.running = True

		self.ft_pg_interactive = FtPgInteractive(self.screen)

		self.ft_pg_interactive.add_input_textbar("url video", pos=(200, 200), size=(800, 50), initial_text="bgoihergiuohego@@@")
		self.ft_pg_interactive.add_input_textbar("blbl", pos=(200, 400), size=(800, 50),
			border_radius=20, font=self.fonts[15])

		self.init_variables()
		#self.yt = YouTube("https://www.youtube.com/watch?v=u4oJhHvqbpo")
		#self.video = self.yt.streams.get_highest_resolution()
		#print(self.video.title, self.yt.video_id, self.yt.age_restricted)
		#self.video.download()
		#url = "https://i.ytimg.com/vi/u4oJhHvqbpo/hqdefault.jpg?sqp=-oaymwEjCOADEI4CSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLBRlf6dgJdsNUqpc6NUKE-LCfJ0tA"
		#r = requests.get(url)
		#img = io.BytesIO(r.content)
		#self.surface = pg.image.load(img)

	def quit(self):
		pass

	def init_variables(self):
		pass

	def event(self, event):
		self.ft_pg_interactive.event(event)

	def display(self, fps=False):
		self.screen.fill(BG)
		
		# display fps
		if not fps:
			fps_real_time_surface = self.fonts[15].render("FPS : -", True, WHITE_TXT)
		else:
			fps_real_time_surface = self.fonts[15].render("FPS : " + str(fps), True, WHITE_TXT)
		self.screen.blit(fps_real_time_surface, (20, 20))
		
		self.ft_pg_interactive.display()

		# refresh the display
		pg.display.flip()


if __name__ == "__main__":

	app = MyApp()
	
	timer = time.time()
	count_fps = 0
	last_count_fps = False
	
	while app.running:
	
		for event in pg.event.get():
			if event.type == pg.QUIT:
				app.running = False
			else:
				app.event(event)
	
		app.display(last_count_fps)
	
		app.clock.tick(app.fps)
	
		count_fps += 1
		if time.time() - timer >= 1:
			last_count_fps = count_fps
			count_fps = 0
			timer = time.time()
	
	app.quit()