#!/usr/bin/env python
import os,sys
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"
try:
	argument = sys.argv[1]
except:
	argument = 0

customday = 0
try:
	customday = int(sys.argv[2])
except:
	customday = 0


def makinGetYear():
	return os.popen("date --date='"+str(customday)+" day ago'  +'%Y'").read()[:-1]
def makinGetMonth():
	return os.popen("date --date='"+str(customday)+" day ago'  +'%m'").read()[:-1]
def makinGetDay():
	return os.popen("date --date='"+str(customday)+" day ago'  +'%d'").read()[:-1]

def makinGetPrevYear(daypassed):
	return os.popen("date --date='"+str(daypassed+customday)+" day ago' +'%Y'").read()[:-1]
def makinGetPrevMonth(daypassed):
	return os.popen("date --date='"+str(daypassed+customday)+" day ago' +'%m'").read()[:-1]
def makinGetPrevDay(daypassed):
	return os.popen("date --date='"+str(daypassed+customday)+" day ago' +'%d'").read()[:-1]
	

#last entry
f = open(folder+"data/last_entry","r")
f.close()
#~ le = f.read()
#~ le_y=le[:4]
#~ le_m=le[4:6]
#~ le_d=le[6:]



#balance_out input
#~ os.system("gedit "+folder+"var/input")
#~ f = open(folder+"var/input","r")
#~ data = f.read()
#~ f.close()
#~ 
#~ balance_out = int(data[:data.find(" ")])
#~ balance_ket = data[data.find(" ")+1:-1]
#~ print balance_ket

os.system("mkdir "+folder+"data")
os.system("mkdir "+folder+"data/"+makinGetYear())
os.system("mkdir "+folder+"data/"+makinGetYear()+"/"+makinGetMonth())
os.system("mkdir "+folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay())

if (argument == "in"):
	os.system("gedit "+folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_in")
elif (argument == "out"):
	os.system("gedit "+folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_out")

balance_before = 0
#get previously recorded balance

dapet = 0
dpassed = 1
while (dapet == 0):
	try:
		f = open(folder+"data/"
					+makinGetPrevYear(dpassed)
					+"/"
					+makinGetPrevMonth(dpassed)
					+"/"
					+makinGetPrevDay(dpassed)
					+"/balance_after","r")
		dapet = 1
	except:
		dapet = 0
		dpassed = dpassed + 1
		f.close()
#~ print dpassed
#~ print (folder+"data/"+makinGetPrevYear(dpassed)+"/"+makinGetPrevMonth(dpassed)+"/"+makinGetPrevDay(dpassed)+"/balance_after")

balance_before = int(f.read())
f.close()
f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_before","w")
f.write(str(balance_before))
f.close()

balance_in = 0

##do the counting
#balance_in
try:
	f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_in","r")
	data = f.read()
	f.close()
	cursor = data.find(" ")
	
	#~ if (data[:cursor])=="clr":
		#~ balance_in = 0
		#~ balance_before = 0
	#~ else:
		#~ balance_in = balance_in + int(data[:cursor])
	balance_in = balance_in + int(data[:cursor])
	cursor = cursor + 1
	cursor = cursor + data[cursor:].find("\n")
	
	while (cursor!=(-1)):
		cursor_2 = data[cursor:].find(" ")
		cursor_2 = cursor + cursor_2
		#~ if (data[cursor:cursor_2])[1:4]=="clr":
			#~ balance_in = 0
			#~ balance_before = 0
		#~ else:
			#~ balance_in = balance_in + int(data[cursor:cursor_2])
		balance_in = balance_in + int(data[cursor:cursor_2])
			
		cursor = cursor_2 + 1
		cursor = cursor + data[cursor:].find("\n")
except:
	balance_in = balance_in
	
print balance_in

balance_out = 0
try:
	f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_out","r")
	data = f.read()
	f.close()
	cursor = data.find(" ")
	#~ if (data[:cursor]=="clr"):
		#~ balance_before = 0
	#~ else:
		#~ balance_out = balance_out + int(data[:cursor])
	balance_out = balance_out + int(data[:cursor])
	cursor = cursor + 1
	cursor = cursor + data[cursor:].find("\n")
	
	while (cursor!=(-1)):
		cursor_2 = data[cursor:].find(" ")
		cursor_2 = cursor + cursor_2
		
		#~ if (data[cursor:cursor_2])[1:4]=="clr":
			#~ balance_before = 0
		#~ else:
			#~ balance_out = balance_out + int(data[cursor:cursor_2])
		balance_out = balance_out + int(data[cursor:cursor_2])
		cursor = cursor_2 + 1
		cursor = cursor + data[cursor:].find("\n")
except:
	balance_out = balance_out

balance_after = balance_before + balance_in - balance_out

print "balance after = "+str(balance_after)
f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_after","w")
f.write(str(balance_after))
f.close()
os.system("fundkeep")

