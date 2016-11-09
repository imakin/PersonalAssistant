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
		for x in range(x0,x1):
			for y in range(y0,y1):
				if (image_grab.getpixel((x,y))==color_tuple):
					return (x,y)
		return False
	
	
	def find_bluestack_logo(self, width=1366, height=768):
		"""width, height is the screen size, for area to search 
		return bluestack logo coordinate (not left top but guaranted fixed point)
				in tuple (x,y)
		"""
		while True:
			img = ImageGrab.grab()
			icon = self.pixel_search(img, 0,0,width,height, (0x79, 0xaf, 0x1b))
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
	
image_manager = ImageManager()
