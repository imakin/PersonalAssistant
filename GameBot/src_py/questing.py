from makinreusable.winfunction import *
import time
import urllib2
import grinding
from image import *
import ImageGrab
from questing_mapping import *
import questing_mapping_saver


class QuestingMakin(object):
	color_node = [(0,0xe4,0), (0,0xf8,0), (0,0xc5,0)]
	node_range_min = 50
	def __init__(self, gui_controller=None, grinding_controller=None):
		self.gui = gui_controller
		if grinding_controller==None:
			self.grinding = grinding.GrindingMakin(self.gui)
		self.mapping = MappingMakin()
		self.nodes = []

	def print_log(self,text):
		if (self.gui!=None):
			self.gui.print_log(text)
		print(text)
	
	
	def next_node_search(self):
		self.nodes = []
		found = False
		is_portal = False
		start = time.clock()
		while not found:
			if image_manager.is_in_quest_portal_select():
				self.print_log("in portal")
				found = True
				is_portal = True
				
				mouse_click(cx(490), cy(450))
				time.sleep(2)
				self.print_log("checking drawer")
				options = 1
				#1st option pos is 840,316, gab each is 44
				self.node_add(840,316)
				posy = 316 #pointer is in option#1
				img = ImageGrab.grab()
				while True:
					posy += 44 #check for options 2,3, and greater
					if img.getpixel((840,posy))==(0x33,0x33,0x33):
						options += 1
						self.node_add(840,posy)
					else:
						break
				self.print_log("there are %d options"%(options))
			else:
				self.print_log("not in portal")
				time.sleep(0.5)
			if int(time.clock()-start)>0.8:
				break
		
		start = time.clock()
		while not found:
			img = ImageGrab.grab()
			for y in range(cy(100),cy(530)):
				for x in range(cx(80),cx(957)):
					if img.getpixel((x,y)) in self.color_node:
						self.node_add(x,y)
						found = True
			if int(time.clock()-start)>20:
				self.print_log("too long")
				return
		
		if len(self.nodes)>1:
			print("branching node with %d options"%len(self.nodes))
			target = self.mapping.add_and_decide(self.nodes)
		else:
			print("single next node")
			target = self.nodes[0]
		
		mouse_pos_set(target[0], target[1])
		self.print_log("will click this in %d"%(4))
		time.sleep(4)
		img = ImageGrab.grab()
		clicked = img.getpixel((target[0], target[1]))
		mouse_click(target[0], target[1])
		
		time.sleep(3)
		
		#check if it's not true clickable node
		img = ImageGrab.grab()
		if img.getpixel((target[0], target[1]))==clicked:
			self.print_log("this is not true clickable node, explored:")
			self.print_log(self.mapping.node_map[self.mapping.current_node].explored)
			self.mapping.current_node = self.mapping.last_changed_curnode
			
		
		req = image_manager.get_quest_request_help_button()
		if req!=(-1,-1):
			self.print_log("no energy")
			mouse_click(req[0],req[1])
		if image_manager.is_in_quest_out_of_energy():
			self.print_log("i'm sure we're out of energy")
			if len(self.nodes)>1:
				self.print_log("was about to pick a choice, revert back pos")
				self.mapping.node_map[self.mapping.current_node].explored = False
				self.mapping.current_node = self.mapping.last_changed_curnode
			return
		
		if is_portal:
			self.print_log("teleporting, searching tele button")
			tele_button_y = 316
			img = ImageGrab.grab()
			while tele_button_y<image_manager.screen_height :
				target = img.getpixel((840,tele_button_y))
				if image_manager.get_dominant_color(target)=="green":
					print(tele_button_y, target)
				if (
					image_manager.get_dominant_color(target)=="green"
					and
					target[2]==0
				):
					break
				tele_button_y+=5
			mouse_click(840,tele_button_y)
		
		self.grinding.wait_timeout_or_check(3,image_manager.is_in_quest,False)
		
		self.questing_fight()
		#end next_node_search
	
	
	def node_add(self, x,y):
		"""
		check if x,y is too close to an already registered node
		
		
		if not accociated to any node:
			will add to self.nodes
			return True
		if accociated :
			ignored 
			return False
		"""
		for node in self.nodes:
			if abs(node[0]-x)<40 and abs(node[1]-y)<40:
				return False
		self.nodes.append((x,y))
		return True
		#nodes_association
	
	def restart_or_next(self):
		"""check popup if restart or next and restart mapping"""
		if image_manager.is_in_quest_complete_button_next():
			self.print_log("the button is next")
			mouse_click(500,478)
			self.mapping = MappingMakin()#reset all
		else:
			self.print_log("the button is replay")
			mouse_click(500,478)
			self.mapping.restart()#restart
			
	
	def questing_act_loop(self):
		try:
			while True:
				self.questing_act()
		except KeyboardInterrupt:
			questing_mapping_saver.save(self.mapping)
	
	def questing_act(self):
		img = ImageGrab.grab()
		
		self.grinding.check_popup_close()
		
		if image_manager.is_in_quest(img):
			self.print_log("act: quest")
			self.next_node_search()
		
		elif image_manager.is_in_quest_complete(img):
			self.restart_or_next()
		elif image_manager.is_in_fighting(img):
			self.questing_fight()
		
		elif image_manager.is_in_quest_out_of_energy(img):
			self.print_log("act: out of energy")
			self.print_log("Warning! I will grind arena in 4")
			mouse_click(938,318)
			time.sleep(4)
			self.grinding.arena_act_loop()
		
		else:
			self.print_log("act: other")
			time.sleep(5)
			for x in range(0,5):
				mouse_click(500,383)
				time.sleep(0.2)
			
		#end questing_act


	def questing_fight(self):
		self.print_log("start fighting")
		sequence = 0
		img = ImageGrab.grab()
		while not (image_manager.is_in_quest(img) or self.grinding.check_popup_close(img)):
			keyboard_send("0")
			#~ time.sleep(0.001)
			if sequence%4==0:
				keyboard_send("K")
			
			sequence += 1
			
			if (sequence>15):
				keyboard_send(KEYCODE_SPACE)
				if (sequence>20):
					sequence = 0
			
			if not image_manager.is_in_fighting(img):
				if image_manager.is_in_quest_complete(img):
					self.print_log("quest complete")
					break
				
				if self.grinding.check_popup_close(img):
					self.print_log("popup woi!")
					break
			img = ImageGrab.grab()
		self.print_log("done_fighting")
		time.sleep(3)

if __name__=="__main__":
	app = QuestingMakin()
	app.grinding.calibrate_position()
	print("the app object is 'app'")
	#app.questing_act_loop()
	
