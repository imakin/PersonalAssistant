"""
@author Izzulmakin, January - July 2015
"""
from PySide import QtCore, QtGui

class MakinButton(QtGui.QPushButton):
	"""custom qpushbutton ta kei ono sinyal dihover & dileave"""
	"""gawe slot? http://www.pythoncentral.io/pysidepyqt-tutorial-creating-your-own-signals-and-slots/"""
	dihover = QtCore.Signal()
	dileave = QtCore.Signal()
		
	def __init__(self,text="",parent=None):
		super(MakinButton,self).__init__(text,parent)
		
	def getStylesheetByName(self,name):
		re.findall(r"([\w-]+:.+;)",self.stylesheet)
	
	def enterEvent(self, event):
		self.dihover.emit()
		return QtGui.QPushButton.enterEvent(self, event)
		
	def leaveEvent(self, event):
		self.dileave.emit()
		return QtGui.QPushButton.leaveEvent(self, event)


class MakinButtonAnimated(MakinButton):
	def __init__(self,p,col1="rgba(58, 107, 115, 155)",col2="rgba(255, 255, 255, 0)"):
		super(MakinButtonAnimated,self).__init__(p)
		self.col1 = col1
		self.col2 = col2
		self.setStyleSheet("background-color:transparent;")
		self.AStop = 0.0
		self.StyleStatic = "border:0px;"
		self.ASpeed = 20
		self.updateAnim()
		self.Ti = QtCore.QTimer(self)
		self.To = QtCore.QTimer(self)
		self.Ti.timeout.connect(self.animIn)
		self.To.timeout.connect(self.animOut)
	
	def setStyleStatic(self,style):
		self.StyleStatic = style
		self.updateAnim()
	
	def enterEvent(self,event):
		self.To.stop()
		self.Ti.start(self.ASpeed)
		return QtGui.QPushButton.enterEvent(self, event)
		
	def leaveEvent(self, event):
		self.Ti.stop()
		self.To.start(self.ASpeed)
		return QtGui.QPushButton.leaveEvent(self, event)
		
	def animIn(self):
		self.AStop += 0.1
		if (self.AStop>=0.90):
			self.AStop = 0.94
			self.updateAnim()
			self.Ti.stop()
		else:
			self.updateAnim()
	
	def animOut(self):
		self.AStop -= 0.1
		if (self.AStop<=0.1):
			self.AStop = 0.0
			self.updateAnim()
			self.To.stop()
		else:
			self.updateAnim()
	
	def updateAnim(self):
		self.setStyleSheet("#"+str(self.objectName())+"""{background-color: qradialgradient(spread:pad, 
																cx:0.5, 
																cy:0.5, 
																radius:0.5, 
																fx:0.5, 
																fy:0.5, 
																stop:"""+str(self.AStop)+" "+self.col1+""", 
																stop:"""+str(self.AStop+0.05)+" "+self.col2+""");}
																"""+str(self.StyleStatic))
