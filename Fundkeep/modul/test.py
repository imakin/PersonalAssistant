#!/usr/bin/env python
import os,sys
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"

def makinGetYear():
	return os.popen("date +'%Y'").read()[:-1]
def makinGetMonth():
	return os.popen("date +'%m'").read()[:-1]
def makinGetDay():
	return os.popen("date +'%d'").read()[:-1]

hari = "01"
bulan = "09"
if (hari=="01"):
	t_day = 31
	t_bulan = ("0"+str(int(bulan)-1))[-2:]
	print t_bulan	
	dapet = 0
	while (dapet==0):
		try:
			print folder+"data/"+makinGetYear()+"/"+t_bulan+"/"+str(t_day)+"/balance_before","r"
			f = open(folder+"data/"+makinGetYear()+"/"+t_bulan+"/"+str(t_day)+"/balance_before","r")
			print t_day
			dapet = 1
		except:
			t_day = t_day - 1
			
