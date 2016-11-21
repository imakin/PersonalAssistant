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
			self.print_log(self.status)
	
	
	def print_log(self,text):
		if (self.gui!=None):
			self.gui.print_log(text)
		print(text)
	
		
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
			
			
			self.print_log("match number :%d"% self.arena_matches)
			
			#helping
			if (	self.arena_matches%self.arena_help==0 and 
					image_manager.is_menu_button_available(img)
			):
				helping = self.alliance_help()
				if (not helping):
					self.arena_matches -= 1 #make sure we keep trying in the next chance
			self.print_log("done helping")
			self.arena_continue = True
			if (not self.arena_allstop):
				self.arena_check_inside_fighting()
				time.sleep(0.5)
				
				#~ self.print_log("check if in fight room")
				#~ if image_manager.is_in_fight_room():
					#~ self.print_log("inside fight menu, not arena (first check)")
					#~ mouse_click_drag(130,255,700,255)
					#~ time.sleep(1)
					#~ mouse_click_drag(130,255,700,255)
					#~ time.sleep(0.5)
					#~ mouse_click(500,446)
					#~ while image_manager.is_in_arena_room()==(-1,-1):
						#~ time.sleep(0.5)
				
				
				if self.arena_tier==5:
					mouse_click_drag(700,255,130,255,1)
					time.sleep(0.5)
					mouse_click_drag(700,255,130,255,1)
					time.sleep(0.5)
				else:
					if (self.arena_tier==3 and 
						image_manager.is_in_team_adding() and
						image_manager.is_in_team_adding_tier(3)
					):
						self.print_log("in correct team adding")
					elif (
							image_manager.get_dominant_color_grab(130,532)=="green" and
							image_manager.get_dominant_color_grab(430,532)=="green" and
							image_manager.get_dominant_color_grab(868,532)=="green"
					):
						self.print_log("no need to drag left most")
						self.arena_check_inside_fighting()
					else:
						mouse_click_drag(130,255,700,255)#drag leftmost foolproof
						self.arena_check_inside_fighting()
						time.sleep(1.5)
						mouse_click_drag(130,255,700,255)#drag leftmost foolproof
				
				self.arena_check_inside_fighting()
				time.sleep(0.5)
				self.arena_check_inside_fighting()
				
				#check if in fight menu, not arena menu
				if (self.arena_tier==3 and 
					image_manager.is_in_team_adding() and
					image_manager.is_in_team_adding_tier(3)
				):
					self.print_log("in correct team adding when checking if in fight menu or arean")
				elif (image_manager.get_dominant_color_grab(346,535)!="green" and
					self.arena_tier!=5
				):
					self.print_log("inside fight menu, not arena")
					mouse_click_drag(130,255,700,255)
					time.sleep(0.4)
					mouse_click_drag(130,255,700,255)
					time.sleep(0.4)
					self.click_fightroom_arena()
					time.sleep(2)
					wait = 10
					while (wait>0 and 
						image_manager.get_dominant_color_grab(435,525)!="green"
					):
						time.sleep(1)
						wait -= 1
						self.arena_check_inside_fighting()
				
				self.arena_check_inside_fighting()
				
				#check if currently in one of the 3 fights in a match
				if image_manager.is_in_more_fight_to_go():
					self.print_log("more fight to go")
					self.status="more fight to go"
					time.sleep(1)
					mouse_click(200,200)
					self.arena_fight()
					self.arena_continue = False
				
				#self.arena_check_inside_fighting()
				if self.arena_continue:
					if self.arena_tier==2:
						mouse_click(386,446)
						time.sleep(5)
						mouse_click(413,522)#double check
						
					elif self.arena_tier==3:
						if (image_manager.is_in_team_adding() and 
							image_manager.is_in_team_adding_tier(3)
						):
							self.print_log("on correct team adding tier 3, now to ask for help")
							mouse_click(760,508)#double check
							time.sleep(1)
						else:
							mouse_click(830,510)
							wait = 10
							while (wait>0 and not image_manager.is_in_team_adding()):
								time.sleep(0.5)
								self.print_log("wait entering arena %d"%wait)
								wait -= 1
							mouse_click(760,508)#double check
					elif self.arena_tier==4:
						mouse_click(433,522)
						time.sleep(5)
					elif self.arena_tier==5:
						#arena special 5
						if image_manager.is_in_fight_room():
							self.print_log("inside fight menu, not arena")
							mouse_click_drag(130,255,700,255)
							time.sleep(1)
							mouse_click_drag(130,255,700,255)
							time.sleep(0.5)
							mouse_click(500,446)
							while image_manager.is_in_arena_room()==(-1,-1):
								self.arena_check_inside_fighting()
								self.print_log("waiting to be in arena room")
								time.sleep(0.5)
								
						t4b_button = image_manager.get_arena_t4b_button()
						while t4b_button==(-1,-1):
							self.print_log("can't find t4b")
							self.arena_check_inside_fighting()
							mouse_click_drag(700,255,130,255)#drag right most
							t4b_button = image_manager.get_arena_t4b_button()
							time.sleep(0.5)
						
						mouse_click(t4b_button[0], t4b_button[1]+265)
						
						time.sleep(5)#waiting to be in team adding
				
				if (image_manager.is_in_team_adding()):
					time.sleep(1)
				else:
					while not image_manager.is_in_team_adding():
						self.print_log("waiting to be in team adding")
						self.arena_check_inside_fighting()
						if image_manager.is_in_more_fight_to_go():
							self.print_log("in more fight to go")
							break
						if image_manager.is_in_find_match():
							self.print_log("in find match")
							break
						time.sleep(1)
				
				#if in milestone info
				if image_manager.is_in_milestone_info():
					self.click_close_topright()
					time.sleep(7)
					self.arena_continue = False
				
				if image_manager.is_in_more_fight_to_go():
					self.arena_continue = False
					self.arena_fight()
				
				self.arena_ask_for_help()
				self.arena_check_inside_fighting()
				
				if self.arena_continue:
					self.arena_add_to_team()
					self.arena_find_match()
					self.arena_fight()
				
			#end if (not self.arena_allstop):
			self.arena_stack -= 1
		#end start_arena	
	
	
	def arena_ask_for_help(self):
		"""in team adding, ask for help if any"""
		self.status="ask for help"
		while image_manager.is_team_adding_need_help():
			keyboard_send("Q")
			time.sleep(3)
		
		#end arena_ask_for_help
	
	
	def arena_find_match(self):
		"""click find match and pick easy and good score enemy"""
		self.status ="find match"
		time.sleep(0.5)
		mouse_click(109,547)
		self.arena_check_inside_fighting()
		time.sleep(4)
		
		img = ImageGrab.grab()
		if image_manager.pixel_search(img,543,416,575,429,(0x31,0x9d,0x32))==False:
			#highest is not easy, check if mid is easy
			if image_manager.pixel_search(img,543,280,575,294,(0x31,0x9d,0x32))==False:
				#mid is not easy
				self.print_log("mid and high is not easy")
				mouse_click(600,200)
			else:
				self.print_log("mid is easy")
				mouse_click(600,320)
		else:
			self.print_log("highest is easy")
			mouse_click(680,445)
		
		self.arena_check_inside_fighting()
		time.sleep(3)
		keyboard_send("0")
		
		self.arena_rearrange_team()
		
		#end arena_find_match
		
		
	def arena_rearrange_team(self):
		if not self.arena_continue:
			return
			
		self.print_log("rearrange")
		
		#give time for manual rearrange
		wait = 10
		while wait>0:
			self.print_log("wait %d"%(wait))
			time.sleep(0.5)
			self.arena_check_inside_fighting()
			wait -= 1
		time.sleep(3)
		
		clear = False
		giveup = 10
		should_check_again = True
		
		while should_check_again:
			should_check_again = False
			
			if image_manager.get_dominant_color_grab(421,262)=="red":
				mouse_click_drag(340,225,340,308)
				time.sleep(2)
				should_check_again = True
				
			if image_manager.get_dominant_color_grab(421,338)=="red":
				mouse_click_drag(340,308,340,380)
				time.sleep(2)
				should_check_again = True
			
			if image_manager.get_dominant_color_grab(421,413)=="red":
				mouse_click_drag(340,308,340,225)
				time.sleep(2)
				should_check_again = True	
				
			giveup -= 1
			if giveup<1:
				should_check_again = False
		#end arena_rearrange_team
			
	
	def arena_add_to_team(self):
		while ImageGrab.grab().getpixel((145,135))==(0x17,0x19,0x1a):
			mouse_click_drag(319,235,145,135)
			time.sleep(0.5)
		while ImageGrab.grab().getpixel((145,210))==(0x17,0x19,0x1a):
			mouse_click_drag(319,235,145,210)
			time.sleep(0.5)
		while ImageGrab.grab().getpixel((145,290))==(0x17,0x19,0x1a):
			mouse_click_drag(319,235,145,290)
			time.sleep(0.5)
		#end arena_add_to_team
	
	
	def stop_arena(self):
		self.arena_allstop = True
		#end stop_arena
	
	
	def arena_check_inside_fighting(self):
		"""check if inside fighting, if true, control fight """
		if (image_manager.is_in_fighting()):
			self.print_log("inside fight")
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
				self.print_log("check stuck")
				if image_manager.is_stuck() and not(image_manager.is_in_fighting()):
					self.print_log("check stuck: stuck detected")
					self.status = "state fighting, stuck detected"
					self.show_status()
					image_manager.update_capture()
					stop = True
					self.print_log("i guess we're stuck")
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
					self.print_log("check stuck: stuck undetected")
					self.status = "state fighting, stuck undetected"
					self.show_status()
				image_manager.update_capture()
				
				
				#check if too long fighting maybe someting is not right
				if (time.clock()-self.arena_fighting_time_start)>300:
					self.print_log("too long in fight")
					if (image_manager.is_in_fighting()):
						self.print_log("guess the fight stuck bug")
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
			
			img = ImageGrab.grab()
			if image_manager.get_dominant_color(img.getpixel((144,541)))=="red":
				keyboard_send(KEYCODE_SPACE)
			
			
			#indicates fight has ended
			elif img.getpixel((640,540))==(0x02,0x5c,0):
				if img.getpixel((620,540))==(0x16,0x1a,0x1b):
					stop = True
					self.print_log("shall i press back button? (loading screen)")
					time.sleep(2)
					if (image_manager.is_in_team_adding()):
						self.click_back()
						time.sleep(10)
			
			#or chat bar has been licked
			elif image_manager.is_in_chat(img):
				stop = True
				self.print_log("this is chat window")
				time.sleep(1)
				self.click_close_topright()
				time.sleep(2)
				self.click_menu_fight()
				time.sleep(5)
			
			#or view reward
			elif (	img.getpixel((480,270))==(0x2b,0x2c,0x30) and
					img.getpixel((480,330))==(0x2b,0x2c,0x30)
			):
				self.print_log("view rewards ?(TODO)")
				time.sleep(2)
				keyboard_send("J")
				time.sleep(2)
				
				img = ImageGrab.grab()
				if (	img.getpixel((480,270))==(0x2b,0x2c,0x30) and
						img.getpixel((480,330))==(0x2b,0x2c,0x30)
				):
					self.arena_fighting_time_start = time.clock()
					if (
						image_manager.get_dominant_color(
								img.getpixel((142,510)))=="green" 
						and
						image_manager.get_dominant_color(
								img.getpixel((390,510)))=="green" 
						and
						image_manager.get_dominant_color(
								img.getpixel((800,510)))=="green"
					):
						self.print_log("view rewards now in fight menu arena")
					if image_manager.get_dominant_color_grab(930,560)=="green":
						stop = True
						self.click_back()
						time.sleep(1)
					else:
						status = "view rewards that doesn't end yet"
						stop = True
						keyboard_send("J")
						self.click_back()
						time.sleep(1)
			
			#if in alliance quest 
			if img.getpixel((480,270))==(0,0,0):
				if img.getpixel((838,366))==(0x2b,0x2c,0x30):
					stop = True
					self.print_log("alliance quest cuy")
					time.sleep(2)
					self.click_back()
					time.sleep(8)
			
			#if in alliance quest empty
			elif (
				img.getpixel((384,142))==(0x1a,0x1a,0x1a) and
				img.getpixel((551,142))==(0x1a,0x1a,0x1a) and
				img.getpixel((504,142))!=(0x1a,0x1a,0x1a)
			):
				stop = True
				self.print_log("empty alliance quest cuy")
				time.sleep(2)
				self.click_back()
				time.sleep(8)
			
			
			#if in event info
			elif (
				img.getpixel((50,100))==(0x29,0x2c,0x30) and
				img.getpixel((50,500))==(0x29,0x2c,0x30) and
				img.getpixel((900,100))==(0x29,0x2c,0x30) and
				img.getpixel((900,500))==(0x29,0x2c,0x30) and
				img.getpixel((939,61))==(0x6c,0x6e,0x71)	
			):
				stop =True
				self.print_log("event board")
				self.click_close_topright()
				
			#if in team adding
			elif (
				image_manager.is_in_team_adding(img)
			):
				self.print_log("team adding")
				stop = True
				if image_manager.is_in_team_adding(True, img)=="dark":
					self.print_log("team adding dark")
					time.sleep(1)
					mouse_click(100,400)
					time.sleep(2)
				if (self.arena_tier==3 and 
					image_manager.is_in_team_adding_tier(3)
				):
					self.print_log("in correct tier 3")
				else:
					time.sleep(1)
					self.click_back()
					time.sleep(7)
			
			#if in somewhere outside
			#not yet implemented
			
			
			#when blue stack error/game kick out to home
			elif (
				image_manager.is_in_bluestack_home(img) or 
				image_manager.is_in_bluestack_login(img)
			):
				self.arena_allstop = 1
				time.sleep(2)
				mouse_click(175,613) #android home button
				time.sleep(2)
				mouse_click_drag(900,310,900,70, 1)#close app
				time.sleep(2)
				mouse_click(175,613) #android home button
				time.sleep(2)
				
				#make sure scroll up most in launcher
				repeat = 10
				while repeat>0:
					mouse_click_drag(500,100,500,550)
					time.sleep(0.8)
					repeat -= 1
					#check if in upmost now
					img = ImageGrab.grab() 
					if (
						img.getpixel((73,135))==(0xf3,0x80,0x25) and #search logo
						img.getpixel((74,165))==(0xff,0xff,0xff) and #search logo
						img.getpixel((914,150))==(0xff,0xff,0xff) and #plus logo
						img.getpixel((935,147))==(0xf3,0x80,0x25) #plus logo
					):
						repeat = 0
				
				mouse_click(200,160)#mcoc game
				time.sleep(10)
				while (not image_manager.is_in_game_home()):
					self.print_log("not yet")
					time.sleep(1)
				self.click_menu_fight()
				time.sleep(2)
				self.start_arena()
		
		#end arena_fight
	
	
	def alliance_help(self):
		"""send help for loyalty, return False if failed to perform"""
		img = ImageGrab.grab()
		self.print_log("helping")
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


	def click_close_topright(self):
		"""click close chat button"""
		mouse_click(943,52)
		#end click_close_topright

	def click_back(self):
		"""click back button"""
		mouse_click(57,55)
		time.sleep(0.5)
		mouse_click(57,55)
		#end click_back


	def click_menu(self,delay=1):
		"""perform clickingthe menu button"""
		mouse_click(190,58)#menu button
		time.sleep(delay)
		mouse_click(190,58)
		time.sleep(delay)
		#end click_menu


	def click_menu_fight(self, delay=1):
		"""
		perform clicking the menu button then fight button to go to fight room
		delay is the wait between clicks
		delay after fight button clicked not performed here
		"""
		self.click_menu(delay)
		mouse_click(270,132)#fight button
		#end click_menu_fight
	
	def click_fightroom_arena(self):
		"""click arena button in fight room menus"""
		mouse_click(500,446)
