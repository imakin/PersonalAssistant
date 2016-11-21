from makinreusable.winfunction import *
import ImageGrab
import time

def tab(x):
	return "\t"*x

class main(object):
	def __init__(self):
		self.display("position your mouse then press C button")
		
		while windll.user32.GetAsyncKeyState(ord("C"))==0:
			x0,y0 = mouse_pos_get()
		while windll.user32.GetAsyncKeyState(ord("C"))!=0:
			pass
		
		print("capture from",x0,y0,
			"\n",
			"now position your mouse then press C button again"
		)
		
		while windll.user32.GetAsyncKeyState(ord("C"))==0:
			x1,y1 = mouse_pos_get()
		while windll.user32.GetAsyncKeyState(ord("C"))!=0:
			pass
		
		img = ImageGrab.grab()
		print("capture from",x0,y0,"to",x1,y1)
		
		step = 2
		print("input resolution detail steps: ")
		step = input()
		step = int(step)*1
		
		#working
		
		code = ""
		code += "from image import ImageManager \n\n"
		code += "class test(ImageManager):"+"\n"
		code += tab(1)+"def is_something(self, image_grab=None):"	+"\n"
		code += tab(2)+"\"\"\""	+"\n"
		code += tab(2)+"doc"		+"\n"
		code += tab(2)+"\"\"\""	+"\n"
		code += tab(2)+"img = self.get_grab(image_grab)"		+"\n"
		
		code += tab(2)+"step = %d"%step+"\n"
		code += tab(2)+"coltol = %d"%10+"\n"
		
		#this is loop for in generated code
		code += tab(2)+"for y_code in range(0,self.screen_height):"	+"\n"
		code += tab(3)+"for x_code in range(0,self.screen_width):"	+"\n"
		code += tab(4)+"if ("+"\n"
		#this is loop for in captured image
		for y in range(y0,y1,step):
			for x in range(x0,x1,step):
				r,g,b = img.getpixel((x,y))
				code += (
						tab(5)+
						("self.is_color_similar(img.getpixel((x_code+%d,y_code+%d)),(%d,%d,%d),coltol) and" %
							(x-x0,y-y0, r,g,b)
						)+
						"\n"
					)
		#remove last " and"
		code = code[:-5]+"\n"
		
		code += tab(4)+"):"+"\n"
		code += tab(5)+"return x_code,y_code"+"\n"
		
		code += tab(2)+"return -1,-1"+"\n"
		
		code += tab(1)+"def is_color_similar(self, colorA, colorB, color_tolerance):"+"\n"
		code += tab(2)+"if ("+"\n"
		code += tab(3)+"abs(colorA[0]-colorB[0])<color_tolerance and"+"\n"
		code += tab(3)+"abs(colorA[1]-colorB[1])<color_tolerance and"+"\n"
		code += tab(3)+"abs(colorA[2]-colorB[2])<color_tolerance"+"\n"
		code += tab(2)+"):"+"\n"
		code += tab(3)+"return True"+"\n"
		code += tab(2)+"return False"+"\n"
		
		
		code += "import time"+"\n"
		code += "a=test()"+"\n"
		code += "print(3)"+"\n"
		code += "time.sleep(2)"+"\n"
		code += "print(2)"+"\n"
		code += "time.sleep(2)"+"\n"
		code += "print(1)"+"\n"
		code += "time.sleep(3)"+"\n"
		code += "print(a.is_something())"+"\n"
		
		f = open("captured_code.py", "w")
		f.write(code)
		f.close()
		
		
	def display(self, *text):
		print text
	
app = main()
