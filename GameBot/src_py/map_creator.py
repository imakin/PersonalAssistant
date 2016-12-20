from makinreusable.winfunction import *
import ImageGrab
import time
from questing_mapping import *
from questing_mapping_saver import save

def tab(x):
	return "\t"*x

class main(object):
	current_node_name = "node0"
	code = ""
	current_childs_pos = []
	mapping = None
	def __init__(self):
		self.current_node_name = "node0"
		self.code = ""
		self.current_childs_pos = []
		self.mapping = MappingMakin()
		try:
			while True:
				self.menu()
		except KeyboardInterrupt:
			save(self.mapping)
		raw_input()
	
	
	def is_key_c(self):
		return windll.user32.GetAsyncKeyState(ord("C"))!=0
	def is_key_n(self):
		return windll.user32.GetAsyncKeyState(ord("N"))!=0
	
	def menu(self):
		print("position your mouse and")
		print("add childs for current node press (C) node"+str(self.mapping.current_node))
		print("set childs for other node press (N)")
		
		while not(self.is_key_c()) and not(self.is_key_n()):
			pass
		if self.is_key_c():
			while self.is_key_c(): pass
			print("add childs for current node")
			mos = mouse_pos_get()
			self.current_childs_pos.append((int(mos[0]), int(mos[1])))
			
		elif self.is_key_n():
			while self.is_key_n(): pass
			print("done for current childs, recalculating relative pos")
			if self.current_childs_pos!=[]:
				self.mapping.add_and_decide(self.current_childs_pos)
			else:
				print("current node has empty childs")
			
			
			print("pick which to be current node:")
			index = 0
			for n in self.mapping.node_map:
				print("\tnode "+str(index))
				index += 1
			print("input number",)
			self.mapping.current_node = input()
			self.current_childs_pos = []
		
	def display(self, *text):
		print text
	
app = main()
