
import time
import dlib
import cv2

from interface_dummy import Connection

class Main(object):
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.face_detector_dlib = dlib.get_frontal_face_detector()
        self.face_detector_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        
        self.connection = Connection()
        self.connection.start()
    
    
    def run(self):
        while True:
            s, image = self.camera.read()
            if not s:continue
            
            s = time.clock()
            dets_dlib = self.face_detector_dlib(image, 1)
            time_dlib = time.clock()-s
            
            max_width = 0
            for rectangle in dets_dlib:
                if rectangle.width()>max_width:
                    max_width = rectangle.width()
            if max_width>0:
                sisi_depan = max_width/2
                
                print(max_width)
                self.connection.send("distance", str(max_width))
            
            #~ s = time.clock()
            #~ gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #~ dets_cv2 = self.face_detector_cascade.detectMultiScale(
                #~ gray,
                #~ scaleFactor=1.1,
                #~ minNeighbors=40,
                #~ minSize=(30, 30),
                #~ flags=cv2.CASCADE_SCALE_IMAGE,
            #~ )
            #~ time_cv2 = time.clock()-s
            #~ if len(dets_cv2)>0 or len(dets_dlib):
                #~ print(dets_cv2, time_cv2, " | ", dets_dlib, time_dlib)
            


app = Main()
app.run()
