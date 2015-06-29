#!/usr/bin/env python
import sys
from PySide import QtCore
from PySide import QtGui
from AnimK import MakinButton,MakinButtonExit

SURAT = 81
AYAT = 4
def Surat():
	if SURAT<10:
		return "s00"+str(SURAT)
	elif SURAT<100:
		return "s0"+str(SURAT)
	else:
		return "s"+str(SURAT)
def Ayat():
	if AYAT<10:
		return "a00"+str(AYAT)+".png"
	elif AYAT<100:
		return "a0"+str(AYAT)+".png"
	else:
		return "a"+str(AYAT)+".png"

class MainGUI(QtGui.QMainWindow):
	def __init__(self,p=None):
		super(MainGUI,self).__init__(p)
		self.setObjectName("MainWindow")
		self.resize(500, 200)
		self.DrawInit();
		self.startTimer = QtCore.QTimer(self)
		self.startTimer.timeout.connect(self.DrawImage)
		self.startTimer.start(50)
		self.show()
    
	def DrawInit(self):
		self.centralwidget = QtGui.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.igr_cetralwidget = QtGui.QGridLayout(self.centralwidget)
		self.igr_cetralwidget.setObjectName("igr_cetralwidget")
		self.igr_cetralwidget.setContentsMargins(0,0,0,0)
		self.igr_cetralwidget.setSpacing(0)
		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)
		
		self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
		self.graphicsView.setObjectName("graphicsView")
		self.igr_cetralwidget.addWidget(self.graphicsView, 0, 0, 1, 1)
		
		
	def DrawImage(self):
		self.startTimer.stop()
		self.scene = QtGui.QGraphicsScene(self)
		self.image = QtGui.QPixmap("/media/kentir1/Development/Ebook/quran/img/"+Surat()+"/"+Ayat())
		self.scene.addPixmap(self.image)
		self.graphicsView.setScene(self.scene)
		#-- Exit button
		WinW = self.centralwidget.geometry().width()
		WinH = self.centralwidget.geometry().height()
		size = 50
		self.tb_Exit = MakinButtonExit("Hide",self)
		self.tb_Exit.setGeometry(QtCore.QRect((WinW-size-2), 2, size, size))
		self.tb_Exit.setObjectName("tb_Exit")
		self.tb_Exit.show()
		self.tb_Exit.clicked.connect(self.Exit)
		
		#-- Next prev button
		WinW = self.centralwidget.geometry().width()
		WinH = self.centralwidget.geometry().height()
		size = 30
		self.tb_Next = MakinButtonExit(">>",self,0,250,3,40,"80,50,30","180,50,30")
		self.tb_Next.setGeometry(QtCore.QRect((WinW-size-2), WinH/2-size/2, size, size))
		self.tb_Next.setObjectName("tb_Next")
		self.tb_Next.setProperty("cursor", QtCore.Qt.PointingHandCursor)
		self.tb_Next.show()
		self.tb_Next.clicked.connect(self.Next)
		
		self.tb_Prev = MakinButtonExit("<<",self,0,250,3,40,"80,50,30","180,50,30")
		self.tb_Prev.setGeometry(QtCore.QRect(2, WinH/2-size/2, size, size))
		self.tb_Prev.setObjectName("tb_Prev")
		self.tb_Prev.setProperty("cursor", QtCore.Qt.PointingHandCursor)
		self.tb_Prev.show()
		self.tb_Prev.clicked.connect(self.Prev)
	
	def Next(self):
		global AYAT
		AYAT = AYAT+1
		self.ReloadImage()
		
	def Prev(self):
		global AYAT
		AYAT = AYAT-1
		self.ReloadImage()
		
	
	def ReloadImage(self):
		global AYAT
		global SURAT
		
		print(Surat()+" "+Ayat())
		self.scene.removeItem(self.scene.items()[0])
		if (not self.image.load("/media/kentir1/Development/Ebook/quran/img/"+Surat()+"/"+Ayat())):
			if (AYAT>0):
				SURAT += 1
				AYAT = 1
				self.image.load("/media/kentir1/Development/Ebook/quran/img/"+Surat()+"/"+Ayat())
			else:
				SURAT -= 1
				AYAT = 287 #--- todo AYAT yang paling belakang dengan cepat!
				while (
						(not self.image.load("/media/kentir1/Development/Ebook/quran/img/"+Surat()+"/"+Ayat()))
						and 
						(AYAT>0)
						):
					AYAT = AYAT-1
		self.scene.addPixmap(self.image)
		
	def Exit(self):
		sys.exit()
		
if (__name__=="__main__"):
	app = QtGui.QApplication(sys.argv)
	dmw = MainGUI()
	sys.exit(app.exec_())
