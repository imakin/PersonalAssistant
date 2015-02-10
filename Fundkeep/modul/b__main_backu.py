#!/usr/bin/env python
import os,sys
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"

def makinGetYear():
	return os.popen("date +'%Y'").read()[:-1]
def makinGetMonth():
	return os.popen("date +'%m'").read()[:-1]
def makinGetDay():
	return os.popen("date +'%d'").read()[:-1]

def makinGetPrevYear(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%Y'").read()[:-1]
def makinGetPrevMonth(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%m'").read()[:-1]
def makinGetPrevDay(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%d'").read()[:-1]
	

#last entry
f = open(folder+"data/last_entry","r")
le = f.read()
le_y=le[:4]
le_m=le[4:6]
le_d=le[6:]



#input
os.system("gedit "+folder+"var/input")
f = open(folder+"var/input","r")
data = f.read()
f.close()

balance_out = int(data[:data.find(" ")])
balance_ket = data[data.find(" ")+1:-1]
print balance_ket

os.system("mkdir "+folder+"data")
os.system("mkdir "+folder+"data/"+makinGetYear())
os.system("mkdir "+folder+"data/"+makinGetYear()+"/"+makinGetMonth())
os.system("mkdir "+folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay())

balance_before = 0

#ambil balance dr hari sebelumnya

dapet = 0
while (dapet == 0):
	dpassed = 1
	try:
		f = open(folder+"data/"
					+makinGetPrevYear(dpassed)
					+"/"
					+makinGetPrevMonth(dpassed)
					+"/"
					+makinGetPrevDay(dpassed)
					+"/balance_after","r")
		

if (makinGetDay()=="01"):
	t_day = 31
	t_bulan = ("0"+str(int(makinGetMonth())-1))[-2:]
	t_tahun = makinGetYear()
	if (int(makinGetMonth())=1):
		t_bulan = 12
		t_tahun = makinGetYear()-1
	print t_bulan	
	dapet = 0
	while (dapet==0):
		try:
			f = open(folder+"data/"+t_tahun+"/"+t_bulan+"/"+("0"+str(t_day))[-2:]+"/balance_after","r")
			print t_day
			dapet = 1
			balance_before = int(f.read())
		except:
			t_day = t_day - 1
			f.close()
else:
	t_day = int(makinGetDay())-1
	#~ t_bulan = ("0"+str(int(makinGetMonth())))[-2:]
	t_bulan = makinGetMonth()
	
	f = open(folder+"data/"+makinGetYear()+"/"+t_bulan+"/"+("0"+str(t_day))[-2:]+"/balance_after","r")
	balance_before = int(f.read())

#bila fresh input
try:
	f = open(folder+"data/"+t_tahun+"/"+t_bulan+"/"+("0"+str(t_day))[-2:]+"/balance_after","r")
	
except:
	
	
#bila hanya mengupdate isi balance_out (pengeluaran hari ini)




