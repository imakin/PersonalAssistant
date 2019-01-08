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
# electronics bug make my laptop sometimes turned on by itself, or waking up by itself
# re standby when no activity detected
import sys
import os
import subprocess
import re
import configparser
import pyautogui
import time

realpath = os.path.realpath(sys.argv[0])
if (sys.argv[0]!=""):
  realpath = os.path.dirname(realpath)

print(realpath)

class Main(object):
  WAIT_TIME = 4*60 
  def __init__(self):
    self.tv_shutdown = Main.WAIT_TIME # 10menit
    
    self.idle_count_biggest = 0
    self.idle_sampling = 0
    
    self.tv_start = time.time()
    
    while True:
      if (time.time()-self.tv_start)<self.tv_shutdown:
        print("will be sleep in " + str(self.tv_shutdown - int(time.time()-self.tv_start)))
        time.sleep(1)
      else:
        self.tv_start = time.time()
        self.go_standby()

  def go_standby(self):
    self.tv_shutdown = (Main.WAIT_TIME) #reset timer
    screensize = pyautogui.size()
    pyautogui.moveTo(screensize[0]-8, 8)
    time.sleep(1)
    pyautogui.click()
    time.sleep(1)
    pyautogui.moveRel(0, 215)
    time.sleep(1)
    pyautogui.click()
    time.sleep(10)



a = Main()
