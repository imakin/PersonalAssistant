#!/usr/bin/env python
import subprocess
import re
import time
from sys import argv
verbose = False
if (len(argv)>1):
	if argv[1]=="-v" or argv[1]=="--verbose":
		verbose = True
		
bulan = ["madu", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

wget = "wget --user-agent=\"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0\" "
wget = wget + "\"https://tiket.kereta-api.co.id\" -O /tmp/ka.html"
if (not verbose):
	wget = wget + " -o /tmp/ka_wgetoutput"
	
subprocess.call(wget, shell=True)

f = open("/tmp/ka.html","r")
halaman = f.read()
f.close()

ptanggal = halaman[halaman.find("<select name=\"tanggal\""):]
ptanggal = ptanggal[:ptanggal.find("</select")]

tanggals = re.compile("(\d{8}#)").findall(ptanggal)
tanggals.reverse()

if (verbose):
	print ("full list of date can be seen at /tmp/ka_tlist.md\n\n")
	
print "Furthest available date to purchase ticket is :"
print tanggals[0][6:8]+" "+bulan[int(tanggals[0][4:6])]+" "+tanggals[0][:4]

if (bulan[int(tanggals[0][4:6])]=="Juli"):
	while (True):
		#~ print "Warnung, Tiket kereta api bulan juli (lebaran) sudah bisa dipesan!"
		print "Warnung, Train ticket for Juli (lebaran) can be purchased now!"
		subprocess.call("notify-send 'warning' 'Warnung, Train ticket for Juli (lebaran) can be purchased now!'",shell=True)
		time.sleep(15)
	
	
f = open("/tmp/ka_tlist.md","w")
for tanggal in tanggals:
	f.write( tanggal[:4]+"-"+tanggal[4:6]+"-"+tanggal[6:8])
f.close()

