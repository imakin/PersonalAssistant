#!/usr/bin/env python
import os,sys
try:
	argument = sys.argv[1]
except:
	argument = 0

def elinsGetDate():
	return os.popen("date +'%Y%m%d'").read()[:-1]

#-- set path to program folder, or just hardcode where it is if main.py is in separated place
Path = str(__file__).replace("main.py","").replace("\\","/")
print Path

namafile = "time"+elinsGetDate()+".xml"
todayexist = 0
k = open(Path+"kosong","r")
datakosong = k.read()
k.close()
dummy = 0
programoutput = " "

try:
	today = open(""+Path+""+namafile,"r")
	#~ print "today file found"
	data = today.read()
	today.close()
	if (data!=datakosong):
		todayexist = 1
	os.system("cp "+Path+"*.xml "+Path+"back/")
except:
	#~ print "today time file not found"
	dummy = 0
	
if (todayexist==0):
	#~ print "fetching new file"
	os.system("cp "+Path+"*.xml "+Path+"back/")
	os.system("rm -f "+Path+"*.xml")
	os.system("wget -q 'http://www.mahesajenar.com/scripts/adzan.php?kota=Yogyakarta&type=text3' --output-document="+Path+""+namafile)
	os.system("cp "+Path+"*.xml "+Path+"back/")
	f =  open(""+Path+""+namafile,"r")
	data = f.read()
	f.close()

if (data==datakosong):
	print "fetching failed"
	programoutput = "fetching time for today failed"
	os.system("rm -f "+Path+"back/"+namafile)
	dummy = 123
	#~ dummy = 0
else:
	#bikin cukup 1 backup, the latest...
	os.system("cp "+Path+"back/"+namafile+" /tmp/"+namafile)
	os.system("rm -f "+Path+"back/*.xml")
	os.system("cp /tmp/"+namafile+" "+Path+"back/")
	data=data.upper()
	posisi_awal=data.upper().find("IMSAK")
	if (posisi_awal<0):
		programoutput = "fetching time for today failed"
		dummy = 123
	else:
		pos=posisi_awal
		programoutput = data[pos:pos+15]
		pos=pos+15+2
		programoutput = programoutput+"\n"+ data[pos:pos+16]
		pos=pos+16+2
		programoutput = programoutput+"\n"+ data[pos:pos+16]
		pos=pos+16+2
		programoutput = programoutput+"\n"+ data[pos:pos+15]
		pos=pos+15+2
		programoutput = programoutput+"\n"+ data[pos:pos+17]
		pos=pos+17+2
		programoutput = programoutput+"\n"+ data[pos:pos+14]

if (dummy==123):
	programoutput = "sikik"
	backupfile = os.popen("ls "+Path+"back/").read()[:-1]
	backupfile_tahun = backupfile[4:8].upper()
	backupfile_bulan = backupfile[8:10].upper()
	backupfile_hari = backupfile[10:12].upper()
	programoutput = "Today fetch failed, last fetched info:\n\t\t\t["+backupfile_hari+" - "+backupfile_bulan+" - "+backupfile_tahun+"]\n"
	today = open(""+Path+"back/"+backupfile,"r")
	data = today.read()
	today.close()
	posisi_awal=data.upper().find("IMSAK")
	pos=posisi_awal
	programoutput = programoutput+data[pos:pos+15]
	pos=pos+15+2
	programoutput = programoutput+"\n"+ data[pos:pos+16]
	pos=pos+16+2
	programoutput = programoutput+"\n"+ data[pos:pos+16]
	pos=pos+16+2
	programoutput = programoutput+"\n"+ data[pos:pos+15]
	pos=pos+15+2
	programoutput = programoutput+"\n"+ data[pos:pos+17]
	pos=pos+17+2
	programoutput = programoutput+"\n"+ data[pos:pos+14]
	print(programoutput)
	
	
	

programoutput = "notify-send \"Jarwo Info\" \""+programoutput+"\""
os.system(programoutput)
