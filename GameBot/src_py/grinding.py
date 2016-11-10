from makinreusable.winfunction import *
import time
from image import *

class GrindingMakin(object):
	def __init__(self):
		self.status = ""
		self.quest_active = False
		
		self.arena_stop = False
		self.arena_stack = 0
		self.arena_matches = 0
		self.arena_help = 30#when matches hit multiplier of this value, help alliance
		self.arena_tier = 3#the tier in arena to pick
		
		self.arena_continue = True #inside arena loop status
		
	def calibrate_position(self):
		win = image_manager.find_bluestack_logo()
		mouse_click_drag(win[0],win[1], 30, 12)
		#end calibrate_position

	def start_arena(self):
		self.status = "start arena"
		self.arena_stop = False
		
		while not(self.arena_stop):
			self.arena_stack += 1
			self.arena_matches += 1
			self.calibrate_position()
			
			img = ImageGrab.grab()
			
			if (	self.quest_active and 
					image_manager.is_menu_button_available(img) and
					image_manager.is_energy_full(img)
			):
				pass
				self.arena_stop = True
				##TODO: quest_play()
			
			
			print("match number :", self.arena_matches)
			
			#helping
			if (	self.arena_matches%self.arena_help==0 and 
					image_manager.is_menu_button_available(img)
			):
				helping = self.alliance_help()
				if (not helping):
					self.matches -= 1 #make sure we keep trying in the next chance
			
			self.arena_continue = True
			if (not self.arena_stop):
				self.arena_check_inside_fighting()
				time.sleep(0.5)
				
				if self.arena_tier==5:
					mouse_click_drag(700,255,130,255,1)
					time.sleep(0.5)
					mouse_click_drag(700,255,130,255,1)
					time.sleep(0.5)
				else:
					if (self.arena_tier==3 and 
						image_manager.is_in_team_adding() and
						image.manager.is_in_team_adding_tier(3)
					):
						print("in correct team adding")
					elif (
							image_manager.get_dominant_color_grab(130,532)=="green" and
							image_manager.get_dominant_color_grab(430,532)=="green" and
							image_manager.get_dominant_color_grab(868,532)=="green"
					):
						print("no need to drag left most")
						self.arena_check_inside_fighting()
					else:
						mouse_click_drag(130,255,700,255)#drag leftmost foolproof
						self.arena_check_inside_fighting()
						time.sleep(1.5)
						mouse_click_drag(130,255,700,255)#drag leftmost foolproof
				
				self.arena_check_inside_fighting()
				time.sleep(1)
				#LINE189
			
		#end start_arena	
	
	
	def stop_arena(self):
		self.arena_stop = True
		#end stop_arena
	
	
	def arena_check_inside_fighting(self):
		"""check if inside fighting, if true, control fight """
		if (image_manager.is_inside_fighting()):
			print("inside fight")
			mouse_click(200,200)
			mouse_click(200,200)
			self.arena_continue = False
			self.arena_fight()
			return True
		return False
		#end arena_check_inside_fighting
	
	
	def arena_fight(self):
		"""control fighting in arena"""
		self.status = "fighting in arena"
		sequence = 0
		self.arena_stop = False
		#end arena_fight
	
	
	def alliance_help(self):
		"""send help for loyalty, return False if failed to perform"""
		img = ImageGrab.grab()
		
		mouse_click(190,58) #menu button
		time.sleep(1)
		mouse_click(190,58) #menu button again
		time.sleep(1)
		
		if img.getpixel((400,92))==(0x59,0,0):
			mouse_click(375,131)#alliance button
			time.sleep(10)#todo change to image processing
			mouse_click(490,180)#help tab
			time.sleep(2)
			while (image_manager.get_dominant_color(img.getpixel((750,235)))=="green"):
				mouse_click(760,235)#help button
				time.sleep(2)
			#done
			mouse_click(190,58) #menu
			time.sleep(1)
			mouse_click(190,58) #menu
			time.sleep(1)
			mouse_click(270,132)#fight button
			time.sleep(8)#todo change to image processing
			return True
		else:
			return False
		#end alliance_help
