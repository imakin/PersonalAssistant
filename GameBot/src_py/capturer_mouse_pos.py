import time
from makinreusable.winfunction import *
import ImageGrab

while True:
    pos = mouse_pos_get()
    col = ImageGrab.grab().getpixel((int(pos[0]),int(pos[1])))
    print("mouse pos:",pos,"color:",col)
    time.sleep(1)
