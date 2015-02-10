#!/usr/bin/env python
import os,sys
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"

def makinGetYear():
	return os.popen("date +'%Y'").read()[:-1]
def makinGetMonth():
	return os.popen("date +'%m'").read()[:-1]
def makinGetDay():
	return os.popen("date +'%d'").read()[:-1]

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
f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/_balance_out","w")
f.write(str(balance_out))
f.close()

f = open(folder+"data/"+makinGetYear()+"/"+makinGetMonth()+"/"+makinGetDay()+"/_balance_ket","w")
f.write(balance_ket)
f.close()

f = open(folder+"data/balance","r")
balance = int(f.read())
f.close()

balance = balance - balance_out

f = open(folder+"data/balance","w")
f.write(str(balance))
f.close()


