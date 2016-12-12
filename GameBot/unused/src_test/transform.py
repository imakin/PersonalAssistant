import math
clockdeg = 0
pi = math.pi

x = 100
y = 0
while (clockdeg<360):
	print(400+ x*math.cos(clockdeg*pi/180.0) - y*math.sin(clockdeg*pi/180.0))
	print(400+ x*math.sin(clockdeg*pi/180.0) + y*math.cos(clockdeg*pi/180.0))
	clockdeg += 45
