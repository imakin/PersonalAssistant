#!/usr/bin/env python
import os,sys
from random import randint
folder = "/media/kentir1/Development/Linux_Program/Fundkeep/"

message=""

def makinGetYear():
	return int(os.popen("date +'%Y'").read()[:-1])
def makinGetMonth():
	return int(os.popen("date +'%m'").read()[:-1])
def makinGetDay():
	return int(os.popen("date +'%d'").read()[:-1])

def makinGetNextYear(nextday):
	return os.popen("date --date='"+str(nextday)+" day' +'%Y'").read()[:-1]
def makinGetNextMonth(nextday):
	return os.popen("date --date='"+str(nextday)+" day' +'%m'").read()[:-1]
def makinGetNextDay(nextday):
	return os.popen("date --date='"+str(nextday)+" day' +'%d'").read()[:-1]

os.system("mkdir "+folder+"data")
os.system("mkdir "+folder+"data/20ksaves")
os.system("mkdir "+folder+"data/20ksaves/generated")
os.system("mkdir "+folder+"data/20ksaves/generated/rand")

#ada tanggal yang blm kelewat
ada=0
data=""
tahun=0
bulan=0
tanggal=0
try:
	f = open(folder+"data/20ksaves/generated/rand/.d","r")
	data=f.read()
	f.close()
	tahun = int(data[0:4])
	bulan = int(data[5:7])
	tanggal=int(data[8:11])
	if (tahun>makinGetYear()):
		ada=1
	elif ((bulan>makinGetMonth()) 	and	(tahun>=makinGetYear())):
		ada=1
	elif ((tanggal>=makinGetDay())	and	(bulan>=makinGetMonth())	and (tahun>=makinGetYear())):
		ada=1
	else:
		ada = 0
except:
	ada=0

#BIKIN
if (ada==0):
	#get last installment
	f = open(folder+"data/installment/date","r")
	data = f.read()
	f.close()
	i=0
	j = data.find("\n")
	data = data[j+1:]

	j = data.find(" ")
	n_day = (data[i:j])
	data = data[j+1:]

	j = data.find(" ")
	n_month = (data[i:j])
	data = data[j+1:]

	j = data.find(" ")
	n_year = (data[i:j])
	data = data[j+1:]

	yyy = 0
	while ((os.popen("date --date='"+str(yyy)+" day' +'%Y%m%d'").read()[:-1])!=((n_year)+(n_month)+(n_day))):
		yyy=yyy+1
	kapan = randint(yyy,yyy+7)
	print kapan
	tahun = int( makinGetNextYear(kapan))
	bulan = int( makinGetNextMonth(kapan))
	tanggal=int( makinGetNextDay(kapan))
	f = open(folder+"data/20ksaves/generated/rand/.d","w")
	f.write(str(makinGetNextYear(kapan))+"-"+str(makinGetNextMonth(kapan))+"-"+str(makinGetNextDay(kapan)))
	f.close()
	
	
jatuhnya = str(tahun)+str(bulan)+str(tanggal)
if (jatuhnya==(os.popen("date --date='1 day' +'%Y%m%d'").read()[:-1])):
	os.system("notify-send 'Fundkeep' 'tomorrow you have to save all the 20k money you have'")
elif (jatuhnya==(os.popen("date +'%Y%m%d'").read()[:-1])):
	os.system("notify-send 'Fundkeep' 'today you have to save all the 20k money you have'")



