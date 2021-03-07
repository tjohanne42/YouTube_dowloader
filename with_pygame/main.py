import pygame as pg
import time
import os
import random
import numpy as np

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
import imutils
#from pyimagesearch.nms import non_max_suppression_slow

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


def non_max_suppression_fast(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
	# initialize the list of picked indexes	
	pick = []
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("int")


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
			for audiostreams in video.audiostreams:
				print(audiostreams)
			best_video = video.getbestvideo()
			best_audio = video.getbestaudio()
			print("best audio :", best_audio.extension)
			print("bitrate :", best_audio.bitrate)
			print("quality :", best_audio.quality)
			print("rawbitrate :", best_audio.rawbitrate)

			#best_audio.download()
			#best_video.download()

			video_url = best_video.url
			audio_url = best_audio.url

			# play audio
			import vlc
			instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
			player=instance.media_player_new()
			media=instance.media_new(audio_url)
			player.set_media(media)
			player.play()

			"""
			get_time(self)
			Get the current movie time (in ms).	source code
 	
			set_time(self, i_time)
			Set the movie time (in ms).	source code
 	
			get_position(self)
			Get movie position as percentage between 0.0 and 1.0.	source code
 	
			set_position(self, f_pos)
			Set movie position as percentage between 0.0 and 1.0.

			audio_get_volume(self)
			Get current software audio volume.	source code
 	
			audio_set_volume(self, i_volume)
			Set current software audio volume.
			"""

			# play video
			cap = cv2.VideoCapture(video_url)
			fps = cap.get(cv2.CAP_PROP_FPS)
			print("fps =", fps)
			if not cap.isOpened():
				print("File Cannot be Opened")

			# init ORB // not working
			#orb = cv2.ORB()

			# init HOG
			#hog = cv2.HOGDescriptor()
			#hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

			while(True):
				# Capture frame-by-frame
				ret, frame = cap.read()
				#print cap.isOpened(), ret
				if frame is not None:
					# faces detection
					#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
					#eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
					#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					#faces = face_cascade.detectMultiScale(gray, 1.3, 5)
					#for (x,y,w,h) in faces:
					#	frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
					#	roi_gray = gray[y:y+h, x:x+w]
					#	roi_color = frame[y:y+h, x:x+w]
					#	eyes = eye_cascade.detectMultiScale(roi_gray)
					#	for (ex,ey,ew,eh) in eyes:
					#		cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

					# draw contours
					#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
					#edged = cv2.Canny(gray, 30, 200)
					#contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
					#cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

					# ORB // not working
					#kp = orb.detect(frame,None)
					#kp, des = orb.compute(frame, kp)
					#img2 = cv2.drawKeypoints(frame,kp,color=(0,255,0), flags=0)

					# HSV colored object tracking
					#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
					#lower_blue = np.array([110,50,50])
					#upper_blue = np.array([130,255,255])
					#mask = cv2.inRange(hsv, lower_blue, upper_blue)
					#res = cv2.bitwise_and(frame,frame, mask= mask)

					# canny Edge
					#frame = cv2.Canny(frame,100,200)

					# fourrier transform // pas compris
					#f = np.fft.fft2(frame)
					#fshift = np.fft.fftshift(f)
					#magnitude_spectrum = 20*np.log(np.abs(fshift))
					#rows, cols, _ = frame.shape
					#crow,ccol = int(rows/2) , int(cols/2)
					#fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
					#f_ishift = np.fft.ifftshift(fshift)
					#img_back = np.fft.ifft2(f_ishift)
					#img_back = np.abs(img_back)

					# draw circles // not working
					#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
					#img = cv2.medianBlur(gray,5)
					#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
					#circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
					#                            param1=50,param2=30,minRadius=0,maxRadius=0)
					#circles = np.uint16(np.around(circles))
					#for i in circles[0,:]:
						# draw the outer circle
					#    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
						# draw the center of the circle
					#    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

					# draw body
					#found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
					#for x, y, w, h in found:
					#	pad_w, pad_h = int(0.15*w), int(0.05*h)
					#	cv2.rectangle(frame, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), 1)

					#draw body v2
					#frame = imutils.resize(frame , width=min(800, frame.shape[1]))
					#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
					#bounding_box_cordinates, weights =  hog.detectMultiScale(gray, winStride = (4, 4),
					#	padding = (8, 8), scale = 1.03)
					#bounding_box_cordinates, weights =  hog.detectMultiScale(frame, winStride = (4, 4),
					#	padding = (8, 8), scale = 1.10, useMeanshiftGrouping=True)
					#person = 1
					#pick = non_max_suppression_fast(bounding_box_cordinates, 0.3)
					#for x,y,w,h in bounding_box_cordinates:
					#	cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
					#	cv2.putText(frame, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
					#	person += 1
					#cv2.putText(frame, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
					#cv2.putText(frame, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
					#cv2.imshow('output', frame)

					cv2.imshow('frame', frame)
					#cv2.imshow('edges', edges)
					#cv2.imshow('fourrier', img_back)
					#cv2.imshow('circles', cimg)
					#cv2.imshow('mask', mask)
					#cv2.imshow('res', res)

					if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
						break
				else:
					print("Frame is None")
					break
			cap.release()
			cv2.destroyAllWindows()

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