from makinreusable.winfunction import *
import time
from image import *

class GrindingMakin(object):
	def __init__(self):
		pass
	
	def start_arena(self):
		pass
	
	def calibrate_position(self):
		win = image_manager.find_bluestack_logo()
		mouse_click_drag(win[0],win[1], 30, 12)
