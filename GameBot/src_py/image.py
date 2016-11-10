"""
all reusable image processing should be here
"""

import ImageGrab

class ImageManager(object):
	def __init__(self):
		#default image
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
	
	
	def is_inside_fighting(self, image_grab=None):
		""" is inside fighting match """
		img  = self.get_grab(image_grab)
		
		#check if there is pause button
		leftborder = img.getpixel((466,57))
		rightborder = img.getpixel((511,57))
		if leftborder==(0x22,0x22,0x22) or leftborder==(0x21,0x21,0x21):
			if rightborder==(0x22,0x22,0x22) or rightborder==(0x21,0x21,0x21):
				return True
		return False
		#end is_inside_fighting
	
	
	def is_in_team_adding(self, image_grab=None):
		img = self.get_grab(image_grab)
		#TODO:
		return False
		#end is_in_team_adding
	
	
	def is_in_team_adding_tier(self, tier, image_grab=None):
		img = self.get_grab(image_grab)
		#TODO:
		return False
		
	
	
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
		self.get_dominant_color(ImageGrab.grab().getpixel((x,y)))
		#end get_dominant_color_grab
	
	
	
	
	
image_manager = ImageManager()
