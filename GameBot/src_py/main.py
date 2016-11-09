from grinding import GrindingMakin
import sys, os
from PySide import QtCore #-- LGPL
from PySide import QtGui
from makinreusable.makinbutton import MakinButton
from makinreusable.makinframe import MakinFrame

class MainGUI(QtGui.QMainWindow):
	
	def __init__(self,parent=None,quit_command=None):
		super(MainGUI,self).__init__(parent)
		self.show()
		self.quit_command = quit_command
		self.grinding = GrindingMakin()
		
		
		self.build_display()
		self.build_signal()
		
	def build_display(self):
		self.move(1000,0)
		self.resize(300,600)
		
		self.display_width = self.geometry().width()
		self.display_height = self.geometry().height()
		
		
		self.centralwidget = QtGui.QWidget(self)
		self.centralwidget.setObjectName("centralwidget")
		self.igr_centralwidget = QtGui.QGridLayout(self.centralwidget)
		self.igr_centralwidget.setObjectName("igr_cetralwidget")
		self.igr_centralwidget.setContentsMargins(0,0,0,0)
		self.igr_centralwidget.setSpacing(0)
		
		
		self.fr_main = MakinFrame(self.centralwidget)
		self.igr_main = QtGui.QGridLayout(self.fr_main)
		self.igr_centralwidget.addWidget(self.fr_main, 0,0,1,1)
		
		
		# self.lb_title
		self.lb_title = QtGui.QLabel(self.fr_main)
		self.lb_title.setText("Makin MCOC bot")
		self.igr_main.addWidget(self.lb_title, 0,0,1,3,QtCore.Qt.AlignTop)#(row), (column), spand row, spand column
		
		# self.bt_calibrateposition
		self.bt_calibrateposition = MakinButton(self.fr_main)
		self.bt_calibrateposition.setObjectName("bt_calibrate_position")
		self.bt_calibrateposition.setText("calibrate position")
		self.igr_main.addWidget(self.bt_calibrateposition, 1,0,1,1,QtCore.Qt.AlignTop)
		
		
		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	def build_signal(self):
		self.bt_calibrateposition.clicked.connect(self.grinding.calibrate_position)

if (__name__=="__main__"):
	app = QtGui.QApplication(sys.argv)
	def quitapp():
		app.quit()
	dmw = MainGUI(None,quitapp)
	sys.exit(app.exec_())
