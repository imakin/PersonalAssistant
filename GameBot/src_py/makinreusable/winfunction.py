from ctypes import *
import time
import thread

MOUSEEVENTF_LEFTDOWN = 2
MOUSEEVENTF_LEFTUP = 4
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYCODE_LBUTTON = 0x01
KEYCODE_RBUTTON = 0x02
KEYCODE_MBUTTON = 0x04
KEYCODE_0 = 0x30
KEYCODE_A = 0x41
KEYCODE_ALT = 0xA4
KEYCODE_F1 = 0x70
KEYCODE_SPACE = 0x20

class Point(Structure):
	""" struct """
	_fields_ = [("x", c_ulong), ("y", c_ulong)]



def mouse_click(x,y):
	"""LEFT"""
	windll.user32.SetCursorPos(x,y)
	windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0,0,0,0)
	windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0,0,0,0)

def mouse_click_drag(x,y, to_x, to_y, drag_time=0.5):
	windll.user32.SetCursorPos(x,y)
	windll.user32.mouse_event(
			MOUSEEVENTF_LEFTDOWN,
			0,0,0,0
		)
	time.sleep(drag_time/2)
	windll.user32.SetCursorPos(to_x,to_y)
	time.sleep(drag_time/2)
	windll.user32.mouse_event(
			MOUSEEVENTF_LEFTUP | MOUSEEVENTF_MOVE, 
			0,0,0,0
		)

def keyboard_send(keyvalue):
	"""keyvalue is key code or string letter/number"""
	if type(keyvalue)==str:
		keyvalue = ord(keyvalue.upper())
	windll.user32.keybd_event(keyvalue,0,0,0)
	windll.user32.keybd_event(keyvalue,0,KEYEVENTF_KEYUP,0)


def mouse_pos_get():
	pos = Point()
	windll.user32.GetCursorPos(byref(pos))
	return pos

def mouse_pos_set(x,y):
	windll.user32.SetCursorPos(x,y)


class HotKeyManager(object):
	hotkeys = []
	def __init__(self):
		self.check_continue = False
		pass
	
	def add(self, letter_key, function_pointer):
		"""
		@param letter_key the hotkey letter will be ALT+(letter_key)
		@param function_pointer the callback function to be executed
		"""
		letter_key = ord(letter_key.upper()[0])
		if (letter_key>=ord('A') and letter_key<=ord('Z')):
			self.hotkeys.append({"key":letter_key, "f":function_pointer})
	
	def check(self):
		self.check_continue = True
		while self.check_continue:
			for hotkey in self.hotkeys:
				if (
					(windll.user32.GetAsyncKeyState(KEYCODE_ALT))!=0 and
					(windll.user32.GetAsyncKeyState(hotkey["key"]))!=0
				):
					thread.start_new_thread(hotkey["f"], ())
					print("HotKeyManager: "+str(hotkey["key"])+" triggered")
					while (
							(windll.user32.GetAsyncKeyState(KEYCODE_ALT))!=0 and
							(windll.user32.GetAsyncKeyState(hotkey["key"]))!=0
						):pass
					


	def start(self):
		thread.start_new_thread(self.check, ())
	def stop(self):
		self.check_continue = False
			
			
	def test(self):
		while True:
			for hotkey in self.hotkeys:
				print(windll.user32.GetAsyncKeyState(KEYCODE_ALT),
					windll.user32.GetAsyncKeyState(hotkey["key"]))
