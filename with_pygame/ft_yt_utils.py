from youtubesearchpython import VideosSearch
import pafy
import os

import pygame as pg
import requests
import io

def	get_pg_surface_from_youtube_video_info(video_info, i, width, height, bg, big_font, small_font, font_color):
	surface = pg.Surface((width, height))
	surface.fill(bg)
	
	# video thumbnail
	r = requests.get(video_info["video_thumbnail_url"][i])
	img = io.BytesIO(r.content)
	video_thumbnail_surface = pg.image.load(img)
	video_thumbnail_surface = pg.transform.scale(video_thumbnail_surface, (width, int(height / 2)))
	surface.blit(video_thumbnail_surface, (0, 0))
	y = int(height / 2)

	# duration, view_count, title, date publish
	tmp_str = video_info["video_title"][i]
	tmp_surface = big_font.render(tmp_str, True, font_color)
	surface.blit(tmp_surface, (0, y))
	y += tmp_surface.get_size()[1]

	str_duration_views = video_info["video_duration"][i] + " min   " + video_info["video_view_count"][i]
	duration_views_surface = small_font.render(str_duration_views, True, font_color)
	surface.blit(duration_views_surface, (0, y))
	y += duration_views_surface.get_size()[1]

	tmp_str = video_info["video_published_time"][i]
	tmp_surface = small_font.render(tmp_str, True, font_color)
	surface.blit(tmp_surface, (0, y))
	y += tmp_surface.get_size()[1]

	# channel thumbnail
	r = requests.get(video_info["video_channel_thumbnail_url"][i])
	img = io.BytesIO(r.content)
	video_channel_thumbnail_surface = pg.image.load(img)
	video_channel_thumbnail_surface = pg.transform.scale(video_channel_thumbnail_surface, (int(width / 2), int(height - y)))
	surface.blit(video_channel_thumbnail_surface, (0, y))

	# channel name
	channel_name_surface = small_font.render(video_info["video_channel_name"][i], True, font_color)
	surface.blit(channel_name_surface, (width / 2, y + (height - y) / 2 - channel_name_surface.get_size()[1] / 2))

	return surface

def	search_youtube_video_list(search, limit=1):
	videos_infos = 	{
					"video_url": [],
					"video_thumbnail_url": [],
					"video_title": [],
					"video_duration": [],
					"video_published_time": [],
					"video_view_count": [],
					"video_channel_name": [],
					"video_channel_thumbnail_url": []
					}
	videosSearch = VideosSearch(search, limit=limit, language="en", region="us")
	result_size = len(videosSearch.result()["result"])
	for i in range(0, min(limit, result_size)):
		videos_infos["video_url"].append(videosSearch.result()["result"][i]["link"])
		videos_infos["video_thumbnail_url"].append(videosSearch.result()["result"][i]["thumbnails"][0]["url"])
		videos_infos["video_title"].append(videosSearch.result()["result"][i]["title"])
		videos_infos["video_duration"].append(videosSearch.result()["result"][i]["duration"])
		videos_infos["video_published_time"].append(videosSearch.result()["result"][i]["publishedTime"])
		videos_infos["video_view_count"].append(videosSearch.result()["result"][i]["viewCount"]["short"])
		videos_infos["video_channel_name"].append(videosSearch.result()["result"][i]["channel"]["name"])
		videos_infos["video_channel_thumbnail_url"].append(videosSearch.result()["result"][i]["channel"]["thumbnails"][0]["url"])
	return videos_infos


def download_best_video_youtube(url, download_path="", callback=None):
	"""
	func:
		download the video with the best audio and video quality
		the audio is download as "ogg"
	params:
		url -> url of the video to get
		download_path -> path to download the video
	return:
		file_video_name -> path to video file
		file_audio_name -> path to audio file
	"""
	video = pafy.new(url)
	video_title = video.title.replace("|", " ").encode("ascii", "ignore").decode()

	best_audio = video.getbestaudio()
	best_video = video.getbestvideo()

	# best_audio_url = best_audio.url
	# best_video_url = best_video.url

	# download files
	file_audio_name = download_path + "/aud" + video_title + "." + best_audio.extension
	file_video_name = download_path + "/vid" + video_title + "." + best_video.extension

	best_audio.download(filepath=file_audio_name, callback=callback, quiet=True)
	best_video.download(filepath=file_video_name, callback=callback, quiet=True)

	# convert audio file to "ogg"
	file_audio_name_ogg = download_path + "/aud" + video_title + ".ogg"
	if not os.path.isfile(file_audio_name_ogg) and best_audio.extension != "ogg":
		os.system(f'ffmpeg -loglevel panic -i "{file_audio_name}" -vn "{file_audio_name_ogg}"')
		file_audio_name = file_audio_name_ogg

	return file_video_name, file_audio_name