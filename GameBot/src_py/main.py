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
		
		# self.bt_arena_start_no_thread
		self.bt_arena_start_no_thread = MakinButton(self.fr_main)
		self.bt_arena_start_no_thread.setObjectName("bt_arena_start_no_thread")
		self.bt_arena_start_no_thread.setText("arena start no thread")
		self.igr_main.addWidget(self.bt_arena_start_no_thread, 25,0,1,1,QtCore.Qt.AlignTop)
		
		# self.bt_arena_start_over
		self.bt_arena_start_over = MakinButton(self.fr_main)
		self.bt_arena_start_over.setObjectName("bt_arena_start_over")
		self.bt_arena_start_over.setText("arena start over")
		self.igr_main.addWidget(self.bt_arena_start_over, 26,0,1,1,QtCore.Qt.AlignTop)
		
		
		#~ self.gv_graphic = QtGui.QGraphicsView(self.fr_main)
		#~ self.gv_graphic.setObjectName("gv_graphic")
		#~ self.igr_main.addWidget(self.gv_graphic, 27,0,1,1,QtCore.Qt.AlignTop)
		
		# self.bt_update_score
		self.bt_update_score = MakinButton(self.fr_main)
		self.bt_update_score.setObjectName("bt_update_score")
		self.bt_update_score.setText("update score (alt-U)")
		self.igr_main.addWidget(self.bt_update_score, 27,1,1,1,QtCore.Qt.AlignTop)
		
		
		# self.bt_arena_standby
		self.bt_arena_standby = MakinButton(self.fr_main)
		self.bt_arena_standby.setObjectName("bt_arena_standby")
		self.bt_arena_standby.setText("standby ")
		self.igr_main.addWidget(self.bt_arena_standby, 27,0,1,1,QtCore.Qt.AlignTop)
		
		
		self.setCentralWidget(self.centralwidget)
		QtCore.QMetaObject.connectSlotsByName(self)
	
	
	def update_score(self, image=None):
		pass
		"""from PIL import Image
		self.print_log("updating score")
		
		self.scene = QtGui.QGraphicsScene(self)
		self.gv_graphic.setScene(self.scene)
		
		#~ self.image = QtGui.QPixmap("./data/score.png")
		#~ self.image.load("data/score.png")
		
		#~ self.scene.addPixmap(self.image)
		#~ self.scene.addText("blablabla")
		if image is not None:
			self.scoreimage = image
			#~ im = image
			#~ data = im.tostring("raw","RGB")
			#~ image = QtGui.QImage(data, im.size[0],  im.size[1], QtGui.QImage.Format_RGB32)
			#~ pix = QtGui.QPixmap.fromImage(image)
			#~ self.scene.addPixmap(pix)
			#~ self.lb_status.setPixmap(pix)
		else:
			im = self.scoreimage
			data = im.tostring("raw","RGB")
			image = QtGui.QImage(data, im.size[0],  im.size[1], QtGui.QImage.Format_RGB32)
			pix = QtGui.QPixmap.fromImage(image)
			self.scene.addPixmap(pix)
			self.lb_status.setPixmap(pix)
		"""
	
	def signal_calibrate_position(self):
		thread.start_new_thread(self.grinding.calibrate_position, ())
	
	def signal_start_arena(self):
		thread.start_new_thread(self.grinding.start_arena, ())
		
	def signal_arena_fight(self):
		thread.start_new_thread(self.grinding.arena_fight, ())
	
	def signal_arena_start_no_thread(self):
		self.grinding.start_arena()
	
	def signal_arena_start_over(self):
		thread.start_new_thread(self.grinding.arena_start_over, ())
	
	
	def signal_arena_standby(self):
		thread.start_new_thread(self.grinding.arena_standby, ())
	
	def build_signal(self):
		self.bt_calibrateposition.clicked.connect(self.signal_calibrate_position)
		self.bt_start_arena.clicked.connect(self.signal_start_arena)
		self.bt_arena_start_no_thread.clicked.connect(self.signal_arena_fight)
		self.bt_arena_start_over.clicked.connect(self.signal_arena_start_over)
		self.bt_arena_standby.clicked.connect(self.signal_arena_standby)
		#~ self.bt_update_score.clicked.connect(self.update_score)
		
		self.hotkey.add("s", self.grinding.stop_arena)
		#~ self.hotkey.add("u", self.update_score)
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
