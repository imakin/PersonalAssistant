#!/usr/bin/env python

#
# Copyright 2018 <Muhammad Izzulmakin> <makin.ugm@gmail.com>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
#
import sys
import os
import subprocess
import re
import configparser

from PySide import QtCore
from PySide import QtGui

realpath = os.path.realpath(sys.argv[0])
if (sys.argv[0]!=""):
  realpath = os.path.dirname(realpath)

print(realpath)

class Main(QtGui.QMainWindow):
  def __init__(self):
    super(Main, self).__init__()
    self.fr = QtGui.QFrame(self)
    self.igr = QtGui.QGridLayout(self.fr)
    self.fr.setLayout(self.igr)
    self.setCentralWidget(self.fr)
    
    self.button = QtGui.QPushButton(self.fr)
    self.button.setText("I'm aware, do not shutdown")
    self.button.setObjectName("but")
    self.button.clicked.connect(self.app_quit)
    self.igr.addWidget(self.button)
    
    
    self.setStyleSheet("#but { padding:10; height:300;width:400px; }")
    
    self.t_shutdown = QtCore.QTimer()
    self.tv_shutdown = 60*3 # 10menit
    self.t_shutdown.timeout.connect(self.check_shutdown)
    self.t_shutdown.start(1000)
    
    self.idle_count_biggest = 0
    self.idle_sampling = 0

  def run_application(self, cmd):
    app_name = "_".join(re.findall("[A-z]+", cmd))
    subprocess.call(
      "nohup "+
      cmd +
      " > " +
      "/tmp/"+app_name+".makin_autostart &",
      shell=True
    )

  def app_quit(self):
    # start up apps
    # ~ /usr/bin/skypeforlinux
    for f in os.listdir(realpath):
      if f.lower().endswith("desktop"):
        f = os.path.join(realpath, str(f))
        cf = configparser.ConfigParser()
        cf.read(f)
        try:
          self.run_application(cf["Desktop Entry"]["Exec"])
        except:
          print("error")
          print(cf.keys())
    # quit
    quit()

  def check_shutdown(self):
    if (self.tv_shutdown<=0):
      os.system("/sbin/shutdown now")
    else:
      self.button.setText("shutdown in ("+str(self.tv_shutdown)+") - idle sampling:"+str(self.idle_sampling))
    #if idle count is big
    idle_count = int(subprocess.check_output("xprintidle"))
    if idle_count<1000:
      if self.idle_sampling<1:
        self.idle_sampling += 1
      else:
        self.idle_sampling += self.idle_sampling*1.1
    elif self.idle_sampling>0:
      self.idle_sampling -= 1

    if self.idle_sampling<=0:
      self.tv_shutdown -= 1
    elif self.idle_sampling>10:
      #this means user has moved the mouse/keyboard
      self.t_shutdown.stop()
      self.button.setText("idle broke, you're awake. starting startup applications")
      self.t = QtCore.QTimer()
      self.t.timeout.connect(self.app_quit)
      self.t.start(5000)
    print(self.idle_sampling)



x = QtGui.QApplication(sys.argv)
a = Main()
a.show()
x.exec_()
