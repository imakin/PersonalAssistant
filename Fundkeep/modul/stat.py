#!/usr/bin/python
import os


def makinGetPrevYear(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%Y'").read()[:-1]
def makinGetPrevMonth(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%m'").read()[:-1]
def makinGetPrevDay(daypassed):
	return os.popen("date --date='"+str(daypassed)+" day ago' +'%d'").read()[:-1]


base_folder = "/media/kentir1/Development/Linux_Program/Fundkeep/data/"

folder = ""

dayago = 0
dayget = 0
outToday = 0

lastDayD = makinGetPrevDay(dayago)
lastDayM = makinGetPrevMonth(dayago)
lastDayY = makinGetPrevYear(dayago)

outData = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
datamax=0
datamin=1000000000

#~ outData[1] = 3
print '\tLoading...'
if __name__ == '__main__':
	while (dayget < 14) and (int(lastDayY)>2012):
		lastDayD = makinGetPrevDay(dayago)
		lastDayM = makinGetPrevMonth(dayago)
		lastDayY = makinGetPrevYear(dayago)
		
		folder = base_folder+lastDayY+'/'+lastDayM+'/'+lastDayD+'/'	
		
		#yang ini tentang keluaran dikurangi masukan
		#~ try:
			#~ f = open(folder+"balance_after","r")
			#~ data_after= f.read()
			#~ f.close()
			#~ f = open(folder+"balance_before","r")
			#~ data_before= f.read()
			#~ f.close()
			#~ 
			#~ outToday = int(data_before)-int(data_after)
			#~ dayget = dayget+1
			#~ print str(lastDayY)+"-"+str(lastDayM)+'-'+str(lastDayD)+':'+str(outToday)
		#~ except:
			#~ outToday = 0
		#~ 
		
		#yang ini tentang keluarannya saja 
		try:
			f = open(folder+"balance_out","r")
			data= f.read()
			f.close()
			
			balance_out = 0
			
			#ambil pengeluaran di tiap baris dalam masing-masing file balance_out
			try:
				cursor = data.find(" ")
				balance_out = balance_out + int(data[:cursor])
				cursor = cursor + 1
				cursor = cursor + data[cursor:].find("\n")
				
				while (cursor!=(-1)):
					cursor_2 = data[cursor:].find(" ")
					cursor_2 = cursor + cursor_2
					
					balance_out = balance_out + int(data[cursor:cursor_2])
					cursor = cursor_2 + 1
					cursor = cursor + data[cursor:].find("\n")
			except:
				balance_out = balance_out
			
			outToday = balance_out
			outData[dayget]=outToday
			dayget = dayget+1
			print str(lastDayY)+"-"+str(lastDayM)+'-'+str(lastDayD)+':'+str(outToday)
			
			if (datamax<outToday):
				datamax=outToday
			if (datamin>outToday):
				datamin=outToday
		except:
			outToday = 0
		
		
		dayago = dayago+1
		
		


totbaris = 40
totkolom = 14
baris= 40
textbaris=''
while (baris>0):
	kolom=0
	textbaris=' '
	while(kolom<14):
		if (((float(outData[kolom]-datamin)/float(datamax-datamin))*totbaris)<baris):
			textbaris = textbaris+'[   ]'
		else:
			textbaris = textbaris+'[###]'
		kolom=kolom+1
	print textbaris
	baris=baris-1
	

kolom=0
textbaris='  '
while(kolom<14):
	textnilai=str(outData[kolom]/1000)+'k'
	while len(textnilai)<4:
		textnilai=textnilai+' '
	textbaris = textbaris+textnilai+' '
	kolom=kolom+1
print textbaris

