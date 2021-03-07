import pygame as pg
import time
import os
import random

# show path
#import sys
#print(sys.path)

# for loading https images
import requests
import io

# for downloading YouTube video
from pytube import YouTube

# for YouTube search
from youtubesearchpython import VideosSearch

# test playing video directly
import pafy
import cv2

# my modules
from ft_pg_init import *
from ft_pg_gui import *

BG = (40, 40, 40)
WHITE_TXT = (200, 200, 200)

def random_color():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def callback(self, player):

	print('FPS =',  player.get_fps())
	print('time =', player.get_time(), '(ms)')
	print('FRAME =', .001 * player.get_time() * player.get_fps())


class MyApp(object):

	def __init__(self):

		self.screen, self.window_width, self.window_height, self.clock, self.fonts = ft_pg_init()
		print("wm info :", pg.display.get_wm_info())

		print("Using {} renderer".format(pg.display.get_driver()))
		self.fps = 60
		self.running = True

		self.ft_gui = FtPgGui(self.screen)

		self.input_textbar = self.ft_gui.add_input_textbar(pos=(200, 200), size=(800, 50), font=self.fonts[30],
								placeholder="Search Youtube Video")

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
		self.video_thumbnail_surface = False

	def event(self, event):
		ret = self.ft_gui.event(event)
		if ret:
			# search with string "ret" and save all info
			videosSearch = VideosSearch(ret, limit=1)
			#videosSearch.result()
			try:
				video_link = videosSearch.result()["result"][0]["link"]
				video_thumbnail_link = videosSearch.result()["result"][0]["thumbnails"][0]["url"]
				video_title = videosSearch.result()["result"][0]["title"]
				video_duration = videosSearch.result()["result"][0]["duration"]
				video_publishedTime = videosSearch.result()["result"][0]["publishedTime"]
				video_viewCount = videosSearch.result()["result"][0]["viewCount"]["short"]
				video_channel_name = videosSearch.result()["result"][0]["channel"]["name"]
				video_channel_thumbnails_link = videosSearch.result()["result"][0]["channel"]["thumbnails"][0]["url"]
				# load thumbnail image into self.video_thumbnail_surface
				r = requests.get(video_thumbnail_link)
				img = io.BytesIO(r.content)
				self.video_thumbnail_surface = pg.image.load(img)
			except:
				self.video_thumbnail_surface = self.fonts[30].render("No result for :  " + ret, True, WHITE_TXT)
			
			# get video with pafy
			video = pafy.new(video_link)
			best_video = video.getbestvideo()
			best_audio = video.getbestaudio()
			print("bitrate :", best_audio.bitrate)
			print("quality :", best_audio.quality)
			print("rawbitrate :", best_audio.rawbitrate)

			best_audio.download()
			best_video.download()

			video_url = best_video.url
			audio_url = best_audio.url

			cap = cv2.VideoCapture(video_url)
			fps = cap.get(cv2.CAP_PROP_FPS)
			print("fps =", fps)
			if not cap.isOpened():
				print("File Cannot be Opened")

			while(True):
				# Capture frame-by-frame
				ret, frame = cap.read()
				#print cap.isOpened(), ret
				if frame is not None:
					# Display the resulting frame
					cv2.imshow('frame',frame)
					# Press q to close the video windows before it ends if you want
					if cv2.waitKey(22) & 0xFF == ord('q'):
						break
				else:
					print("Frame is None")
					break
			
	def display(self, fps=False):
		self.screen.fill(BG)
		
		# display fps
		if not fps:
			fps_real_time_surface = self.fonts[15].render("FPS : -", True, WHITE_TXT)
		else:
			fps_real_time_surface = self.fonts[15].render("FPS : " + str(fps), True, WHITE_TXT)
		self.screen.blit(fps_real_time_surface, (20, 20))
		
		# display thumbnail video
		if self.video_thumbnail_surface:
			self.screen.blit(self.video_thumbnail_surface, (200, 300))

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