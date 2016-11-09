from PySide import QtCore, QtGui

class MakinFrame(QtGui.QFrame):
	mousegeser = QtCore.Signal(int,int)
	def __init__(self,parent=None):
		super(MakinFrame,self).__init__(parent)
		self.setMouseTracking(True)

	def setMouseTracking(self, flag):
		def recursive_set(parent):
			for child in parent.findChildren(QtCore.QObject):
				try:
					child.setMouseTracking(flag)
				except:
					pass
				recursive_set(child)
		QtGui.QWidget.setMouseTracking(self,flag)
		recursive_set(self)
	
	def mouseMoveEvent(self, me):
		a = QtGui.QFrame.mouseMoveEvent(self,me)
		self.mousegeser.emit(me.x(), me.y())
		return a
	
