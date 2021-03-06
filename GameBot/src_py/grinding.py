from makinreusable.winfunction import *
import time
import urllib2
from image import *

class GrindingMakin(object):
	arena_act_other_timing = 0
	arena_tier_is_right = False
	def __init__(self, gui_controller=None):
		self.status = ""
		self.quest_active = False
		
		self.arena_allstop = False
		self.arena_stack = 0
		self.arena_matches = 0
		self.arena_help = 30#when matches hit multiplier of this value, help alliance
		self.arena_tier = 3#the tier in arena to pick
		
		self.report_mode = False#report everytime entering fight
		
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
		self.print_log("found bluestack logo in (%d,%d)"%(win[0],win[1]))
		if (win[0]==30 and win[1]==12):
			self.print_log("window position is good")
		elif (win[0]<=30 and win[1]<=12):
			self.print_log("window slightly missplaced")
			mouse_click_drag(win[0],win[1], 60, 42)
			mouse_click_drag(60,42, 30, 12)
		else:
			self.print_log("window will be replaced")
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
				#~ time.sleep(0.5)
				
				if image_manager.is_in_fight_room():
					self.print_log("we're in fight room, going to arena")
					mouse_click_drag(130,255,700,255)#drag left most
					time.sleep(1)
					mouse_click_drag(130,255,700,255)
					time.sleep(0.5)
					mouse_click(500,446)
					
					wait = time.clock()
					while not image_manager.is_in_arena_room():
						self.arena_check_inside_fighting()
						self.print_log("waiting to be in arena room")
						time.sleep(0.5)
						self.check_popup_close()
						if time.clock()-wait>300:
							break
					
				
				if (self.arena_tier==3 and 
						image_manager.is_in_team_adding() and
						image_manager.is_in_team_adding_tier(3)
				):
					self.print_log("in correct team adding")
				
				else:
					if image_manager.is_in_arena_room():
						time.sleep(0.5)
						selected = image_manager.get_arena_target()
						left = 2
						while selected==(-1,-1):
							if left>0:
								mouse_click_drag(130,255,700,255)#drag left most
								left -= 1
							else:
								mouse_click_drag(700,255,130,255)#drag right most
							time.sleep(0.5)
							selected = image_manager.get_arena_target()
							self.check_popup_close()
							self.print_log("searching target")
						
						self.print_log("done searching target")
						mouse_click(selected[0], selected[1])
						time.sleep(2)
					else:
						self.print_log("not in arena room")
						time.sleep(1)
						self.click_menu_fight(1,True)
						self.arena_continue = False
					
				if (self.arena_continue and image_manager.is_in_team_adding()):
					time.sleep(1)
				elif self.arena_continue:
					loading_time = time.clock()
					while not image_manager.is_in_team_adding():
						self.print_log("waiting to be in team adding")
						self.arena_check_inside_fighting()
						self.check_popup_close()
						if image_manager.is_in_more_fight_to_go():
							self.print_log("we're in one of three fights")
							break
						if image_manager.is_in_find_match():
							self.print_log("we're in find match selecting opponent")
							break
						if image_manager.is_in_rearrange_team():
							self.print_log("we're in rearrange team")
							break
						if image_manager.is_in_milestone_info():
							self.print_log("we're in milestone info")
							break
						keyboard_send("0")
						self.print_log("sending 0")
						if time.clock()-loading_time>30:
							self.print_log("too long waiting, canceling")
							self.click_menu_fight(1,True)
							self.arena_continue = False
							break
						else:
							self.print_log("time out: %d"%int(time.clock()-loading_time))
						time.sleep(1)
				
				#if in milestone info
				if image_manager.is_in_milestone_info():
					self.click_close_topright()
					time.sleep(7)
					self.arena_continue = False
				
				if image_manager.is_in_more_fight_to_go():
					self.arena_continue = False
					#~ self.arena_capture_score()
					self.arena_fight()
				
				if self.arena_continue:
					self.arena_ask_for_help()
				
				self.arena_check_inside_fighting()
				
				if self.arena_continue:
					if not self.arena_allstop:
						self.arena_add_to_team()
					if not self.arena_allstop:
						self.arena_find_match()
					if not self.arena_allstop:
						self.arena_fight()
				
			#end if (not self.arena_allstop):
			self.arena_stack -= 1
		#end start_arena	
	
	
	def arena_ask_for_help(self):
		"""in team adding, ask for help if any"""
		self.status="ask for help"
		time.sleep(1)
		while image_manager.is_team_adding_need_help():
			keyboard_send("Q")
			time.sleep(3.5)
			self.check_popup_close()
		if image_manager.is_team_adding_all_recharging():
			self.print_log("less than 3 is ready, waiting")
			self.click_back()
			
		#end arena_ask_for_help
	
	
	def arena_find_match(self):
		"""click find match and pick easy and good score enemy"""
		self.status ="find match"
		time.sleep(0.5)
		mouse_click(109,547) #click find
		self.arena_check_inside_fighting()
		
		if (self.wait_timeout_or_check(4,image_manager.is_in_find_match)):
			pass
			#~ self.arena_continue = True
		
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
		keyboard_send("0")
		#~ self.arena_capture_score()
		
		#end arena_find_match
	
	
	def arena_capture_score(self):
		self.print_log("capturing score")
		time.sleep(1)
		img = ImageGrab.grab((520,120,620,140))
		self.gui.update_score(img)
		
	
	def arena_rearrange_team(self):
		self.print_log("rearrange")
		
		if not self.arena_continue:
			self.print_log("arena_continue is False")
			return
		if not image_manager.is_in_rearrange_team():
			self.print_log("not in rearrange team, wait")
			time.sleep(3)
			if not image_manager.is_in_rearrange_team():
				self.print_log("recheck not in rearrange team")
				return
		
		#give time for manual rearrange
		wait = 10
		while wait>0:
			self.print_log("wait %d"%(wait))
			time.sleep(0.5)
			self.arena_check_inside_fighting()
			wait -= 1
			self.check_popup_close()
		time.sleep(3)
		
		clear = False
		giveup = 10
		should_check_again = True
		
		while should_check_again:
			should_check_again = False
			self.check_popup_close()
			if image_manager.get_dominant_color_grab(421,262)=="red":
				mouse_click_drag(340,225,340,308)
				time.sleep(2)
				should_check_again = True
				
			if image_manager.get_dominant_color_grab(421,338)=="red":
				mouse_click_drag(340,308,340,380)
				time.sleep(2)
				should_check_again = True
			
			if image_manager.get_dominant_color_grab(421,413)=="red":
				mouse_click_drag(340,380,340,225)
				time.sleep(2)
				should_check_again = True	
				
			giveup -= 1
			if giveup<1:
				should_check_again = False
		keyboard_send("0")#done
		time.sleep(3)
		#end arena_rearrange_team
			
	
	def arena_add_to_team(self):
		status = "add to team"
		self.print_log("adding to team")
		mouse_click_drag(319,235,145,135)
		time.sleep(0.5)
		while ImageGrab.grab().getpixel((145,135))==(0x17,0x19,0x1a):
			self.check_popup_close()
			mouse_click_drag(319,235,145,135)
			time.sleep(0.5)
		mouse_click_drag(319,235,145,210)
		time.sleep(0.5)
		while ImageGrab.grab().getpixel((145,210))==(0x17,0x19,0x1a):
			self.check_popup_close()
			mouse_click_drag(319,235,145,210)
			time.sleep(0.5)
		mouse_click_drag(319,235,145,290)
		time.sleep(0.5)
		while ImageGrab.grab().getpixel((145,290))==(0x17,0x19,0x1a):
			self.check_popup_close()
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
		self.arena_fight_state_mode()
		return
		
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
						#~ stop = True
						#~ self.arena_allstop = True
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
			
			if not image_manager.is_in_fighting(img):
				#indicates fight has ended
				if img.getpixel((640,540))==(0x02,0x5c,0):
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
							self.print_log("view rewards now i used to click back")
							stop = True
							#~ self.click_back()
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
				
				elif self.check_popup_close():
					pass
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
						if (self.arena_tier==3 and 
							image_manager.is_in_team_adding_tier(3)
						):
							self.print_log("in correct tier 3 on 2nd view")
						else:
							self.print_log("afraid it's not correct tier")
							self.click_back()
							time.sleep(7)
			
			#if in somewhere outside
			#not yet implemented
			
			
			#when blue stack error/game kick out to home
			elif (
				image_manager.is_in_bluestack_home(img) or 
				image_manager.is_in_bluestack_login(img)
			):
				self.arena_start_over()
		self.print_log("done fighting, recalibrate window pos")
		self.calibrate_position()
		#end arena_fight
	
	
	
	def arena_fight_state_mode(self):
		self.arena_tier_is_right = False
		self.print_log("start fighting")
		self.status = "fighting in arena"
		self.fighting_sp_mode = 2
		sequence = 0
		style_changed = False
		while True:
			
			if sequence%4==0:
				keyboard_send("K")
			#~ if sequence<=10:
				#~ keyboard_send("0")
				#~ keyboard_send("J")
			#~ if sequence>10:
				#~ keyboard_send("F")
				#~ if sequence>15:
					#~ keyboard_send("D")
					#~ if sequence>20:
						#~ sequence = 0
			if sequence>25:
				sequence = 0
				keyboard_send("K")
			elif sequence>24:
				keyboard_send("D")
			elif sequence>22:
				keyboard_send("F")
			else:
				keyboard_send("0")
				
			sequence += 1
			
			img = ImageGrab.grab()
			specialbt = img.getpixel((cx(133),cy(507)))
			
			if (not style_changed) and img.getpixel((cx(745),cy(93)))<(35,35,35):
				self.print_log("enemy low")
				style_changed = True
				self.fighting_sp_mode = 1
			
			if self.fighting_sp_mode==1:
				#~ if image_manager.get_dominant_color(specialbt)=="green":
				keyboard_send(KEYCODE_SPACE)
			elif self.fighting_sp_mode==2:
				if image_manager.get_dominant_color(specialbt)=="red":
					if (specialbt[1]-specialbt[2])>(specialbt[0]-specialbt[1]) or (specialbt[0]-specialbt[1])>(specialbt[1]-specialbt[2]):
						keyboard_send(KEYCODE_SPACE)
			elif self.fighting_sp_mode==3:
				if image_manager.get_dominant_color(specialbt)=="red" and (specialbt[0]-specialbt[1])>(specialbt[1]-specialbt[2]):
					keyboard_send(KEYCODE_SPACE)
			
			#~ if not image_manager.is_in_fighting(img):
			if sequence%5==0:
				if not image_manager.is_in_fighting(img):
					print("break in fight room")
					break
			#~ if image_manager.is_in_team_adding(img):
				#~ print("break in team adding")
				#~ break
			#~ elif image_manager.is_in_chat(img):
				#~ print(" break chat")
				#~ break
			#~ if not image_manager.is_in_fighting(img):
				#~ if not image_manager.is_in_
		for x in range(0,10):
			keyboard_send("J")
			time.sleep(0.2)
		self.print_log("done fighting")
		
		if self.report_mode and style_changed:
			self.url_read("http://makin.pythonanywhere.com/cloud_data/aaa/write/bot_arena_report/hit_enemy_low_confirmed")
			self.report_mode = False
	
	
	
	def arena_start_over(self):
		"""start from exiting app and reopen it and play arena"""
		#~ self.arena_allstop = 1
		time.sleep(2)
		self.print_log("closing app")
		mouse_click(175,613) #android window button
		time.sleep(2)
		mouse_click_drag(900,310,900,70, 1)#close app
		time.sleep(2)
		self.print_log("reopening app")
		mouse_click(121,613) #android home button
		time.sleep(2)
		self.arena_allstop = False
		#make sure scroll up most in launcher
		repeat = 10
		while repeat>0:
			mouse_click_drag(500,100,500,550)
			time.sleep(1)
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
			self.print_log("waiting to be in top most scanning for app")
			if self.arena_allstop:
				self.print_log("force stop from hotkey")
				return
		
		mouse_click(200,160)#mcoc game
		time.sleep(10)
		#~ self.loop() #exiting this method is already in a loop
		
		#~ while (not image_manager.is_in_game_home()):
			#~ self.print_log("waiting to be in game home")
			#~ time.sleep(1)
			#~ if self.arena_allstop:
				#~ self.print_log("force stop from hotkey")
				#~ return
		#~ self.click_menu_fight(True)
		#~ time.sleep(2)
		#~ self.arena_allstop = True
		#~ self.start_arena()
		#end arena_start_over
	
	
	def alliance_help(self):
		"""send help for loyalty, return False if failed to perform"""
		
		self.print_log("helping")
		self.click_menu()
		time.sleep(2)
		img = ImageGrab.grab()
		if img.getpixel((400,92))==(0x59,0,0):
			mouse_click(375,131)#alliance button
			time.sleep(10)#todo change to image processing
			
			mouse_click(490,180)#help tab
			time.sleep(2)
			while (image_manager.get_dominant_color_grab(750,235)=="green"):
				self.check_popup_close()
				self.print_log("waiting to empty ally helps")
				mouse_click(760,235)#help button
				time.sleep(2)
			#done
			self.click_menu_fight()
			time.sleep(8)#todo change to image processing
			return True
		else:
			return False
		#end alliance_help
	
	
	def check_popup_close(self, image_grab=None):
		"""check if in popup, close it if true
		return True if there is popup"""
		img = image_manager.get_grab(image_grab)
		c = image_manager.is_in_popup(img)
		if c!=(-1,-1):
			self.print_log("there is popup")
			mouse_click(c[0],c[1])
			time.sleep(1)
			return True
		return False
	

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

	
	def arena_loop_breaker(self):
		"""return true if all is well and loop should be broke"""
		img = ImageGrab.grab()
		if (
			image_manager.is_in_arena_room(img) or
			image_manager.is_in_more_fight_to_go(img) or
			image_manager.is_in_team_adding(False,img) or
			image_manager.is_in_fight_room(img) or
			image_manager.is_in_fighting(img) or
			image_manager.is_in_find_match(img) or
			image_manager.is_in_rearrange_team(img)
		):
			return True
		return False
		#end arena_loop_breaker
			
	


	def click_menu_fight(self, delay=1, until_in_fight_room=False):
		"""
		perform clicking the menu button then fight button to go to fight room
		delay is the wait between clicks
		delay after fight button clicked not performed here
		until_in_fight_room only return from method if game succesfully entered fight room
		"""
		self.check_popup_close()
		if not image_manager.is_menu_button_available() and not image_manager.is_in_game_home():
			self.print_log("menu button is not available but not in game home")
			return
		self.click_menu(delay)
		mouse_click(270,132)#fight button
		if until_in_fight_room:
			start = time.clock()
			while not image_manager.is_in_fight_room():
				self.print_log("waiting to be in fight room")
				time.sleep(1)
				self.check_popup_close()
				self.arena_check_inside_fighting()
				if self.arena_loop_breaker():
					break
				if time.clock()-start>10:
					self.print_log("too long click menu fight waiting")
					return
					#todo self.startover
		#end click_menu_fight
	
	def click_fightroom_arena(self):
		"""click arena button in fight room menus"""
		mouse_click(500,446)


	def url_read(self,url):
		resp = urllib2.urlopen(url)
		data = resp.read()
		resp.close()
		return data
	

	def arena_standby(self):
		"""standby arena wait for online command.
		exiting this method means we're ordered to grind"""
		self.print_log("on your command")
		while True:
			self.print_log("waiting to be ordered to grind")
			try:
				#~ resp = urllib2.urlopen("http://makin.pythonanywhere.com/cloud_data/aaa/read/bot_arena_startover/")
				data = self.url_read("http://makin.pythonanywhere.com/cloud_data/aaa/read/bot_arena_startover/")
				#~ resp.close()
				self.print_log("command is "+data)
				if data=='True':
					self.print_log("we're ordered to grind")
					self.url_read("http://makin.pythonanywhere.com/cloud_data/aaa/write/bot_arena_startover/False")
					self.report_mode = True
					self.url_read("http://makin.pythonanywhere.com/cloud_data/aaa/write/bot_arena_report/hit_enemy_low_unconfirmed")
					self.arena_start_over()
					return True
				time.sleep(10)
			except :
				time.sleep(10)
		return False
		#end arena_standby
	
	def loop(self):
		seq = 0
		while True:
			self.arena_act()
			if seq%4==0:
				self.print_log(time.ctime())
				seq = 0
	
	def arena_act(self, other_tolerant=False):
		
		self.check_popup_close()
		self.arena_check_inside_fighting()
		
		img = ImageGrab.grab()
		is_other = False
		if image_manager.is_in_arena_room(img):#arena (versus) room
			self.print_log("act: arena room")
			self.arena_click_target()
		
		elif image_manager.is_in_fight_room(img):
			self.print_log("act: fight room")
			self.arena_click_versus()
		
		elif image_manager.is_in_team_adding(img):
			self.print_log("act: team adding")
			if image_manager.is_in_team_adding(True)=="dark":
				mouse_click(145,210)
				time.sleep(1)
			play = True
			is_tier_3 = image_manager.is_in_team_adding_tier_3()
			if self.arena_tier==3 and is_tier_3:
				self.print_log("in correct team adding tier 3")
				
			elif self.arena_tier==3 and not is_tier_3:
				self.print_log("afraid not in correct tier")
				play = False
			elif self.arena_tier==4:
				if image_manager.is_in_team_adding_tier_4():
					self.print_log("in correct team adding tier 4")
				else:
					self.print_log("afraid not in correct tier")
					play = False
			else:
				self.print_log("arena tier is %d"%(self.arena_tier))
			
			if not play and self.arena_tier_is_right:
				self.print_log("But i'm pretty sure we've clicked correct arena")
				play = True
			elif not play:
				self.click_back()
				
				
			
			if play:
				self.arena_continue = True
				self.arena_ask_for_help()
				self.arena_add_to_team()
				self.arena_find_match()
				self.arena_fight()
		
		elif image_manager.is_in_find_match(img):
			self.print_log("act: find match")
			keyboard_send("0")
		
		elif image_manager.is_in_rearrange_team(img):
			self.print_log("act: rearrange team")
			self.arena_continue = True
			self.arena_rearrange_team()
			keyboard_send("0")
		
		elif image_manager.is_in_loading(img):
			self.print_log("act: loading")
			self.print_log(time.ctime())
			while image_manager.is_in_loading():
				keyboard_send("0")
				time.sleep(0.8)
		
		elif image_manager.is_in_more_fight_to_go(img):
			self.print_log("act: more fight to go")
			self.arena_fight()
		
		elif image_manager.is_in_fighting(img):
			self.print_log("act: fighting")
			self.arena_fight()
		
		elif image_manager.is_in_game_home(img):
			self.print_log("act: game home")
			self.click_menu_fight(1,True)
		
		elif image_manager.is_in_bluestack_home(img) or image_manager.is_in_bluestack_login(img):
			self.print_log("act: bluestack home")
			self.arena_start_over()
		
		elif image_manager.is_login_other_device(img):
			self.print_log("act: logged in in other device")
			self.print_log("command waiting triggered")
			self.arena_standby()
		
		elif image_manager.is_in_arena_after_fight_reward(img):
			self.print_log("act: reward after finishing arena match")
			while image_manager.is_in_arena_after_fight_reward():
				time.sleep(0.5)
				keyboard_send("0")
		
		elif image_manager.is_continue_button_available(img):
			self.print_log("act: other, continue button available")
			keyboard_send("0")
			time.sleep(0.5)
			
		elif image_manager.is_menu_button_available(img):
			is_other = True
			self.print_log("act: other, menu button available")
			if self.arena_act_other_timing==0:
				self.arena_act_other_timing = time.clock()
				self.print_log("other tolerant, 7 sec")
			else:
				if time.clock()-self.arena_act_other_timing>7:
					self.print_log("other tolerant 7 sec is over")
					self.arena_act_other_timing = 0
					self.click_menu_fight(1,True)
			
		else:
			self.print_log("act: unknown state")
			keyboard_send("J")
			mouse_click(500,350)
			self.calibrate_position()
			time.sleep(2)
		
		if not is_other:
			self.arena_act_other_timing = 0

	def arena_click_target(self):
		"""get arena tier target and goto its team adding"""
		time.sleep(0.5)
		
		if self.arena_tier==3:
			TARGET = "any tier 3"
		elif self.arena_tier==4:
			TARGET = "t4basic"
		else:
			TARGET = "any tier 3"
		selected = image_manager.get_arena_target(None, TARGET)
		left = 2
		giveup = 10
		while selected==(-1,-1):
			if left>0:
				if TARGET=="t4basic":
					self.click_swipe_left()
					time.sleep(1)
				else:
					self.click_swipe_right()
				left -= 1
			else:
				if TARGET=="t4basic":
					self.click_swipe_right()
				else:
					self.click_swipe_left()
				left += 0.5
			time.sleep(0.5)
			selected = image_manager.get_arena_target(None, TARGET)
			self.check_popup_close()
			self.print_log("searching target")
			giveup -= 1
			if giveup<1:
				self.click_back()
				self.print_log("failed searching target")
				return
		self.print_log("done searching target")
		mouse_click(selected[0], selected[1])
		self.arena_tier_is_right = True
		time.sleep(2)
		#end arena_click_target


	def arena_click_versus(self):
		"""click versus(arena) in fight room"""
		self.print_log("we're in fight room, going to arena")
		mouse_click_drag(130,255,700,255)#drag left most
		time.sleep(1)
		mouse_click_drag(130,255,700,255)
		time.sleep(0.5)
		mouse_click(500,446)
		
		wait = time.clock()
		while not image_manager.is_in_arena_room():
			self.arena_check_inside_fighting()
			self.print_log("waiting to be in arena room")
			time.sleep(0.5)
			self.check_popup_close()
			if time.clock()-wait>10:
				break
		#end arena_click_versus


	def wait_timeout_or_check(self, timeout, check_method, exit_when_check_method_condition=True):
		"""
		perform wait until check_method execution returns check_method_condition or timeout is 0
		checking performed every approx. 1 second passed
		@param timeout in second
		@param check_method the method checking pointer
		@param check_method_condition default is True. break loop if check_method()==check_method_condition
		@return True if check_method break, False if timeout break
		"""
		while True:
			time.sleep(1)
			if check_method()==exit_when_check_method_condition:
				return True
			if timeout<=0:
				return False
			timeout = timeout-1
		#end wait_timeout_or_check


	def click_swipe_right(self):
		mouse_click_drag(130,255,700,255)
		
	def click_swipe_left(self):
		mouse_click_drag(700,255,130,255)
		

if __name__=="__main__":
	app = GrindingMakin()
	print("the app object is 'app'")
	v = raw_input("press enter to continue")
	img = ImageGrab.grab()
	def cmd_geser():
		for y in range(300,400):
			for x in range(0,700):
				if img.getpixel((x,y))==(0,0,0):
					while img.getpixel((x,y))==(0,0,0) and y>10:
						y -= 5
					
					
					mouse_click_drag(x,y,940,20, 5)
					mouse_pos_set(940,20)
					return
	cmd_geser()
	
	app.calibrate_position()
	app.loop()
	
