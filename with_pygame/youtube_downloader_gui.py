import pygame as pg
import time
import os
import random
import numpy as np

# show path
#import sys
#print(sys.path)


# test playing video directly
import cv2
import imutils
import vlc

# my modules
from ft_pg_init import *
from ft_pg_gui import *
from ft_yt_utils import *

BG = (40, 40, 40)
WHITE_TXT = (200, 200, 200)

def random_color():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class MyApp(object):

	def __init__(self):

		self.screen, self.window_width, self.window_height, self.clock, self.fonts = ft_pg_init()
		self.fps = 60
		self.running = True

		self.ft_gui = FtPgGui(self.screen)

		self._init_variables()


	def quit(self):
		pass

	def _init_variables(self):
		self.textbar_url_yt = self.ft_gui.add_input_textbar(id_="urlyt", pos=(200, 100), size=(800, 50), font=self.fonts[30],
								placeholder="Url Youtube Video")

		self.textbar_keyword_yt = self.ft_gui.add_input_textbar(id_="keywordyt", pos=(200, 200), size=(800, 50), font=self.fonts[30],
									placeholder="Search Youtube Video")

		
		self.video_infos_surface = [False, False, False]
		self.downloads_button = []
		for i in range(len(self.video_infos_surface)):
			self.downloads_button.append(self.ft_gui.add_button(id_="button" + str(i), pos=(300 + i * 400, 600),
									size=[300, 50], font=self.fonts[15], text="dl", display_on=False))


	def _pafy_download_callback(self, total, recvd, ratio, rate, eta):
		print(round(ratio * 100, 2), "%")

	def event(self, event):
		ret = self.ft_gui.event(event)
		if ret["input_textbar"][self.textbar_keyword_yt.id_]:

			limit = len(self.video_infos_surface)
			self.videos_infos = search_youtube_video_list(self.textbar_keyword_yt.text, limit=limit)

			for i in range(limit):
				if i < len(self.videos_infos["video_thumbnail_url"]):
					self.video_infos_surface[i] = get_pg_surface_from_youtube_video_info(self.videos_infos, i, 300, 300, BG,
																						self.fonts[20], self.fonts[15], WHITE_TXT)
					self.downloads_button[i].display_on = True
				else:
					self.video_infos_surface[i] = False
					self.downloads_button[i].display_on = False

		for i in range(len(self.downloads_button)):
			if ret["button"][self.downloads_button[i].id_]:
				file_video_name, file_audio_name = download_best_video_youtube(self.videos_infos["video_url"][i], download_path="video", callback=self._pafy_download_callback)


	def display(self, fps=False):
		self.screen.fill(BG)
		
		# display fps
		if not fps:
			fps_real_time_surface = self.fonts[15].render("FPS : -", True, WHITE_TXT)
		else:
			fps_real_time_surface = self.fonts[15].render("FPS : " + str(fps), True, WHITE_TXT)
		self.screen.blit(fps_real_time_surface, (20, 20))
		
		# display thumbnail video
		for i in range(len(self.video_infos_surface)):
			if self.video_infos_surface[i]:
				self.screen.blit(self.video_infos_surface[i], (300 + 400*i, 300))

		self.ft_gui.display()

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