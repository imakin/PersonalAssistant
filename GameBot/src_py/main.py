from grinding import GrindingMakin
import sys, os
from PySide import QtCore #-- LGPL
from PySide import QtGui
from makinreusable.makinbutton import MakinButton
from makinreusable.makinframe import MakinFrame
from makinreusable.winfunction import HotKeyManager
import thread

class MainGUI(QtGui.QMainWindow):
	
	def __init__(self,parent=None,quit_command=None):
		super(MainGUI,self).__init__(parent)
		self.show()
		self.quit_command = quit_command
		self.grinding = GrindingMakin(self)
		self.hotkey = HotKeyManager()
		self.log = [""]
		self.build_display()
		self.build_signal()
		
	def build_display(self):
		self.move(1000,0)
		self.resize(300,480)
		
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
		
		# self.lb_status
		self.lb_status = QtGui.QLabel(self.fr_main)
		self.lb_status.setText("status")
		self.igr_main.addWidget(self.lb_status, 1,0,1,3,QtCore.Qt.AlignTop)#(row), (column), spand row, spand column
		
		# self.lb_print
		self.lb_print = QtGui.QLabel(self.fr_main)
		self.lb_print.setText("status")
		self.igr_main.addWidget(self.lb_print, 2,0,20,3,QtCore.Qt.AlignTop)#(row), (column), spand row, spand column
		
		# self.bt_calibrateposition
		self.bt_calibrateposition = MakinButton(self.fr_main)
		self.bt_calibrateposition.setObjectName("bt_calibrate_position")
		self.bt_calibrateposition.setText("calibrate position")
		self.igr_main.addWidget(self.bt_calibrateposition, 23,0,1,1,QtCore.Qt.AlignTop)
		
		# self.bt_start_arena
		self.bt_start_arena = MakinButton(self.fr_main)
		self.bt_start_arena.setObjectName("bt_start_arena")
		self.bt_start_arena.setText("start arena")
		self.igr_main.addWidget(self.bt_start_arena, 24,0,1,1,QtCore.Qt.AlignTop)
		
		# self.bt_arena_fight
		self.bt_arena_fight = MakinButton(self.fr_main)
		self.bt_arena_fight.setObjectName("bt_arena_fight")
		self.bt_arena_fight.setText("arena fight")
		self.igr_main.addWidget(self.bt_arena_fight, 25,0,1,1,QtCore.Qt.AlignTop)
		
		
		
		
		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	
	def signal_calibrate_position(self):
		thread.start_new_thread(self.grinding.calibrate_position, ())
	
	def signal_start_arena(self):
		thread.start_new_thread(self.grinding.start_arena, ())
		
	def signal_arena_fight(self):
		thread.start_new_thread(self.grinding.arena_fight, ())
	
	
	def build_signal(self):
		self.bt_calibrateposition.clicked.connect(self.signal_calibrate_position)
		self.bt_start_arena.clicked.connect(self.signal_start_arena)
		self.bt_arena_fight.clicked.connect(self.signal_arena_fight)
		
		self.hotkey.add("s", self.grinding.stop_arena)
		self.hotkey.start()
		#end build_signal
	
	
	def update_status(self, status_message=None):
		if status_message is None:
			self.lb_status.setText(self.grinding.status)
		else:
			self.lb_status.setText(status_message)
		#end update_status
	
	
	def print_log(self, text):
		self.log.append(text+"\n")
		self.log = self.log[-20:]#only store last 20 logs
		text = ""
		for t in self.log:
			text += t
		self.lb_print.setText(text)
		self.lb_print.show()
		#end update_status

if (__name__=="__main__"):
	app = QtGui.QApplication(sys.argv)
	def quitapp():
		app.quit()
	dmw = MainGUI(None,quitapp)
	sys.exit(app.exec_())
