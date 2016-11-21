"""
all reusable image processing should be here
"""

import ImageGrab

class ImageManager(object):
	def __init__(self):
		#default image
		self.screen_save = ImageGrab.grab()
		self.screen_loading = self.screen_save
		self.screen_size = (970,632)
		self.screen_width = self.screen_size[0]
		self.screen_height = self.screen_size[1]
		pass
	
	def pixel_search(self, image_grab, x0, y0, x1, y1, color_tuple):
		""" 
		image_grab is the pointer to ImageGrab.grab() result,
		xy is the area to search
		color_tuple in tuple (red, green, blue)
		return tuple (x,y), or False
		"""
		for y in range(y0,y1):
			for x in range(x0,x1):
				if (image_grab.getpixel((x,y))==color_tuple):
					return (x,y)
		return False
		#end pixel_search
	
	
	def find_bluestack_logo(self, width=1366, height=768):
		"""width, height is the screen size, for area to search 
		return bluestack logo coordinate (not left top but guaranted fixed point)
				in tuple (x,y)
		"""
		while True:
			img = ImageGrab.grab()
			icon = self.pixel_search(img, 0,0,width,height, (0x79, 0xaf, 0x1b))
			try:
				if (icon!=False):
					find = self.pixel_search(
									img, 
									icon[0]-8,
									icon[1],
									icon[0]+8,
									icon[1]+10,
									(0xf6, 0xd5, 0x02)
								)
					if (find!=False):
						find = self.pixel_search(
									img, 
									icon[0]-8,
									icon[1],
									icon[0]+8,
									icon[1]+10,
									(0xdd, 0x3a, 0x17)
								)
						if (find!=False):
							#found!!
							return(icon[0]+14, icon[1])
							break;
			except IndexError as e:
				pass#continue searching
		#end find_bluestack_logo
	
	
	def get_grab(self, image_grab):
		""" used many times, check if param is not none, 
		if none, new screen capture will be performed """
		if image_grab==None:
			return ImageGrab.grab()
		return image_grab
		#end get_grab
	
	
	def is_color_similar(self, colorA, colorB,tolerant=10):
		"""check if color is similar, tolerant is the max difference """
		if (
			abs(colorA[0]-colorB[0])<tolerant and
			abs(colorA[1]-colorB[1])<tolerant and
			abs(colorA[2]-colorB[2])<tolerant
		):
			return True
		return False
	
	
	def is_in_more_fight_to_go(self, image_grab=None):
		"""
		check if in one of the 3 fights room 
		displaying score
		"""
		img = self.get_grab(image_grab)
		
		if (img.getpixel((235,338))==(0x2b,0x2c,0x30) and
			img.getpixel((235,416))==(0x2b,0x2c,0x30) and
			img.getpixel((235,500))==(0x2b,0x2c,0x30) and
			img.getpixel((720,338))==(0x2b,0x2c,0x30) and
			img.getpixel((720,416))==(0x2b,0x2c,0x30) and
			img.getpixel((720,500))==(0x2b,0x2c,0x30) and
			img.getpixel((490,338))!=(0x2b,0x2c,0x30) and
			img.getpixel((490,416))!=(0x2b,0x2c,0x30) and
			img.getpixel((490,500))!=(0x2b,0x2c,0x30)
		):
			return True
		
		if (img.getpixel((160,222))==(0x2b,0x2c,0x30) and 
			img.getpixel((816,222))==(0x2b,0x2c,0x30)
		):
			#lose red, win green, 
			lose = (0x72,0x1a,0x1a)
			win = (0x26,0x55,0x2e)
			left_result = img.getpixel((294,280))
			right_result = img.getpixel((697,280))
			if (
				(left_result==win and right_result==lose) or
				(left_result==lose and right_result==win)
			):
				return True
		return False
		#end is_in_more_fight_to_go
		
		
	def is_energy_full(self, image_grab=None):
		"""
		check if energy bar is full, from the screenshot image_grab
		if Not specified image_grab, new screen capture will be performed
		"""
		img = self.get_grab(image_grab)
		
		if not(img.getpixel((499,61))==(0xff,0xe2,0x65)):
			print("can not check energy")
			return False
		
		red,green,blue = img.getpixel(597,62)
		if (red-green)>45 and blue<7:
			return True
		return False
		#end is_energy_full


	def is_menu_button_available(self, image_grab=None):
		""" check if we're in room where we can click menu button """
		img = self.get_grab(image_grab)
		
		if img.getpixel((203,43))==(0x2b,0x2c,0x30):
			return True
		return False
		#end is_menu_button_available
	
	
	def is_in_game_home(self, image_grab=None):
		"""check if in game home, is setting button available"""
		img = self.get_grab(image_grab)
		
		if (img.getpixel((70,53))==(0x2b,0x2c,0x30) and #setting button
			img.getpixel((94,53))==(0x2b,0x2c,0x30) and
			img.getpixel((78,54))==(0x5f,0x5f,0x62) 
		):
			return True
		return False
		#end is_in_game_home
	
	
	def is_in_fighting(self, image_grab=None):
		""" is inside fighting match """
		img  = self.get_grab(image_grab)
		
		#check if there is pause button
		leftborder = img.getpixel((466,57))
		rightborder = img.getpixel((511,57))
		if leftborder==(0x22,0x22,0x22) or leftborder==(0x21,0x21,0x21):
			if rightborder==(0x22,0x22,0x22) or rightborder==(0x21,0x21,0x21):
				return True
		return False
		#end is_in_fighting
	
	
	def is_in_team_adding(self, check_lightdark=False, image_grab=None):
		""" check whether in team adding or not (True or False
		if check_lightdark is True, return value will be "light", "dark", or boolean False
		"""
		img = self.get_grab(image_grab)
		c1 = img.getpixel((18,130))#the left bar team list
		c2 = img.getpixel((936,511))#the champion filter button
		if (c1==c2):
			if (check_lightdark):
				if c1==(0x2b,0x2c,0x30):
					return "light"
				elif c1==(0x0b,0x0b,0x0c):
					return "dark"
			elif c1==(0x2b,0x2c,0x30) or c1==(0x0b,0x0b,0x0c):
				return True
		return False
		#end is_in_team_adding
	
	
	def is_in_team_adding_tier(self, tier, image_grab=None):
		""" only check tier (light), if desired, check is_in_team_adding must be performed separately """
		img = self.get_grab(image_grab)
		if tier==3 and img.getpixel((108,559))==(0x38,0x38,0x38):
			return True
		#TODO: OTHER tier value
		return False
		#end is_in_team_adding_tier
		
	
	def is_stuck(self, image_grab=None):
		"""
		perform check if we're stuck in a room 
		(any current click affects nothing)
		but tries not to set as stuck if known is loading
		return True if stuck, False if not
		"""
		img = self.get_grab(image_grab)
		if (self.is_loading(img)):
			return False
		
		if img.getpixel((100,100))!=self.screen_save.getpixel((100,100)):
			return False
		if img.getpixel((400,100))!=self.screen_save.getpixel((400,100)):
			return False
		if img.getpixel((700,100))!=self.screen_save.getpixel((700,100)):
			return False
		if img.getpixel((100,500))!=self.screen_save.getpixel((100,500)):
			return False
		if img.getpixel((498,298))!=self.screen_save.getpixel((498,298)):
			return False
		if img.getpixel((700,500))!=self.screen_save.getpixel((700,500)):
			return False
		return True
		#end is_stuck
	
	
	def is_loading(self, image_grab=None):
		# check is in loading, update_capture_loading must be up to date
		img = self.get_grab(image_grab)
		if img.getpixel((100,100))!=self.screen_loading.getpixel((100,100)):
			return False
		if img.getpixel((400,100))!=self.screen_loading.getpixel((400,100)):
			return False
		if img.getpixel((700,100))!=self.screen_loading.getpixel((700,100)):
			return False
		if img.getpixel((100,500))!=self.screen_loading.getpixel((100,500)):
			return False
		if img.getpixel((498,298))!=self.screen_loading.getpixel((498,298)):
			return False
		if img.getpixel((700,500))!=self.screen_loading.getpixel((700,500)):
			return False
		return True
		#end is_loading
	
	
	def is_in_leaderboard(self, image_grab=None):
		"""check if it's in leaderboard (throphy button clicked) """
		img = self.get_grab(image_grab)
		if (img.getpixel((921,138))==(0x29,0x2c,0x30) and
			img.getpixel((939,61))==0x6c6e71):
				print("leaderboard")
				return True
		return False
				
		#end is_in_leaderboard
	
	
	def is_in_chat(self, image_grab=None):
		"""check if in chat """
		img = self.get_grab(image_grab)
		if img.getpixel((640,540))==(0x16,0xa1,0x1d):
			if img.getpixel((15,540))==(0x2a,0x2d,0x31):
				return True
		return False
		#end is_in_chat
	
	
	def is_in_bluestack_home(self, image_grab=None):
		"""check if in home / not in the application """
		img = self.get_grab(image_grab)
		plus_logo = self.pixel_search(img, 885,40,945,260, (0xf3,0x80,0x25))
		if plus_logo!=False:
			logo_x, logo_y = plus_logo
			if (img.getpixel((logo_x+1, logo_y+1))==(0xf3,0x80,0x25) and
				image_manager.pixel_search(
					img, logo_x-10, logo_y-10, logo_x+50, logo_y+50,
					(0xff,0xff,0xff)
				)!=False
			):
				print("in bluestack home launcher")
				return True
		return False
		#end is_in_bluestack_home
	
	
	def is_in_bluestack_login(self, image_grab=None):
		"""check if in bluestack login error"""
		img = self.get_grab(image_grab)
		
		check_again = False
		if (self.get_dominant_color(img.getpixel((745,500)) )=="blue" and
			self.get_dominant_color(img.getpixel((847,502)) )=="blue" and
			img.getpixel((70,90,))==(0,0,0) and 
			img.getpixel((290,90,))==(0,0,0) and 
			img.getpixel((300,470,))==(0,0,0) and 
			img.getpixel((860,470,))==(0,0,0)
		):
			time.sleep(2)
			img = ImageGrab.grab()
			check_again = True
			
		if (check_again and
			self.get_dominant_color(img.getpixel((745,500)) )=="blue" and
			self.get_dominant_color(img.getpixel((847,502)) )=="blue" and
			img.getpixel((70,90,))==(0,0,0) and 
			img.getpixel((290,90,))==(0,0,0) and 
			img.getpixel((300,470,))==(0,0,0) and 
			img.getpixel((860,470,))==(0,0,0)
		):	
			print("in bluestack home login error")
			return True
		return False
		#end is_in_bluestack_login

		
	def is_t4b_available(self, image_grab=None):
		"""
		check if in current view (arena room) there is arena t4b 
		"""
		img = self.get_grab(image_grab)
		step = 75
		for y_code in range(0,self.screen_height):
			for x_code in range(0,self.screen_width):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(56,58,70)) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+0)),(172,175,190)) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+75)),(50,53,62)) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+75)),(83,86,103)) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+150)),(38,38,46)) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+150)),(145,148,167))
				):
					return x_code,y_code
		return -1,-1
		#end is_t4b_available
		
	def is_in_fight_room(self, image_grab=None):
		"""
		check if in fight room (menu->fight)
		will check for alliance mode button
		"""
		img = self.get_grab(image_grab)
		step = 75
		for y_code in range(0,self.screen_height):
			for x_code in range(0,self.screen_width):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(17,58,96),20) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+0)),(48,124,164),20) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+75)),(93,159,211),20) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+75)),(172,214,238),20)
				):
					return x_code,y_code
		return -1,-1
		#end is_in_fight_room

	
	def is_team_adding_need_help(self, image_grab=None):
		"""check if in team adding we have champion to be asked for help"""
		img = self.get_grab(image_grab)
		if self.get_dominant_color(img.getpixel((260,175)))=="green":
			return True
		return False
		#end is_team_adding_need_help

	
	def is_in_milestone_info(self, image_grab=None):
		img = self.get_grab(image_grab)
		if self.get_dominant_color(img.getpixel((934,55)))=="green":
			if img.getpixel((492,337))==(0x2b,0x2c,0x30):
				return True
		return False
		#is_in_milestone_info


	def update_capture(self):
		"""capture current image"""
		self.screen_save = ImageGrab.grab()
		#end update_capture

	def update_capture_loading(self):
		img = ImageGrab.grab()
		signif = [(0,0,0)]*6
		signif[0] = img.getpixel(100,100)
		signif[1] = img.getpixel(400,100)
		signif[2] = img.getpixel(700,100)
		signif[3] = img.getpixel(100,500)
		signif[4] = img.getpixel(498,298)
		signif[5] = img.getpixel(700,500)
		self.screen_loading = img
		print("loading captured")
		print(signif)
		#end update_capture_loading
	
	
	
	
	def get_dominant_color(self, color_tuple):
		"""
		return string "red", "green", or "blue" of dominant color
		from parameter color_tuple in tuple form (red, green, blue)
		"""
		red, green, blue = color_tuple
		if (red>green and red>blue):
			return "red"
		elif (green>blue and green>red):
			return "green"
		elif (blue>red and blue>green):
			return "blue"
		else:
			if red>green or red>blue:
				return "red"
			elif green>blue or green>red:
				return "green"
			else:
				return "blue"
		#end get_dominant_color
	
	
	def get_dominant_color_grab(self, x,y):
		"""grab current screen then get dominant color in coordinate x,y"""
		return self.get_dominant_color(ImageGrab.grab().getpixel((x,y)))
		#end get_dominant_color_grab
	
	
	
	
	
image_manager = ImageManager()
