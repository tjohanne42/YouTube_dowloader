from ft_pg_init import *
from ft_pg_gui import *
from ft_yt_utils import *

BG = (40, 40, 40)
WHITE_TXT = (200, 200, 200)

class MyApp(object):

	def __init__(self):

		self.screen, self.window_width, self.window_height, self.clock, self.fonts = ft_pg_init()
		self.fps = 60
		self.running = True

		self.ft_gui = FtPgGui(self.screen)

		self._init_variables()


	def quit(self):
		self.running = False


	def _init_variables(self):
		self.button1 = self.ft_gui.add_button(id_="button1", pos=(10, 10),
									size=[100, 50], font=self.fonts[15], text="play", display_on=True)


	def event(self, event):
		ret = self.ft_gui.event(event)

		if self.button1.click():
			print("clicked")


	def display(self, fps):
		self.screen.fill(BG)

		if not fps:
			fps_real_time_surface = self.fonts[15].render("FPS : -", True, WHITE_TXT)
		else:
			fps_real_time_surface = self.fonts[15].render("FPS : " + str(fps), True, WHITE_TXT)
		self.screen.blit(fps_real_time_surface, (20, 20))

		# display gui interface
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