"""
all reusable image processing should be here
"""
from rescaler import cx,cy
import ImageGrab
import time

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
	
	
	def get_arena_target(self, image_grab=None, desired="any tier 3"):
		"""
		This is the method called to get arena tier target,
		replace this method's image processing as needed
		@return
			the corresponding continue button position if found, 
			or (-1,-1) if false
		@param desired "any tier 3", "cornucopia"
		"""
		
		#~ desired = "any tier 3"
		print("target is "+desired)
		"""
		current: orb of agamoto dr strange
		"""
		if (desired=="dr strange"):
			img = self.get_grab(image_grab)
			step = 15
			coltol = 50
			for y_code in range(300,380):
				for x_code in range(0,self.screen_width):
					if (
						self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(204,138,48),coltol) and
						self.is_color_similar(img.getpixel((x_code+15,y_code+0)),(232,182,72),coltol) and
						self.is_color_similar(img.getpixel((x_code+30,y_code+0)),(251,245,253),coltol) and
						self.is_color_similar(img.getpixel((x_code+0,y_code+15)),(92,65,98),coltol) and
						self.is_color_similar(img.getpixel((x_code+15,y_code+15)),(153,135,175),coltol) and
						self.is_color_similar(img.getpixel((x_code+30,y_code+15)),(234,191,214),coltol) and
						self.is_color_similar(img.getpixel((x_code+0,y_code+30)),(92,63,93),coltol) and
						self.is_color_similar(img.getpixel((x_code+15,y_code+30)),(162,105,32),coltol) and
						self.is_color_similar(img.getpixel((x_code+30,y_code+30)),(12,3,3),coltol)
					):
						return x_code+100,y_code+200
			return -1,-1
		
		elif desired=="cornucopia":
			"""
			Crystal cornucopia
			"""
			img = self.get_grab(image_grab)
			step = 20
			coltol = 30
			for y_code in range(315,350):
				for x_code in range(0,self.screen_width):
					if (
						self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(139,147,164),coltol) and
						self.is_color_similar(img.getpixel((x_code+20,y_code+0)),(185,22,10),coltol) and
						self.is_color_similar(img.getpixel((x_code+0,y_code+20)),(158,173,122),coltol) and
						self.is_color_similar(img.getpixel((x_code+20,y_code+20)),(231,128,61),coltol)
					):
						return x_code,y_code+200
			return -1,-1
		
		elif desired=="any tier 3":
			"""for any tier 3, search for 1v1 and calculate tier 3's continue button"""
			img = self.get_grab(image_grab)
			step = 10
			coltol = 30
			for y_code in range(cy(220),cy(240)):
				for x_code in range(cx(0),cx(100)):
					if (
						self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(199,169,62),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(0))),(219,148,79),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(0))),(207,48,15),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(30),y_code+cy(0))),(67,11,6),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(40),y_code+cy(0))),(51,11,19),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(50),y_code+cy(0))),(37,16,32),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(60),y_code+cy(0))),(45,22,57),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(70),y_code+cy(0))),(73,47,128),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(80),y_code+cy(0))),(43,34,70),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(90),y_code+cy(0))),(80,106,214),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(100),y_code+cy(0))),(162,144,211),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(10))),(190,166,155),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(10))),(233,225,216),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(10))),(183,165,147),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(30),y_code+cy(10))),(253,253,253),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(40),y_code+cy(10))),(198,185,191),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(50),y_code+cy(10))),(179,164,175),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(60),y_code+cy(10))),(139,114,137),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(70),y_code+cy(10))),(252,250,251),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(80),y_code+cy(10))),(197,192,221),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(90),y_code+cy(10))),(126,143,253),coltol) and
						self.is_color_similar(img.getpixel((x_code+cx(100),y_code+cy(10))),(210,189,254),coltol)
					):
						return x_code+cx(730),y_code+cy(300)
			return -1,-1
		#end get_arena_target

	
	def is_color_similar(self, colorA, colorB,tolerant=10):
		"""check if color is similar, tolerant is the max difference """
		if (
			abs(colorA[0]-colorB[0])<tolerant and
			abs(colorA[1]-colorB[1])<tolerant and
			abs(colorA[2]-colorB[2])<tolerant
		):
			return True
		return False
	
	
	def is_in_rearrange_team(self, image_grab=None):
		"""
		check if in rearrange team, looking for opponent (i) button
		"""
		img = self.get_grab(image_grab)
		step = 5
		coltol = 10
		for y_code in range(167,200):
			for x_code in range(812,850):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+5,y_code+0)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+0)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+15,y_code+0)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+0)),(43,45,49),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+5)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+5,y_code+5)),(90,91,91),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+5)),(78,78,80),coltol) and
					self.is_color_similar(img.getpixel((x_code+15,y_code+5)),(101,101,101),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+5)),(44,45,49),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+10)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+5,y_code+10)),(101,101,101),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+10)),(54,55,58),coltol) and
					self.is_color_similar(img.getpixel((x_code+15,y_code+10)),(101,101,101),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+10)),(101,101,101),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+15)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+5,y_code+15)),(101,101,101),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+15)),(65,65,68),coltol) and
					self.is_color_similar(img.getpixel((x_code+15,y_code+15)),(101,101,101),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+15)),(100,100,100),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+20)),(43,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+5,y_code+20)),(75,76,78),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+20)),(87,87,89),coltol) and
					self.is_color_similar(img.getpixel((x_code+15,y_code+20)),(95,95,95),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+20)),(43,44,48),coltol)
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
	
	
	def is_in_team_adding_tier_2(self, image_grab=None):
		"""
		check if in tier 2 team adding
		"""
		img = self.get_grab(image_grab)
		step = 5
		coltol = 10
		for y_code in range(547,548):
			for x_code in range(94,95):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(49,48,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(0))),(49,48,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(0))),(49,48,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(15),y_code+cy(0))),(49,48,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(0))),(49,48,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(5))),(55,52,45),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(5))),(44,44,44),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(5))),(44,44,44),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(15),y_code+cy(5))),(62,62,62),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(5))),(60,60,60),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(10))),(53,49,41),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(10))),(42,42,42),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(10))),(42,42,42),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(15),y_code+cy(10))),(60,60,60),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(10))),(60,60,60),coltol)
				):
					return True
		return False
		#end is_in_team_adding_tier_2
	
	
	def is_in_team_adding_tier_3(self, image_grab=None):
		"""
		check if in tier 3 team adding
		check for disabled find match button with 400 gold price
		"""
		img = self.get_grab(image_grab)
		step = 5
		coltol = 10
		for y_code in range(547,555):
			for x_code in range(100,108):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(46,46,46),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(0))),(49,49,49),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(0))),(47,47,47),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(15),y_code+cy(0))),(50,50,50),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(0))),(49,49,49),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(25),y_code+cy(0))),(50,50,50),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(5))),(44,44,44),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(5))),(44,44,44),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(5))),(61,61,61),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(15),y_code+cy(5))),(44,44,44),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(5))),(54,54,54),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(25),y_code+cy(5))),(44,44,44),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(10))),(41,41,41),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(10))),(42,42,42),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(10))),(50,50,50),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(15),y_code+cy(10))),(53,53,53),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(10))),(54,54,54),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(25),y_code+cy(10))),(53,53,53),coltol)
				):
					return True
		return False
		#end is_in_team_adding_tier_3
	
	
	def is_in_team_adding_tier_1(self, image_grab=None):
		"""
		check in tier 1 disabled or enabled button
		"""
		img = self.get_grab(image_grab)
		step = 5
		coltol = 10
		#check for disabled find match button
		for y_code in range(549,550):
			for x_code in range(104,105):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(7,82,5),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(0))),(7,82,5),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(0))),(7,82,5),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(5))),(5,78,4),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(5))),(24,92,23),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(5))),(5,78,4),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(10))),(4,75,2),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(10))),(23,88,21),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(10))),(8,78,6),coltol)
				):
					return True
		#check for enabled button
		for y_code in range(551,552):
			for x_code in range(108,109):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(7,81,6),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(0))),(59,118,58),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(5))),(5,77,3),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(5))),(35,99,33),coltol)
				):
					return True
		return False
		#end is_in_team_adding_tier_1
	
	
	def is_in_team_adding_tier(self, tier, image_grab=None):
		""" only check tier (light), if desired, check is_in_team_adding must be performed separately """
		#~ img = self.get_grab(image_grab)
		#~ if tier==3 and img.getpixel((108,559))==(0x38,0x38,0x38):
			#~ return True
		if tier==3:
			if self.is_in_team_adding_tier_3():
				return True
			elif self.is_in_team_adding_tier_1():
				return False
			elif self.is_in_team_adding_tier_2():
				return False
			else:
				print("tier 3: as long as not tier 1 and 2 is accepted")
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
		"""privately used by is_stuck
		# check is in loading, update_capture_loading must be up to date
		"""
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
	
	
	def is_in_popup(self, image_grab=None):
		"""
		is_in_leaderboard, is_in_chat, etc has close button
		this method detect if there are any popup that has close button, 
		returns coordinate of the close button or -1,-1
		"""
		img = self.get_grab(image_grab)
		step = 10
		coltol = 10
		for y_code in range(cy(15),cy(60)):
			for x_code in range(cx(910),cx(950)):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(41,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(0))),(41,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(0))),(41,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(10))),(41,44,48),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(10))),(108,110,113),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(10))),(107,109,112),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(20))),(45,48,52),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(20))),(107,109,112),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(20),y_code+cy(20))),(108,110,113),coltol)
				):
					return x_code+cx(15),y_code+cy(15)
		return -1,-1
		#end is_in_popup
	
	
	def is_in_leaderboard(self, image_grab=None):
		"""check if it's in leaderboard (throphy button clicked) """
		img = self.get_grab(image_grab)
		if (img.getpixel((921,138))==(0x29,0x2c,0x30) and
			img.getpixel((939,61))==0x6c6e71):
				print("leaderboard")
				return True
		return False
				
		#end is_in_leaderboard
	
	
	def is_in_loading(self, image_grab=None):
		"""
		doc
		"""
		img = self.get_grab(image_grab)
		step = 40
		coltol = 50
		for y_code in range(29,39):
			for x_code in range(714,726):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(18,59,84),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(40),y_code+cy(0))),(28,61,86),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(80),y_code+cy(0))),(26,57,82),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(120),y_code+cy(0))),(15,40,56),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(40))),(37,71,105),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(40),y_code+cy(40))),(38,90,121),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(80),y_code+cy(40))),(36,78,111),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(120),y_code+cy(40))),(22,56,73),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(80))),(52,77,125),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(40),y_code+cy(80))),(49,98,140),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(80),y_code+cy(80))),(31,94,134),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(120),y_code+cy(80))),(34,83,116),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(120))),(151,134,202),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(40),y_code+cy(120))),(70,103,154),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(80),y_code+cy(120))),(81,159,192),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(120),y_code+cy(120))),(51,138,169),coltol)
				):
					return True
		return False
		#end is_in_loading
		
	
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


	def is_in_arena_room(self, image_grab=None):
		"""
		check if in arena room where we can choose which versus tier
		scan for multiverse arena button inactive tab
		"""
		img = self.get_grab(image_grab)
		step = 10
		coltol = 10
		for y_code in range(100,125):
			for x_code in range(0,self.screen_width):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(63,63,63),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+0)),(63,63,63),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+0)),(63,63,63),coltol) and
					self.is_color_similar(img.getpixel((x_code+30,y_code+0)),(63,63,63),coltol) and
					self.is_color_similar(img.getpixel((x_code+40,y_code+0)),(63,63,63),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+10)),(64,64,64),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+10)),(109,109,109),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+10)),(215,215,215),coltol) and
					self.is_color_similar(img.getpixel((x_code+30,y_code+10)),(85,85,85),coltol) and
					self.is_color_similar(img.getpixel((x_code+40,y_code+10)),(67,67,67),coltol)
				):
					return True
		return False

		
	def get_arena_t4b_button(self, image_grab=None):
		"""
		check if in current view (arena room) there is arena t4b 
		return the place where the text "catalyst clash - basic"
		"""
		
		img = self.get_grab(image_grab)
		step = 10
		coltol = 50
		for y_code in range(226,264):
			for x_code in range(0,self.screen_width):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(42,43,47),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+0)),(43,44,49),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+0)),(40,39,45),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+10)),(29,30,35),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+10)),(252,252,252),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+10)),(32,33,38),coltol) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+20)),(39,39,49),coltol) and
					self.is_color_similar(img.getpixel((x_code+10,y_code+20)),(216,216,218),coltol) and
					self.is_color_similar(img.getpixel((x_code+20,y_code+20)),(244,244,244),coltol)
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
		for y_code in range(141,327):
			for x_code in range(100,self.screen_width):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(17,58,96),20) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+0)),(48,124,164),20) and
					self.is_color_similar(img.getpixel((x_code+0,y_code+75)),(93,159,211),20) and
					self.is_color_similar(img.getpixel((x_code+75,y_code+75)),(172,214,238),20)
				):
					return True
		return False
		#end is_in_fight_room

	
	def is_in_find_match(self, image_grab=None):
		"""
		in find match where we can choose enemy player and decide which 
		is the most effective regarding score and difficulty.
		searching for "find new match" button with 5 unit cost
		"""
		img = self.get_grab(image_grab)
		step = 50
		#~ for y_code in range(0,self.screen_height):
			#~ for x_code in range(0,self.screen_width):
		for y_code in range(517,556):
			for x_code in range(609,668):
				if (
					self.is_color_similar(img.getpixel((x_code+0,y_code+0)),(54,121,53)) and
					self.is_color_similar(img.getpixel((x_code+50,y_code+0)),(53,121,51)) and
					self.is_color_similar(img.getpixel((x_code+100,y_code+0)),(154,188,153))
				):
					return True
		return False
		#end is_in_find_match
	
	def is_team_adding_need_help(self, image_grab=None):
		"""check if in team adding we have champion to be asked for help"""
		img = self.get_grab(image_grab)
		if self.get_dominant_color(img.getpixel((260,175)))=="green":
			return True
		return False
		#end is_team_adding_need_help


	def is_team_adding_all_recharging(self, image_grab=None):
		"""
		return True if less than 3 champions is ready
		"""
		img = self.get_grab(image_grab)
		step = 5
		coltol = 10
		for y_code in range(177,179):
			for x_code in range(608,610):
				if (
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(0))),(168,39,31),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(0))),(225,185,183),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(0))),(224,183,181),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(5))),(241,240,239),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(5))),(162,37,29),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(5))),(239,238,238),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(0),y_code+cy(10))),(170,88,83),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(5),y_code+cy(10))),(154,35,26),coltol) and
					self.is_color_similar(img.getpixel((x_code+cx(10),y_code+cy(10))),(224,224,224),coltol)
				):
					return True
		return False
		#end is_team_adding_all_recharging
	
	
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
