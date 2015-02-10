#!/usr/bin/env python
import os,sys
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"

message=""

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
	
os.system("mkdir "+folder+"data")
os.system("mkdir "+folder+"data/"+makinGetYear())
os.system("mkdir "+folder+"data/"+makinGetYear()+"/"+makinGetMonth())
os.system("mkdir "+folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay())

message=""
blm=0
try:
	f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_in","r")
except:
	message = message + "You have not record your income today, press ctrl-alt-i to do it.\n"
	blm = 1

try:
	f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_out","r")
except:
	if (blm==1):
		message = message + "You have not record your outcome today either, press ctrl-alt-o to do it.\n"
	else:
		message = message + "You have not record your outcome today, press ctrl-alt-i to do it.\n"
	blm=1

try:
	f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/balance_after","r")
	balance_after = str(int(f.read()))
	f.close()
	pjg = len(balance_after)

	#bikin tulisan format rupiah
	duit_c = int(balance_after)
	duit= ""
	while (duit_c>999):
		duit = (str(duit_c)[-3:])+"."+duit
		duit_c = duit_c/1000
	duit = ((str(duit_c)[-3:])+"."+duit)[:-1]
	duit_c = duit_c/1000
	message = message+"Your balance is Rp "+duit+",00\n"
	f = open(folder+"data/bank/balance")
	data = f.read()
	f.close()
	duit_c = int(data)+int(balance_after)
	duit= ""
	while (duit_c>999):
		duit = (str(duit_c)[-3:])+"."+duit
		duit_c = duit_c/1000
	duit = ((str(duit_c)[-3:])+"."+duit)[:-1]
	duit_c = duit_c/1000
	message = message+"Your total balance is Rp "+duit+",00"
except:
	message = message
print message
os.system("notify-send 'Fundkeep (c) makin 2013' '"+message+"'")
os.system(folder+"modul/budgetmaintainer.py")
os.system(folder+"modul/tsave.py")
