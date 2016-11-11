from makinreusable.winfunction import *
import time
from image import *

class GrindingMakin(object):
	def __init__(self, gui_controller=None):
		self.status = ""
		self.quest_active = False
		
		self.arena_allstop = False
		self.arena_stack = 0
		self.arena_matches = 0
		self.arena_help = 30#when matches hit multiplier of this value, help alliance
		self.arena_tier = 3#the tier in arena to pick
		
		self.arena_continue = True #inside arena loop status
		
		self.gui = gui_controller
		#end init
	
	def show_status(self):
		if (self.gui!=None):
			self.gui.update_status(
				str(self.arena_stack)+" "+
				self.status
			)
		else:
			print(self.status)
	
		
	def calibrate_position(self):
		win = image_manager.find_bluestack_logo()
		mouse_click_drag(win[0],win[1], 30, 12)
		#end calibrate_position

	def start_arena(self):
		self.status = "start arena"
		self.arena_allstop = False
		
		while not(self.arena_allstop):
			self.arena_stack += 1
			self.arena_matches += 1
			self.calibrate_position()
			
			img = ImageGrab.grab()
			
			if (	self.quest_active and 
					image_manager.is_menu_button_available(img) and
					image_manager.is_energy_full(img)
			):
				pass
				self.arena_allstop = True
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
			if (not self.arena_allstop):
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
		self.arena_allstop = True
		#end stop_arena
	
	
	def arena_check_inside_fighting(self):
		"""check if inside fighting, if true, control fight """
		if (image_manager.is_in_fighting()):
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
		self.arena_allstop = False
		stop = False #local
		
		#handle if stuck in something
		counter_somewhereoutside = 0
		self.arena_fighting_stuck_seq = 0
		self.arena_fighting_time_start = time.clock()
		self.arena_fighting_timer_second = 0
		
		while (not(self.arena_allstop) and not(stop)):
			self.arena_fighting_stuck_seq += 1
			if (self.arena_fighting_stuck_seq%100==0):
				self.arena_fighting_stuck_seq = 1
				print("check stuck")
				if image_manager.is_stuck() and not(image_manager.is_in_fighting()):
					print("check stuck: stuck detected")
					self.status = "state fighting, stuck detected"
					self.show_status()
					image_manager.update_capture()
					stop = True
					print("i guess we're stuck")
					time.sleep(2)
					
					#check if stuck in leaderboard
					if (image_manager.is_in_leaderboard()):
						status = "leaderboard, i'll close it"
						self.show_status()
						time.sleep(2)
						mouse_click(939,61)#close button
						time.sleep(3)
					
					self.click_menu_fight()
					time.sleep(10)
				else:
					print("check stuck: stuck undetected")
					self.status = "state fighting, stuck undetected"
					self.show_status()
				image_manager.update_capture()
				
				
				#check if too long fighting maybe someting is not right
				if (time.clock()-self.arena_fighting_time_start)>300:
					print("too long in fight")
					if (image_manager.is_in_fighting()):
						print("guess the fight stuck bug")
						#TODO: startover()
						stop = True
						self.arena_allstop = True
					else:
						time.sleep(5)
						self.click_menu_fight()
						time.sleep(10)
			#end if (self.arena_stuck_seq%100==0):
			
			keyboard_send("0")
			time.sleep(0.001)
			if sequence%4==0:
				keyboard_send("K")
			sequence += 1
			if (sequence>15):
				keyboard_send(KEYCODE_SPACE)
				if (sequence>20):
					sequence = 0
			
			if image_manager.get_dominant_color_grab(144,541)=="red":
				keyboard_send(KEYCODE_SPACE)
			
				
				
			#LINE593
		
		#end arena_fight
	
	
	def alliance_help(self):
		"""send help for loyalty, return False if failed to perform"""
		img = ImageGrab.grab()
		
		self.click_menu()
		
		if img.getpixel((400,92))==(0x59,0,0):
			mouse_click(375,131)#alliance button
			time.sleep(10)#todo change to image processing
			mouse_click(490,180)#help tab
			time.sleep(2)
			while (image_manager.get_dominant_color(img.getpixel((750,235)))=="green"):
				mouse_click(760,235)#help button
				time.sleep(2)
			#done
			self.click_menu_fight()
			time.sleep(8)#todo change to image processing
			return True
		else:
			return False
		#end alliance_help


	def click_menu(self,delay=1):
		"""perform clickingthe menu button"""
		mouse_click(190,58)#menu button
		time.sleep(delay)
		mouse_click(190,58)
		time.sleep(delay)


	def click_menu_fight(self, delay=1):
		"""
		perform clicking the menu button then fight button to go to fight room
		delay is the wait between clicks
		delay after fight button clicked not performed here
		"""
		click_menu(delay)
		mouse_click(270,132)#fight button