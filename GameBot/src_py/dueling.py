from makinreusable.winfunction import *
import time
import urllib2
import grinding
from image import *
import ImageGrab
from questing_mapping import *
import questing_mapping_saver


class DuelingMakin(object):
	
	target_name = "HRMS0"
	target_pos = 2
	def __init__(self, target_name=None, target_pos = 2):
		if target_name is not None:
			self.target_name = target_name
		self.target_pos = target_pos
		self.grinding = grinding.GrindingMakin()
		
		
	def loop(self):
		try:
			while True:
				self.dueling_act()
		except KeyboardInterrupt:
			print("exit by user")
	
	
	def dueling_act(self):
		img = ImageGrab.grab()
		
		#~ self.grinding.check_popup_close()
		if image_manager.is_in_game_home(img):
			time.sleep(3)
			if image_manager.is_in_game_home():
				print("act: in game home, claiming duel credits")
				self.act_game_home()
			
		elif image_manager.is_in_fight_room(img):
			print("act: room fight")
			self.act_room_fight()
			
		elif image_manager.is_in_duel_continue(img):
			print("act: duel continue")
			self.act_room_duel_continue()
		
		elif image_manager.is_in_chat(img) or image_manager.is_in_popup(img)!=(-1,-1):
			print("act: chat room/popup")
			self.act_room_chat()
		
		elif image_manager.is_in_team_adding(img):
			print("act: team adding")
			self.act_room_team_select()
		
		elif image_manager.is_in_fighting(img):
			print("act: fighting")
			self.dueling_fight()
		
		elif image_manager.is_in_loading(img):
			print("act: loading")
		
		elif image_manager.is_in_fighting_done(img):
			print("act: done fighting")
			mouse_click(200,200)
		
		else:
			print("act: other")
	
	def dueling_fight(self):
		print("start fighting")
		sequence = 0
		img = ImageGrab.grab()
		while image_manager.is_in_fighting():
			keyboard_send("0")
			
			if sequence%4==0:
				keyboard_send("K")
			
			sequence += 1
			
			if (sequence>10):
				keyboard_send(KEYCODE_SPACE)
				if (sequence>20):
					sequence = 0
			
			img = ImageGrab.grab()
		print("done_fighting")
		time.sleep(3)
	
	
	def act_game_home(self):
		time.sleep(4)
		mouse_click(716,485) #click stash in game home
		self.grinding.wait_timeout_or_check(3,image_manager.is_in_game_home,False)
		self.grinding.wait_timeout_or_check(3,image_manager.is_in_loading,False)
		
		time.sleep(4)
		mouse_click(742,117) #click Item tab
		time.sleep(2)
		mouse_click(748,169) #click claim max
		
		time.sleep(2)
		self.grinding.click_menu_fight(1,True)
	
	def act_room_fight(self):
		mouse_click(35,564) #click chat button
		self.grinding.wait_timeout_or_check(3, image_manager.is_in_chat, True)
	
	def act_room_chat(self):
		#getting the search button
		time.sleep(1)
		img = ImageGrab.grab()
		
		#first click the email button to avoid too much stacking chat (when AQ and AW active)
		pos_y = 100
		while img.getpixel((170,pos_y))!=(0x14,0x19,0x1d) and img.getpixel((170,pos_y))!=(0x12,0x17,0x1b) and pos_y<600:
			pos_y += 5
		mouse_click(170,pos_y)# click the email button
		time.sleep(1)
		
		img = ImageGrab.grab()
		
		pos_y = 585
		while img.getpixel((170,pos_y))!=(0x14,0x19,0x1d) and img.getpixel((170,pos_y))!=(0x12,0x17,0x1b) and pos_y>100:
			pos_y -= 5
		time.sleep(0.5)
		mouse_click(170,pos_y) #click the Search button
		time.sleep(1)
	
		mouse_click(388,106) #click search bar
		time.sleep(1)
		for c in self.target_name:
			keyboard_send(c)
			time.sleep(0.05)
		mouse_click(770,108) #do search button
		time.sleep(4)
		
		if self.target_pos==1:
			mouse_click(292,191) #click target
			time.sleep(1)
			mouse_click(476,183) #duel
			time.sleep(3)
		elif self.target_pos==2:
			mouse_click(292,263) #click target
			time.sleep(1)
			mouse_click(476,259) #duel
			time.sleep(3)
			
		
		self.grinding.wait_timeout_or_check(2,image_manager.is_in_duel_continue,True)
		self.act_room_duel_continue()
		
	
	def act_room_duel_continue(self):
		mouse_click(597,461) #continue
		time.sleep(3)
	
	
	def act_room_team_select(self):
		mouse_click_drag(346,232, 151,133) #select fighter
		time.sleep(0.5)
		mouse_click(126,546)
		time.sleep(2)
		if image_manager.is_in_team_adding(True)=="dark":
			print("out of duel credit, claiming")
			mouse_click(218,55) #skip popup
			time.sleep(0.5)
			mouse_click(218,55) #menu
			time.sleep(0.5)
			mouse_click(188,140) #home
			
			self.grinding.wait_timeout_or_check(10,image_manager.is_in_game_home,True)
			self.act_game_home()
	
		
if __name__=="__main__":
	try:input()
	except:pass
	app = DuelingMakin()
	app.loop()
